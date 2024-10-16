from langchain_openai import OpenAI
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.document_loaders import PyPDFLoader,PyPDFDirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Pinecone
from pinecone import Pinecone as PineconeClient
import os
os.environ["OPENAI_API_KEY"]='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'
os.environ['PINECONE_API_KEY']='1b7fb9bd-104f-41ce-b2b4-12c763b5b1eb'
# Path to a single PDF file
pdf_file_path = 'simple_resume.pdf'

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
pc=PineconeClient(api_key=os.environ['PINECONE_API_KEY'],environment='us-east-1')    # it is just for creating connection 
index='lawpdf'
index=Pinecone.from_documents(splits,embeddings,index_name=index)    # returns pinecone object








