from util import convertWordsToNumber
from judgeUtil import chairSynonymsEn, tableSynonymsEn, peopleSynonymsEn, addSynonymsEn, reduceSynonymsEn, colorSynonymsEn, acceptableColorsEn, denseSynonymsEn, sparseSynonymsEn
from judgeUtil import calculateChangePeopleNum,modifyCommands, punctuations, indexToWord, obtainAndEntities, printEntities, extractEntities, extractPeopleNumber, decideStyle

eachSynonymsEn = ["each", "every"]
circleSynonymsEn = ["circle", "row", "layer", "ring", "lap", "round", "time"]
innerSynonymsEn = ["inner", "inside"]
outerSynonymsEn = ["outer", "outside", "periphery"]
surroundSynonymsEn = ["surround", "around"]
surroundAttributes = ["surrounding", "around"]
middleSynonymsEn = ["middle", "center", "centre"]
positionAttributeWords = innerSynonymsEn + outerSynonymsEn + middleSynonymsEn
extraHandlePositionWords = ["inside", "outside"]

chairSynonymsEn = chairSynonymsEn + peopleSynonymsEn

defaultOuterCircleNumber = 2
defaultInnerCircleChairNumber = 5
defaultLowestPeopleEachOuterCircle = 5
defaultLargestPeopleEachOuterCircle = 30
defaultLowestPeopleEachOuterCircleAddStep = 1
defaultLargestPeopleEachOuterCircleAddStep = 20
defaultPeopleEachOuterCircle = 10
defaultPeopleEachOuterCircleAddStep = 2
defaultOuterPeople = 20

class JudgeFishbowl:
    def __init__(self, sentences, s_ch, s_en, conjAnd, posTag, relationships, commands, lastDataForModify=None):
        if lastDataForModify is None:
            lastDataForModify = dict()
        self.commands = modifyCommands(commands, relationships)
        self.posTag = posTag
        self.relationships = relationships
        self.s_ch = s_ch
        self.s_en = s_en
        self.wordIndex = indexToWord(s_en)
        self.entities, self.noEntities = extractEntities(sentences, self.wordIndex)
        self.andEntities = self._extractConjAnd(conjAnd)
        self._modifyEntities()
        self.people_number = extractPeopleNumber(self.wordIndex,self.entities,self.relationships)
        self.innerCircle = None
        self.hasInnerCircle = None
        self.innerCircleNumber = -1
        self.outerCircleNumber = -1
        self.lastDataForModify = lastDataForModify

    def process(self):
        innerCircleNumber, outerCircleNumber = self.circleNumber()
        eachChairHasEachTable = self.eachChairHasEachTable()
        self.innerCircleNumber = innerCircleNumber
        self.outerCircleNumber = outerCircleNumber
        tableColor, innerChairColor, outerChairColor = self.decideTableAndChairColor()
        style = decideStyle(self.s_ch)
        if self.lastDataForModify is None or len(self.lastDataForModify.keys()) == 0:
            if style == "":
                style = "简约现代"
            # if tableColor == "":
            #     tableColor = "blue"
            if innerChairColor == "":
                innerChairColor = "white"
            if outerChairColor == "":
                outerChairColor = "white"
            chairInInnerCircle = self.chairInInnerCircle()
            chairInOuterCircle = self._decideOuterChairNumber()
            if chairInInnerCircle == -2:
                chairInInnerCircle = 0
            self.people_number = self._checkPeopleNumber(chairInInnerCircle, chairInOuterCircle)
            if self.people_number == -1:
                self.people_number = self._decideDefaultPeopleNumber(chairInInnerCircle)
            return [innerCircleNumber, outerCircleNumber, eachChairHasEachTable,chairInInnerCircle,self.people_number, tableColor, innerChairColor, outerChairColor, style, ""]
        else:
            ifDesk = self.lastDataForModify["if_desk"]
            if not eachChairHasEachTable:
                eachChairHasEachTable = ifDesk
            if self._checkNoEachTable():
                eachChairHasEachTable = False

            if style == "":
                style = self.lastDataForModify["style"]

            if tableColor == "":
                tableColor = self.lastDataForModify["table_color"]
            if innerChairColor == "":
                innerChairColor = self.lastDataForModify["inner_chair_color"]
            if outerChairColor == "":
                outerChairColor = self.lastDataForModify["outer_chair_color"]

            otherInstructions = self.handleOtherInstructions()

            lastInnerCircleNumber = int(self.lastDataForModify["inner_circle_num"])
            lastOuterCircleNumber = int(self.lastDataForModify["outer_circle_num"])
            # TODO check command, 如果是add，delete，则加上而不是等于
            addReduceCommands = self._getAddOrReduceCommands()
            innerCircleNumber, outerCircleNumber = self._handleInnerOuterCircleCommand(addReduceCommands,innerCircleNumber,outerCircleNumber,lastInnerCircleNumber,lastOuterCircleNumber)
            self.innerCircleNumber = innerCircleNumber
            self.outerCircleNumber = outerCircleNumber
            chairInInnerCircle = self.chairInInnerCircle()
            innerCircleChairNumber = int(self.lastDataForModify["inner_circle_chair_num"])
            if chairInInnerCircle == 0:
                chairInInnerCircle = innerCircleChairNumber
            elif chairInInnerCircle == -1:
                if innerCircleChairNumber > 0:
                    chairInInnerCircle = innerCircleChairNumber
            elif chairInInnerCircle == -2:
                chairInInnerCircle = 0

            chairInOuterCircle = self._decideOuterChairNumber()
            self.people_number = self._checkPeopleNumber(chairInInnerCircle, chairInOuterCircle)
            if self.people_number == -1:
                self.people_number = int(self.lastDataForModify["people_number"])
            self.people_number += calculateChangePeopleNum(self.people_number, self.commands,self.entities,self.relationships)
            if chairInInnerCircle == 0 and innerCircleChairNumber > 0:
                self.people_number -= (innerCircleChairNumber)
            return [innerCircleNumber, outerCircleNumber, eachChairHasEachTable, chairInInnerCircle, self.people_number,tableColor, innerChairColor, outerChairColor, style, otherInstructions]


    def handleOtherInstructions(self):
        for key in self.entities.keys():
            for chair in chairSynonymsEn:
                if chair in key:
                    for dense in denseSynonymsEn:
                        if dense in self.entities[key]["attributes"]:
                            return "dense"
                    for sparse in sparseSynonymsEn:
                        if sparse in self.entities[key]["attributes"]:
                            return "sparse"
        return ""

    def _getAddOrReduceCommands(self):
        # 如果圈是内圈或者外圈，直接赋值；如果不是，则当成外圈
        addReduceCommands = set()
        for key in self.commands.keys():
            for add in addSynonymsEn:
                if add in key:
                    if self.innerCircle != None and self.innerCircle in self.commands[key]["targets"]:
                        addReduceCommands.add("add inner")
                    else:
                        addReduceCommands.add("add outer")
            for reduce in reduceSynonymsEn:
                if reduce in key:
                    if self.innerCircle != None and self.innerCircle in self.commands[key]["targets"]:
                        addReduceCommands.add("sub inner")
                    else:
                        addReduceCommands.add("sub outer")
        return list(addReduceCommands)

    def _checkNoEachTable(self):
        for key in self.noEntities.keys():
            for table in tableSynonymsEn:
                if table in key:
                    if not self._whetherBelongToInnerCircle(key, dict(list(self.entities.items())+list(self.noEntities.items()))):
                        return True
        return False

    def _modifyEntities(self):
        # TODO There are three circles of chairs outside and two circles of chairs inside. inside给chair的attribute
        ctcs = circleSynonymsEn + tableSynonymsEn + chairSynonymsEn
        for k in self.entities.keys():
            for ctc in ctcs:
                if ctc in k:
                    try:
                        positionWord = self.wordIndex[int(self.entities[k]["index"]) + 1]
                        if positionWord in extraHandlePositionWords:
                            if positionWord not in self.entities[k]["attributes"]:
                                self.entities[k]["attributes"] += positionWord + ","
                    except Exception as e:
                        pass

        positionWords = innerSynonymsEn + outerSynonymsEn + middleSynonymsEn
        for k in self.andEntities.keys():
            # 特判：对于conjAnd，with three chairs and a table in the middle.
            andWords = self.andEntities[k]
            for p in positionWords:
                if p not in self.entities[k]["attributes"]:
                    continue
                for aw in andWords:
                    if p not in self.entities[aw]["attributes"]:
                        self.entities[aw]["attributes"] += p + ","
            # 特判：对于conjAnd，The green chairs surrounded the four red leather sofas and two black chairs.
            for entityKey in self.entities.keys():
                if k in self.entities[entityKey]["relationships"]:
                    rs = self.entities[entityKey]["relationships"].split(",")
                    for r in rs:
                        if k in r:
                            prefix = r[0:r.index(":") + 1]
                            for aw in andWords:
                                if (prefix + aw) not in self.entities[entityKey]["relationships"]:
                                    self.entities[entityKey]["relationships"] += prefix + aw + ","
        # 对于attributes:ring-14
        for k in self.entities.keys():
            for andEntityKey in self.andEntities.keys():
                if andEntityKey in self.entities[k]["attributes"]:
                    for anotherEntityKey in self.andEntities[andEntityKey]:
                        if anotherEntityKey not in self.entities[k]["attributes"]:
                            self.entities[k]["attributes"] += anotherEntityKey+","
        # entity中chair和table如果有inside，outside或者middle这些attribute；
        # TODO 并且relationships有in:circle-xx，在circle-xx的attribute加上这些方位词
        circleEntities = []
        chairTableEntities = []
        for k in self.entities.keys():
            for cts in (chairSynonymsEn + tableSynonymsEn):
                if cts in k:
                    chairTableEntities.append(k)
            for cs in circleSynonymsEn:
                if cs in k:
                    circleEntities.append(k)
        for cte in chairTableEntities:
            for p in positionAttributeWords:
                if p in self.entities[cte]["attributes"]:
                    for ce in circleEntities:
                        if ("in:"+ce) in self.entities[cte]["relationships"] and p not in self.entities[ce]["attributes"]:
                            self.entities[ce]["attributes"] += p + ","
        # in the middle are 10 chairs in each circle.
        VBPEntity = ""
        for r in self.relationships:
            for middle in middleSynonymsEn:
                if middle in r[1][1]:
                    VBPEntity = r[1][0]
        if VBPEntity != "":
            for r in self.relationships:
                ek = r[1][1].split("~")[0]
                if "nsubj" == r[0] and VBPEntity == r[1][0] and ek in self.entities.keys():
                    self.entities[ek]["attributes"] += "middle,"

        # inside are 2 circles, each with 10 chairs.
        eachEntityKey = ""
        circleEntityKey = ""
        for r in self.relationships:
            for circle in circleSynonymsEn:
                if r[0] == "appos" and circle in r[1][0]:
                    for each in eachSynonymsEn:
                        if each in r[1][1]:
                            eachEntityKey = r[1][1].split("~")[0]
                            circleEntityKey = r[1][0]
        if eachEntityKey != "" and circleEntityKey != "":
            for r in self.relationships:
                ek = r[1][1].split("~")[0]
                if "nmod" in r[0] and r[1][0] == eachEntityKey and ek in self.entities.keys():
                    if circleEntityKey in self.entities.keys():
                        self.entities[circleEntityKey]["relationships"] += "each with:" + ek + ","

        printEntities(self.entities)

    def _extractConjAnd(self, conjAnd):
        # TODO Th
        conjAnd = []
        # TODO A, B and C (A around the center circle, the inner ring is five yellow chairs所以不能简单加逗号)
        conjAndAllowPosTags = ["CD","JJ","RB", "DT"]
        conjAndAllowWords = ["and", "of", "in"]
        # 只有table，circle，chair才能被算进NN
        ctcsWords = chairSynonymsEn + tableSynonymsEn + circleSynonymsEn
        for k in self.entities.keys():
            index = int(self.entities[k]["index"]) + 1
            while index < len(self.wordIndex):
                breakFlag = True
                for ctc in ctcsWords:
                    if ctc in k and "NN" in self.posTag[index]:
                        conjAnd.append([k, self.wordIndex[index] + "-" + str(index)])
                        breakFlag = False
                for tag in conjAndAllowPosTags:
                    if tag in self.posTag[index]:
                        breakFlag = False
                for word in conjAndAllowWords:
                    if self.wordIndex[index] == word:
                        breakFlag = False
                for p in positionAttributeWords:
                    if p in self.wordIndex[index]:
                        breakFlag = True
                if breakFlag:
                    break
                index += 1

        andEntites = obtainAndEntities(conjAnd, self.entities)
        print(andEntites)
        return andEntites

    def _handleInnerOuterCircleCommand(self, addReduceCommands, currentInnerCircleNum, currentOuterCircleNum, lastInnerCircleNum, lastOuterCircleNum):
        changeInnerCircleNum = currentInnerCircleNum
        changeOuterCircleNum = currentOuterCircleNum
        if changeOuterCircleNum == -1:
            changeOuterCircleNum = 0
        if changeInnerCircleNum == -1:
            changeInnerCircleNum = 0

        for command in addReduceCommands:
            if command == "add inner":
                currentInnerCircleNum = changeInnerCircleNum + lastInnerCircleNum
            elif command == "add outer":
                currentOuterCircleNum = changeOuterCircleNum + lastOuterCircleNum
            elif command == "sub inner":
                currentInnerCircleNum = lastInnerCircleNum - changeInnerCircleNum
                if currentInnerCircleNum < 0:
                    currentInnerCircleNum = lastInnerCircleNum
            elif command == "sub outer":
                currentOuterCircleNum = lastOuterCircleNum - changeOuterCircleNum
                if currentOuterCircleNum < 0:
                    currentOuterCircleNum = lastOuterCircleNum


        if currentInnerCircleNum == -1:
            currentInnerCircleNum = lastInnerCircleNum
        if currentOuterCircleNum == -1:
            currentOuterCircleNum = lastOuterCircleNum

        return currentInnerCircleNum, currentOuterCircleNum


    def decideTableAndChairColor(self):
        tableColor = ""
        innerChairColor = ""
        outerChairColor = ""
        for key in self.entities.keys():
            for table in tableSynonymsEn:
                if table in key:
                    if self._whetherBelongToInnerCircle(key, self.entities):
                        tableColor = self._decideEntityColor(key)
            for chair in chairSynonymsEn:
                if chair in key:
                    if self._whetherBelongToInnerCircle(key, self.entities):
                        innerChairColor = self._decideEntityColor(key)
                    else:
                        outerChairColor = self._decideEntityColor(key)
        return tableColor, innerChairColor, outerChairColor

    def _decideEntityColor(self, entityKey):
        for color in acceptableColorsEn:
            if color in self.entities[entityKey]["attributes"]:
                return color
            for key in self.entities.keys():
                if color in key:
                    if entityKey in self.entities[key]["attributes"]:
                        return color
        for key in self.entities.keys():
            for colorWord in colorSynonymsEn:
                if colorWord in key:
                    if ("of:" + entityKey) in self.entities[key]["relationships"]:
                        for color in acceptableColorsEn:
                            if color in self.entities[key]["attributes"]:
                                return color
        return ""

    # 没有提的话默认是没有的，即返回False
    # TODO 必须先调用circleNumber的方法
    def eachChairHasEachTable(self):
        if "桌" not in self.s_ch:
            return False
        tableEntities = {}
        # 如果有chair有has table的relationship，则直接返回True，反之亦然；或者table前面附近有each/every
        # ？如果所有entities附近都有关键词表示内圈（near word和relationship），则返回False
        # 存在桌子不在内圈
        # 以上都不满足，问chatGPT（一共有多少个椅子，有多少个桌子？）（T5太笨了……）
        for key in self.entities.keys():
            for cs in chairSynonymsEn:
                if cs in key:
                    for ts in tableSynonymsEn:
                        if "relationships" in self.entities[key].keys() and "has:"+ts in self.entities[key]["relationships"]:
                            return True
            for ts in tableSynonymsEn:
                if ts in key:
                    tableEntities[key] = self.entities[key]
                    haveSynonyms =["has","having","have"]
                    for cs in chairSynonymsEn:
                        for h in haveSynonyms:
                            if "relationships" in self.entities[key].keys() and h+":"+cs in self.entities[key]["relationships"]:
                                return True
                    index = int(self.entities[key]["index"])
                    if self._beforeWordExistWords(index, eachSynonymsEn):
                        return True
                    try:
                        if self.wordIndex[index+1] == "," and self.wordIndex[index+2] in eachSynonymsEn:
                            return True
                    except Exception as e:
                        pass
        # TODO：桌子和椅子围成好几圈
        for tk in tableEntities.keys():
            if not self._whetherBelongToInnerCircle(tk, self.entities):
                return True
        return False


    def _beforeWordExistWords(self, index, synonyms):
        currentIndex = index - 1
        while currentIndex > 0:
            for p in punctuations:
                if p in self.wordIndex[currentIndex]:
                    return False
            for s in synonyms:
                if s in self.wordIndex[currentIndex]:
                    return True
            currentIndex -= 1
        return False

    def _afterWordExistWords(self, index, synonyms):
        currentIndex = index + 1
        while currentIndex < len(self.wordIndex):
            for p in punctuations:
                if p in self.wordIndex[currentIndex]:
                    return False
            for s in synonyms:
                if s in self.wordIndex[currentIndex]:
                    return True
            currentIndex += 1
        return False

    # 依据临近单词和relationship;surround?
    def _whetherBelongToInnerCircle(self, entityKey, entites):
        innerAttributes = innerSynonymsEn + middleSynonymsEn + surroundAttributes
        for ia in innerAttributes:
            if ia in entites[entityKey]["attributes"] or ("on:"+ia+"-" in entites[entityKey]["relationships"] ):
                return True
        circleChairTableEntites = circleSynonymsEn + chairSynonymsEn + tableSynonymsEn
        for k in entites.keys():
            for cce in circleChairTableEntites:
                if cce in k:
                    relationships = entites[k]["relationships"].split(",")
                    for r in relationships:
                        if "surround" in r:
                            if "agent" not in r:
                                if entityKey in r:
                                    return True
                            elif k == entityKey:
                                return True
                        if "around" in r and entityKey in r:
                            return True
        objectAndWords = [entityKey]
        if entityKey in self.andEntities.keys():
            objectAndWords += self.andEntities[entityKey]
        for oaw in objectAndWords:
            currentIndex = int(oaw.split("-")[1])
            if "surrounded by" in " ".join(self.wordIndex[currentIndex:currentIndex+5]):
                return True

        if self.innerCircle:
            if self.innerCircle in entites[entityKey]["relationships"] or self.innerCircle in entites[entityKey]["attributes"]:
                return True
            if entityKey in entites[self.innerCircle]["relationships"]:
                return True

        return False


    # 如果只有一个circle，直接返回count
    # 如果有多个circle，则看所有给出count的，先看attribute；如果只有一个count，给外圈；最大给外圈，最小给内圈
    # -1只代表没说，不表示没有
    # TODO 内圈数量和下面的有无内圈冲突怎么办？
    def circleNumber(self):
        innerCircleNumber = -1
        outerCircleNumber = -1
        count = []
        for key in self.entities.keys():
            for cs in circleSynonymsEn:
                if cs in key:
                    countNumber = -1
                    # TODO 改成determiner为“a”？
                    if "a," == self.entities[key]["determiners"]:
                        countNumber = 1
                    if "count" in self.entities[key].keys():
                        try:
                            countNumber = convertWordsToNumber(self.entities[key]["count"])
                        except Exception as e:
                            pass

                    addFlag = True
                    # TODO 是有要relationships加上判断（当on the inside时）
                    for ins in (innerSynonymsEn + middleSynonymsEn):
                        if ins in self.entities[key]["attributes"] or ins in self.entities[key]["relationships"]:
                            if innerCircleNumber == -1 or (innerCircleNumber != -1 and innerCircleNumber > countNumber):
                                if countNumber != -1:
                                    innerCircleNumber = countNumber
                                self.innerCircle = key
                            addFlag = False
                    for os in outerSynonymsEn:
                        if os in self.entities[key]["attributes"] or os in self.entities[key]["relationships"]:
                            if countNumber != -1:
                                outerCircleNumber = countNumber
                            addFlag = False
                    if addFlag and countNumber != -1:
                        count.append([countNumber, key])
        if (outerCircleNumber != -1 and innerCircleNumber != -1):
            return innerCircleNumber, outerCircleNumber
        for nokey in self.noEntities.keys():
            for circleChair in circleSynonymsEn + chairSynonymsEn:
                if circleChair in nokey:
                    for inner in innerSynonymsEn:
                        if inner in self.noEntities[nokey]["attributes"] or inner in self.noEntities[nokey]["relationships"]:
                            innerCircleNumber = 0
                            self.innerCircleNumber = 0
        if len(count) == 0:
            return innerCircleNumber, outerCircleNumber
        count.sort(key = lambda x : x[0])
        if len(count) == 1 and outerCircleNumber == -1:
            outerCircleNumber = count[0][0]
            return innerCircleNumber, outerCircleNumber
        if outerCircleNumber == -1:
            outerCircleNumber = count[-1][0]

        # TODO 感觉此处不一定正确,是因为翻译是呈圆形这种会翻译成in a circle
        # 例如："There are five rows of chairs outside in a circle and three circles inside."
        for c, key in count:
            if 1 < c < count[-1][0] and innerCircleNumber == -1:
                innerCircleNumber = c
                self.innerCircle = key
                return innerCircleNumber, outerCircleNumber
        # TODO "There are five rows of chairs outside in a circle and one circle inside."
        # if innerCircleNumber == -1:
        #     innerCircleNumber = count[0][0]
        #     self.innerCircle = count[0][1]

        return innerCircleNumber, outerCircleNumber

    def _chairNumberForEach(self, key):
        # inside are 2 circles, each with 10 chairs.
        index = int(key.split("-")[1]) - 1
        if self.relationships[index][0] == "nmod:with":
            for each in eachSynonymsEn:
                if each in self.relationships[index][1][0]:
                    indexForEach = int(self.relationships[index][1][0].split("-")[1]) - 1
                    if self.relationships[indexForEach][0] == "appos":
                        for circle in circleSynonymsEn:
                            if circle in self.relationships[indexForEach][1][0]:
                                return True
        # each circle has 10 chairs.
        # on the outside, there are 10 chairs in each circle.
        for k in self.entities.keys():
            for circle in circleSynonymsEn:
                if circle in k:
                    for each in eachSynonymsEn:
                        if each in self.entities[k]["determiners"]:
                            if ("has:"+key) in self.entities[k]["relationships"]:
                                return True
                            if ("in:"+k) in self.entities[key]["relationships"]:
                                return True

        return False

    # TODO 请在计算circleNumber后调用此函数
    # 出现一个chair，问是否属于内圈？属于的话返回count
    # innerChairNumber为0时代表没有内圈，为-1时代表有但不知道数目，为正数时代表有和数目
    def chairInInnerCircle(self):
        innerChairNumber = 0
        if self.innerCircle != None:
            innerChairNumber = -1
        if self.innerCircleNumber == 0:
            return -2

        for k in self.entities.keys():
            for cs in chairSynonymsEn:
                if cs in k:
                    if self._whetherBelongToInnerCircle(k, self.entities):
                        if "count" in self.entities[k].keys():
                            try:
                                number = convertWordsToNumber(self.entities[k]["count"])
                                # number的话，看是否是each，如果是的，看innerCircleNumber，如果是-1则当1算，反之则正常算
                                if self._chairNumberForEach(k):
                                    if self.innerCircleNumber == 0:
                                        number = 0
                                    elif self.innerCircleNumber > 0:
                                        number = number * int(self.innerCircleNumber)
                                if number > innerChairNumber:
                                    innerChairNumber = number
                            except Exception as e:
                                if innerChairNumber == 0:
                                    innerChairNumber = -1
                        elif innerChairNumber == 0:
                            innerChairNumber = -1
            for ts in tableSynonymsEn:
                if ts in k and self._whetherBelongToInnerCircle(k, self.entities):
                    if innerChairNumber == 0:
                        innerChairNumber = -1

        # TODO -2直接代表说了没有内圈
        if self._checkInnerCircleNoEntities():
            innerChairNumber = -2

        return innerChairNumber

    def _checkBelongToAddOrReduceEntity(self, entityKey):
        addOrReduceCommands = addSynonymsEn + reduceSynonymsEn
        for commandKey in self.commands.keys():
            for command in addOrReduceCommands:
                if command in commandKey:
                    if entityKey in self.commands[commandKey]["targets"]:
                        return True
        return False

    def _decideOuterChairNumber(self):
        outerChairNumber = -1
        for k in self.entities.keys():
            for cs in chairSynonymsEn:
                if cs in k:
                    if not self._whetherBelongToInnerCircle(k, self.entities) and not self._checkBelongToAddOrReduceEntity(k):
                        # TODO 提到了椅子且说了数量，则不是外圈就是内圈，不是each就是一共
                        if "count" in self.entities[k].keys():
                            try:
                                number = convertWordsToNumber(self.entities[k]["count"])
                                if self._chairNumberForEach(k):
                                    if self.outerCircleNumber == -1:
                                        number = number * defaultOuterCircleNumber
                                    elif self.outerCircleNumber > 0:
                                        number = number * self.outerCircleNumber
                                if number > outerChairNumber:
                                    outerChairNumber = number
                            except Exception as e:
                                pass
        return outerChairNumber

    def _checkInnerCircleNoEntities(self):
        for ne in self.noEntities:
            for chair in chairSynonymsEn:
                if chair in ne:
                    if self._whetherBelongToInnerCircle(ne,dict(list(self.entities.items())+list(self.noEntities.items()))):
                        return True
        if self.innerCircle != None and self.innerCircle in self.noEntities.keys():
            return True
        return False

    def _decideDefaultPeopleNumber(self, innerChairNumber):
        innerPeople = innerChairNumber
        if innerChairNumber == -1:
            innerPeople = defaultInnerCircleChairNumber
        if self.outerCircleNumber > 0:
            outerPeople = 0
            outerAdd = 0
            for i in range(self.outerCircleNumber):
                outerPeople += defaultPeopleEachOuterCircle + outerAdd
                outerAdd += defaultPeopleEachOuterCircleAddStep
            return innerPeople + outerPeople

        return innerPeople + defaultOuterPeople

    # people_number 是所有的椅子，包括内圈和外圈
    # TODO 应该改成没有提就是-1，然后预设的值逻辑放到外面
    def _checkPeopleNumber(self, innerChairNumber, outerChairNumber):
        if self.people_number != -1:
            return self.people_number
        innerPeople = innerChairNumber
        outerPeople = outerChairNumber
        if innerChairNumber == -1:
            innerPeople = defaultInnerCircleChairNumber
        if outerChairNumber <= 5 and innerChairNumber != 0:
            outerPeople = -1

        print("inner people: ", innerPeople)

        lowestOuterPeople = -1
        largestOuterPeople = 10000
        if self.outerCircleNumber > 0:
            lowestAdd = 0
            largestAdd = 0
            lowestOuterPeople = 0
            largestOuterPeople = 0
            for i in range(self.outerCircleNumber):
                lowestOuterPeople += defaultLowestPeopleEachOuterCircle + lowestAdd
                lowestAdd += defaultLowestPeopleEachOuterCircleAddStep
                largestOuterPeople += defaultLargestPeopleEachOuterCircle + largestAdd
                largestAdd += defaultLargestPeopleEachOuterCircleAddStep
        if outerPeople < lowestOuterPeople or outerPeople > largestOuterPeople:
            outerPeople = -1

        if outerPeople != -1:
            return innerPeople + outerPeople

        return -1


