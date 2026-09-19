from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.tools import tool
from tavily import TavilyClient
from langchain.agents import create_agent
from langchain.agents.middleware import wrap_tool_call
from langchain.messages import ToolMessage
from rich import print

import os
import requests

load_dotenv()


# ==========================================
# 1. WEATHER TOOL
# ==========================================

@tool
def get_weather(city: str) -> str:
    """Get current weather of a city."""

    API_KEY = os.getenv("OPENWEATHER_API_KEY")

    url = (
        f"https://api.openweathermap.org/data/2.5/weather"
        f"?q={city}&appid={API_KEY}&units=metric"
    )

    response = requests.get(url)
    data = response.json()

    if str(data.get("cod")) != "200":
        return f"Error: {data.get('message', 'Something went wrong')}"

    temperature = data["main"]["temp"]
    description = data["weather"][0]["description"]

    return f"Weather in {city}: {description}, {temperature}°C"


# ==========================================
# 2. NEWS TOOL
# ==========================================

tavily_client = TavilyClient(
    api_key=os.getenv("TAVILY_API_KEY")
)


@tool
def get_news(city: str) -> str:
    """Get the latest news about a city."""

    response = tavily_client.search(
        query=f"latest news about {city}",
        search_depth="advanced",
        max_results=5
    )

    results = response.get("results", [])

    if not results:
        return f"No recent news found for {city}."

    news = []

    for result in results:
        title = result.get("title", "No title")
        content = result.get("content", "No description")
        url = result.get("url", "")

        news.append(
            f"Title: {title}\n"
            f"Description: {content}\n"
            f"URL: {url}"
        )

    return "\n\n".join(news)


# ==========================================
# 3. LLM
# ==========================================

model = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0
)



# =============================================
# 4. MIDDLEWARE
# =============================================

@wrap_tool_call #decorator
def human_approval(request, handler):
    """Ask for human approval before every tool call."""

    tool_name = request.tool_call["name"]

    confirm = input(
        f"Agent wants to call '{tool_name}'. Approve? (yes/no): "
    )

    if confirm.lower() != "yes":
        return ToolMessage(
            content="Tool call denied by user.",
            tool_call_id=request.tool_call["id"]
        )

    return handler(request)




# ==========================================
# 5. CREATE AGENT
# ==========================================

agent = create_agent(
    model,
    tools=[get_weather, get_news],
    system_prompt="You are a helpful city assistant.",
    middleware = [human_approval]
)


# ==========================================
# 6. USER ↔ AGENT INTERACTION
# ==========================================

#  NOW ADDING @wrap_tool_call FOR AUTHENTICATION (MIDDLEWARE)


while True:

    user_input = input("You: ")

    if user_input.strip() == "0":
        print("Bot: Goodbye!")
        break

    result = agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": user_input
                }
            ]
        }
    )

    print("Bot:", result["messages"][-1].content)


















































# from dotenv import load_dotenv
# from langchain_groq import ChatGroq
# from langchain_community.tools.tavily_search import TavilySearchResults
# from langchain_core.prompts import ChatPromptTemplate
# from langchain_core.output_parsers import StrOutputParser
# from langchain.tools import tool
# from langchain_core.messages import HumanMessage, ToolMessage
# from tavily import TavilyClient
# from rich import print
# from langchain.agents import create_agent

# import os
# import requests

# load_dotenv()

# # NOW LETS CREATE SOME TOOLS


# # 1 . Weather tool 

# @tool
# def get_weather(city: str) -> str:
#     #doc string 
#     """Get current weather of a city."""

#     API_KEY = os.getenv("OPENWEATHER_API_KEY")

#     url = (
#         f"http://api.openweathermap.org/data/2.5/weather"
#         f"?q={city}&appid={API_KEY}&units=metric"
#     )

#     response = requests.get(url)
#     data = response.json()

#     print("DEBUG:", data)

#     if str(data.get("cod")) != "200":
#         return f"Error: {data.get('message', 'Something went wrong')}"

#     temperature = data["main"]["temp"]
#     description = data["weather"][0]["description"]

#     return f"Weather in {city}: {description}, {temperature}°C"


# print(get_weather.invoke({"city": "Bhopal"}))



# # 2. Creating News Tool

# tavily_client = TavilyClient(
#     api_key=os.getenv("TAVILY_API_KEY")
# )


# @tool
# def get_news(city: str) -> str:
#     """Get the latest news about a city."""

#     response = tavily_client.search(
#         query=f"latest news about {city}",
#         search_depth="advanced",
#         max_results=5
#     )

#     results = response.get("results", [])

#     if not results:
#         return f"No recent news found for {city}."

#     news = []

#     for result in results:
#         title = result.get("title", "No title")
#         content = result.get("content", "No description")
#         url = result.get("url", "")

#         news.append(
#             f"Title: {title}\n"
#             f"Description: {content}\n"
#             f"URL: {url}"
#         )

#     return "\n\n".join(news)


# print(get_news.invoke({"city": "Bhopal"}))




# model = ChatGroq(
#     model="openai/gpt-oss-20b",
#     temperature=0
# )

# agent = create_agent(
#     model,
#     tools = [get_weather, get_news],
#     system_prompt = "You are a helpful city assistant."
# )

# print("City Agent | Type 0 to exit")

# while True:
#     user_input = input("You: ")

#     if user_input == "0":
#         break

#     result = agent.invoke(
#         {
#             "messages": [
#                 {"role": "user", "content": user_input}
#             ]
#         }
#     )

#     print("Bot:", result["messages"][-1].content)
