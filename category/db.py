import pymysql
import csv
import random
from translateUtil import translate_baidu
from translateUtil import translate
from time import sleep

usage_prompt = ["这个会议室适合于", "我想拿这个会议室进行", "这个会议室适合进行", "这个会议室用途是", "我想开展", "此虚拟会议室目的是开展"]
bool_list = [False, True]
remove_student_number = ["522022320138"]

def convertPic2Category(pic_number):
    if pic_number <= 15:
        return 0
    elif pic_number <= 30:
        return 1
    elif pic_number <= 45:
        return 2
    elif pic_number <= 60:
        return 3
    elif pic_number <= 75:
        return 4
    else:
        return 5

def handle_punct_in_sentence(sentence):
    if len(sentence) == 0:
        return sentence
    if sentence[-1] != "。":
        sentence += "。"
    sentence = sentence[:-1].replace("。", "，") + "。"
    return sentence.replace(" ","")

def handle_layout_detail(layout, detail):
    layout_detail = handle_punct_in_sentence(layout)
    if random.choice(bool_list):
        layout_detail = handle_punct_in_sentence(layout_detail + detail)
    return layout_detail

def generate_data(category, usage, layout, detail, advantage):
    data = []
    for i in range(len(category)):
        c = category[i]
        u = handle_punct_in_sentence(usage[i])
        a = handle_punct_in_sentence(advantage[i])
        l = handle_punct_in_sentence(layout[i])
        d = handle_punct_in_sentence(detail[i])
        if d == handle_punct_in_sentence("无"):
            d = ""
        data.append([handle_punct_in_sentence(handle_layout_detail(l, d)), c])
        data.append([handle_punct_in_sentence(u), c])
        data.append([handle_punct_in_sentence(u+handle_layout_detail(l, d)), c])
        data.append([handle_punct_in_sentence(handle_layout_detail(l,d)+u), c])
        if a != "":
            data.append([handle_punct_in_sentence(handle_layout_detail(l,d)+a), c])
            data.append([handle_punct_in_sentence(a+handle_layout_detail(l,d)+u), c])
            data.append([handle_punct_in_sentence(u+a+handle_layout_detail(l,d)), c])
            data.append([handle_punct_in_sentence(u+a), c])
    random.shuffle(data)
    return data

def save_data_to_csv(data, path):
    csv_file = open(path, 'w', newline='', encoding='utf8')
    writer = csv.writer(csv_file)
    writer.writerow(["input", "category"])
    for d in data:
        writer.writerow(d)
    csv_file.close()

def translate_data(data):
    new_data = []
    count = 0
    for d in data:
        count += 1
        print(count)
        new_d = translate(d[0])
        new_data.append([new_d, d[1]])
        # sleep(2)
    return new_data

def read_data_from_csv(path):
    category = []
    usage = []
    layout = []
    detail = []
    advantage = []
    with open(path, encoding='utf8') as csvfile:
        csv_reader = csv.reader(csvfile)
        for row in csv_reader:
            if row[1] in remove_student_number:
                continue
            category.append(convertPic2Category(int(row[2])))
            usage.append(random.choice(usage_prompt) + row[3])
            layout.append(row[4])
            detail.append(row[5])
            advantage.append(row[8])
    return generate_data(category, usage, layout, detail, advantage)

class DatabaseConnector:
    def __init__(self, host, username, password, database):
        self.conn = None
        self.cur = None
        self.get_connection_and_cursor(host, username, password, database)

    def get_connection_and_cursor(self, host, username, password, database):
        self.conn = pymysql.connect(host=host, user=username, passwd=password,
                                    db=database, charset="utf8")
        self.cur = self.conn.cursor()

    def commit_and_close(self):
        self.conn.commit()

    def select_data(self, table_name):
        sql = "select * from " + table_name
        self.cur.execute(sql)
        res = self.cur.fetchall()
        self.commit_and_close()
        return res


if __name__=="__main__":
    data = read_data_from_csv(r"../../collected_data.csv")
    print(len(data))
    data = translate_data(data)
    save_data_to_csv(data, "data.csv")



