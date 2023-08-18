import json
import math
import random

import request


CHAIR_SPACE_LR = 0.2 # 椅子最小左右间隔
CHAIR_SPACE_FE = random.uniform(0.2, 0.4)  # 椅子和桌子前后间隔
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
    height= 0

    def __init__(self, id, width, length, height):
        self.id = id
        self.width = width
        self.length = length
        self.height =height

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
    # people,width_people,length_people
    init(json_dict["people_number"], json_dict["middle_side_chair_number"], json_dict["double_side_chair_number"])

now_desk=desk('Desk011', 0.8,0.8,0.7)
now_chair=chair('Chair012', 1.0, 1.0,1.0)
now_screen=screen('TV001', 0.0,1.3,0.8)
def init(people,width_people,length_people):
    global now_desk
    global now_chair
    # now_desk=json.loads(request.get_method('ushape','desk','','rectangle'))
    # now_desk = desk(now_desk["id"], float(now_desk["width"]), float(now_desk["length"]),
    #                 float(now_desk["height"]))
    # now_chair=json.loads(request.get_method('ushape','chair','',''))
    # now_chair = chair(now_chair["id"], float(now_chair["width"]), float(now_chair["length"]),
    #                   float(now_chair["height"]))
    one_desk_people=math.floor((now_desk.length-CHAIR_SPACE_LR)/(now_chair.width+CHAIR_SPACE_LR))
    if(one_desk_people<1):
        one_desk_people=1
    if(width_people<0 and length_people<0):
        desk_num=math.ceil(people/one_desk_people)
        if(desk_num<3):
            desk_num=3
        i=desk_num
        width_num=0
        while(i>0):
            i=i-1
            width_num=width_num+1
            if(i%2==0):
                length_num=int(i/2)
                if(length_num-width_num<3):
                    break
        if(i==0):
            print("error!未找到合适的布局")
    else:
        width_num=math.ceil(width_people/one_desk_people)
        length_num=math.ceil(length_people/one_desk_people)
    print(width_people,length_people)
    request.post_method(calculate_position(width_num,length_num,width_people,length_people))

def calculate_position(width_num,length_num,width_people,length_people):
    object_position=[]
    one_desk_people = math.floor((now_desk.length - CHAIR_SPACE_LR) / (now_chair.width + CHAIR_SPACE_LR))
    if (one_desk_people < 1):
        one_desk_people = 1
    if(width_people<0 and length_people<0):
        for i in range(0,math.ceil(width_num/2)):
            x_desk=float(format((-width_num/2*now_desk.length+i*now_desk.length+now_desk.length/2),'.3f'))
            z_desk=float(format((-length_num/2*now_desk.length+now_desk.width/2),'.3f'))
            position1 = position(now_desk.id, 'desk', x_desk, 0.0, z_desk, 0.0, 180.0, 0.0)
            object_position.append(position1)
            for j in range(0,one_desk_people):
                x=float(format((x_desk-now_desk.length/2+(j+1)*CHAIR_SPACE_LR+j*now_chair.width+0.5*now_chair.width),'.3f'))
                z=float(format((z_desk-CHAIR_SPACE_FE-now_chair.length/2),'.3f'))
                position1 = position(now_chair.id, 'chair', x, 0.0, z, 0.0, 180.0, 0.0)
                object_position.append(position1)
            if(x_desk!=0):#对称位置生成一个桌子
                position1 = position(now_desk.id, 'desk', -x_desk, 0.0, z_desk, 0.0, 0.0, 0.0)
                object_position.append(position1)
                for j in range(0, one_desk_people):
                    x =float(format(( -x_desk + now_desk.length / 2 - (j + 1) * CHAIR_SPACE_LR - j * now_chair.width - 0.5 * now_chair.width),'.3f'))
                    z = float(format((z_desk - CHAIR_SPACE_FE - now_chair.length / 2),'.3f'))
                    position1 = position(now_chair.id, 'chair', x, 0.0, z, 0.0, 180.0, 0.0)
                    object_position.append(position1)
        for i in range(0,math.ceil(length_num/2)):
            x_desk=float(format((-width_num/2*now_desk.length-now_desk.width/2),'.3f'))
            z_desk=float(format((length_num/2*now_desk.length-i*now_desk.length-now_desk.length/2),'.3f'))
            position1 = position(now_desk.id, 'desk', x_desk, 0.0, z_desk, 0.0, 90.0, 0.0)
            object_position.append(position1)
            position1 = position(now_desk.id, 'desk', -x_desk, 0.0, z_desk, 0.0, 90.0, 0.0)
            object_position.append(position1)
            for j in range(0,one_desk_people):
                x=float(format((x_desk-now_desk.width/2-CHAIR_SPACE_FE-now_chair.length/2),'.3f'))
                z=float(format((z_desk+now_desk.length/2-(j+1)*CHAIR_SPACE_LR-j*now_chair.width-0.5*now_chair.width),'.3f'))
                position1 = position(now_chair.id, 'chair', x, 0.0, z, 0.0, -90.0, 0.0)
                object_position.append(position1)
                position1 = position(now_chair.id, 'chair', -x, 0.0, z, 0.0, 90.0, 0.0)
                object_position.append(position1)
            if(z_desk!=0):#对称位置生成
                position1 = position(now_desk.id, 'desk', x_desk, 0.0, -z_desk, 0.0, 90.0, 0.0)
                object_position.append(position1)
                position1 = position(now_desk.id, 'desk', -x_desk, 0.0, -z_desk, 0.0, 90.0, 0.0)
                object_position.append(position1)
                for j in range(0, one_desk_people):
                    x = float(format((x_desk - now_desk.width / 2 - CHAIR_SPACE_FE - now_chair.length / 2),'.3f'))
                    z = float(format((-z_desk - now_desk.length / 2 + (j + 1) * CHAIR_SPACE_LR + j * now_chair.width + 0.5 * now_chair.width),'.3f'))
                    position1 = position(now_chair.id, 'chair', x, 0.0, z, 0.0, -90.0, 0.0)
                    object_position.append(position1)
                    position1 = position(now_chair.id, 'chair', -x, 0.0, z, 0.0, 90.0, 0.0)
                    object_position.append(position1)
    else:
        #生成宽上的桌子
        for i in range(0, math.ceil(width_num / 2)):
            x_desk =float(format(( -width_num / 2 * now_desk.length + i * now_desk.length + now_desk.length / 2),'.3f'))
            z_desk = float(format((-length_num / 2 * now_desk.length + now_desk.width / 2),'.3f'))
            position1 = position(now_desk.id, 'desk', x_desk, 0.0, z_desk, 0.0, 0.0, 0.0)
            object_position.append(position1)
            if (x_desk != 0):  # 对称位置生成一个桌子
                position1 = position(now_desk.id, 'desk', -x_desk, 0.0, z_desk, 0.0, 0.0, 0.0)
                object_position.append(position1)
        #生成宽上的椅子
        x_desk=float(format((-width_num / 2 * now_desk.length),'.3f'))
        z_desk = float(format((-length_num / 2 * now_desk.length),'.3f'))
        d=(width_num*now_desk.length-width_people*now_chair.width)/(width_people+1)
        for j in range(0, width_people):
            x = float(format((x_desk + d * (j + 1) + now_chair.width * j + now_chair.width / 2),'.3f'))
            z = float(format((z_desk - CHAIR_SPACE_FE - now_chair.length / 2),'.3f'))
            position1 = position(now_chair.id, 'chair', x, 0.0, z, 0.0, 180.0, 0.0)
            object_position.append(position1)
        #生成长上的桌子
        for i in range(0, math.ceil(length_num / 2)):
            x_desk = float(format((-width_num / 2 * now_desk.length - now_desk.width / 2),'.3f'))
            z_desk = float(format((length_num / 2 * now_desk.length - i * now_desk.length - now_desk.length / 2),'.3f'))
            position1 = position(now_desk.id, 'desk', x_desk, 0.0, z_desk, 0.0, 90.0, 0.0)
            object_position.append(position1)
            position1 = position(now_desk.id, 'desk', -x_desk, 0.0, z_desk, 0.0, 90.0, 0.0)
            object_position.append(position1)
            if (z_desk != 0):  # 对称位置生成
                position1 = position(now_desk.id, 'desk', x_desk, 0.0, -z_desk, 0.0, 90.0, 0.0)
                object_position.append(position1)
                position1 = position(now_desk.id, 'desk', -x_desk, 0.0, -z_desk, 0.0, 90.0, 0.0)
                object_position.append(position1)
        #生成长上的椅子
        x_desk = float(format((-width_num / 2 * now_desk.length-now_desk.width),'.3f'))
        z_desk = float(format((length_num / 2 * now_desk.length),'.3f'))
        d = (length_num * now_desk.length - length_people * now_chair.width) / (length_people + 1)
        for j in range(0, length_people):
            x = float(format((x_desk - CHAIR_SPACE_FE - now_chair.length / 2),'.3f'))
            z = float(format((z_desk - (j + 1) * d - j * now_chair.width - now_chair.width / 2),'.3f'))
            position1 = position(now_chair.id, 'chair', x, 0.0, z, 0.0, -90.0, 0.0)
            object_position.append(position1)
            position1 = position(now_chair.id, 'chair', -x, 0.0, z, 0.0, 90.0, 0.0)
            object_position.append(position1)

    #生成房间
    length = (-object_position[0].zPosition + now_desk.length/2+CHAIR_SPACE_FE+now_chair.length+CHAIR_WALL) * 2
    width = (-object_position[0].xPosition + now_desk.length/2+now_desk.width+CHAIR_SPACE_FE+now_chair.length+CHAIR_WALL) * 2
    room1 = room('Room001', width, length)
    room_position = position(room1.id, 'room', float(format(room1.width / 10, '.3f')), 0.0,
                             float(format(room1.length/ 10, '.3f')), 0.0, 0.0, 0.0)
    object_position.insert(0, room_position)

    #生成投影
    now_screen=json.loads(request.get_method('ushape','screen','',''))
    now_screen = screen(now_screen["id"], float(now_screen["width"]), float(now_screen["length"]),
                        float(now_screen["height"]))
    z=float(format(length/2,'.3f'))
    position1 = position(now_screen.id, 'decoration', 0.0, 2.0, z, 0.0, 0.0, 0.0)
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
    LayoutObjects["dataForModify"] = {"type":"ushape"}
    LayoutObjects = json.dumps(LayoutObjects)
    print(LayoutObjects)
    return LayoutObjects
