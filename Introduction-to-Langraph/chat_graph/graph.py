
from typing_extensions import TypedDict
from openai import OpenAI
from typing import Annotated
from langgraph.graph import StateGraph, START, END
from dotenv import load_dotenv
from pydantic import BaseModel
# pydantic is like ZOD npm package in js environment
from langgraph.graph.message import add_messages
from langchain.chat_models import init_chat_model


load_dotenv()

client = OpenAI()

# Messages is a list in which we keep adding one message at a time.
# In my state, there is a key called messages which is a list where
# we keep adding our messages continuously.

class State(TypedDict):
      messages: Annotated[list, add_messages]

llm = init_chat_model(model_provider="openai", model="gpt-4.1")

def chat_node(state: State):
    response = llm.invoke(state["messages"])
    #  since we have used Annotated, whatever we will return in this list, this will get appended in the add_messages list
    return {"messages": [response]}



graph_builder = StateGraph(State)

graph_builder.add_node("chat_node",chat_node)


graph_builder.add_edge(START,"chat_node")
graph_builder.add_edge("chat_node",END)


graph = graph_builder.compile()

def main():
     query = input("> ")
     _state ={
          "messages" : [{"role":"user", "content":query}]
     }
     # This created a fresh new state
     result = graph.invoke(_state)
     # This deleted the state  
     print("result --> ",result)
    
main()

# in Annotation, the state gets reset whenever the graph ends 
      
             

# Annotation
# Checkpointing
# Streaming