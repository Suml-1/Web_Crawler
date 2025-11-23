import execjs
import os

# 1.实例化一个node对象
node = execjs.get()

# 2.js源文件编译
# 获取当前脚本目录
script_dir = os.path.dirname(os.path.abspath(__file__))
js_file = os.path.join(script_dir, "wechat.js")

# 读取 JavaScript 文件
with open(js_file, "r", encoding="utf-8") as f:
    js_code = f.read()

# 编译 JavaScript 代码
ctx = node.compile(js_code)

# 3.执行js函数
# 修正语法错误：使用正确的字符串格式化
funcName = "getPwd('{0}')".format('123456')
pwd = ctx.eval(funcName)
print(pwd)