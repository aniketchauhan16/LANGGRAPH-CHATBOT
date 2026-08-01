from langgraph.graph import StateGraph, START, END
from typing import TypedDict,Annotated
from langchain_core.messages import BaseMessage
from langchain_groq import ChatGroq
from dotenv import load_dotenv
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import add_messages

load_dotenv()\

llm = ChatGroq(model="openai/gpt-oss-20b")

class chatState(TypedDict):
    messages : Annotated[list[BaseMessage],add_messages]

def chat_node(state: chatState):
    messages = state['messages']
    response = llm.invoke(messages)
    return {"messages" : [response]}

checkpointer = InMemorySaver()

graph = StateGraph(chatState)

graph.add_node("chat_node",chat_node)
graph.add_edge(START,'chat_node')
graph.add_edge('chat_node',END)

chatbot = graph.compile(checkpointer=checkpointer)