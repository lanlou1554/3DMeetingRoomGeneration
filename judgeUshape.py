from judgeUtil import chairSynonymsEn
from judgeUtil import indexToWord
from judgeUtil import obtainAndEntities
from judgeUtil import printEntities
from judgeUtil import extractEntities, extractPeopleNumber
from util import convertWordsToNumber
import math

middleSynonymsEn = ["middle"]
sideSynonymsEn = ["side"]

class JudgeUshape:
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
        if self.people_number <= 0:
            self.people_number = 10

    def _extractConjAnd(self, conjAnd):
        andEntites = obtainAndEntities(conjAnd, self.entities)
        print(andEntites)
        return andEntites

    def _modifyEntities(self):
        # TODO 六张桌子和椅子
        printEntities(self.entities)

    def extractChairNumber(self):
        chairCount = []
        middleChairCount = -1
        sideChairCount = -1
        for k in self.entities.keys():
            for chair in chairSynonymsEn:
                if chair in k:
                    if "count" in self.entities[k].keys():
                        try:
                            count = convertWordsToNumber(self.entities[k]["count"])
                            if count > 0:
                                for middle in middleSynonymsEn:
                                    if middle in self.entities[k]["attributes"]:
                                        middleChairCount = count
                                for side in sideSynonymsEn:
                                    if side in self.entities[k]["attributes"]:
                                        sideChairCount = count
                                chairCount.append(count)
                        except Exception as e:
                            pass
        if sideChairCount != -1:
            middleChairCount = math.ceil(self.people_number-(sideChairCount*2.0))
            if middleChairCount > 0 and sideChairCount > 0:
                return middleChairCount, sideChairCount
        if middleChairCount != -1:
            sideChairCount = math.ceil((self.people_number-middleChairCount)*1.0/2)
            if middleChairCount > 0 and sideChairCount > 0:
                return middleChairCount, sideChairCount
        chairCount.sort(reverse=True)
        for count in chairCount:
            if count * 2 >= self.people_number:
                continue
            if count <= 1:
                continue
            sideChairCount = math.ceil((self.people_number-count)*1.0/2)
            middleChairCount = math.ceil(self.people_number-(count*2.0))
            if sideChairCount <= 0 or middleChairCount <= 0:
                continue
            if sideChairCount >= count:
                print("count: (middle)", count)
                return count, sideChairCount
            if count >= middleChairCount:
                print("count: (side)", count)
                return middleChairCount, count
        return -1, -1


# if __name__=="__main__":
#     sentences = ["两侧长桌对应了多把椅子，长桌中间有一短桌对应了四把椅子，每扇落地窗边各有一个沙发椅",
#                  "桌子三面围绕，中间两把椅子，两边分别四把椅子"]
#     for s in sentences:
#         sentences, s_ch, s_en, conjAnd, posTag = processInputEnglish(s)
#         judge = JudgeUshape(sentences, s_ch, s_en, conjAnd, 20)
#         print(judge.extractChairNumber())
#         print("=========================")