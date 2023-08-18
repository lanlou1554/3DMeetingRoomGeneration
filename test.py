from translateUtil import Translator
from stanfordcorenlp import StanfordCoreNLP
import requests
import time
from urllib import parse
import whisper
# import stable_whisper as whisper
from pydub import AudioSegment


def trans_mp3_to_other(filepath, hz):
    song = AudioSegment.from_mp3(filepath)
    song.export("Newsound." + str(hz), format=str(hz))


def trans_wav_to_other(filepath, hz):
    song = AudioSegment.from_wav(filepath)
    song.export("Newsound." + str(hz), format=str(hz))


def trans_ogg_to_other(filepath, hz):
    song = AudioSegment.from_ogg(filepath)
    song.export("Newsound." + str(hz), format=str(hz))


def trans_flac_to_other(filepath, hz):
    song = AudioSegment.from_file(filepath)
    song.export("Newsound." + str(hz), format=str(hz))


def trans_m4a_to_other(filepath, hz):
    song = AudioSegment.from_file(filepath)
    song.export("Newsound." + str(hz), format=str(hz))

def use_package(path):
    whisper_model = whisper.load_model(r"D:\four2\Graduating Design\nlp\models\small.pt")
    result = whisper_model.transcribe(path,language='Chinese',fp16=False)
    print(", ".join([i["text"] for i in result["segments"] if i is not None]))

def dependency_parse():
    # nlp = StanfordCoreNLP(r'D:\four1\HCI\task3\language-driven\NLP_release\stanford-corenlp-full-2016-10-31', lang='zh')
    nlp = StanfordCoreNLP(r'D:\Downloads\stanford-corenlp-full-2018-01-31\stanford-corenlp-full-2018-01-31', lang='zh')
    # nlp = StanfordCoreNLP(r'../stanford-corenlp-4.5.4', lang='zh')
    # sentence = parse.quote(sentence, encoding='utf8')
    # print('Tokenize:')
    # print(nlp.word_tokenize(sentence))
    # print('Part of Speech:')
    # print(nlp.pos_tag(sentence))
    # print('Named Entities:')
    # print(nlp.ner(sentence))
    # print('Constituency Parsing:')
    # print(nlp.parse(sentence))
    # print('Dependency Parsing:')
    # print(nlp.dependency_parse(sentence))
    sentences = ["我想要一个能做得下几百个人类的会议室。","我想要一个有几十个椅子的会议室。","我想要一个有十几个椅子的会议室。"]
    # sentences = ["人数是20个人。", "人数有20个人。", "会议室人数有20个人。", "会议室一共有20个人。"]
    for sentence in sentences:
        print(sentence)
        words = list(nlp.word_tokenize(sentence))
        arcs = list(nlp.dependency_parse(sentence))
        print(arcs)
        arcs.sort(key=lambda x: x[2])
        words = [w + "-" + str(idx) for idx, w in enumerate(words)]
        rely_id = [arc[1] for arc in arcs]
        relation = [arc[0] for arc in arcs]
        heads = ['Root' if id == 0 else words[id - 1] for id in rely_id]
        for i in range(len(words)):
            print(relation[i] + '(' + heads[i] + ', ' + words[i] + ')')
        print("==================================")
    nlp.close()  # Do not forget to close! The backend server will consume a lot memery.

def translate():
    # 中文翻译成英文
    translator = Translator(from_lang="ZH", to_lang="EN-US")

    translation = translator.translate("四个红凳子围成一个圈，然后是绿椅子围成两个圈，最中间是一个桌子。")
    print(translation + "\n")

    translation = translator.translate("绿色椅子围着四个皮质的红色沙发，然后沙发中间有一个小桌子。")
    print(translation + "\n")

    translation = translator.translate("以四张方形小沙发为中心，绿色椅子层层环绕，围绕成两圈。")
    print(translation + "\n")

    translation = translator.translate("围绕一张小桌子和五把椅子，几十张椅子围绕中心点向四周呈射线式分散。")
    print(translation + "\n")

    translation = translator.translate("几张小桌围绕一个圆桌。")
    print(translation + "\n")

    translation = translator.translate("椅子围绕中心圆形放置逐渐向外扩展，最内圈是五把黄色的椅子，外围是黑色的椅子。")
    print(translation + "\n")

    translation = translator.translate("外圈围绕着一圈小型书桌，每张书桌配有一张椅子，内圈有六张椅子围绕着一张大圆桌。")
    print(translation + "\n")

    translation = translator.translate("外圈两排椅子围绕着内圈的四张沙发，其中两张沙发之间有一个小圆桌。")
    print(translation + "\n")

    translation = translator.translate("里外有几层座位，环环围绕成一个圈，没有桌子只有椅子，间距不一，较为随意。")
    print(translation + "\n")


def translateYouDao(con):
    try:
        data = {'doctype': 'json',
                type: 'ZH_CN2EN',
                'i': con}
        r = requests.get("https://fanyi.youdao.com/translate", params=data)
        res_json = r.json()
        res_d = res_json['translateResult'][0]
        tgt = []
        for i in range(len(res_d)):
            tgt.append(res_d[i]['tgt'])
        return ''.join(tgt)
    except Exception as e:
        print('翻译失败：', e)
        return '翻译失败：' + con

if __name__ == '__main__':
    # import time
    # # dependency_parse()
    # # trans_m4a_to_other(r"D:\Downloads\audioTest\video.m4a", "mp3")
    # use_package(r"C:\Users\15548\Documents\Tencent Files\1554893443\FileRecv\MobileFile\inputAudio.wav")
    # time_start = time.time()  # 记录开始时间
    # use_package(r"C:\Users\15548\Documents\Tencent Files\1554893443\FileRecv\MobileFile\inputAudio.wav")
    # # function()   执行的程序
    # time_end = time.time()  # 记录结束时间
    # time_sum = time_end - time_start  # 计算的时间差为程序的执行时间，单位为秒/s
    # print(time_sum)
    import json
    lastJsonDataStr = "{'type': 'fishbowl', 'people_number': 24, 'inner_circle_num': 1,'outer_circle_num': -1, 'if_desk': False, 'inner_circle_chair_num': 4, 'table_color': 'green', 'inner_chair_color': 'black', 'outer_chair_color': 'white', 'style': '简约现代', 'other_instruction': ''}"
    lastJsonDataStr = "{'LayoutObjects': [], 'dataForModify': {}}"
    lastJsonDataStr = lastJsonDataStr.replace("\'", "\"")
    print(lastJsonDataStr)
    lastJsonData = json.loads(lastJsonDataStr)
    print(lastJsonData)
