# 1.反转字典
my_dict={
    "brand":"ford",
    "model":"mustang",
    "year":2012
}

print(dict(map(reversed,my_dict.items())))
# 结果：{'ford': 'brand', 'mustang': 'model', 2012: 'year'}

#2.对字典列表进行排序
dicts_lists = [
    {
        "Name":"Jane",
        "Age":19,
    },
    {
        "Name": "Jack",
        "Age": 35,
    },
    {
        "Name": "mid",
        "Age": 15,
    }
]
dicts_lists.sort(key=lambda item: item.get("Age"))
print(dicts_lists)
#结果：[{'Name': 'mid', 'Age': 15}, {'Name': 'Jane', 'Age': 19}, {'Name': 'Jack', 'Age': 35}]



#3.根据另一个列表对一个列表进行排序
a = ["blue","green","red","black","yellow"]
b=[4,2,1,3,5]
sortedlist = [val for(_,val) in sorted(zip(b, a), key=lambda x: x[0])]
print(sortedlist)
#结果：['red', 'green', 'black', 'blue', 'yellow']


#4.将两个列表合并到一个列表
a = ["blue","green","red","black","yellow"]
b=[4,2,1,3,5]
dict_ = dict(zip(a,b))
print(dict_)
#结果：{'blue': 4, 'green': 2, 'red': 1, 'black': 3, 'yellow': 5}




#5.对字符串列表进行排序
my_list =["blue","green","red","black","yellow"]

#按字母顺序
my_list.sort()
print(my_list)
#结果：['black', 'blue', 'green', 'red', 'yellow']

#长度
print(sorted(my_list, key=len))
#结果：['red', 'blue', 'black', 'green', 'yellow']


#6.检查文件是否存在
import os

#isfile 判断文件
#exists 判断文件夹

exists = os.path.exists('E:\资料\学校')
print(exists)



