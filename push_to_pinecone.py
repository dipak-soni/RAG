from langchain_openai import OpenAI
from langchain_community.embeddings import OpenAIEmbeddings,CohereEmbeddings
from langchain_community.document_loaders import PyPDFLoader,PyPDFDirectoryLoader, DirectoryLoader,TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Pinecone
from pinecone import Pinecone as PineconeClient,ServerlessSpec
import os
from dotenv import load_dotenv
load_dotenv()
COHERE_API_KEY=os.getenv('COHERE_API_KEY')
PINECONE_API_KEY=os.getenv('PINECONE_API_KEY')
PINECONE_REGION=os.getenv('PINECONE_REGION')
PINECONE_INDEX_NAME=os.getenv('PINECONE_INDEX_NAME')

# Initialize the PDF loader
# loader = PyPDFLoader(pdf_file_path)      # if we want to use single pdf file
def push(filename):
    pdf_folder_path = os.getcwd() + '/uploads'
    loader = PyPDFLoader(os.path.join(pdf_folder_path, filename))
    
    # Load the document
    pdf_document = loader.load()     # this returns list object 
    # print(pdf_document)
    # Display the loaded document
    # print(f"Document Name: {pdf_document[0].metadata['source']}")
    # print(f"Content Preview: {pdf_document[0].page_content[:200]}...")


    document = pdf_document

    # chunking the pdf file 
    text_splitter=RecursiveCharacterTextSplitter(chunk_size=1000,chunk_overlap=200)
    splits = text_splitter.split_documents(document)   # list object


    # now create embeddings for this chunks
    # Embed each chunk and store the embeddings
    embeddings=CohereEmbeddings(cohere_api_key=COHERE_API_KEY,user_agent='rag')
    # embedded_splits = [embeddings.embed_query(chunk.page_content) for chunk in splits]   

    # Print a sample of the first embedding (for example, the first chunk's embedding)
    #print(f"First chunk embedding (length {len(embedded_splits[0])}):\n{embedded_splits[0]}")     
    # 1536 chunks

    

    # insert document splits to pinecone 
    pc=PineconeClient(api_key=PINECONE_API_KEY,environment=PINECONE_REGION)    # it is just for creating connection 
    
    # delete the old index from pinecone
    # print(pc.list_indexes())

    pc.delete_index('rag')
    print(f"Index 'rag' deleted successfully.")
    

    # create a new index in pinecone new index is rag 
    index_model = pc.create_index(
    name='rag',
    dimension=4096,
    metric='cosine',
    spec=ServerlessSpec(cloud="aws", region="us-east-1")
    )
    print('index created successfully:')

    index=Pinecone.from_documents(splits,embeddings,index_name=PINECONE_INDEX_NAME)    # returns pinecone object
    print('pushed to pinecone')
    return 1











