from langchain_core.prompts import ChatPromptTemplate
from app.common.llm import llm_qwen
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableMap, RunnableLambda

prompt_en_2_zh = ChatPromptTemplate.from_messages([
    ("system", "translate the following from english to chinese"),
    ("user", "{text}"),
])

prompt_en_2_fr = ChatPromptTemplate.from_messages([
    ("system", "translate the following from english to french"),
    ("user", "{text}"),
])

parser = StrOutputParser()

chain_zh = prompt_en_2_zh | llm_qwen | parser

chain_fr = prompt_en_2_fr | llm_qwen | parser

parallel_chains = RunnableMap(
    {"zh_translation": chain_zh,
     "fr_translation": chain_fr}
)

final_chain = parallel_chains | RunnableLambda(
    lambda x: f"Chinese:{x['zh_translation']}\nFrench:{x['fr_translation']}")

print(final_chain.invoke({"text": "hello world"}))
