
import json
import math
import random

import request

#修改意见：加入随机值

# 椅子长LENGTH宽b 宽度是椅子背 长度是扶手
# 第一圈半径（1.6+a/2）m
# 同一排椅子间距（0.6+b）m
# 每排椅子之间的间距（0.6+a）m
# 第x圈半径（1.6+a/2+（0.6+a）*（x-1））m
# 每圈椅子上限2pai*r/（b+0.6）
CHAIR_SPACE_LR = random.uniform(0.4,0.6)  # 椅子左右间隔
CHAIR_SPACE_FE = random.uniform(0.4,0.6)  # 椅子前后间隔
FRONT = random.uniform(0.6,0.8)  # 第一排与中央的距离
CHAIR_WALL = random.uniform(1.5,1.8) # 最后一排椅子和墙壁的距离
WIDTH = 0.5
LENGTH = 0.5

class layout(object):
    LayoutObjects= []
    dataForModify = []
    def __init__(self, LayoutObjects,dataForModify):
        self.LayoutObjects=LayoutObjects
        self.dataForModify = dataForModify
    def add_position(self,position):
        self.LayoutObjects.append(position)

    def insert_position(self,position):
        self.LayoutObjects.insert(0,position)



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

class room_object(object):
    id = ''
    width = 0
    length = 0
    height = 0

    def __init__(self, id, width, length, height):
        self.id = id
        self.width = width
        self.length = length
        self.height = height
class room(object):
    id = ''
    width = 0.0
    length = 0.0

    def __init__(self, id, width, length):
        self.id = id
        self.width = width
        self.length = length

class chair(room_object):
    id = ''
    width = 0
    length = 0
    height = 0

class desk(room_object):
    id = ''
    width = 0
    length = 0
    height = 0

class modify(object):
    outer_chair=chair('Chair001', 1.0, 1.0,1.0)
    inner_chair=chair('Chair001', 1.0, 1.0,1.0)
    desk=desk('Desk001', 0.5,0.5,1.5)
    room=room('Room001',1.0,1.0)
    if_desk=False
    inner_circle_chair_num=-1
    inner_circle_num=-1
    outer_circle_num=-1
    people_number= 20
    type='fishbowl'
    table_color= ''
    outer_chair_color= ''
    inner_chair_color=''
    style=''
    other_instruction=''
    def __init__(self, outer_chair,inner_chair,desk,room,if_desk, inner_circle_chair_num,inner_circle_num,outer_circle_num,
                 people_number,type,table_color,outer_chair_color,inner_chair_color,style,other_instruction):
        self.outer_chair=outer_chair
        self.inner_chair=inner_chair
        self.desk=desk
        self.room=room
        self.if_desk=if_desk
        self.inner_circle_chair_num=inner_circle_chair_num
        self.inner_circle_num=inner_circle_num
        self.outer_circle_num=outer_circle_num
        self.people_number=people_number
        self.type=type
        self.table_color=table_color
        self.outer_chair_color=outer_chair_color
        self.inner_chair_color=inner_chair_color
        self.style=style
        self.other_instruction=other_instruction

now_desk=desk('Desk001', 0.5,0.5,1.5)
now_chair_outer=chair('Chair001', 1.0, 1.0,1.0)
now_chair_inner=chair('Chair001', 1.0, 1.0,1.0)
now_room=room('Room001',1.0,1.0)
dataForModify=modify('','','','',False,-1,-1,-1,20,'fishbowl','','','','','')
def post(json_dict):
    print(json_dict)
    json_dict_dataForModify = json_dict["newDataForModify"]
    json_dict_lastDataForModify = json_dict["lastDataForModify"]
    if(json_dict_dataForModify==-1):
        json_dict_dataForModify=json_dict_lastDataForModify
    if(json_dict_lastDataForModify!={}):
        if(json_dict_dataForModify["table_color"]!=json_dict_lastDataForModify["table_color"] or json_dict_dataForModify["style"]!=json_dict_lastDataForModify["style"]):
            json_dict_lastDataForModify["desk"]=''
        if(json_dict_dataForModify["outer_chair_color"]!=json_dict_lastDataForModify["outer_chair_color"] or json_dict_dataForModify["if_desk"]!=json_dict_lastDataForModify["if_desk"] or json_dict_dataForModify["style"]!=json_dict_lastDataForModify["style"]):
            json_dict_lastDataForModify["outer_chair"] = ''
        if(json_dict_dataForModify["inner_chair_color"]!=json_dict_lastDataForModify["inner_chair_color"] or json_dict_dataForModify["style"]!=json_dict_lastDataForModify["style"]):
            json_dict_lastDataForModify["inner_chair"] = ''
        if(json_dict_dataForModify["style"]!=json_dict_lastDataForModify["style"]):
            json_dict_lastDataForModify["room"] = ''
        init(json_dict_lastDataForModify["outer_chair"], json_dict_lastDataForModify["inner_chair"],
             json_dict_lastDataForModify["desk"], json_dict_lastDataForModify["room"],json_dict_dataForModify["people_number"],
             json_dict_dataForModify["outer_circle_num"], json_dict_dataForModify["inner_circle_num"],
             json_dict_dataForModify["if_desk"], json_dict_dataForModify["inner_circle_chair_num"],
             json_dict_dataForModify["table_color"], json_dict_dataForModify["outer_chair_color"],
             json_dict_dataForModify["inner_chair_color"], json_dict_dataForModify["other_instruction"],
             json_dict_dataForModify["style"])
    else:
        init("", "","", "",json_dict_dataForModify["people_number"],
             json_dict_dataForModify["outer_circle_num"], json_dict_dataForModify["inner_circle_num"],
             json_dict_dataForModify["if_desk"], json_dict_dataForModify["inner_circle_chair_num"],
             json_dict_dataForModify["table_color"], json_dict_dataForModify["outer_chair_color"],
             json_dict_dataForModify["inner_chair_color"], json_dict_dataForModify["other_instruction"],
             json_dict_dataForModify["style"])
    # people_num, outer_circle_num,inner_circle_num, if_desk, inner_circle_chair_num,desk_color,outer_chair_color,inner_chair_color,other_instruction,style

def count_chair(num):  # 根据圈数计算最大容纳椅子数
    chair_num = 0
    if (num == 0):
        return 0
    if (num == 1):
        chair_num = math.floor(chair_num + ((FRONT + LENGTH / 2) * 2 * math.pi) / (WIDTH + CHAIR_SPACE_LR))
        # print(chair_num)
    else:
        chair_num = chair_num + count_chair_circle(num) + count_chair(num - 1)
        # print(chair_num)
    return chair_num


def count_chair_circle(num):  # 每一圈最大容纳椅子数
    chair_num = math.floor(
        ((FRONT + LENGTH / 2 + (CHAIR_SPACE_FE + LENGTH) * (num - 1)) * 2 * math.pi) / (WIDTH + CHAIR_SPACE_LR))
    return chair_num


def count_circle(num):  # 根据椅子数计算需要几圈
    i = 1
    while (1):
        if (count_chair(i) >= num):
            # print(i)
            return i
        else:
            i = i + 1


def define_sparsity(num, first_circle, last_circle):  # 根据系数程度决定每一圈摆多少椅子
    seat = count_chair(last_circle) - count_chair(first_circle - 1)
    sparsity = num / seat  # 稀疏度计算
    list = []
    for i in range(first_circle, last_circle + 1):
        list.append(round(count_chair_circle(i) * sparsity))
    n = 0
    for i in list:
        n = n + i
    if (n != num):  # n:现在的座位数 num:需要的座位数
        # print(n,num)
        change = n - num  # +为需要减少的数量 -为需要增加的数量
        now_circle = last_circle
        while (abs(change) != 0):  # 从最外圈开始向内每圈加或减一张椅子 直到数量正确
            list[now_circle - 1] = round(list[now_circle - 1] - change / abs(change))
            if (change > 0):
                change = change - 1
            if (change < 0):
                change = change + 1
    n = 0
    for i in list:
        n = n + i
    if (n != num):  # 抛出错误
        print(n, num + "ERROR:椅子数与需要人数不符！")
        return -1
    return list


def circle_num_count_chair(people_num, circle_num):  # 已知圈数，挑选出应该围在哪几圈
    i = 0
    while (1):
        n = count_chair(i + circle_num) - count_chair(i)
        if (n >= people_num):
            break
        i = i + 1
    # 选择使用第i+circle_num圈到i+1圈
    return i


def calculate_position(list):  # 计算坐标
    global dataForModify
    object_position = layout([],dataForModify.__dict__)
    if (list[0] != 0):
        desk_position = position(now_desk.id, 'desk', 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
        object_position.add_position(desk_position)
        angle = 360 / list[0]
        r = now_desk.width/2 + CHAIR_SPACE_FE + now_chair_inner.length / 2
        i = list[0]
        while (i > 0):
            x = float(format(r * math.cos(angle * (i - 1) * math.pi / 180),'.3f'))
            z = float(format(r * math.sin(angle * (i - 1) * math.pi / 180),'.3f'))
            position1 = position(now_chair_inner.id, 'chair', x, 0.0, z, 0.0, float(format(90-angle * (i - 1),'.3f')), 0.0)
            i = i - 1
            object_position.add_position(position1)

    i = len(list) - 1
    # 生成room大小
    if (list[0] != 0):
        r = now_desk.width/2 + CHAIR_SPACE_FE * i + FRONT + LENGTH * i + LENGTH / 2
    else:
        r = FRONT + CHAIR_SPACE_FE * (i - 1) + LENGTH * (i - 1) + LENGTH / 2
    room1 = room(now_room.id, r * 2 + CHAIR_WALL * 2, r * 2 + CHAIR_WALL * 2)
    room_position = position(room1.id, 'room', float(format(room1.width / 10, '.3f')), 0.0,
                             float(format(room1.length / 10, '.3f')), 0.0, 0.0, 0.0)
    object_position.insert_position(room_position)

    while (list[i] > 0 and i>0):
        if (list[0] != 0):
            r = now_desk.width/2 + CHAIR_SPACE_FE * i + FRONT + LENGTH * i + LENGTH / 2
        else:
            r = FRONT + CHAIR_SPACE_FE * (i - 1) + LENGTH * (i - 1) + LENGTH / 2
        angle = 360 / list[i]
        j = list[i]
        while (j > 0):
            x = float(format(r * math.cos(angle * (j - 1) * math.pi / 180),'.3f'))
            z = float(format(r * math.sin(angle * (j - 1) * math.pi / 180),'.3f'))
            position1 = position(now_chair_outer.id, 'chair', x, 0.0, z, 0.0, float(format(90-angle * (j - 1),'.3f')), 0.0)
            j = j - 1
            object_position.add_position(position1)
        i = i - 1

    i = len(object_position.LayoutObjects) - 1
    while (i >= 0):
        object_position.LayoutObjects[i] = object_position.LayoutObjects[i].__dict__
        print(object_position.LayoutObjects[i])
        i = i - 1
    LayoutObjects = json.dumps(object_position.__dict__)
    print(LayoutObjects)
    return LayoutObjects
    # return object_position

def init(last_outer_chair,last_inner_chair,last_desk,last_room,people_num, outer_circle_num,inner_circle_num, if_desk, inner_circle_chair_num,desk_color,outer_chair_color,inner_chair_color,other_instruction,style):#inner_circle_num暂时没有用
    global FRONT
    global WIDTH
    global LENGTH
    global now_desk
    global now_chair_inner
    global now_chair_outer
    global now_room
    global dataForModify
    global CHAIR_SPACE_FE
    global CHAIR_SPACE_LR
    global FRONT
    if(other_instruction=='dense'):
        CHAIR_SPACE_LR=CHAIR_SPACE_LR/2
        CHAIR_SPACE_FE=CHAIR_SPACE_FE/2
        FRONT=FRONT/2
    if(other_instruction=='sparse'):
        CHAIR_SPACE_LR = CHAIR_SPACE_LR*1.5
        CHAIR_SPACE_FE = CHAIR_SPACE_FE*1.5
        FRONT = FRONT*1.5
    list = []
    # list的格式：
    # 第一项代表有无内圈 有则为内圈椅子数/无则为0
    # 第二项开始是外圈椅子数，由于可能是不连续的圈故也可能为0
    # 示例：[4,0,0,10,15]表示内圈4个椅子，外圈第1、2圈没有椅子，第3圈10个椅子，第四圈15个椅子

    if(last_room==''):
        now_room=json.loads(request.get_method('fishbowl','room','','','',style).decode('utf-8'))
        now_room=room(now_room["id"],float(now_room["width"]),float(now_room["length"]))
    else:
        now_room=room(last_room['id'],last_room['width'],last_room['length'])
    # now_room=room('Room001',1.0,1.0)
    if (if_desk==True):
        if(last_outer_chair==''):
            now_chair_outer = json.loads(request.get_method('fishbowl','chair',outer_chair_color,'','board',style).decode('utf-8'))
            # now_chair_outer = chair('Chair001',1.0,1.0,1.0)
            now_chair_outer = chair(now_chair_outer["id"], float(now_chair_outer["width"]), float(now_chair_outer["length"]),
                              float(now_chair_outer["height"]))
        else:
            now_chair_outer=chair(last_outer_chair['id'], last_outer_chair['width'], last_outer_chair['length'], last_outer_chair['height'])
    else:
        if (last_outer_chair == ''):
            now_chair_outer = json.loads(
                request.get_method('fishbowl', 'chair', outer_chair_color, '', '', style).decode('utf-8'))
            # now_chair_outer = chair('Chair001',1.0,1.0,1.0)
            now_chair_outer = chair(now_chair_outer["id"], float(now_chair_outer["width"]),
                                    float(now_chair_outer["length"]),
                                    float(now_chair_outer["height"]))
        else:
            now_chair_outer = chair(last_outer_chair['id'], last_outer_chair['width'], last_outer_chair['length'],
                                    last_outer_chair['height'])
    WIDTH = now_chair_outer.width
    LENGTH = now_chair_outer.length
    if (inner_circle_chair_num != 0):#inner_circle_chair_number -1:有内圈但没有说椅子数量，0:没有内圈，正数:内圈椅子数量
        if (inner_circle_chair_num == -1):
            # 默认5个座位 如果人数比5少 且有内圈 则都在内圈/若人数比5多 且只有内圈没有外圈 则都在内圈
            if (people_num < 5 or outer_circle_num == 0):
                inner_circle_chair_num = people_num
            else:
                inner_circle_chair_num = 5
        size=''
        if(inner_circle_chair_num<5):
            size='small'
        if(inner_circle_chair_num>=5 and inner_circle_chair_num<9):
            size='medium'
        if(inner_circle_chair_num>=10):
            size='large'

        if(last_desk==''):
            now_desk = json.loads(request.get_method('fishbowl','desk',desk_color,'round',size,style).decode('utf-8'))
            # now_desk = desk('Desk001',1.2,1.2,0.7)
            now_desk = desk(now_desk["id"], float(now_desk["width"]), float(now_desk["length"]),
                            float(now_desk["height"]))
        else:
            now_desk=desk(last_desk['id'], last_desk['width'], last_desk['length'], last_desk['height'])
        if(last_inner_chair==''):
            now_chair_inner=json.loads(request.get_method('fishbowl','chair',inner_chair_color,'','',style).decode('utf-8'))
            # now_chair_inner=chair('Chair002',1.0,1.0,1.0)
            now_chair_inner = chair(now_chair_inner["id"], float(now_chair_inner["width"]),
                                    float(now_chair_inner["length"]),
                                    float(now_chair_inner["height"]))
        else:
            now_chair_inner=chair(last_inner_chair['id'], last_inner_chair['width'], last_inner_chair['length'], last_inner_chair['height'])
        FRONT = 1.6 + now_desk.width/2 + CHAIR_SPACE_FE + now_chair_inner.length
    list.append(inner_circle_chair_num)  # 内圈椅子数量 没有内圈则为0
    if (outer_circle_num> 0):
        i = circle_num_count_chair(people_num - inner_circle_chair_num, outer_circle_num)
        j = i
        # 选择使用第i+circle_num圈到i+1圈 之前的圈椅子数为0
        while (i > 0):
            list.append(0)
            i = i - 1
        list = list + define_sparsity(people_num - inner_circle_chair_num, j + 1, j + outer_circle_num)
    else:
        circle = count_circle(people_num - inner_circle_chair_num)
        list = list + define_sparsity(people_num - inner_circle_chair_num, 1, circle)
    if(list[0]==0):
        inner_circle_chair_num=-1
    else:
        inner_circle_chair_num=list[0]

    if(list[0]!=0):
        inner_circle_num=1
    else:
        inner_circle_num=0

    outer_circle_num=0
    for i in range(1,len(list)):
        if(list[i]!=0):
            outer_circle_num=outer_circle_num+1
    dataForModify=modify(now_chair_outer.__dict__,now_chair_inner.__dict__,now_desk.__dict__,now_room.__dict__,if_desk,inner_circle_chair_num,inner_circle_num,outer_circle_num,people_num,'fishbowl',desk_color,outer_chair_color,inner_chair_color,style,other_instruction)
    # print(calculate_position(list, chair))
    request.post_method(calculate_position(list))