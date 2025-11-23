#数据请求模块
import requests
# #正则表达式模块
# import re
#数据解析模块
import parsel
#文件操作模块
import os
import time

import concurrent.futures

def selector(text):
    """
    将传入的数据解析，使得可以选择元素
    :param text:html文本
    :return:
    """
    url_selector = parsel.Selector(text)
    return url_selector


def get_response(url):
    """
    发送请求函数
    :param url: 请求链接
    :return: response 响应的对象
    """
    headers = {
        "User_Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36",
        "accept-language": "h-CN,zh;q=0.9"
    }
    response = requests.get(url=url, headers=headers)
    return response

def get_chapter_url(url):
    """
    获取全部章节url/小说名
    :param url: 小说目录页
    :return:小说名称，全部章节链接
    """
    #调用发送请求函数
    html_data = get_response(url).text
    #解析获取到的内容，使可以选择元素
    url_selector = selector(html_data)
    #提取小说名
    book_name = url_selector.css("#content h1::text").extract_first().replace("最新章节列表", "")
    #提取全部章节url
    chapter_urllist = url_selector.xpath("//*[@id=\"chapter\"]/a/@href").getall()
    return book_name,chapter_urllist

def get_content(url):
    """
    获取小说内容/标题
    :param url: 小说章节url
    :return:章节名称，小说内容
    """
    #调用发送请求函数
    html_data = get_response(url).text
    #解析获取到的内容，使可以选择元素
    url_selector = selector(html_data)
    #提取章节名称
    chapter_title = url_selector.css(".neirong h2::text").get()
    #提取章节内容
    content = "\n".join(url_selector.css("#txt p::text").getall())
    return chapter_title,content


def save(book_name,chapter_title,content):
    """
    保存数据函数
    :param book_name: 小说名称
    :param chapter_title: 章节名
    :param content: 内容
    :return:
    """
    # 自动创建一个文件夹
    file = f"{book_name}\\"
    if not os.path.exists(file):
        os.mkdir(file)
    with open(file+chapter_title + ".txt", mode="a", encoding="utf-8") as f:
        f.write(chapter_title + "\n")
        f.write(content + "\n")
    print(chapter_title,"已经保存")


def main(home_url):
    index_url = 'https://www.xiakexsw.com/chapter/8492/' + chapter_url
    chapter_title,content = get_content(url=home_url)
    save(book_name, chapter_title, content)


if __name__ == '__main__':
    url = "https://www.xiakexsw.com/chapter/8492/"
    book_name,chapter_urllist = get_chapter_url(url=url)
    exe = concurrent.futures.ThreadPoolExecutor(max_workers=7)
    for chapter_url in chapter_urllist:
        index_url = 'https://www.xiakexsw.com/chapter/8492/' + chapter_url
        exe.submit(main, index_url)
        time.sleep(1)
    exe.shutdown()