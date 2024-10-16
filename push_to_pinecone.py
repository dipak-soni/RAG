from langchain_openai import OpenAI
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.document_loaders import PyPDFLoader,PyPDFDirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Pinecone
from pinecone import Pinecone as PineconeClient
import os
from dotenv import load_dotenv
load_dotenv()
OPENAI_API_KEY=os.getenv["OPENAI_API_KEY"]
PINECONE_API_KEY=os.getenv['PINECONE_API_KEY']
PINECONE_REGION=os.getenv['PINECONE_REGION']
PINECONE_INDEX_NAME=os.getenv['PINECONE_INDEX_NAME']

# Initialize the PDF loader
# loader = PyPDFLoader(pdf_file_path)
pdf_folder_path = os.getcwd() + '/law_documents'
loader = PyPDFDirectoryLoader(pdf_folder_path)

# Load the document
document = loader.load()     # this returns list object 
# print(document)
# Display the loaded document
# print(f"Document Name: {document[0].metadata['source']}")
# print(f"Content Preview: {document[0].page_content[:200]}...")


# chunking the pdf file 
text_splitter=RecursiveCharacterTextSplitter(chunk_size=1000,chunk_overlap=200)
splits = text_splitter.split_documents(document)   # list object


# now create embeddings for this chunks
# Embed each chunk and store the embeddings
embeddings=OpenAIEmbeddings()
# embedded_splits = [embeddings.embed_query(chunk.page_content) for chunk in splits]   

# Print a sample of the first embedding (for example, the first chunk's embedding)
#print(f"First chunk embedding (length {len(embedded_splits[0])}):\n{embedded_splits[0]}")     
# 1536 chunks


# insert document splits to pinecone 
pc=PineconeClient(api_key=PINECONE_API_KEY,environment=PINECONE_REGION)    # it is just for creating connection 
index=Pinecone.from_documents(splits,embeddings,index_name=PINECONE_INDEX_NAME)    # returns pinecone object








