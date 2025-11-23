import tkinter as tk
import tkinter.ttk as ttk

# 数据请求模块
import requests
# #正则表达式模块
# import re
# 数据解析模块
import parsel
# 文件操作模块
import os
#漂亮的表格
import prettytable as pt
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
    # 调用发送请求函数
    html_data = get_response(url).text
    # 解析获取到的内容，使可以选择元素
    url_selector = selector(html_data)
    # 提取小说名
    book_name = url_selector.css("#content h1::text").extract_first().replace("最新章节列表", "")
    # 提取全部章节url
    chapter_urllist = url_selector.xpath("//*[@id=\"chapter\"]/a/@href").getall()
    return book_name, chapter_urllist


def get_content(url):
    """
    获取小说内容/标题
    :param url: 小说章节url
    :return:章节名称，小说内容
    """
    # 调用发送请求函数
    html_data = get_response(url).text
    # 解析获取到的内容，使可以选择元素
    url_selector = selector(html_data)
    # 提取章节名称
    chapter_title = url_selector.css(".neirong h2::text").get()
    # 提取章节内容
    content = "\n".join(url_selector.css("#txt p::text").getall())
    return chapter_title, content


def save(book_name, chapter_title, content):
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
    with open(file + chapter_title + ".txt", mode="a", encoding="utf-8") as f:
        f.write(chapter_title + "\n")
        f.write(content + "\n")
    print(book_name,"--------",chapter_title, "已经保存")

def get_novel_id(url):
    """
    获取小说ID
    :param url: 某分类的链接
    :return:
    """
    # 调用发送请求函数
    html_data = get_response(url).text
    # 解析获取到的内容，使可以选择元素
    url_selector = selector(html_data)
    href = url_selector.css(".subject-item h2 a::attr(href)").getall()
    href = [i.replace("/novel/","").replace(".html","") for i in href]
    return href





def search(word):
    """
    搜索功能
    :param word: 书名/作者
    :return:
    """
    # 调用发送请求函数
    search_url = f"https://www.xiakexsw.com/search/?keyword={word}&t=0"
    html_data = get_response(search_url).text
    # 解析获取到的内容，使可以选择元素
    url_selector = selector(html_data)
    lis = url_selector.css(".subject-item")
    book_info = []
    num = 0
    for li in lis:
        #小说名字
        book_name = "".join(li.css(".info h2 a ::text").getall())
        book_id = li.css(".info h2 a::attr(href)").get().replace("/novel/","").replace(".html","")
        book_author = li.css(".info .pub a::text").get()
        dit = {
            "num": num,  # 添加序号
            "book_name": book_name,
            "book_id": book_id,
            "book_author": book_author,
        }
        num += 1
        book_info.append(dit)
    return book_info





# 单线程
def main(word):
    novel_url = f'https://www.xiakexsw.com/chapter/{word}/'
    book_name, chapter_urllist = get_chapter_url(url=novel_url)
    print(book_name)
    for chapter_url in chapter_urllist:
        index_url = f'https://www.xiakexsw.com/chapter/{word}/' + chapter_url
        chapter_title, content = get_content(url=index_url)
        save(book_name, chapter_title, content)
        time.sleep(1)


def show():
    name = name_va.get()
    print("输入的查询内容为：", name)

    # 执行搜索并显示结果
    search_list = search(name)
    for stu in search_list:
        tree_view.insert('', tk.END, values=(stu['num'], stu['book_name'], stu['book_author'], stu['book_id']))


def download():
    # 获取小说名字
    name = name_va.get()
    # 小说名字传递到 搜索功能函数
    search_list = search(name)
    # 根据选择序号获取书ID
    num = num_va.get()
    if num and num.isdigit():
        book_id = search_list[int(num)]['book_id']
        book_name = search_list[int(num)]['book_name']
        print("ID号为：", book_id)
        print("开始下载：", book_name)
        main(book_id)
    else:
        print("请输入有效的序号")




if __name__ == '__main__':
    # 创建界面
    root = tk.Tk()
    # 设置一个标题
    root.title("小说下载器")
    # 设置界面大小
    root.geometry("600x500+300+300")
    # 设置可变变量
    name_va = tk.StringVar()

    # 主框架
    main_frame = tk.Frame(root)
    main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    # 搜索框架
    search_frame = tk.Frame(main_frame)
    search_frame.pack(fill=tk.X, pady=10)

    # 设置文本
    tk.Label(search_frame, text="书名/作者", font=("微软雅黑", 12)).pack(side=tk.LEFT, padx=10)
    # 设置一个输入框
    tk.Entry(search_frame, relief="flat", textvariable=name_va, width=30).pack(side=tk.LEFT, padx=5)

    # 查询按钮
    tk.Button(search_frame, text='查询', font=('微软雅黑', 10), relief="flat",
              bg='#88e2d6', width=10, command=show).pack(side=tk.LEFT, padx=10)

    # 下载框架
    download_frame = tk.Frame(main_frame)
    download_frame.pack(fill=tk.X, pady=10)

    # 序号获取
    num_va = tk.StringVar()
    # 设置文本
    tk.Label(download_frame, text="下载序号", font=("微软雅黑", 12)).pack(side=tk.LEFT, padx=10)
    # 设置一个输入框
    tk.Entry(download_frame, relief="flat", textvariable=num_va, width=10).pack(side=tk.LEFT, padx=5)

    # 设置下载按钮
    tk.Button(download_frame, text='下载', font=("微软雅黑", 10), relief="flat",
              bg='#88e2d6', width=10, command=download).pack(side=tk.LEFT, padx=10)

    # 表格框架
    table_frame = tk.Frame(main_frame)
    table_frame.pack(fill=tk.BOTH, expand=True, pady=10)

    # 设置标签名字和中文显示的内容
    columns = ('num', 'book_name', 'book_author', 'book_id')
    tree_view = ttk.Treeview(table_frame, height=15, show='headings', columns=columns)

    # 设置列名和宽度
    tree_view.column('num', width=50, anchor='center')
    tree_view.column('book_name', width=200, anchor='center')
    tree_view.column('book_author', width=100, anchor='center')
    tree_view.column('book_id', width=100, anchor='center')

    # 给列名设置显示的名字
    tree_view.heading('num', text='序号')
    tree_view.heading('book_name', text='书名')
    tree_view.heading('book_author', text='作者')
    tree_view.heading('book_id', text='书ID')

    # 添加滚动条
    scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=tree_view.yview)
    tree_view.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    tree_view.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    root.mainloop()