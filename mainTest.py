import os
import json

from translateUtil import translate_baidu
from translateUtil import translate_youdao
from translateUtil import translate
from judgeFishbowl import JudgeFishbowl
from util import solveTranslationProblem


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
    # s_en = "i want generate rooms without tables."

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

replaceWordsEn = [["people classes", "people"],["human classes", "humans"],["middle there", "middle"], ["center there", "center"], ["centre there", "center"], ["inside there","inside"],["outside there","outside"],["inside, there","inside"],["outside, there","outside"],["middle, there", "middle"],["center, there", "center"],["centre, there","center"]]
replaceWordsEn += [["adding", "add"],["increasing","increase"],["removing","remove"],["reducing","reduce"],["lowering","lower"],["deleting","delete"]]

if __name__=="__main__":
    s_ch = "一共有三十个座位。"
    # TODO 多个句子还是一个句子？多个句子务必解决entity Index冲突问题
    # TODO 解决翻译问题： “外面有三排椅子”， “外面有三圈椅子” ”三列椅子“翻译的不正确

    # TODO 内圈一共有两圈椅子，每圈各有10个椅子。
    # sentences = ["外圈一共有两圈，每圈各有10个椅子。","外面围绕着20个椅子。","外圈一共有20张椅子。","椅子的颜色是红色的","外圈增加一圈椅子","每把椅子都配有桌子","一共有20人"]
    sentences = ["外圈一共有两圈椅子，每圈各有10个椅子。","在外部，每圈各有10个椅子","在外部，一共有2圈，每圈各有10个椅子。","在内部，每圈各有10个椅子","在内部，一共有2圈，每圈各有10个椅子。"]
    sentences = ["每圈有10把椅子。","一共有2圈，每圈有10把椅子。","内部一共有两圈椅子，每圈各有10个椅子。","在内圈，一共有两圈椅子，每圈各有10个椅子。"]
    sentences = ["一共有20人","椅子的颜色是红色的","把椅子的颜色变成红色","每把椅子都配有桌子","外圈增加一圈椅子","把椅子变得更加密集一些"]
    sentences = ["我想生成10人的教室"]
    lastDataForModify = {}
    lastDataForModify["if_desk"] = True
    lastDataForModify["inner_circle_chair_num"] = "4"
    lastDataForModify["inner_circle_num"] = "1"
    lastDataForModify["outer_circle_num"] = "2"
    lastDataForModify["people_number"] = "24"
    lastDataForModify["inner_chair_color"] = "black"
    lastDataForModify["outer_chair_color"] = "white"
    lastDataForModify["table_color"] = "black"
    lastDataForModify["style"] = "简约现代"
    lastDataForModify["other_instruction"] = ""
    print(lastDataForModify)
    for s_ch in sentences:
        print(s_ch)
        sentences, s_ch, s_en, conjAnd, posTag, relationships, commands = processInputEnglish(s_ch)
        print(sentences)
        print(conjAnd)
        print(posTag)

        judge = JudgeFishbowl(sentences, s_ch, s_en, conjAnd, posTag, relationships,commands, lastDataForModify=lastDataForModify)
        print(judge.process())

