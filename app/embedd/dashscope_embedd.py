from langchain_community.embeddings import DashScopeEmbeddings
import os

from langchain_redis import RedisVectorStore

from redis_util import redis_config

dashscope_api_key = os.getenv("DASHSCOPE_API_KEY")

embeddings = DashScopeEmbeddings(model="text-embedding-v4", dashscope_api_key=dashscope_api_key)


vector_store = RedisVectorStore(embeddings, config=redis_config)

vector_store.add_texts(["实现以文搜图、以图搜视频、以图搜图等跨模态的语义搜索。", "在统一的向量空间中，衡量不同模态内容之间的语义相似性。", "基于内容的语义向量进行智能分组、打标和聚类分析。"])

store_result = vector_store.similarity_search_with_score("语义相似度计算", k=3)

for text, score in store_result:
    print(text, score)





