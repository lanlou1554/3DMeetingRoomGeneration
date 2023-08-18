import requests


# # 发送请求
# x = requests.request('get', 'https://www.runoob.com/')
#
# # 返回网页内容
# print(x.status_code)

def post_method(data):
    # url = ''
    # res = requests.post(url, data)
    # print(res)
    f = open(r"D:\four2\Graduating Design\nlp\generate_position\algorithm\result.json", "w")
    f.write(data)
    f.close()

def get_method(type,object,color,shape,size="",style=""):
    url = 'http://localhost:9000'
    params ={
        'type': type,
        'object': object,
        'color': color,
        'shape': shape,
        'size': size,
        'style':style
    }
    res = requests.get(url,params)
    print(res.content)
    return res.content