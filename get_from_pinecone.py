from langchain_pinecone import PineconeVectorStore
import os
from langchain_community.embeddings import OpenAIEmbeddings
from pinecone import Pinecone 
from dotenv import load_dotenv
load_dotenv()

OPENAI_API_KEY=os.getenv("OPENAI_API_KEY")
PINECONE_API_KEY=os.getenv('PINECONE_API_KEY')
PINECONE_REGION=os.getenv('PINECONE_REGION')
PINECONE_INDEX_NAME=os.getenv('PINECONE_INDEX_NAME')

def get_context(query):
    pc=Pinecone(api_key=PINECONE_API_KEY,environment=PINECONE_REGION)    # it is just for creating connection 
    index_name=PINECONE_INDEX_NAME
    index=pc.Index(name=index_name)
    print(index.describe_index_stats())

    embeddings=OpenAIEmbeddings()
    vector_store = PineconeVectorStore(index=index, embedding=embeddings)

    results = vector_store.similarity_search(
        query,
        k=1,
    )
    
    context=results[0].page_content
    print(context)
    return context
    # query='what percentage I got in 10th class?'
    # embed_query=embeddings.embed_query(query)
    # print(embed_query)
    # result=index.query(vector=embed_query,top_k=2, include_metadata=True)
    # print(result)
   
