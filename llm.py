from langchain.llms import Cohere 
from langchain.prompts import PromptTemplate
from langchain.chains import ConversationChain,LLMChain
from langchain.memory import ConversationBufferMemory
import os
from get_from_pinecone import get_context
os.environ['COHERE_API_KEY']='C8buajOpTJaqrmm4cF9kKswk7RbRPnstQy0sQFjh'

def get_response(user_query):
    
    llm=Cohere(temperature=0.5)
    
    prompt=PromptTemplate(
        input_variables=["input","context","history"],
            template="""
            Task: You are a law assisting chatbot.
            Instructions:
            1. based on the query of users you have to answer it using context {context}
            2. you have previous history as well {history}.
            3. If user just greets then reply with "hello how can i assist you Today".
            user question : {input}
            """
        )
    
    
    memory=ConversationBufferMemory(input_key="input")
    chain=LLMChain(
            llm=llm,
            memory=memory,
            prompt=prompt,
            verbose=True
        ) 
    
    # get pdf data first from user query
    context=get_context(user_query)
    
    result=chain.invoke({"input":user_query,"context":context})
    print(result)
    return result['text']

  
       
    
    
