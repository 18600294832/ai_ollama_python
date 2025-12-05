from langchain_experimental.tools.python.tool import PythonREPLTool
from app.bailian.common import llm
from langchain.agents import create_agent
from langchain_core.prompts import PromptTemplate
from langchain_core.messages import HumanMessage
# 定义工具
tools = [PythonREPLTool()]
tool_names = ["PythonREPLTool"]


# 创建系统提示词
prompt_template = PromptTemplate.from_template(template=f"""
尽你所能回答用户的问题或执行用户的命令，你可以使用一下工具：{tool_names}
--
请按照以下格式进行思考：
- 问题：你必须回答的输入问题
- 思考：你考虑应该怎么做
- 行动：要采取的行动，应该是[{tool_names}]中的一个
- 行动输入：行动的输入
- 观察：行动的结果
···（这个思考/行动/行动输入/观察可以重复N次）
# 最终答案
对原始输入问题的最终答案
```
注意：
- PythonREPLTool工具的入参是python的代码，不允许添加```python或 ```py等标记
--
""")


# 创建智能体
agent = create_agent(
    llm,
    tools=tools,
)


# 调用智能体 - 使用消息格式
user_task = """
1. 向 /Users/dingyu/Documents/company/ai_ollama_python/.tmp 目录下写入一个新文件，名称为index.html
2. 写一个在线教育的官网。包含3个tab，分别是：首页、实战课、体系课和关于我们
3. 首页展示3个模块，分别是：热门课程、上新课程、爆款课程
4. 关于我们展示平台的联系方式等基本信息
5. 要参考一下目前市面上的优秀的在线教育的网站，比如慕课网
6. 课程需要一些课程名称，以及一些课程图片，图片从网上找一些可以看到的图片展示出来
"""

response = agent.invoke({
    "messages": [HumanMessage(content=user_task)]
})


print(response)
