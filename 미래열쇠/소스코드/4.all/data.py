import os
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter


#os.environ

# txt파일 로드
loader = TextLoader("/home/hope/work4/work/4.all/Handong4.txt") 
docs = loader.load()

# 문서 분할
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
split_documents = text_splitter.split_text(docs[0].page_content)


# 임베딩 생성
embeddings = OpenAIEmbeddings()

# 벡터 DB 생성 및 저장
vectorstore = FAISS.from_texts(split_documents, embedding=embeddings)
vectorstore.save_local('./db1/faiss') 
