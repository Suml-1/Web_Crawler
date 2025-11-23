"""

http2.0爬虫解决方案
https://spa16.scrape.center/

user-agent
Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36 Edg/142.0.0.0
 数据来源：https://spa16.scrape.center/api/book/?limit=18&offset=54
"""
# 不行
# import requests
#
# headers = {
#     "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36 Edg/142.0.0.0"
# }
#
# url = "https://spa16.scrape.center/api/book/?limit=18&offset=54"
# response = requests.get(url,headers=headers)
# print(response.status_code)


import httpx

client = httpx.Client(http2=True)
response = client.get("https://spa16.scrape.center/api/book/?limit=18&offset=54")
print(response.text)

