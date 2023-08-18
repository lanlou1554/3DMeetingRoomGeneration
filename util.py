all = {
        "one" : 1,
        "two" : 2,
        "three" : 3,
        "four" : 4,
        "five" : 5,
        "six" : 6,
        "seven" : 7,
        "eight" : 8,
        "nine" : 9,
        "ten" : 10,
        "eleven": 11,
        "twelve": 12,
        "thirteen": 13,
        "fourteen": 14,
        "fifteen": 15,
        "sixteen": 16,
        "seventeen": 17,
        "eighteen": 18,
        "nineteen": 19,
        "twenty" : 20,
        "thirty" : 30,
        "forty" : 40,
        "fifty" : 50,
        "sixty" : 60,
        "seventy" : 70,
        "eighty" : 80,
        "ninety" : 90,
        "hundred" : 100,
        "thousand" : 1000,
        "million" : 1000000,
        "billion" : 1000000000,
        "trillion" : 1000000000000,
        "quadrillion" : 1000000000000000,
        "quintillion" : 1000000000000000000,
        "sextillion" : 1000000000000000000000,
        "septillion" : 1000000000000000000000000,
        "octillion" : 1000000000000000000000000000,
        "nonillion" : 1000000000000000000000000000000
        };


spliter = {
        "thousand" : 1000,
        "million" : 1000000,
        "billion" : 1000000000,
        "trillion" : 1000000000000,
        "quadrillion" : 1000000000000000,
        "quintillion" : 1000000000000000000,
        "sextillion" : 1000000000000000000000,
        "septillion" : 1000000000000000000000000,
        "octillion" : 1000000000000000000000000000,
        "nonillion" : 1000000000000000000000000000000
        };

# 数字映射
number_map = {
    "零": 0,
    "一": 1,
    "二": 2,
    "两": 2,
    "三": 3,
    "四": 4,
    "五": 5,
    "六": 6,
    "七": 7,
    "八": 8,
    "九": 9
}

# 单位映射
unit_map = {
    "十": 10,
    "百": 100,
    "千": 1000,
    "万": 10000,
    "亿": 100000000
}

ChineseNumberWords = ["零", "一", "二", "三", "四", "五", "六", "七", "八", "九", "十", "百", "千", "两"]
allowNumberWordsCh = ["1","2","3","4","5","6","7","8","9","0","一","二","三","四","五","六","七","八","九","十","零","几","百"]

def judgeBelongToChineseNumbers(inputnumber):
    for s in inputnumber:
        if s not in ChineseNumberWords:
            return False
    return True


def convertWordsToNumber_Chinese(inputnumber):
    if len(inputnumber) == 0:
        return -1
    try:
        return int(inputnumber)
    except Exception as e:
        if "十几" in inputnumber:
            return 15
        if "几十" in inputnumber:
            return 20
        if "几百" in inputnumber:
            return 150
        if not judgeBelongToChineseNumbers(inputnumber):
            return -1
        if "十" == inputnumber:
            return 10
        output = 0
        num = 0
        for index, cn_num in enumerate(inputnumber):
            if cn_num in number_map:
                # 数字
                num = number_map[cn_num]
                # 最后的个位数字
                if index == len(inputnumber) - 1:
                    output = output + num
            elif cn_num in unit_map:
                # 单位
                unit = unit_map[cn_num]
                # 累加
                output = output + num * unit
                num = 0
            else:
                return -1

        return output


def convertWordsToNumber(inputnumber):
    try:
        return int(inputnumber)
    except Exception as e:
        try:
            inputnumber = inputnumber.lower()
            inputnumber = inputnumber.replace("-"," ")
            tokens = inputnumber.split(" ")

            result = 0
            partial_result = 0
            for index in range(len(tokens)):
                if tokens[index] in spliter:
                    if partial_result == 0:
                        partial_result = 1
                    partial_result *= all[tokens[index]]
                    result += partial_result
                    partial_result = 0
                else:
                    if tokens[index] == "hundred":
                        if partial_result == 0:
                            partial_result = 1
                        partial_result *= all[tokens[index]]

                    else:
                        partial_result += all[tokens[index]]


            result += partial_result
            return result
        except Exception as e:
            if "dozens" in inputnumber:
                return 20
            elif "hundreds" in inputnumber:
                return 150
            else:
                raise e


def solveTranslationProblem(s_ch):
    s_ch = s_ch.replace(" ", "")
    if s_ch[-1] != "。":
        s_ch += "。"
    s_ch = s_ch[:-1].replace("。", "，") + "。"

    # 为了解决翻译bug，处理人
    indexList = []
    for i, w in enumerate(s_ch):
        if s_ch[i] != '人':
            continue
        if i > 0:
            if s_ch[i-1] in allowNumberWordsCh:
                indexList.append([i,0])
        if i > 1:
            if s_ch[i-1] == '个' and s_ch[i-2] in allowNumberWordsCh:
                indexList.append([i,1])
    res = ""
    lastIndex = 0
    for index in indexList:
        res += s_ch[lastIndex:index[0]]
        lastIndex = index[0] + 1
        if index[1] == 0:
            res += "个人类"
        else:
            res += "人类"
    res += s_ch[lastIndex:]
    return res

if __name__=="__main__":
    print(convertWordsToNumber("thirty-five"))
    print(convertWordsToNumber_Chinese("一百二十三"))
    print(solveTranslationProblem("一共有20人，一共有30个人，你说呢"))