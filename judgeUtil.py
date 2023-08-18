from util import convertWordsToNumber

tableSynonymsEn = ["table", "desk"]
chairSynonymsEn = ["chair", "sofa", "stool", "seat"]
peopleSynonymsEn = ["people", "human"]
roomSynonymsEn = ["room","auditorium"]
numberSynonymsEn = ["number"]
addSynonymsEn = ["add", "increas"]
reduceSynonymsEn = ["reduc", "lower", "delet", "remov"]
colorSynonymsEn = ["color"]
denseSynonymsEn = ["dense"]
sparseSynonymsEn = ["sparse"]

acceptableColorsEn = ["white", "black", "blue", "yellow"]
acceptableStylesCh = {"简约现代":["简约","现代","明亮","干净","简洁"],"传统经典":["传统","经典","古典","稳重","庄重","沉稳"]}

punctuations = [",",".","?","!"]

def modifyCommands(commands, relationships):
    # 确保commands都有attributes和targets
    for key in commands.keys():
        if "attributes" not in commands[key].keys():
            commands[key]["attributes"] = ""
        if "targets" not in commands[key].keys():
            commands[key]["targets"] = ""
        if "number" not in commands[key].keys():
            commands[key]["number"] = ""

    # 处理VBP
    for r in relationships:
        if "dobj" in r[0]:
            if r[1][0] in commands.keys():
                entityKey = r[1][1].split("~")[0]
                if ("dobj:"+ entityKey) not in commands[r[1][0]]["targets"]:
                    commands[r[1][0]]["targets"] += ("dobj:"+ entityKey + ",")
        if "nmod:by" in r[0]:
            if r[1][0] in commands.keys():
                try:
                    commands[r[1][0]]["number"] = convertWordsToNumber(r[1][1].split("-")[0])
                except Exception as e:
                    pass
    print("commands: ", commands)
    return commands


def indexToWord(s_en):
    for p in punctuations:
        s_en = s_en.replace(p, " " + p)
    tempRes = s_en.split(" ")
    res = [""]
    for r in tempRes:
        if len(r) > 0:
            res.append(r)
    return res

def decideStyle(s_ch):
    style = ""
    countdict = {}
    for key in acceptableStylesCh.keys():
        countdict[key] = 0
        for word in acceptableStylesCh[key]:
            if word in s_ch:
                countdict[key] += 1
    maxCount = 0
    for key in countdict:
        if countdict[key] > maxCount:
            style = key
            maxCount = countdict[key]
    return style

def obtainAndEntities(conjAnd, entities):
    andEntites = {}
    for first, second in conjAnd:
        if first not in entities.keys() or second not in entities.keys():
            continue
        if first in andEntites.keys():
            andEntites[first].add(second)
        else:
            andEntites[first] = {second}
        if second in andEntites.keys():
            andEntites[second].add(first)
        else:
            andEntites[second] = {first}
    return andEntites

def extractEntities(sentences, wordIndex):
    #TODO 同一实体合并（看determiner，但是determiner不大准，例如those）
    entities = {}
    noEntities = {}
    for s in sentences:
        for es in s:
            if "determiners" not in es.keys():
                es["determiners"] = ""
            if "relationships" not in es.keys():
                es["relationships"] = ""
            if "attributes" not in es.keys():
                es["attributes"] = ""
            if wordIndex[int(es["index"])-1] == "a" and "a," not in es["determiners"]:
                es["determiners"] = "a,"
            if "count" not in es.keys():
                if "dozens" in es["determiners"]:
                    es["count"] = "dozens"
                elif "hundreds" in es["determiners"]:
                    es["count"] = "hundreds"
            if "non-existent" in es["determiners"]:
                noEntities[es["name"] + "-" + es["index"]] = es
            else:
                entities[es["name"]+"-"+es["index"]] = es

    return entities, noEntities

def printEntities(entities):
    for k in entities.keys():
        print(k)
        print("   " + "attributes:" + entities[k]["attributes"])
        print("   " + "determiners:" + entities[k]["determiners"])
        print("   " + "relationships:" + entities[k]["relationships"])
        if "count" in entities[k].keys():
            print("   " + "count:" + entities[k]["count"])
        print()

def getCountFromEntities(entities, relationships, k):
    count = -1
    if "count" in entities[k].keys():
        try:
            count = convertWordsToNumber(entities[k]["count"])
        except Exception as e:
            pass
    else:
        for subK in entities.keys():
            for number in numberSynonymsEn:
                if number in subK and k in entities[subK]["relationships"]:
                    for r in relationships:
                        if r[0] == "nsubj" and subK in r[1][1]:
                            try:
                                count = convertWordsToNumber(r[1][0].split("-")[0])
                            except Exception as e:
                                pass
    if "attributes" in entities[k].keys() and entities[k]["attributes"] != "":
        for attribute in entities[k]["attributes"].split(","):
            try:
                count = convertWordsToNumber(attribute)
            except Exception as e:
                pass
    return count

# there are 20 people.
# there are a total of 20 people.
# there are 20 people in total.
# the (total) number of people is 20.
def checkBelongToSpecificSituation(wordsIndex, index):
    beforeIndex = index
    while beforeIndex > 1:
        if wordsIndex[beforeIndex] not in punctuations:
            beforeIndex -= 1
        else:
            break
    if wordsIndex[beforeIndex] in punctuations:
        beforeIndex += 1
    afterIndex = index
    while afterIndex < len(wordsIndex):
        if wordsIndex[afterIndex] not in punctuations:
            afterIndex += 1
        else:
            break
    if wordsIndex[afterIndex-2]+" "+wordsIndex[afterIndex-1] == "in total":
        afterIndex = afterIndex - 2
    if wordsIndex[beforeIndex] == "there":
        if index == (afterIndex - 1):
            return True
    if wordsIndex[beforeIndex] == "the" and (wordsIndex[beforeIndex+1] == "number" or wordsIndex[beforeIndex+2] == "number"):
        try:
            count = convertWordsToNumber(wordsIndex[afterIndex-1])
            return True
        except Exception as e:
            pass
    return False

# TODO 现在只考虑，add和remove后面一定跟的是总人数的加减
def calculateChangePeopleNum(currentPoepleNum, commands, entities, relationships):
    chairPeopleSynonymsEn = chairSynonymsEn + peopleSynonymsEn
    # add 15 people
    for commandKey in commands.keys():
        addEntityKey = ""
        for add in addSynonymsEn:
            if add in commandKey:
                for entityKey in entities.keys():
                    for cp in chairPeopleSynonymsEn:
                        if cp in entityKey:
                            if "dobj:"+entityKey in commands[commandKey]["targets"]:
                                addEntityKey = entityKey
        if addEntityKey != "":
            count = getCountFromEntities(entities,relationships,addEntityKey)
            if count > 0:
                return count
        subEntityKey = ""
        for reduce in reduceSynonymsEn:
            if reduce in commandKey:
                for entityKey in entities.keys():
                    for cp in chairPeopleSynonymsEn:
                        if cp in entityKey:
                            if "dobj:"+entityKey in commands[commandKey]["targets"]:
                                subEntityKey = entityKey
        if subEntityKey != "":
            count = getCountFromEntities(entities,relationships,subEntityKey)
            if count > 0:
                if (currentPoepleNum - count) > 0:
                    return -count

    # add a circle of chairs to the outer circle, increase the number of humans by 15.
    for commandKey in commands.keys():
        count = 0
        if commands[commandKey]["number"] != "":
            for entityKey in entities.keys():
                for number in numberSynonymsEn:
                    if number in entityKey:
                        if entityKey in commands[commandKey]["targets"]:
                            for cp in chairPeopleSynonymsEn:
                                if ("of:" + cp) in entities[entityKey]["relationships"]:
                                    try:
                                        count = int(commands[commandKey]["number"])
                                    except Exception as e:
                                        pass
        if count > 0:
            for add in addSynonymsEn:
                if add in commandKey:
                    return count
            for reduce in reduceSynonymsEn:
                if reduce in commandKey:
                    if (currentPoepleNum - count) > 0:
                        return -count
    return 0


def extractPeopleNumber(wordsIndex, entities, relationships):
    chairPeopleSynonymsEn = chairSynonymsEn + peopleSynonymsEn
    count = -1
    for k in entities.keys():
        for cp in chairPeopleSynonymsEn:
            if cp in k:
                for r in roomSynonymsEn:
                    if "in:" + r in entities[k]["relationships"]:
                        count = getCountFromEntities(entities, relationships, k)
                        if count != -1:
                            return count
                for subK in entities.keys():
                    for r in roomSynonymsEn:
                        if r in subK:
                            if "accommodate:" + k in entities[subK]["relationships"] or "with:" + k in entities[subK]["relationships"]:
                                count = getCountFromEntities(entities, relationships, k)
                                if count != -1:
                                    return count
                if checkBelongToSpecificSituation(wordsIndex, int(k.split("-")[1])):
                    count = getCountFromEntities(entities, relationships, k)
                    if count != -1:
                        return count
    for key in entities.keys():
        for room in roomSynonymsEn:
            if room in key:
                for key2 in entities.keys():
                    for cp in chairPeopleSynonymsEn:
                        if cp in key2:
                            if "for:" + key2 in entities[key]["relationships"]:
                                count = getCountFromEntities(entities,relationships,key2)
                                if count != -1:
                                    return count
                for human in peopleSynonymsEn:
                    if human in entities[key]["attributes"]:
                        count = getCountFromEntities(entities,relationships,key)
                        if count != -1:
                            return count
                if "attributes" in entities[key].keys() and entities[key]["attributes"] != "":
                    for attribute in entities[key]["attributes"].split(","):
                        try:
                            count = convertWordsToNumber(attribute)
                        except Exception as e:
                            pass


    return count
