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

loader = MyTextLoader("temp.txt")
document = loader.load()

text_splitter = RecursiveCharacterTextSplitter(chunk_size = 1000, chunk_overlap=0, separators=[" ", ",", "\n"])
docs = text_splitter.split_documents(document)

embedding = HuggingFaceEmbeddings()
db = FAISS.from_documents(docs, embedding)

os.environ["HUGGINGFACEHUB_API_TOKEN"] = "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"

llm=HuggingFaceHub(
    repo_id="google/flan-t5-small", 
    model_kwargs={"temperature":0.2, "max_length":256}
    )
chain = load_qa_chain(llm, chain_type="stuff")

def get_answer(ques):
    docs = db.similarity_search(ques)
    res = chain.run(input_documents=docs, question=ques)
    return res

