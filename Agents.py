from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel,RunnablePassthrough
from langchain.tools import tool 
from langchain_core.messages import HumanMessage, ToolMessage
from tavily import TavilyClient

load_dotenv()

import os
import requests



# NOW LETS CREATE SOME TOOLS

# 1. Weather Tool
@tool
def get_weather(city : str) -> str:
    #doc string 
    """Get Current weather of a city."""
    url = 




















# 1.Creating a tool
@tool
def get_textLen(text: str) -> int:
    #doc string
    """Return the number of character in a given text"""
    return len(text)

# 2.LLM
model = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0
)


# 3.Tool Binding 
modelWithTool = model.bind_tools([get_textLen])

res = model.invoke("hello ")
print(res)