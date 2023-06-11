from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse
from fastapi.templating import Jinja2Templates
import requests
from bs4 import BeautifulSoup, Comment
from model import *
from fastapi.middleware.cors import CORSMiddleware 
#importing moudles
import os
import requests
from bs4 import BeautifulSoup
from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain import HuggingFaceHub
from myloader import MyTextLoader

doc = None
try:
    loader = MyTextLoader("data.txt")
    document = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size = 1000, chunk_overlap=0, separators=[" ", ",", "\n"])
    docs = text_splitter.split_documents(document)

    embedding = HuggingFaceEmbeddings()
    db = FAISS.from_documents(docs, embedding)
except Exception as e:
    print('Here')

os.environ["HUGGINGFACEHUB_API_TOKEN"] = "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"

llm=HuggingFaceHub(
    repo_id="google/flan-t5-small", 
    model_kwargs={"temperature":0.2, "max_length":256}
    )
chain = load_qa_chain(llm, chain_type="stuff")

app = FastAPI()

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

templates = Jinja2Templates(directory="templates")

def is_element_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True
def scrape_content(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    # Find all text elements in the HTML
    text_elements = soup.find_all(text=True)
    # Filter out specific elements (comments, script contents, CSS styles)
    filtered_text_elements = [element for element in text_elements if is_element_visible(element)]
    # Concatenate all the filtered text elements into a single string
    scraped_text = '\n'.join(filtered_text_elements)
    return scraped_text

@app.get("/scrape")
async def scrape(url: str):
    scraped_text = str(scrape_content(url))

    await train(scraped_text)
    return PlainTextResponse(content=scraped_text, headers={"Content-Disposition": "attachment; filename=scraped_text.txt"})

async def train(scraped_text: str):
    with open('data.txt', 'a', encoding='utf8', errors='ignore') as f:
        f.write(scraped_text)
    
    loader = MyTextLoader("data.txt")
    document = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size = 1000, chunk_overlap=0, separators=[" ", ",", "\n"])
    docs = text_splitter.split_documents(document)

    embedding = HuggingFaceEmbeddings()
    
    global db
    db = FAISS.from_documents(docs, embedding)

@app.get("/ask")
def ask(ques: str):
    global db, chain
    docs = db.similarity_search(ques)
    res = chain.run(input_documents=docs, question=ques)
    # print(res)
    return res

def search_text_file(search_string):
    str = ""
    with open("data.txt", 'r') as file:
        for line in file:
            if search_string in line:
                str = str +line.strip()
    return str

@app.get("/")
async def read_root(request: Request):
    return "working"
