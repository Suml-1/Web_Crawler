"""
https://22d25e16be9eaf91b79966.a26b53.lol/book/82506/1.html

解析数据：
    re正则表达式
        re.findall()
    CSS选择器
        import parsel
    xpath节点提取

"""
# response = requests.get(url=url, headers=headers)
# 1.正则表达式
# title = re.findall("<span class=\"title\">.*(第.章.*)</span>",response.text)[0]
#
# content = re.findall("<div id=\"chaptercontent\" class=\"Readarea ReadAjax_content\">(.*?)</p>",response.text,re.S)[0].replace("<br /><br />","\n")
# content = content.replace("\n","").replace("(.*)","$1")
# # print(response.text)
# print(content)
# # print(title)

# print(response.status_code)
#2. css

#
# selector = parsel.Selector(response.text)
# title = selector.css(".neirong h2::text").get()
# content = "\n".join(selector.css("#txt p::text").getall())
# print(title)
# print(content)
#
# #xpath
# #改css为xpath并修改语法就行了
#
# with open(title+".txt",mode="a",encoding="utf-8") as f:
#     f.write(title+"\n")
#     f.write(content+"\n")



#数据请求模块
import requests
#正则表达式模块
import re
#数据解析模块
import parsel
#文件操作模块
import os
import time



#章节链接
url = "https://www.xiakexsw.com/chapter/8492/16985.html"
#目录链接
list_url="https://www.xiakexsw.com/chapter/8492/"
# 请求头
headers = {
    "User_Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36",
    "accept-language":"h-CN,zh;q=0.9"
}
#目录所在页html
html_data = requests.get(url=list_url,headers=headers)
chapter_url_selector = parsel.Selector(html_data.text)
#小说名字获取
book_name = chapter_url_selector.css("#content h1::text").extract_first().replace("最新章节列表","")
print(book_name)
#自动创建一个文件夹
file = f"{book_name}\\"
if not os.path.exists(file):
    os.mkdir(file)
#提取全部章节url
chapter_urllist = chapter_url_selector.xpath("//*[@id=\"chapter\"]/a/@href").getall()

#for循环遍历
for chapter_url in chapter_urllist:
    index_url = 'https://www.xiakexsw.com/chapter/8492/' + chapter_url
    # 章节所在页HTML
    response = requests.get(url=index_url, headers=headers)
    selector = parsel.Selector(response.text)
    # 提取章节标题
    title = selector.css(".neirong h2::text").get()
    #提取章节内容
    content = "\n".join(selector.css("#txt p::text").getall())
    # 创建文档
    with open(file+book_name + ".txt", mode="a", encoding="utf-8") as f:
        f.write(title + "\n")
        f.write(content + "\n")
        time.sleep(1)




