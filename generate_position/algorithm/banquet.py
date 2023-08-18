import json
import math
import random

import request


CHAIR_SPACE_LR =random.uniform(0.2,0.4) # 椅子左右间隔
CHAIR_SPACE_FE = random.uniform(0.2, 0.4)  # 椅子和桌子的间隔
DESK_SPACE = random.uniform(0.4, 0.6) #桌子和桌子的间隔
CHAIR_WALL = random.uniform(0.9, 1.8)#最后一排和墙的距离


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


class desk(object):
    id = ''
    width = 0
    length = 0
    height = 0

    def __init__(self, id, width, length ,height):
        self.id = id
        self.width = width
        self.length = length
        self.height = height

class screen(object):
    id = ''
    width = 0
    length = 0
    height = 0

    def __init__(self, id, width, length, height):
        self.id = id
        self.width = width
        self.length = length
        self.height = height

def post(json_dict):
    print(json_dict)
    # people,desk_num,half_or_whole
    init(json_dict["people_number"], json_dict["table_number"], json_dict["if_half_circle"])


now_desk=desk('Desk001', 0.5,0.5,1.0)
now_chair=chair('Chair001', 1.0, 1.0,0.8)
now_screen=screen('Screen001', 0.5,0.0,0.8)
#失败的回文探索
def count_table_num(people,if_half_cricle):
    #默认围成一圈
    max_people=int(math.floor((2*math.pi*(now_desk.width/2+CHAIR_SPACE_FE))/(CHAIR_SPACE_LR+now_chair.width)))
    if(if_half_cricle==True):
        max_people = math.ceil(((2 * math.pi * (now_desk.width/2 + CHAIR_SPACE_FE)) / (CHAIR_SPACE_LR + now_chair.width))/2)
    desk_num=math.ceil(people/max_people)
    table_list=define_table_list(desk_num)
    return calculate_position(table_list,if_half_cricle,max_people)

def define_table_list(desk_num):#生成桌子数量数组
    if (desk_num & 1):
        num=desk_num+1
        start = int(math.sqrt(num))
        factor = num / start
        while not (factor % 1 == 0):
            start += 1
            factor = num / start
        length1 = max(int(factor), start)
        width1 = min(int(factor), start)
        length2 = float("inf")
        width2 = 0
        if(desk_num>1):
            num=desk_num-1
            start = int(math.sqrt(num))
            factor = num / start
            while not (factor % 1 == 0):
                start += 1
                factor = num / start
            length2 = max(int(factor), start)
            width2 = min(int(factor), start)
        if(length1-width1>length2-width2):
            length=length2
            width=width2
            change=1#代表应该多加一个
        else:
            length = length1
            width = width1
            change=-1#代表应该减去一个
    else:
        num=desk_num
        start = int(math.sqrt(num))
        factor = num / start
        while not (factor % 1 == 0):
            start += 1
            factor = num / start
        length = max(int(factor), start)
        width = min(int(factor), start)
    desk_column_list=[]
    for i in range(0,length):
        desk_column_list.append(width)
    if(desk_num&1 and change==-1):
        desk_column_list[0] = width - 1
    if(desk_num&1 and change==1):
        desk_column_list[len(desk_column_list)-1] = width + 1
    print(desk_column_list)
    return desk_column_list

def calculate_position(desk_row_list,if_half_cricle,max_people):
    #half_or_whole 0.5 half 1 whole
    object_position = []
    hallway_num=len(desk_row_list)-1
    for i in range(0,int(len(desk_row_list))):
        z_desk=float(format((((len(desk_row_list)-1)/2-i)*(DESK_SPACE+2*now_chair.length+2*CHAIR_SPACE_FE)+(len(desk_row_list)/2-i)*now_desk.width-now_desk.width/2),'.3f'))
        for j in range(0,math.ceil(desk_row_list[i]/2)):
            x_desk=float(format((-((desk_row_list[i]-1)/2-j)*(DESK_SPACE+2*now_chair.length+2*CHAIR_SPACE_FE)-(desk_row_list[i]/2-j)*now_desk.width+now_desk.width/2),'.3f'))
            position1 = position(now_desk.id, 'desk', x_desk, 0.0, z_desk, 0.0, 0.0, 0.0)
            object_position.append(position1)
            if(if_half_cricle==True):
                r=now_desk.width/2+CHAIR_SPACE_FE+now_chair.length/2
                angle=180/math.floor(max_people)
                for q in range(0,math.floor(max_people)):
                    x = float(format(r * math.cos(-math.pi*(180-angle*math.floor(max_people)-1)/180+angle * q * math.pi / 180)+x_desk, '.3f'))
                    z = float(format(r * math.sin(-math.pi*(180-angle*math.floor(max_people)-1)/180+angle * q * math.pi / 180)+z_desk, '.3f'))
                    position1 = position(now_chair.id, 'chair', x, 0.0, z, 0.0, 180.0, 0.0)
                    object_position.append(position1)
            if(if_half_cricle==False):
                r = now_desk.width/2 + CHAIR_SPACE_FE + now_chair.length / 2
                angle = 360 / max_people
                for q in range(0,max_people):
                    x = float(format(r * math.cos(angle * q * math.pi / 180)+x_desk, '.3f'))
                    z = float(format(r * math.sin(angle * q * math.pi / 180)+z_desk, '.3f'))
                    position1 = position(now_chair.id, 'chair', x, 0.0, z, 0.0, 90-angle * q, 0.0)
                    object_position.append(position1)
            if(x_desk!=0):#对称位置生成一个桌子
                position1 = position(now_desk.id, 'desk', -x_desk, 0.0, z_desk, 0.0, 0.0, 0.0)
                object_position.append(position1)
                if (if_half_cricle == True):
                    r = now_desk.width/2 + CHAIR_SPACE_FE + now_chair.length / 2
                    angle = 180 / math.floor(max_people)
                    for q in range(0, math.floor(max_people)):
                        x = float(format(r * math.cos(-math.pi*(180-angle*math.floor(max_people)-1)/180+angle * q * math.pi / 180)- x_desk, '.3f'))
                        z = float(format(r * math.sin(-math.pi*(180-angle*math.floor(max_people)-1)/180+angle * q * math.pi / 180)+ z_desk, '.3f'))
                        position1 = position(now_chair.id, 'chair', x, 0.0, z, 0.0, 180.0, 0.0)
                        object_position.append(position1)
                if (if_half_cricle==False):
                    r = now_desk.width/2 + CHAIR_SPACE_FE + now_chair.length / 2
                    angle = 360 / max_people
                    for q in range(0, max_people):
                        x = float(format(r * math.cos(angle * q * math.pi / 180) - x_desk, '.3f'))
                        z = float(format(r * math.sin(angle * q * math.pi / 180)+ z_desk, '.3f'))
                        position1 = position(now_chair.id, 'chair', x, 0.0, z, 0.0, 90 - angle * q, 0.0)
                        object_position.append(position1)

    # 房间坐标的生成
    length = (object_position[0].zPosition + CHAIR_WALL + now_chair.length +now_desk.width/2+CHAIR_SPACE_FE) * 2
    width = 2*(((desk_row_list[len(desk_row_list)-1]-1)/2)*(DESK_SPACE+2*now_chair.length+2*CHAIR_SPACE_FE)
            +(desk_row_list[len(desk_row_list)-1]/2)*now_desk.width+CHAIR_SPACE_FE+now_chair.length+CHAIR_WALL)
    room1 = room('Room001', width, length)
    room_position = position(room1.id, 'room', float(format(room1.width / 10, '.3f')), 0.0,
                                 float(format(room1.length / 10, '.3f')), 0.0, 0.0, 0.0)
    object_position.insert(0, room_position)

    #投影坐标的生成
    z=float(format(length/2,'.3f'))
    y=float(format((random.uniform(1, 1.2)+now_screen.height/2),'.3f'))
    position1 = position(now_screen.id, 'decoration', 0.0, y, z, 0.0, 0.0, 0.0)
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
    LayoutObjects["dataForModify"] = {"type":"banquet"}
    LayoutObjects = json.dumps(LayoutObjects)
    print(LayoutObjects)
    return LayoutObjects

def init(people,desk_num,if_half_cricle):
    global now_desk, now_chair, now_screen
    now_desk = json.loads(request.get_method('banquet', 'desk', '', 'round'))
    now_desk = desk(now_desk["id"], float(now_desk["width"]), float(now_desk["length"]),
                    float(now_desk["height"]))
    now_chair = json.loads(request.get_method('banquet', 'chair', '', ''))
    now_chair = chair(now_chair["id"], float(now_chair["width"]), float(now_chair["length"]),
                      float(now_chair["height"]))
    now_screen = json.loads(request.get_method('banquet', 'screen', '', ''))
    now_screen = screen(now_screen["id"], float(now_screen["width"]), float(now_screen["length"]),
                        float(now_screen["height"]))
    if(desk_num>0):
        table_list=define_table_list(desk_num)
        request.post_method(calculate_position(table_list, if_half_cricle, int(people/desk_num)))
    else:
        request.post_method(count_table_num(people,if_half_cricle))