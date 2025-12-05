from langchain_ollama.llms import OllamaLLM
from langchain_ollama.chat_models import ChatOllama
from langchain.messages import AIMessage


def chatOllamaTest():
    llm = ChatOllama(model="qwen3-vl:2b", temperature=3)
    resp = llm.invoke("你好 。你是谁")
    print(resp.content)


def main():
    print("hello world")
    model = OllamaLLM(model="qwen3-vl:2b")
    result = model.invoke("你是谁")
    print(result)
    print("----")
    if isinstance(result, AIMessage) and result.tool_calls:
        print(result.tool_calls)


if __name__ == '__main__':
    llm = ChatOllama(model="qwen3-vl:2b")
    messages = [
        (
            "system",
            "You are a helpful assistant that translates English to French. Translate the user sentence.",
        ),
        ("human", "I love programming."),
    ]
    ai_msg = llm.stream(messages)
    for chunk in ai_msg:
        print(chunk.content, end="")


