import json
import math
import random

import request

HALLWAY=random.uniform(0.6,1)#过道宽度
WIDTH = 0.5#桌子宽度 面向黑板的边
LENGTH = 0.5#桌子长度
FRONT_DISTANT=random.uniform(0.9,1.2)#前后距离
FRONT_WALL=random.uniform(2.2, 3)#第一排和黑板的距离
FINAL_WALL=random.uniform(1.1, 1.5)#最后一排和墙的距离

class layout(object):
    LayoutObjects=[]

    def __init__(self, LayoutObjects):
        self.LayoutObjects=LayoutObjects

class position(object):
    id = ''
    type = ''
    xPosition = 0.0
    yPosition = 0.0
    zPosition = 0.0
    xRotation = 0.0
    yRotation = 0.0
    zRotation = 0.0

    def __init__(self, id, type, xPosition, yPosition, zPosition, xRotation, yRotation, zRotation):
        self.id = id
        self.type = type
        self.xPosition = xPosition
        self.yPosition = yPosition
        self.zPosition = zPosition
        self.xRotation = xRotation
        self.yRotation = yRotation
        self.zRotation = zRotation


class room(object):
    id = ''
    width = 0.0
    length = 0.0

    def __init__(self, id, width, length):
        self.id = id
        self.width = width
        self.length = length


class chair(object):
    id = ''
    width = 0
    length = 0
    height = 0

    def __init__(self, id, width, length, height):
        self.id = id
        self.width = width
        self.length = length
        self.height = height

class blackboard(object):
    id=''
    width=0
    length=0
    height = 0
    def __init__(self, id, width, length, height):
        self.id = id
        self.width = width
        self.length = length
        self.height = height

class table(object):
    id=''
    width=0
    length=0
    height = 0
    def __init__(self, id, width, length, height):
        self.id = id
        self.width = width
        self.length = length
        self.height = height

class lectern(object):
    id=''
    width=0
    length=0
    height = 0
    def __init__(self, id, width, length, height):
        self.id = id
        self.width = width
        self.length = length
        self.height = height
def post(json_dict):
    print(json_dict)
    # people,row,hallway
    init(json_dict["people_number"], json_dict["row_number"], json_dict["aisle_number"])
    #      json_dict["inner_circle_chair_num"])


def init(people,row,hallway):#根据人数计算几行几列
    #行:列=6:4
    column=0
    if(row<0 and hallway<0):
        column=math.ceil(math.sqrt((2*people)/3))
        row=int((3*column)/2)
        if(row*column<people):
            print("error:座位数不够！！")
    if(row>0 and hallway>0):
        column=math.ceil(people/row)
        if(column<hallway+1):
            column=hallway+1
        if(column&1 and hallway&1):
            column=column+1

    if(row>0 and hallway<0):
        column = math.ceil(people/row)

    if(row<0 and hallway>0):
        column = math.ceil(math.sqrt((2 * people) / 3))
        row = int((3 * column) / 2)
        if (column < hallway + 1):
            column = hallway + 1
            row = math.ceil(people/column)
        if (column & 1 and hallway & 1):
            column = column + 1
        if (row * column < people):
            print("error:座位数不够！！")
    # calculate_position(row, column, hallway)
    request.post_method(calculate_position(row, column,hallway))
def calculate_position(row,column,hallway):
    global WIDTH,LENGTH
    object_position = []
    now_chair=json.loads(request.get_method('classroom','chair','',''))
    now_chair = chair(now_chair["id"], float(now_chair["width"]), float(now_chair["length"]),
                      float(now_chair["height"]))
    now_blackboard=json.loads(request.get_method('classroom','screen','',''))
    now_blackboard = blackboard(now_blackboard["id"], float(now_blackboard["width"]), float(now_blackboard["length"]),
                      float(now_blackboard["height"]))
    now_table=table('Step001',0.5,0.5,0.2)#自生成讲台台阶
    now_lectern=json.loads(request.get_method('classroom','desk','',''))
    now_lectern = lectern(now_lectern["id"], float(now_lectern["width"]), float(now_lectern["length"]),
                      float(now_lectern["height"]))
    list=palindrome_partitions(column)
    LENGTH=now_chair.length
    WIDTH=now_chair.width
    correct_list=[]
    if(hallway>0):
        for i in list:
            if(len(i)==hallway+1):
                correct_list.append(i)
    else:#保证最多三个过道
        for i in list:
            if(len(i)<=4):
                correct_list.append(i)
    n=random.randint(0, len(correct_list) - 1)#随机选一个合理的分列
    choose_layout=correct_list[n]#选出的[1,2,3,2,1]
    hallway_num= len(choose_layout)-1
    column_remain=column/2
    #桌椅坐标的生成
    for i in range(0,math.ceil(len(choose_layout)/2)):#只计算一个象限的坐标即可
        num=choose_layout[i]
        for j in range(1,num+1):
            x=float(format((-(hallway_num/2-i)*HALLWAY-(column_remain-j+0.5)*WIDTH),'.3f'))
            for q in range(1,row+1):
                z=float(format((FRONT_DISTANT*((row-1)/2-q+1)+LENGTH*(row/2-q+0.5)),'.3f'))
                if(x<=0 and z>=0):
                    position1 = position(now_chair.id, 'chair', x, 0.0, z, 0.0, 0.0, 0.0)
                    object_position.append(position1)
                    if(x!=0):
                        position1 = position(now_chair.id, 'chair', -x, 0.0, z, 0.0, 0.0, 0.0)
                        object_position.append(position1)
                    if(z!=0):
                        position1 = position(now_chair.id, 'chair', x, 0.0, -z, 0.0, 0.0, 0.0)
                        object_position.append(position1)
                    if(x!=0 and z!=0):
                        position1 = position(now_chair.id, 'chair', -x, 0.0, -z, 0.0, 0.0, 0.0)
                        object_position.append(position1)
        column_remain=column_remain-num
    # 黑板坐标的生成
    d=(-object_position[0].xPosition+now_blackboard.height/2)/math.sqrt(3) #保证前排边座座椅与黑板远端的水平视角不应小于30°
    z=float(format((object_position[0].zPosition+max(FRONT_WALL+LENGTH/2,d)),'.3f'))
    y=float(format(random.uniform(1.2, 1.3),'.3f'))
    x=0
    position1 = position(now_blackboard.id, 'decoration', x, y, z, 0.0, 0.0, 0.0)
    object_position.append(position1)
    # 房间坐标的生成
    length = (object_position[0].zPosition + max(FRONT_WALL + LENGTH / 2, d)) * 2
    width = (-object_position[0].xPosition + WIDTH / 2 +FINAL_WALL) * 2
    room1 = room('Room001', width, length)
    room_position = position(room1.id, 'room', float(format(room1.width/ 10, '.3f')), 0.0,
                             float(format(room1.length / 10, '.3f')), 0.0, 0.0, 0.0)
    object_position.insert(0, room_position)
    # 讲台坐标的生成
    now_table.length =width*0.8
    now_table.width= max(FRONT_WALL + LENGTH / 2, d)*0.5
    z = float(format((z-now_table.width/2),'.3f'))
    position1 = position(now_table.id, 'step', 0.0, 0.0, z, float(format(now_table.length,'.3f')), float(format(now_table.width,'.3f')), 0.2)
    object_position.append(position1)
    # 讲桌坐标的生成
    z = float(format((z - now_table.width/2+now_lectern.width/2),'.3f'))
    position1 = position(now_lectern.id, 'desk', 0, 0, z, 0.0, 180.0, 0.0)
    object_position.append(position1)

    i = len(object_position) - 1
    while (i >= 0):
        object_position[i] = object_position[i].__dict__
        print(object_position[i])
        i = i - 1
    # object_position=json.dumps(object_position)
    LayoutObjects = layout(object_position)
    LayoutObjects = json.dumps(LayoutObjects.__dict__)
    LayoutObjects = json.loads(LayoutObjects)
    LayoutObjects["dataForModify"] = {"type":"classroom"}
    LayoutObjects = json.dumps(LayoutObjects)
    print(LayoutObjects)
    return LayoutObjects

def is_palindrome(s):#验证是否是回文字符串
    return s == s[::-1]

def get_partitions(n):#递归算所有拆分
    partitions = []
    if n == 1:
        return [[1]]
    for i in range(1, n):
        for p in get_partitions(n - i):
            partitions.append([i] + p)
    partitions.append([n])
    return partitions

def palindrome_partitions(k):#计算一个整数的全部回文拆分方法
    partitions = get_partitions(k)
    palindrome_partitions = []
    for p in partitions:
        s = ''.join(map(str, p))#用map函数将p内每一项转化为string再连接起来
        if is_palindrome(s):
            palindrome_partitions.append(p)
    increasing_palindrome_partitions = []
    for i in palindrome_partitions:#选出递增序列，防止出现12121这种波浪
        if_increasing = True
        for j in range(1,math.ceil(len(i)/2)):
            if(i[j]<i[j-1]):
                if_increasing=False
        if(if_increasing and max(i)<10):
            increasing_palindrome_partitions.append(i)
    return increasing_palindrome_partitions





