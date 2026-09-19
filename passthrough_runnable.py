from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel,RunnablePassthrough
load_dotenv()


# 1.Prompt template
code_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a code Generator"),
    ("human", "{topic}")
])

explain_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assitant who explains code in simple terms"),
    ("human", "Explain the following code in simple words:\n{code}")
])


# 2.Model
model = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0
)



# 3.Output Parser
parser = StrOutputParser()



# chain = code_prompt | model | parser | explain_prompt | model | parser 

# 4. PASSTHROUGH RUNNABLE 
seq1 = code_prompt | model | parser

seq2 = RunnableParallel({
    "code" : RunnablePassthrough(),
    "explaination" : explain_prompt | model | parser
})

chain = seq1 | seq2





result = chain.invoke({
    "topic":"Write a code of palindrome in c++"
})


print(result['code'])
print(result['explaination'])






