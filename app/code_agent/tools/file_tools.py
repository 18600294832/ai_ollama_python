from langchain_community.agent_toolkits.file_management import FileManagementToolkit

file_management_toolkit = FileManagementToolkit(root_dir="/Users/dingyu/Documents/company/ai_ollama_python/.tmp")
file_tools = file_management_toolkit.get_tools()
