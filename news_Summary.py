from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel,RunnablePassthrough
load_dotenv()

search_tool = TavilySearchResults(max_res = 5)

# 2.Model
model = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0
)

prompt = ChatPromptTemplate.from_template(
    """
    You are a helpful assistant 
    summarize the following news into clear bullet points in 5 lines 
    {news}

"""
)

parser = StrOutputParser();

chain = prompt | model | parser

news_result = search_tool.run("Latest AI news of 2026")

result = chain.invoke({"news" : news_result})

print(result)

