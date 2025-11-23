import tkinter as tk
import tkinter.ttk as ttk
import requests
import parsel
import os
import time


class NovelDownloader:
    def __init__(self, root):
        self.root = root
        self.setup_ui()
        self.search_list = []
        self.session = requests.Session()  # 使用会话保持连接

    def setup_ui(self):
        self.root.title("小说下载器 - 优化版")
        self.root.geometry("650x550+300+200")

        # 主框架
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)

        # 搜索框架
        search_frame = tk.Frame(main_frame)
        search_frame.pack(fill=tk.X, pady=10)

        tk.Label(search_frame, text="书名/作者", font=("微软雅黑", 12)).pack(side=tk.LEFT, padx=10)
        self.name_va = tk.StringVar()
        self.search_entry = tk.Entry(search_frame, relief="flat", textvariable=self.name_va,
                                     width=30, font=("微软雅黑", 10))
        self.search_entry.pack(side=tk.LEFT, padx=5)
        self.search_entry.bind('<Return>', lambda e: self.show())  # 回车搜索

        tk.Button(search_frame, text='查询', font=('微软雅黑', 10), relief="flat",
                  bg='#88e2d6', width=8, command=self.show).pack(side=tk.LEFT, padx=5)

        # 下载框架
        download_frame = tk.Frame(main_frame)
        download_frame.pack(fill=tk.X, pady=10)

        tk.Label(download_frame, text="下载序号", font=("微软雅黑", 12)).pack(side=tk.LEFT, padx=10)
        self.num_va = tk.StringVar()
        self.download_entry = tk.Entry(download_frame, relief="flat", textvariable=self.num_va,
                                       width=8, font=("微软雅黑", 10))
        self.download_entry.pack(side=tk.LEFT, padx=5)
        self.download_entry.bind('<Return>', lambda e: self.download())  # 回车下载

        tk.Button(download_frame, text='下载', font=("微软雅黑", 10), relief="flat",
                  bg='#88e2d6', width=8, command=self.download).pack(side=tk.LEFT, padx=10)

        # 状态显示
        self.status_var = tk.StringVar(value="就绪")
        status_label = tk.Label(main_frame, textvariable=self.status_var, font=("微软雅黑", 10),
                                fg="blue")
        status_label.pack(anchor=tk.W)

        # 进度显示
        self.progress_var = tk.StringVar()
        progress_label = tk.Label(main_frame, textvariable=self.progress_var, font=("微软雅黑", 9),
                                  fg="green")
        progress_label.pack(anchor=tk.W)

        # 表格框架
        table_frame = tk.Frame(main_frame)
        table_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        columns = ('num', 'book_name', 'book_author', 'book_id')
        self.tree_view = ttk.Treeview(table_frame, height=15, show='headings', columns=columns)

        # 设置列
        self.tree_view.column('num', width=60, anchor='center')
        self.tree_view.column('book_name', width=250, anchor='w')
        self.tree_view.column('book_author', width=120, anchor='center')
        self.tree_view.column('book_id', width=100, anchor='center')

        self.tree_view.heading('num', text='序号')
        self.tree_view.heading('book_name', text='书名')
        self.tree_view.heading('book_author', text='作者')
        self.tree_view.heading('book_id', text='书ID')

        # 滚动条
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree_view.yview)
        self.tree_view.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree_view.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    def get_response(self, url, retry=2):
        """
        优化的请求函数：使用会话、超时、重试机制
        """
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Connection": "keep-alive"
        }

        for attempt in range(retry):
            try:
                response = self.session.get(url, headers=headers, timeout=8)
                response.encoding = 'utf-8'  # 强制使用UTF-8编码
                if response.status_code == 200:
                    return response
                else:
                    print(f"请求失败，状态码: {response.status_code}")
            except Exception as e:
                if attempt == retry - 1:  # 最后一次重试也失败
                    print(f"请求失败: {url}, 错误: {e}")
                    return None
                time.sleep(0.5)  # 短暂等待后重试

        return None

    def search(self, word):
        """
        优化的搜索功能
        """
        search_url = f"https://www.xiakexsw.com/search/?keyword={word}&t=0"
        response = self.get_response(search_url)
        if not response:
            return []

        html_data = response.text
        url_selector = parsel.Selector(html_data)
        lis = url_selector.css(".subject-item")

        book_info = []
        for num, li in enumerate(lis):
            # 小说名字
            book_name = "".join(li.css(".info h2 a ::text").getall()).strip()
            if not book_name:
                continue

            book_link = li.css(".info h2 a::attr(href)").get()
            if not book_link:
                continue

            book_id = book_link.replace("/novel/", "").replace(".html", "")
            book_author = li.css(".info .pub a::text").get() or "未知作者"

            book_info.append({
                "num": num,
                "book_name": book_name,
                "book_id": book_id,
                "book_author": book_author,
            })

        return book_info

    def get_chapter_url(self, book_id):
        """
        优化的获取章节列表函数
        """
        novel_url = f'https://www.xiakexsw.com/chapter/{book_id}/'
        response = self.get_response(novel_url)
        if not response:
            return None, []

        html_data = response.text
        url_selector = parsel.Selector(html_data)

        # 提取小说名
        book_name_element = url_selector.css("#content h1::text")
        if not book_name_element:
            return None, []

        book_name = book_name_element.extract_first().replace("最新章节列表", "").strip()

        # 提取全部章节url
        chapter_urllist = url_selector.xpath("//*[@id=\"chapter\"]/a/@href").getall()
        return book_name, chapter_urllist

    def get_content(self, url):
        """
        优化的内容获取函数
        """
        response = self.get_response(url)
        if not response:
            return None, None

        html_data = response.text
        url_selector = parsel.Selector(html_data)

        # 提取章节名称
        chapter_title = url_selector.css(".neirong h2::text").get()
        if not chapter_title:
            return None, None

        # 提取章节内容 - 更精确的选择器
        content_paragraphs = url_selector.css("#txt p::text").getall()
        if not content_paragraphs:
            # 尝试其他可能的选择器
            content_paragraphs = url_selector.css(".content p::text").getall()
            if not content_paragraphs:
                content_paragraphs = url_selector.css(".novelcontent p::text").getall()

        content = "\n".join(content_paragraphs)
        return chapter_title, content

    def save_chapter(self, book_name, chapter_title, content):
        """
        优化的保存函数
        """
        if not chapter_title or not content:
            return False

        # 创建目录
        file_dir = f"{book_name}"
        if not os.path.exists(file_dir):
            os.makedirs(file_dir)

        # 清理文件名中的非法字符
        safe_title = "".join(c for c in chapter_title if c not in r'\/:*?"<>|')
        file_path = os.path.join(file_dir, f"{safe_title}.txt")

        try:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(chapter_title + "\n\n")
                f.write(content + "\n")
            return True
        except Exception as e:
            print(f"保存失败 {chapter_title}: {e}")
            return False

    def show(self):
        """显示搜索结果"""
        name = self.name_va.get().strip()
        if not name:
            self.status_var.set("请输入搜索内容")
            return

        self.status_var.set("搜索中...")
        self.progress_var.set("")

        # 清空表格
        for item in self.tree_view.get_children():
            self.tree_view.delete(item)

        try:
            self.search_list = self.search(name)
            self.update_results()
        except Exception as e:
            self.status_var.set(f"搜索失败: {str(e)}")

    def update_results(self):
        """更新结果显示"""
        for book in self.search_list:
            self.tree_view.insert('', tk.END, values=(
                book['num'], book['book_name'], book['book_author'], book['book_id']
            ))

        count = len(self.search_list)
        self.status_var.set(f"找到 {count} 本小说")

    def download(self):
        """下载小说"""
        if not self.search_list:
            self.status_var.set("请先查询小说")
            return

        num_str = self.num_va.get().strip()
        if not num_str or not num_str.isdigit():
            self.status_var.set("请输入有效的序号")
            return

        num = int(num_str)
        if num < 0 or num >= len(self.search_list):
            self.status_var.set("序号超出范围")
            return

        book_id = self.search_list[num]['book_id']
        book_name = self.search_list[num]['book_name']

        self.status_var.set(f"开始下载: {book_name}")
        self.progress_var.set("获取章节列表中...")

        # 获取章节列表
        book_name, chapter_urllist = self.get_chapter_url(book_id)
        if not book_name or not chapter_urllist:
            self.status_var.set("获取章节列表失败")
            return

        total_chapters = len(chapter_urllist)
        self.progress_var.set(f"共{total_chapters}章，开始下载...")

        base_url = f'https://www.xiakexsw.com/chapter/{book_id}/'
        success_count = 0

        # 单线程顺序下载，但优化了请求间隔
        for i, chapter_url in enumerate(chapter_urllist, 1):
            full_url = base_url + chapter_url

            # 更新进度
            self.progress_var.set(f"下载进度: {i}/{total_chapters} ({i / total_chapters * 100:.1f}%)")
            self.root.update()  # 更新界面

            chapter_title, content = self.get_content(full_url)
            if chapter_title and content:
                if self.save_chapter(book_name, chapter_title, content):
                    success_count += 1
                    print(f"[{i}/{total_chapters}] {chapter_title} - 成功")
                else:
                    print(f"[{i}/{total_chapters}] {chapter_title} - 保存失败")
            else:
                print(f"[{i}/{total_chapters}] 章节获取失败")

            # 智能延迟：根据章节数量调整请求间隔
            if total_chapters > 50:
                time.sleep(0.3)  # 章节多时延迟短一些
            else:
                time.sleep(0.5)  # 章节少时延迟正常

        self.status_var.set(f"下载完成: {book_name}")
        self.progress_var.set(f"成功下载 {success_count}/{total_chapters} 章")


if __name__ == '__main__':
    root = tk.Tk()
    app = NovelDownloader(root)
    root.mainloop()