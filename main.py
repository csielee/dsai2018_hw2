#import jieba
import argparse
import pandas as pd
import json
import codecs
import re
import time

def parseQuery(query):
    words = query.split(" ")
    op = None
    queryWord = []
    for word in words:
        if (word == "and") or (word == "or") or (word == "not"):
            op = word
            continue
        queryWord.append(word)
    
    return [queryWord, op]

def English(str):
    regex = r"[a-zA-Z]+\'*[a-z]*"
    matches = re.findall(regex, str, re.UNICODE)
    if matches:
        return True
    else:
        return False

def spliteKeyWord(str):
    regex = r"[\u4e00-\ufaff]|[0-9]+|[a-zA-Z]+\'*[a-z]*|[^0-9]"
    matches = re.findall(regex, str, re.UNICODE)
    return matches



if __name__ == '__main__':
    # You should not modify this part.

    parser = argparse.ArgumentParser()
    parser.add_argument('--source',
                       default='source.csv',
                       help='input source data file name')
    parser.add_argument('--query',
                        default='query.txt',
                        help='query file name')
    parser.add_argument('--output',
                        default='output.txt',
                        help='output file name')
    args = parser.parse_args()
    
    # Please implement your algorithm below
    
    # init
    #jieba.set_dictionary('./dict.txt.big.txt')
    #jieba.initialize()

    # TODO load source data, build search engine
    source = pd.read_csv(args.source, header=None)
    source = source.iloc[:,1].values

    start_time = time.time()
    engine = [dict(), dict(), dict()]
    for index,title in enumerate(source):
        #print(row[0])
        #title = row[1]
        #terms = jieba.cut(title)
        #terms = jieba.cut_for_search(title)
        

        #terms = list()
        words = spliteKeyWord(title)

        for j in range(1,4):
            for i in range(0,len(words) - j + 1):
                term = ''.join(words[i:i+j])
                if term not in engine[j-1]:
                    engine[j-1][term] = set()
                engine[j-1][term].add(index+1)

    
    print("build engine finish for %s sec" % (time.time() - start_time))
    
    #with open('dictlist.txt','w') as dictfile:
    #    for i in range(0,3):
    #        for key in engine[i]:
    #            dictfile.write(key)
    #            dictfile.write('\n')
    
    
    # TODO compute query result
    

  
    # TODO output result
    start_time = time.time()
    ouputfile = open(args.output, "w")
    querylist = pd.read_csv(args.query, header=None)

    for index,row in querylist.iterrows():
        querys, op = parseQuery(row[0])
        #print('query : ', querys)
        #print('op : ', op)
        answer = None
        for i in querys:
            if English(i):
                engine_index = 0
            else:
                engine_index = len(i) - 1

            if answer == None:
                answer = engine[engine_index].get(i, set())
            else:
                if op == "and":
                    answer = answer & engine[engine_index].get(i, set())
                if op == "or":
                    answer = answer | engine[engine_index].get(i, set())
                if op == "not":
                    answer = answer - engine[engine_index].get(i, set())
        
        #print(answer)
        answer = list(answer)
        answer.sort()
        #print(answer)
        if len(answer) == 0:
            answer = "0"
        else:
            answer = ",".join(str(num) for num in answer)

        if index != 0:
            ouputfile.write('\n')
        ouputfile.write(answer)
    
    ouputfile.close()

    print("query finish for %s sec" % (time.time() - start_time))