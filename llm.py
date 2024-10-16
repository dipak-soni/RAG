from langchain.llms import Cohere 
from langchain.prompts import PromptTemplate
from langchain.chains import ConversationChain,LLMChain
from langchain.memory import ConversationBufferMemory
import os
from get_from_pinecone import get_context
COHERE_API_KEY=os.getenv('COHERE_API_KEY')

def get_response(user_query,history):
    
    prompt=PromptTemplate(
        input_variables=["input","history","context"],
            template="""
            Task: You are a law assisting chatbot.
            Instructions:
            1. take user question {input}.
            2. you have previous history of conversation {history}.
            3. you have context {context}.
            4. give answer in short
            
            """
        )
    
   
    
    llm=Cohere()
    # memory=ConversationBufferMemory(input_key="input")
    chain=LLMChain(
            llm=llm,
            prompt=prompt,
            verbose=True
        ) 
    
    # get pdf data first from user query
    context=get_context(user_query)
    result=chain.invoke({"input":user_query,"context":context,"history":history})
    print(result)
    return result['text']


  
       
    
    
