
# Documentation

Below is the documentation for the provided code:

## Import Statements


```from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse
from fastapi.templating import Jinja2Templates
import requests
from bs4 import BeautifulSoup, Comment
from model import *
from fastapi.middleware.cors import CORSMiddleware
import os
from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain import HuggingFaceHub
from myloader import MyTextLoader` 
```

Imports the necessary modules and packages required for the code execution.

## Initialize Variables

```
doc = None
```

Initializes the variable `doc` with a `None` value.

## Load Text Document and Prepare for Training

```
try:
    loader = MyTextLoader("data.txt")
    document = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0, separators=[" ", ",", "\n"])
    docs = text_splitter.split_documents(document)

    embedding = HuggingFaceEmbeddings()
    db = FAISS.from_documents(docs, embedding)
except Exception as e:
    print('Here')
```

Attempts to load the text document from the file "data.txt" using the `MyTextLoader` class. If successful, the document is split into smaller chunks using the `RecursiveCharacterTextSplitter` with a chunk size of 1000 and no overlap. The text chunks are then converted into embeddings using the `HuggingFaceEmbeddings` class, and a vector store is created using the `FAISS` class. If any exception occurs during this process, the string "Here" is printed.

## Initialize HuggingFaceHub and Question Answering Chain

```
os.environ["HUGGINGFACEHUB_API_TOKEN"] = "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"

llm = HuggingFaceHub(repo_id="google/flan-t5-small", model_kwargs={"temperature": 0.2, "max_length": 256})
chain = load_qa_chain(llm, chain_type="stuff") 
```
Sets the environment variable "HUGGINGFACEHUB_API_TOKEN" to a specific value. Then, initializes the `HuggingFaceHub` with the repository ID "google/flan-t5-small" and model keyword arguments "temperature" and "max_length". Finally, loads a question answering chain using the `load_qa_chain` function, passing the `llm` (HuggingFaceHub) object and chain type "stuff".

## Create FastAPI Application

```
app = FastAPI()
```

Creates a FastAPI application instance.

## Configure CORS Middleware

```
origins = [
    "*",  # Update with your extension's origin
    # Add more allowed origins if needed
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

Configures the Cross-Origin Resource Sharing (CORS) middleware for the FastAPI application. Allows all origins, credentials, methods, and headers for CORS requests.

## Initialize Jinja2Templates

```
templates = Jinja2Templates(directory="templates")
```

Initializes the `Jinja2Templates` class with the directory set to "templates".

## Helper Function: is_element_visible

```
def is_element_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True
```

Defines a helper function `is_element_visible` that checks if an HTML element is visible or should be filtered out. Returns `False` if the element's parent name is in the list ['style', 'script', 'head', 'title', 'meta', '[document]'] or if the element is an instance of `Comment`. Otherwise, it returns `True`.

## Async Function: train
```
async def train(scraped_text: str):
    with open('data.txt', 'a', encoding='utf8', errors='ignore') as f:
        f.write(scraped_text)
    loader = MyTextLoader("data.txt")
    document = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0, separators=[" ", ",", "\n"])
    docs = text_splitter.split_documents(document)
    embedding = HuggingFaceEmbeddings()
    global db
    db = FAISS.from_documents(docs, embedding) 
```
Defines an async function `train` that takes the scraped text as input. It opens the file "data.txt" in append mode and writes the scraped text into it. Then, it loads the updated document using the `MyTextLoader` class, splits the document into smaller chunks using the `RecursiveCharacterTextSplitter`, and converts the text chunks into embeddings using the `HuggingFaceEmbeddings` class. Finally, it assigns the resulting vector store to the global variable `db`.


## Helper Function: scrape_content
```
def scrape_content(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    text_elements = soup.find_all(text=True)
    filtered_text_elements = [element for element in text_elements if is_element_visible(element)]
    scraped_text = '\n'.join(filtered_text_elements)
    return scraped_text
``` 

Defines a helper function `scrape_content` that takes a URL as input and performs web scraping to extract visible text content from the HTML page. It sends a GET request to the URL, parses the response content using BeautifulSoup, finds all text elements in the HTML, filters out non-visible elements using the `is_element_visible` function, and concatenates the filtered text elements into a single string separated by newline characters. The resulting scraped text is returned.

## Route: /scrape [GET]

```
@app.get("/scrape")
async def scrape(url: str):
    scraped_text = str(scrape_content(url))
    await train(scraped_text)
    return PlainTextResponse(content=scraped_text, headers={"Content-Disposition": "attachment; filename=scraped_text.txt"})
```

Defines a route `/scrape` that accepts a GET request with a query parameter `url` representing the URL of a web page to scrape. It calls the `scrape_content` function to extract the text content from the web page, converts the scraped text to a string, and passes it to the `train` function. Finally, it returns a `PlainTextResponse` with the scraped text as the content and sets the content disposition header to download the scraped text as a file named "scraped_text.txt".

## Route: /ask [GET]

```
@app.get("/ask")
def ask(ques: str):
    global db, chain
    docs = db.similarity_search(ques)
    res = chain.run(input_documents=docs, question=ques)
    return res 
```
Defines a route `/ask` that accepts a GET request with a query parameter `ques` representing a question. It retrieves the global variables `db` and `chain` and performs a similarity search on the `db` vector store using the question. The resulting documents are passed to the `chain.run` method along with the question to obtain an answer. The answer is then returned as the response.

## Helper Function: search_text_file

```
def search_text_file(search_string):
    str = ""
    with open("data.txt", 'r') as file:
        for line in file:
            if search_string in line:
                str = str + line.strip()
    return str 

```
Defines a helper function `search_text_file` that takes a search string as input. It opens the file "data.txt" in read mode and iterates over each line. If the search string is found in a line, the line (stripped of leading and trailing whitespaces) is added to the result string. Finally, the result string is returned.

## Route: / [GET]

```
@app.get("/")
async def read_root(request: Request):
    return "working"
```
Defines the root route `/` that accepts a GET request. It returns the string "working" as the response if the server is up.
