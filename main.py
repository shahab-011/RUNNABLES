from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
load_dotenv()

# 1.Prompt template
prompt = ChatPromptTemplate.from_template(
    "Explain {topic} in simple words"
)

# 2.Model
model = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0
)


# 3.Output Parser
parser = StrOutputParser()

# SEQUENCE RUNNABLES  
chain = prompt | model | parser

result = chain.invoke("Machine learning.")
print(result)

