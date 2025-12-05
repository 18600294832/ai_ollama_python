from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder, ChatMessagePromptTemplate, \
    SystemMessagePromptTemplate, HumanMessagePromptTemplate


# invoke 或者 call 或者 stream 时候需要的是一个message对象。 所以一定要使用template.from_message函数，不能使用 from_template函数
# invoke 或者 call 或者 stream 时候需要的是一个message对象。 所以一定要使用template.from_message函数，不能使用 from_template函数
# invoke 或者 call 或者 stream 时候需要的是一个message对象。 所以一定要使用template.from_message函数，不能使用 from_template函数

system_message_template = ChatMessagePromptTemplate.from_template(
    template="你是一位优秀的技术专家，擅长解决各种开发中的技术问题",
    role="system",
)

user_message_template = ChatMessagePromptTemplate.from_template(
    template="{question}",
    role="user",
)

multi_chat_prompt_1 = ChatPromptTemplate.from_messages([
    system_message_template,
    MessagesPlaceholder(variable_name="chat_history"),
    user_message_template,
]
)

multi_chat_prompt_2 = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template("你是一位优秀的技术专家，擅长解决各种开发中的技术问题"),
    MessagesPlaceholder(variable_name="chat_history"),
    HumanMessagePromptTemplate.from_template("{question}")
])


multi_chat_prompt_3 = ChatPromptTemplate.from_messages([
    ("system", "你是一位优秀技术专家，擅长解决各种开发中的技术问题"),
    ("human", "{question}"),
])
