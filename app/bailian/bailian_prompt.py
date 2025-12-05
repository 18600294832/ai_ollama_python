import os

from langchain_core.prompts import ChatPromptTemplate, PromptTemplate, ChatMessagePromptTemplate, FewShotPromptTemplate
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    model="qwen3-max",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    streaming=True,
)


def chatPromptTemplateTest():
    # 提示词测试  promptTemplate 开始
    promptTemplate = PromptTemplate.from_template("今天{something}真不错")
    print(promptTemplate)
    # 模版 + 变量 => 提示词
    prompt = promptTemplate.format(something="天气")
    print(prompt)

    resp = llm.stream(prompt)

    for chunk in resp:
        print(chunk.content, end="")
    # 提示词测试 promptTemplate 结束


def chatMessagePromptTemplateTest():
    # 聊天提示词测试 chatPromptTemplate 开始
    system_message_template = ChatMessagePromptTemplate.from_template(
        template="你是一个{role}专家，擅长回答{domain}领域问题",
        role="system",
    )
    user_message_template = ChatMessagePromptTemplate.from_template(
        template="用户问题：{question}",
        role="user",
    )

    chat_prompt_template = ChatPromptTemplate.from_messages([
        system_message_template,
        user_message_template
    ])

    prompt = chat_prompt_template.format_prompt(
        role="编程",
        domain="web开发",
        question="你擅长什么？"
    )

    llm.stream(prompt)
    for chunk in llm.stream(prompt):
        print(chunk.content, end="")
    # 聊天提示词测试 chatPromptTemplate 结束


# 少样本提示模版
def fewShotPromptTemplateTest():
    # fewShotPromptTemplate 测试开始
    example_template = "输入：{input}\n输出：{output}"

    examples = [
        {"input": "hello", "output": "你好"}, {"input": "how are you", "output": "你如何"},
        {"input": "what's your name", "output": "你的名字"}
    ]

    few_shot_prompt = FewShotPromptTemplate(
        examples=examples,
        example_prompt=PromptTemplate.from_template(example_template),
        prefix="请将以下英文翻译中文：",
        suffix="输出：{text}\n输出：",
        input_variables=["text"],
    )

    prompt = few_shot_prompt.format(text="Thank you!")
    resp = llm.stream(prompt)
    for chunk in resp:
        print(chunk.content, end="")


# 少样本提示模版 chain
def fewShotPromptTemplateChainTest():
    # fewShotPromptTemplate 测试开始
    example_template = "输入：{input}\n输出：{output}"

    examples = [
        {"input": "hello", "output": "你好"}, {"input": "how are you", "output": "你如何"},
        {"input": "what's your name", "output": "你的名字"}
    ]

    few_shot_prompt = FewShotPromptTemplate(
        examples=examples,
        example_prompt=PromptTemplate.from_template(example_template),
        prefix="请将以下英文翻译中文：",
        suffix="输出：{text}\n输出：",
        input_variables=["text"],
    )

    chain = few_shot_prompt | llm
    resp = chain.stream(input={"text": "Thank you!"})
    for chunk in resp:
        print(chunk.content, end="")


if __name__ == '__main__':
    chatPromptTemplateTest()
    print("\n")
    print("---------------------------------------------------------------------------------------------------------")
    chatMessagePromptTemplateTest()
    print("\n")
    print("---------------------------------------------------------------------------------------------------------")
    fewShotPromptTemplateTest()
    print("\n")
    print("---------------------------------------------------------------------------------------------------------")
    fewShotPromptTemplateChainTest()
