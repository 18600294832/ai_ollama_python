import uuid

from app.code_agent.prompts.multi_chat_prompt import multi_chat_prompt_1, multi_chat_prompt_2, multi_chat_prompt_3
from langchain_community.chat_message_histories import ChatMessageHistory, FileChatMessageHistory
from app.code_agent.model.qwen import llm_qwen
from langchain_core.messages import HumanMessage, AIMessage
from langchain_community.agent_toolkits.file_management import FileManagementToolkit
from langchain_core.runnables import RunnableWithMessageHistory, RunnableLambda
from langchain.agents import create_agent


def get_session_history(session_id: str):
    return FileChatMessageHistory(file_path=f"{session_id}.json")


file_management_toolkit = FileManagementToolkit(root_dir="/Users/dingyu/Documents/company/ai_ollama_python/.tmp")
file_tools = file_management_toolkit.get_tools()

agent = create_agent(model=llm_qwen, tools=file_tools)


# chain = multi_chat_prompt_1 | llm_qwen
# chain = multi_chat_prompt_2 | llm_qwen
chain = multi_chat_prompt_3 | agent

chain_with_history = RunnableWithMessageHistory(
    runnable=chain,
    get_session_history=get_session_history,
)

# session_id = uuid.uuid4()
session_id = "66d855d9-8a06-457f-83d4-47c3cd13fcf9"
print("session_id:" + str(session_id))

while True:
    user_input = input("用户：")
    if user_input.lower() == "exit" or user_input.lower() == "quit" or user_input.lower() == "q":
        break

    resp = chain_with_history.stream(
        {"question": user_input},
        config={
            "configurable": {"session_id": session_id}
        },
        stream=True
    )
    print("助理：")
    # print(resp)
    for chunk in resp:
        if "messages" in chunk and chunk["messages"]:
            last_message = chunk["messages"][-1]
            if hasattr(last_message, 'content') and last_message.content:
                print(last_message.content, end="", flush=True)  # Stream content
            # Optional: Handle tool calls
            elif hasattr(last_message, 'tool_calls') and last_message.tool_calls:
                print(f"[Calling tools: {[tc.name for tc in last_message.tool_calls]}]", end="", flush=True)
    print("\n")

