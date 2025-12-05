from langgraph.checkpoint.memory import InMemorySaver
from langgraph.checkpoint.redis import RedisSaver
from langchain.agents import create_agent
from app.code_agent.model.qwen import llm_qwen
from app.code_agent.tools.file_tools import file_tools
from langchain_core.runnables import RunnableConfig

def create_memory_saver():
    return InMemorySaver()




def create_chat_agent():

    with RedisSaver.from_conn_string("redis://:matrx_test@192.168.201.9:6379/0") as memory:
        memory.setup()
        agent = create_agent(
            model=llm_qwen,
            tools=file_tools,
        )
    return agent


def run_agent():
    config = RunnableConfig(configurable={"thread_id": 1})

    agent = create_chat_agent()

    resp = agent.stream(
        {"messages": [{"role": "user", "content": "我叫丁宇,你是谁"}]},
        stream_mode="messages",
        config=config,
    )

    for token, metadata in resp:
        print_content_blocks(token)

    print("\n============\n")

    resp = agent.stream(
        {"messages": [{"role": "user", "content": "我叫什么"}]},
        stream_mode="messages",
        config=config,
    )

    for token, metadata in resp:
        print_content_blocks(token)



def print_content_blocks(token):
    """只输出纯文本内容"""
    if token.content_blocks:
        for block in token.content_blocks:
            if isinstance(block, dict) and 'text' in block:
                print(block['text'], end="", flush=True)



if __name__ == "__main__":
    run_agent()
