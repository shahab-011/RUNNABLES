from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel,RunnablePassthrough
load_dotenv()

search_tool = TavilySearchResults(max_res = 5)
from langchain.tools import tool

model = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0
)



@tool
def get_greeting(name : str) -> str:
    #doc string -> to tell what this fn is going to do 
    """Generate a greeting message for a user."""
    return f"Hello {name}, Welcome to the AI world"

#this is tool and tool is also treated as runnables 




res = model.invoke({"name":"Shahab"})
print(res)


# print(search_tool.name)
# print(search_tool.description)
# print(search_tool.args)