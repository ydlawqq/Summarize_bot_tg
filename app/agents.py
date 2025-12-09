from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama
from langchain_core.runnables import RunnablePassthrough
from dotenv import load_dotenv
from prompts import prompt_router, prompt_test_agent
from langgraph.checkpoint.postgres import PostgresSaver
from langchain.agents import create_agent
from classes import RouterOutput
import os
load_dotenv()

api = os.getenv('mistral')


DB = 'postgresql+asyncpg://ydlawq:retrofm.ru1@localhost:5432/ai_agent'
### LLMs
llm = ChatMistralAI(
    model_name='mistral-medium',
    api_key=api
)
llm_ollama = ChatOllama(
    model='llama3.2:3b'
)




agent = ({
    'input': RunnablePassthrough(),
    'history': RunnablePassthrough()
})


### CHAINS
router_chain = ({'input': RunnablePassthrough()}
                | prompt_router
                | llm_ollama.with_structured_output(method='json_schema', schema=RouterOutput))


agent_chain =  prompt_test_agent | llm




