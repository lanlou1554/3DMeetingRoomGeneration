from util import convertWordsToNumber_Chinese
from coreNLP import dependency_parse_chinese
from judgeUtil import obtainAndEntities, indexToWord, extractEntities
from judgeUtil import printEntities, extractPeopleNumber
import math

chairSynonymsCh = ["椅", "凳"]


class JudgeHuddleBoard:
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

    def extractEachSideChairNumber(self):
        chairCount = set()
        for d in self.dependencies:
            if d[0] == "nummod":
                for c in chairSynonymsCh:
                    if c in d[1]:
                        count = convertWordsToNumber_Chinese(d[2].split("-")[0])
                        if count != -1:
                            chairCount.add(count)
        chairCount = list(chairCount)
        chairCount.sort(reverse=True)

        finalCount = -1
        for count in chairCount:
            if count * 2 <= self.people_number:
                finalCount = count
                break
        if finalCount == -1:
            return -1, -1
        else:
            print("final count:", finalCount)
            anotherCount = math.ceil((self.people_number - (finalCount * 2.0)) / 2)
            if anotherCount > finalCount:
                return finalCount, anotherCount
            else:
                return anotherCount, finalCount


if __name__ == "__main__":
    ss = ['中间有一个桌子，左右两侧都有九把椅子，后方有一把椅子',
                 "房间内只有一张长桌子，桌子较长的两侧各放置一排约九个椅子，桌子较窄的一侧放置一张椅子，较窄的另一侧正对显示屏",
                 "一张大长桌两侧分布了多把椅子，长桌一头有一把椅子",
                 "一张很大的原木色长桌，周围摆放着许多白色滑轮椅子，桌子的两端各有一把椅子",
                 "有一张长的、大的桌子，短的一端对应放映机，短的另一端放置一个椅子，领导位置，然后长的两端整齐放置椅子"]
    for sentence in ss:
        words, dependencies = dependency_parse_chinese(sentence)
        judge = JudgeHuddleBoard(words, dependencies, sentence, 20)
        print(judge.extractEachSideChairNumber())
        print("=========================")
