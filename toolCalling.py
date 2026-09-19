from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel,RunnablePassthrough
load_dotenv()

from rich import print 

search_tool = TavilySearchResults(max_res = 5)
from langchain.tools import tool


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