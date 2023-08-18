from flask import Flask
from flask_restful import Api,reqparse,request
import json
import whisper
from zhconv import convert
categoryMapping = {"auditorium":0, "banquet":1, "classroom":2, "fishbowl":3, "huddle":4, "ushape":5}
parserMeetingRoom = reqparse.RequestParser()
parserMeetingRoom.add_argument('input',help='strings param required',required=True)
parserMeetingRoom.add_argument('lastJsonData',help='strings param required',required=True)

parserAudio = reqparse.RequestParser()

app = Flask(__name__)
api = Api(app)

count = 7
fishbowlJson = []

for i in range(8):
    f = open('./fishbowl'+str(i+1)+'.txt', encoding='utf-8')
    temp = ""
    for line in f:
        temp += line
    fishbowlJson.append(temp)



def nlp_algorithm(category, lastDataForModify, description):
    newDataForModify = {}
    return newDataForModify

def position_algorithm(lastDataForModify, newDataForModify, lastLayoutObjects):
    global count
    if count == 8:
        count = 0
    return fishbowlJson[count]


def use_package(path):
    whisper_model = whisper.load_model(r"D:\four2\Graduating Design\nlp\models\small.pt")
    result = whisper_model.transcribe(path,language='Chinese',fp16=False)
    return ", ".join([i["text"] for i in result["segments"] if i is not None])

@app.route('/processAudio',methods=['GET'])
def processAudio():
    parserAudio.parse_args()
    path = r"D:\four2\Graduating Design\第八次构建\SceneGenerator_Data\StreamingAssets\audio\inputAudio.wav"
    text = use_package(path)
    text = convert(text, 'zh-cn')
    # text = "语音转文字结果"
    print("语音转文字结果：",text)
    return text

@app.route('/meetingRoom',methods=['POST'])
def processMeetingRoom():
    parserMeetingRoom.parse_args()
    description = request.json["input"]
    lastJsonDataStr = request.json["lastJsonData"]

    print("lastJsonDataStr:",lastJsonDataStr)
    print(description)
    lastJsonDataStr = lastJsonDataStr.replace("false", "'false'")
    lastJsonDataStr = lastJsonDataStr.replace("true", "'true'")
    lastJsonDataStr = lastJsonDataStr.replace("False", "'false'")
    lastJsonDataStr = lastJsonDataStr.replace("True", "'true'")
    lastJsonDataStr = lastJsonDataStr.replace("\'", "\"")
    lastJsonData = {}
    print("lastJsonDataStr:", lastJsonDataStr)

    if len(lastJsonDataStr) > 2:
        print("jsondata>0")
        lastJsonData = json.loads(lastJsonDataStr)
    print("lastJsonData:",lastJsonData)
    lastLayoutObjects = []
    lastDataForModify = {}
    category = 3
    if len(lastJsonData.keys()) > 0:
        lastLayoutObjects = lastJsonData["LayoutObjects"]
        lastDataForModify = lastJsonData["dataForModify"]
        if lastDataForModify["if_desk"] == "false":
            lastDataForModify["if_desk"] = False
        else:
            lastDataForModify["if_desk"] = True
        category = categoryMapping[lastDataForModify["type"]]
    else:
        category = 3

    newDataForModify = nlp_algorithm(category,lastDataForModify,description)
    jsonResult = position_algorithm(lastDataForModify, newDataForModify, lastLayoutObjects)

    print("jsonResut:",jsonResult)

    global count
    count += 1
    return jsonResult



if __name__=="__main__":
    app.run(debug=True)