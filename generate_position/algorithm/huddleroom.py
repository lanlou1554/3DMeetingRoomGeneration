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

    def __init__(self, id, width, length,height):
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

# now_chair=chair('',0,0,0)
# now_desk=desk('',0,0,0)
# now_screen=screen('',0,0,0)
now_desk=desk('Desk016', 1.0,1.6,0.8)
now_chair=chair('Chair001', 1.0, 1.0,0.5)
now_screen=screen('TV001', 0.0,1.3,0.8)
def post(json_dict):
    print(json_dict)
    # people,width_num,length_num
    init(json_dict["people_number"], json_dict["short_side_chair_number"],json_dict["long_side_chair_number"])

def count_chair_num(people):#根据总人数算每条边的椅子数量
    if(people&1):#若人数是奇数
        width_num=1#横边人数
        length_num=int((people-1)/2)#竖边人数
    else:#若人数为偶数
        width_num=0
        length_num=int(people/2)
    desk_num=math.ceil((now_chair.width*length_num+CHAIR_SPACE_LR*(length_num+1))/now_desk.length)
    return calculate_position(width_num,length_num,desk_num,1,now_desk,now_chair)
def calculate_position(width_num,length_num,length_desk_num,width_desk_num,now_desk,now_chair):
    object_position = []
    now_screen=json.loads(request.get_method('huddleroom','screen','',''))
    now_screen = screen(now_screen["id"], float(now_screen["width"]), float(now_screen["length"]),
                    float(now_screen["height"]))
    global CHAIR_SPACE_LR
    CHAIR_SPACE_LR_LENGTH=float(format((length_desk_num*now_desk.length-length_num*now_chair.width)/(length_num+1),'.3f'))
    CHAIR_SPACE_LR_WIDTH = float(
        format((width_desk_num * now_desk.width - width_num * now_chair.width) / (width_num + 1), '.3f'))
    # 房间坐标的生成
    length = length_desk_num*now_desk.length + now_chair.length + CHAIR_SPACE_FE + CHAIR_WALL
    width = now_desk.width*width_desk_num+now_chair.length*2+CHAIR_SPACE_FE*2+CHAIR_WALL*2
    room1 = room('Room001', width, length)
    room_position = position(room1.id, 'room', float(format(room1.width / 10, '.3f')), 0.0,
                             float(format(room1.length / 10, '.3f')), 0.0, 0.0, 0.0)
    object_position.append(room_position)
    #桌子坐标的生成
    for i in range(0,length_desk_num):
        z=float(format((length/2-now_desk.length/2-now_desk.length*i),'.3f'))
        for j in range(0,width_desk_num):
            x=float(format((-width/2+now_desk.width*j+now_desk.width/2+now_chair.length+CHAIR_SPACE_FE+CHAIR_WALL),'.3f'))
            position1 = position(now_desk.id, 'desk', x, 0.0, z, 0.0, 90.0, 0.0)
            object_position.append(position1)
    #椅子坐标的生成
    for i in range(0,width_num):
        x=float(format((-width/2+now_chair.length+CHAIR_SPACE_FE+CHAIR_WALL+CHAIR_SPACE_LR_WIDTH*(i+1)+now_chair.width*i+now_chair.width/2),'.3f'))
        z=float(format((length/2-now_desk.length*length_desk_num-CHAIR_SPACE_FE-now_chair.length/2),'.3f'))
        position1 = position(now_chair.id, 'chair', x, 0.0, z, 0.0, 180.0, 0.0)
        object_position.append(position1)
    for i in range(0,length_num):
        x=float(format((-now_desk.width*width_desk_num/2-CHAIR_SPACE_FE-now_chair.length/2),'.3f'))
        z=float(format((length/2-CHAIR_SPACE_LR_LENGTH*(i+1)-now_chair.width*i-now_chair.width/2),'.3f'))
        position1 = position(now_chair.id, 'chair', x, 0.0, z, 0.0, -90.0, 0.0)
        object_position.append(position1)
        position1 = position(now_chair.id, 'chair', -x, 0.0, z, 0.0, 90.0, 0.0)#对称位置生成一个
        object_position.append(position1)
    #屏幕坐标的生成
    z=float(format(length/2,'.3f'))
    y=float(format((now_desk.height+random.uniform(0, 0.2)+now_screen.height/2),'.3f'))
    position1 = position(now_screen.id, 'decoration', 0.0, y, z, 0.0, 0.0, 0.0)
    object_position.append(position1)

    i = len(object_position) - 1
    while (i >= 0):
        object_position[i] = object_position[i].__dict__
        print(object_position[i])
        i = i - 1
    LayoutObjects = layout(object_position)
    LayoutObjects = json.dumps(LayoutObjects.__dict__)
    LayoutObjects = json.loads(LayoutObjects)
    LayoutObjects["dataForModify"] = {"type":"huddle"}
    LayoutObjects = json.dumps(LayoutObjects)
    return LayoutObjects
def init(people,width_num,length_num):
    print('huddle')
    global now_chair,now_desk
    now_desk = json.loads(request.get_method('huddleroom', 'desk', '', 'rectangle'))
    now_desk = desk(now_desk["id"], float(now_desk["width"]), float(now_desk["length"]),
                    float(now_desk["height"]))
    now_chair = json.loads(request.get_method('huddleroom', 'chair', '', ''))
    now_chair = chair(now_chair["id"], float(now_chair["width"]), float(now_chair["length"]),
                      float(now_chair["height"]))
    if(width_num<0 and length_num<0):
        # print(count_chair_num(people))
        request.post_method(count_chair_num(people))
    else:
        length_desk_num=math.ceil((now_chair.width*length_num+CHAIR_SPACE_LR*(length_num+1))/now_desk.length)
        width_desk_num=math.ceil((now_chair.width*width_num+CHAIR_SPACE_LR*(width_num+1))/now_desk.width)
        # print(calculate_position(width_num,length_num,length_desk_num,width_desk_num,now_desk,now_chair))
        request.post_method(calculate_position(width_num,length_num,length_desk_num,width_desk_num,now_desk,now_chair))