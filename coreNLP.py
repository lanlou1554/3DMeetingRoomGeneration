from stanfordcorenlp import StanfordCoreNLP
from translate import Translator
import os
nlp_ch = StanfordCoreNLP(r'D:\Downloads\stanford-corenlp-full-2018-01-31\stanford-corenlp-full-2018-01-31', lang='zh')
nlp_en = StanfordCoreNLP(r'D:\four1\HCI\task3\language-driven\NLP_release\stanford-corenlp-full-2016-10-31')

def dependency_parse_chinese(sentences):
    words = []
    dependencies = []
    if len(sentences) == 0:
        return words, dependencies
    sentences = sentences.replace(" ","")
    if sentences[-1] != "。":
        sentences += "。"
    sentence = sentences[:-1].replace("。","，") + "。"
    print("prcessing chinese document: " + sentence)

    words = list(nlp_ch.word_tokenize(sentence))
    arcs = list(nlp_ch.dependency_parse(sentence))
    arcs.sort(key=lambda x: x[2])
    words_temp = [w + "-" + str(idx) for idx, w in enumerate(words)]
    rely_id = [arc[1] for arc in arcs]
    relation = [arc[0] for arc in arcs]
    heads = ['Root' if id == 0 else words_temp[id - 1] for id in rely_id]
    for i in range(len(words_temp)):
        dependencies.append([relation[i], heads[i], words_temp[i]])
    print(dependencies)
    # TODO 不close，不然太慢了
    # nlp.close()  # Do not forget to close! The backend server will consume a lot memery.

    return words, dependencies

def dependency_parse_english(sentences):
    print("processing english document: " + sentences)
    res = ""
    sentences = sentences.replace(". ", ".").split(".")
    for s in sentences:
        if len(s) == 0:
            continue
        s += "."
        words = list(nlp_en.word_tokenize(s))
        poses = list(nlp_en.pos_tag(s))
        dependencies = list(nlp_en.dependency_parse(s))
        dependencies.sort(key=lambda x: x[2])
        print(dependencies)

        res += s + "#"

        for d in dependencies:
            govLabel = "ROOT"
            if d[1] > 0:
                govLabel = words[d[1]-1]
            res += d[0].lower() + "@" + str(d[1]) + "@" + govLabel + "@" + str(d[2]) + "@" + words[d[2]-1] + "@" + poses[d[2]-1][1] + "^"

        res += "|"
    print(res)
    return res





def translate(sentence):
    translator = Translator(from_lang="ZH", to_lang="EN-US")
    translation = translator.translate(sentence)
    return translation


if __name__=="__main__":
    # res = dependency_parse_english("The green chairs surrounded the four red leather sofas, and then there was a small table in the middle of the sofa.")
    # res = "nojava\n" + res
    s = "There are several layers of seats inside and outside, the ring is surrounded by a circle, there is no table but a chair, the spacing is different, more casual."
    res = "java\n" + s
    with open("in.txt", "w") as f:
        f.write(res)
    r_v = os.system("matt-SEL-playground.exe")
    print(r_v)
