from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_core.prompts import ChatPromptTemplate
from langchain_text_splitters import CharacterTextSplitter
import os
prompt = ChatPromptTemplate.from_messages([
    ("human", "{question}"),
])
# 获取当前脚本的绝对路径
current_file_path = os.path.abspath(__file__)
print(f"当前文件: {current_file_path}")

loader = TextLoader("./resource/a.txt")
document = loader.load()
print(document)


directLoader = DirectoryLoader("./resource/", glob="*.txt", loader_cls=TextLoader, show_progress=True)
document = directLoader.load()
print(document)


text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=0, separator="\n\n", keep_separator=True)

segments = text_splitter.split_documents(document)
for segment in segments:
    print(segment.page_content)
    print("------------")
