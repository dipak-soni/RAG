from langchain_pinecone import PineconeVectorStore
import os
from langchain_community.embeddings import OpenAIEmbeddings
from pinecone import Pinecone 

os.environ["OPENAI_API_KEY"]='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'
os.environ['PINECONE_API_KEY']='1b7fb9bd-104f-41ce-b2b4-12c763b5b1eb'

def get_context(query):
    pc=Pinecone(api_key=os.environ['PINECONE_API_KEY'],environment='us-east-1')    # it is just for creating connection 
    index_name='lawpdf'
    index=pc.Index(name=index_name)
    print(index.describe_index_stats())

    embeddings=OpenAIEmbeddings()
    vector_store = PineconeVectorStore(index=index, embedding=embeddings)

    results = vector_store.similarity_search(
        "what is the percentage I got in 10th?",
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
   
