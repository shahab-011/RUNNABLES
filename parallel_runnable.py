from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel,RunnableLambda
load_dotenv()


# 1.Prompt template
short_prompt = ChatPromptTemplate.from_template(
    "Explain {topic} in 1-2 lines"
)
detailedt_prompt = ChatPromptTemplate.from_template(
    "Explain {topic} in detail"
)


# 2.Model
model = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0
)



# 3.Output Parser
parser = StrOutputParser()

# Sequence runnable
# chain = prompt | model | parser



# PARALLEL RUNNABLES
chain = RunnableParallel({
    "short" : RunnableLambda(lambda x : x['short']) | short_prompt | model | parser,
    "detailed" : RunnableLambda(lambda x : x['detailed']) | detailedt_prompt | model | parser
})

# so when we invoke the chain.invoke in the RunnableParallel it 
# expect to recieve a value single value but it receives a 
# dictionary so resolve this in the pipeline we will use RunnableLambda
# that will create a function to extract the exact value.





# result = chain.invoke({"topic" : "Machine Learning"})

result = chain.invoke({
    "short": {"topic" : "Machine Learning"},
    "detailed": {"topic" : "Deep Learning"}
})

print(result['short'])
print(result['detailed'])


