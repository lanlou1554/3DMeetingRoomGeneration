from judgeUtil import chairSynonymsEn
from judgeUtil import tableSynonymsEn
from judgeUtil import indexToWord
from judgeUtil import obtainAndEntities
from judgeUtil import printEntities
from judgeUtil import extractEntities, extractPeopleNumber
from util import convertWordsToNumber
import math

lowestChairCountPerTable = 4
circleSynonymsEn = ["circle", "lap", "ring"]
groupSynonymsEn = ["group", "set"]
defaultTableCount = 5

class JudgeBanquet:
    def __init__(self, sentences, s_ch, s_en, conjAnd, posTag, relationships, commands):
        self.commands = commands
        self.posTag = posTag
        self.relationships = relationships
        self.wordIndex = indexToWord(s_en)
        self.entities, self.noEntities = extractEntities(sentences, self.wordIndex)
        self.andEntities = self._extractConjAnd(conjAnd)
        self._modifyEntities()
        self.s_ch = s_ch
        self.s_en = s_en
        self.people_number = extractPeopleNumber(self.wordIndex, self.entities, self.relationships)

    def process(self):
        table_number = self.extractTableNumber()
        half_circle_table = self.whetherEachTableHalfCircleChair()
        if self.people_number <= 0:
            self.people_number = self.calculatePeopleNumber(table_number,half_circle_table)
        return table_number, half_circle_table, self.people_number

    def calculatePeopleNumber(self, table_number, half_circle_table):
        if table_number > 0:
            if half_circle_table:
                return table_number * 3
            else:
                return table_number * 6
        else:
            return 25

    def _extractConjAnd(self, conjAnd):
        andEntites = obtainAndEntities(conjAnd, self.entities)
        print(andEntites)
        return andEntites

    def _modifyEntities(self):
        # TODO 六张桌子和椅子
        printEntities(self.entities)

    def extractTableNumber(self):
        tableCount = -1
        chairCount = -1
        for k in self.entities.keys():
            for table in tableSynonymsEn + groupSynonymsEn:
                if table in k:
                    if "count" in self.entities[k].keys():
                        try:
                            count = convertWordsToNumber(self.entities[k]["count"])
                            if count > 1 and count > tableCount:
                                tableCount = count
                        except Exception as e:
                            pass
            for chair in chairSynonymsEn:
                if chair in k:
                    if "count" in self.entities[k].keys():
                        try:
                            count = convertWordsToNumber(self.entities[k]["count"])
                            if count > 1 and count > chairCount:
                                chairCount = count
                        except Exception as e:
                            pass
        if tableCount != -1:
            if chairCount != -1:
                if self.people_number <= 0 and chairCount < 20:
                    self.people_number = tableCount * chairCount
            return tableCount
        if chairCount != -1 and chairCount >= lowestChairCountPerTable and chairCount < 20:
            print("chairCount:",chairCount)
            self.people_number = defaultTableCount * chairCount
            return defaultTableCount
        return -1

    def whetherEachTableHalfCircleChair(self):
        for k in self.entities.keys():
            for circle in circleSynonymsEn:
                if circle in k:
                    if "half" in self.entities[k]["attributes"] or "half" in self.entities[k]["determiners"]:
                        for chair in chairSynonymsEn:
                            if ("of:"+chair) in self.entities[k]["relationships"]:
                                return True
        # False代表没说，不代表不一定……按照默认来
        return False

# if __name__=="__main__":
#     # sentences = ["由若干组桌椅组成，12张椅子围着一个桌子",
#     #              "布局由好几个桌椅围成的小圈组成，每个小圈由6张桌椅组成",
#     #              "好几组环形布局的桌椅，每组6个座位",
#     #              "若干张梯形课桌拼成六边形，每个边有一把椅子，大房间内有多个六边形",
#     #              "每六个桌子成一组，围成一个六边形，房间内多组桌子错落排放，每组桌子的一条边上放置一张椅子",
#     #              "整个会议室分为五组桌椅，每组桌椅是由梯形单人桌围城的六边形大桌，周围有六把椅子",
#     #              "四张桌子纵向面向屏幕，摆放两行，每行两张。每张桌子两侧各三张椅子。",
#     #              "四张椅子围绕着一张小桌子，一共有多组这样的桌椅组合布满整个房间。",
#     #              "五列圆桌，每个圆桌围绕半圈椅子，椅子都朝向正前方。",
#     #              "几十张圆桌均匀分布，每张桌子上10个座位",
#     #              "房间内有很多圆桌，每张圆桌周围放约8张椅子",
#     #              "有很多圆形的桌子，每个桌子周围带有十把椅子",
#     #              "有五张长方形桌子，彼此分开，不靠近。每个桌子四周围绕着五个椅子。",
#     #              "四组长桌椅分布在会议室的两侧，每侧各两组，每张长桌对应五把椅子",
#     #              "以小桌形式，一张桌子周围配置六个椅子"]
#     sentences = ["整个会议室分为五组桌椅，每组桌椅是由梯形单人桌围城的六边形大桌，周围有六把椅子",
#                  "四组长桌椅分布在会议室的两侧，每侧各两组，每张长桌对应五把椅子"]
#     for s in sentences:
#         sentences, s_ch, s_en, conjAnd, posTag = processInputEnglish(s)
#         judge = JudgeBanquet(sentences, s_ch, s_en, conjAnd, 30)
#         print(judge.extractTableNumber())
#         print(judge.whetherEachTableHalfCircleChair())
#         print("=========================")

