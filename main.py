from flask import Flask
from flask_restful import Api,reqparse,request

from coreNLP import dependency_parse_chinese
from translateUtil import translate_youdao, translate_baidu

from judgeFishbowl import JudgeFishbowl
from judgeClassroomAuditorium import JudgeClassroomAuditorium
from judgeBanquet import JudgeBanquet
from judgeUshape import JudgeUshape
from judgeHuddleBoard import JudgeHuddleBoard

from fastai.text import *
from pytorch_pretrained_bert import BertTokenizer

from util import solveTranslationProblem

import whisper
from zhconv import convert

import sys
sys.path.append(r"./generate_position/algorithm")
from generate_position.algorithm.algorithm import position_algorithm


categoryMapping = {"auditorium":0, "banquet":1, "classroom":2, "fishbowl":3, "huddle":4, "ushape":5}
whisper_model = whisper.load_model(r"D:\four2\Graduating Design\nlp\models\small.pt")

class Config(dict):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        for k, v in kwargs.items():
            setattr(self, k, v)

    def set(self, key, val):
        self[key] = val
        setattr(self, key, val)

class FastAiBertTokenizer(BaseTokenizer):
    """Wrapper around a BertTokenizer to be a BaseTokenizer in fastai"""
    def __init__(self, tokenizer: BertTokenizer, max_seq_len: int=128, **kwargs):
        self._pretrained_tokenizer = tokenizer
        self.max_seq_len = max_seq_len

    def __call__(self, *args, **kwargs):
        return self

    def tokenizer(self, t:str) -> List[str]:
        """Limits the maximum sequence length"""
        return ["[CLS]"] + self._pretrained_tokenizer.tokenize(t)[:self.max_seq_len - 2] + ["[SEP]"]

learner = load_learner(r"D:\four2\Graduating Design\nlp\category_predict\models")

replaceWordsEn = [["people classes", "people"],["human classes", "humans"],["middle there", "middle"], ["center there", "center"], ["centre there", "center"], ["inside there","inside"],["outside there","outside"],["inside, there","inside"],["outside, there","outside"],["middle, there", "middle"],["center, there", "center"],["centre, there","center"]]
replaceWordsEn += [["adding", "add"],["increasing","increase"],["removing","remove"],["reducing","reduce"],["lowering","lower"],["deleting","delete"]]
replaceWordsEn += [["human beings", "people"], ["human being", "people"]]

parser = reqparse.RequestParser()
parser.add_argument('input',help='strings param required',required=True)
parser.add_argument('lastJsonData',help='strings param required',required=True)
parserAudio = reqparse.RequestParser()

app = Flask(__name__)
api = Api(app)


def processInputEnglish(s_ch):
    s_ch = solveTranslationProblem(s_ch)
    s_en = translate_baidu(s_ch)
    s_en = s_en.lower()
    if s_en[-1] != ".":
        s_en += "."
    s_en = s_en[:-1].replace(".",",") + "."
    for replace, toRelace in replaceWordsEn:
        s_en = s_en.replace(replace, toRelace)
    print(s_en)

    res = "java\n" + s_en

    with open("in.txt", "w") as f:
        f.write(res)
    r_v = os.system("matt-SEL-playground.exe")
    print(r_v)

    f = open('out.txt', encoding='utf8')
    sentences = []
    startReadFlag = False
    conjAnd = []
    posTag = [""]
    relationships = []
    commands = {}
    lastCommand = ""
    for line in f:
        if startReadFlag:
            try:
                sentences.append(json.loads(line.strip()))
            except Exception as e:
                print("error: " + line.strip())
        if "conj:and" in line:
            firstEntity = line[line.index("(") + 1:line.index(",")]
            secondEntity = line[line.index(",") + 2:line.index("~")]
            conjAnd.append([firstEntity, secondEntity])

        # TODO command目前不考虑attributes信息
        if "command: " in line:
            commands[line[9:-1]] = {}
            lastCommand = line[9:-1]
        if "  attributes: " in line:
            if lastCommand != "":
                commands[lastCommand]["attributes"] = line[14:-2]
        if "  targets: " in line:
            if lastCommand != "":
                commands[lastCommand]["targets"] = line[11:-2]

        if "~" in line and "(" in line:
            l = line[line.index(",") + 2:-2]
            posTag.append(l.split("~")[1])
            index1 = line.index("(")
            index2 = line.index(",")
            index3 = line.index("~")
            r = line[:index1]
            entity1 = line[index1+1:index2]
            entity2 = line[index2+2:index3]
            relationships.append([r, [entity1, entity2]])
        if not startReadFlag and line.strip() == "=== for python ===":
            startReadFlag = True
    return sentences,s_ch,s_en,conjAnd,posTag, relationships, commands

def processFishbowl(s_ch, lastDataForModify):
    sentences, s_ch, s_en, conjAnd, posTag, relationships, commands = processInputEnglish(s_ch)
    data = JudgeFishbowl(sentences,s_ch,s_en,conjAnd,posTag,relationships,commands, lastDataForModify).process()
    res = {}
    res["type"] = "fishbowl"
    res["people_number"] = data[4]
    res["inner_circle_num"] = data[0]
    res["outer_circle_num"] = data[1]
    res["if_desk"] = data[2]
    res["inner_circle_chair_num"] = data[3]
    res["table_color"] = data[5]
    res["inner_chair_color"] = data[6]
    res["outer_chair_color"] = data[7]
    res["style"] = data[8]
    res["other_instruction"] = data[9]
    return res

def processAuditoriumClassroom(s_ch, isAuditorium):
    res = {}
    if isAuditorium:
        res["type"] = "auditorium"
    else:
        res["type"] = "classroom"
    words, dependencies = dependency_parse_chinese(s_ch)
    sentences, s_ch, s_en, conjAnd, posTag, relationships, commands = processInputEnglish(s_ch)
    judge = JudgeClassroomAuditorium(words, dependencies, sentences, s_ch, s_en, conjAnd, posTag, relationships, commands)
    row_number, aisle_number, people_number = judge.process()
    res["row_number"] = row_number
    res["aisle_number"] = aisle_number
    res["people_number"] = people_number
    return res

def processBanquet(s_ch):
    sentences, s_ch, s_en, conjAnd, posTag, relationships, commands = processInputEnglish(s_ch)
    judge = JudgeBanquet(sentences, s_ch, s_en, conjAnd, posTag, relationships, commands)
    table_number, if_half_circle, people_number = judge.process()
    res = {}
    res["type"] = "banquet"
    res["table_number"] = table_number
    res["if_half_circle"] = if_half_circle
    res["people_number"] = people_number
    return res

def processHuddleBoard(s_ch):
    words, dependencies = dependency_parse_chinese(s_ch)
    sentences, s_ch, s_en, conjAnd, posTag, relationships, commands = processInputEnglish(s_ch)
    judge = JudgeHuddleBoard(words, dependencies, sentences, s_ch, s_en, conjAnd, posTag, relationships, commands)
    res = {}
    res["type"] = "huddle"
    smallChairNumber, largeChairNumber = judge.extractEachSideChairNumber()
    res["short_side_chair_number"] = smallChairNumber
    res["long_side_chair_number"] = largeChairNumber
    res["people_number"] = judge.people_number
    return res

def processUshape(s_ch):
    sentences, s_ch, s_en, conjAnd, posTag, relationships, commands = processInputEnglish(s_ch)
    judge = JudgeUshape(sentences, s_ch, s_en, conjAnd,posTag, relationships, commands)
    middleChairCount, sideChairCount = judge.extractChairNumber()
    res = {}
    res["type"] = "ushape"
    res["middle_side_chair_number"] = middleChairCount
    res["double_side_chair_number"] = sideChairCount
    res["people_number"] = judge.people_number
    return res

def use_package(path):
    result = whisper_model.transcribe(path,language='Chinese',fp16=False)
    return ", ".join([i["text"] for i in result["segments"] if i is not None])

@app.route('/processAudio',methods=['GET'])
def processAudio():
    parserAudio.parse_args()
    path = r"D:\four2\Graduating Design\第十次构建4\SceneGenerator_Data\StreamingAssets\audio\inputAudio.wav"
    text = use_package(path)
    text = convert(text, 'zh-cn')
    # text = "语音转文字结果"
    print("语音转文字结果：",text)
    return text


@app.route('/meetingRoom',methods=['POST'])
def processMeetingRoom():
    parser.parse_args()
    sentences = request.json["input"]
    lastJsonDataStr = request.json["lastJsonData"]
    lastJsonDataStr = lastJsonDataStr.replace("false", "'false'")
    lastJsonDataStr = lastJsonDataStr.replace("true", "'true'")
    lastJsonDataStr = lastJsonDataStr.replace("False", "'false'")
    lastJsonDataStr = lastJsonDataStr.replace("True", "'true'")
    lastJsonDataStr = lastJsonDataStr.replace("\'","\"")
    print(lastJsonDataStr)
    lastJsonData = {}
    if len(lastJsonDataStr) > 2:
        lastJsonData = json.loads(lastJsonDataStr)
    lastLayoutObjects = []
    lastDataForModify = {}
    category = 3
    if len(lastJsonData.keys()) > 0:
        lastLayoutObjects = lastJsonData["LayoutObjects"]
        lastDataForModify = lastJsonData["dataForModify"]
        if categoryMapping[lastDataForModify["type"]] == 3:
            if lastDataForModify["if_desk"] == "false":
                lastDataForModify["if_desk"] = False
            else:
                lastDataForModify["if_desk"] = True
        category = categoryMapping[lastDataForModify["type"]]
    else:
        category = int(learner.predict(sentences)[1].item())

    res = {}
    if category == 0:
        print("category: Auditorium")
        res = processAuditoriumClassroom(sentences, True)
    elif category == 1:
        print("category: Banquet")
        res = processBanquet(sentences)
    elif category == 2:
        print("category: Classroom")
        res = processAuditoriumClassroom(sentences, False)
    elif category == 3:
        print("category: Fishbowl")
        res = processFishbowl(sentences, lastDataForModify)
    elif category == 4:
        print("category: HuddleBoard")
        res = processHuddleBoard(sentences)
    else:
        print("category: Ushape")
        res = processUshape(sentences)

    print("newDataForModify:")
    print(res)
    print("lastDataForModify:")
    print(lastDataForModify)

    data = res
    if category == 3:
        data = {}
        data["newDataForModify"] = res
        data["lastDataForModify"] = lastDataForModify
    # # # TODO 加上gwq和jx算法
    res = position_algorithm(data)
    print("json res:",res)

    return res


if __name__=="__main__":
    app.run(debug=True)
