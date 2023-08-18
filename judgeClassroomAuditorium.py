from judgeUtil import indexToWord, extractEntities, obtainAndEntities, printEntities, extractPeopleNumber
from util import convertWordsToNumber_Chinese
from util import ChineseNumberWords
from coreNLP import dependency_parse_chinese


class JudgeClassroomAuditorium:
    def __init__(self, words, dependencies, sentences, s_ch, s_en, conjAnd, posTag, relationships, commands):
        self.commands = commands
        self.words = words
        self.dependencies = dependencies
        self.posTag = posTag
        self.relationships = relationships
        self.wordIndex = indexToWord(s_en)
        self.entities, self.noEntities = extractEntities(sentences, self.wordIndex)
        self.andEntities = self._extractConjAnd(conjAnd)
        self._modifyEntities()
        self.people_number = extractPeopleNumber(self.wordIndex,self.entities, self.relationships)
        self.s_ch = s_ch
        self.s_en = s_en

    def process(self):
        row_number = self.extractRowNumber()
        aisle_number = self.extractAisleNumber()
        if self.people_number == -1:
            self.people_number = self.calculatePeopleNumber(row_number)
        return row_number,aisle_number,self.people_number

    def calculatePeopleNumber(self, row_number):
        if row_number <= 0:
            return 30
        else:
            return row_number * 8

    def _extractConjAnd(self, conjAnd):
        andEntites = obtainAndEntities(conjAnd, self.entities)
        print(andEntites)
        return andEntites

    def _modifyEntities(self):
        # TODO 六张桌子和椅子
        printEntities(self.entities)

    def extractRowNumber(self):
        rowSynonymsCh = ["排", "行"]
        rowNumber = -1
        for row in rowSynonymsCh:
            if rowNumber <= 2:
                rowNumber = self._extractEntityNumber(row,["横","大"])
        print(rowNumber)
        if rowNumber > 2:
            return rowNumber
        else:
            return -1

    # 若列的数目小于等于4，则认为是大列
    def extractAisleNumber(self):
        aisleSynonymsCh = ["过道", "走廊"]
        for aisle in aisleSynonymsCh:
            aisleNumber = self._extractEntityNumber(aisle,["个"])
            if aisleNumber != -1:
                return aisleNumber
        if "左右两边" in self.s_ch or "左右两部分" in self.s_ch:
            return 1
        columnNumber = self._extractEntityNumber("列",["大","竖"])
        if columnNumber > 1 and columnNumber <= 4:
            return columnNumber - 1
        return -1

    def _extractEnitityNumberFromSentence(self, index, ignoreWords):
        countWords = ""
        while index >= 0:
            if self.s_ch[index] in ChineseNumberWords:
                countWords = self.s_ch[index] + countWords
                index -= 1
                continue
            if self.s_ch[index] not in ignoreWords:
                break
            index -= 1
        return convertWordsToNumber_Chinese(countWords)

    def _extractEntityNumber(self, entity, ignoreWords):
        # 先从dependencies里抽
        count = -1
        if entity not in self.s_ch:
            return count
        bigRow = []
        for d in self.dependencies:
            if d[0] == "amod" and d[1].split("-")[0] == "列" and d[2].split("-")[0] == "大":
                bigRow.append(d[1])
        for d in self.dependencies:
            if d[0] == "mark:clf":
                if d[2].split("-")[0] == entity:
                    count = convertWordsToNumber_Chinese(d[1].split("-")[0])
                    if d[2] in bigRow:
                        break
            if d[0] == "dobj" and "没有" in d[1]:
                if d[2].split("-")[0] == entity:
                    count = 0

        if count != -1:
            return count

        # 再直接从句子里抽
        for i in range(len(self.s_ch)):
            if self.s_ch[i:i+len(entity)] == entity:
                countTemp = self._extractEnitityNumberFromSentence(i-1,ignoreWords)
                if entity == "列" and i >0 and self.s_ch[i-1] == "大" and countTemp != -1:
                    return countTemp
                if count == -1 or (countTemp > count):
                    count = countTemp
        return count

if __name__=="__main__":
    # ss = ["大学教室布局，紧密排布，中间一行八个座椅，两侧一行四个座椅。从前到后座位高度依次变高",
    #              "两列多排桌椅，分布紧密",
    #              "整齐分布，较为紧凑，2列3排",
    #              "六张桌子组成三排，中间有一个过道，每排桌子有8个椅子。",
    #              "有四个弧形的长桌子，中间的空间有很多把椅子",
    #              "五排半圆形长桌，每一排10余张椅子，椅子数量每排递增",
    #              "整个教室有两大列桌椅，中间有一个过道",
    #              "两侧有多排长桌，每个长桌后有两把椅子",
    #              "五排椅子，每排椅子都有四张桌。",
    #              "五排桌椅，两侧有过道；每个带桌布的长桌配四张椅子",
    #              "每两张桌子并排放形成一条直线，两排桌子之间有一定间隔，间隔之间放置椅子",
    #              "三大列桌椅，每大列三小列。正前方靠左侧有一个讲台。",
    #              "按列和排规律分成三列排布，有两个过道",
    #              "桌椅分布在教师中间走廊的两侧，一张长桌对应两把椅子，一侧有三张长桌"]
    # ss = ["两大列座位分布在道路两侧，每大列座位由数列、数行座位组成",
    #              "有许多排红色椅子，有靠背，面向前方，中间有一个过道。最前面有一个长桌子和7张椅子。",
    #              "十多排椅子，每排20把",
    #              "成排的塑料椅，分成三列，有两个过道，没有桌子",
    #              "椅子摆放在左右两边，中间是过道，两边各有7列12排",
    #              "有八行椅子，都面向前方，没有过道。",
    #              "有八排椅子，都面向前方，没有过道。",
    #              "共有三排椅子，并且有两个过道",
    #              "共有三行椅子，并且有两个过道",
    #              "没有桌子，有很多排椅子，分为左右两部分",
    #              "一共两大列，8小列，每大列4小列共5排椅子"]
    ss = ["共有三排椅子，并且有两个过道"]
    for sentence in ss:
        words, dependencies = dependency_parse_chinese(sentence)
        judge = JudgeClassroomAuditorium(words, dependencies,sentence)
        print(judge.extractRowNumber())
        print(judge.extractAisleNumber())
        print("====================================")