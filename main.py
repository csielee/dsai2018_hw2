import argparse
import re
import pandas as pd
import time

def parseQuery(query):
    if query[-1] == '\n':
        query = query[:-1]
    words = query.split(" ")
    op = None
    queryWord = []
    for word in words:
        if (word == "and") or (word == "or") or (word == "not"):
            op = word
            continue
        queryWord.append(word)
    return [queryWord, op]

def splitKeyWordByRE(str,n):
    words = [re.findall(r"[\u4e00-\ufaff]{1}|[0-9]+|[a-zA-Z]+\'*[a-zA-Z]*", str, re.UNICODE)]        
    for i in range(2,n+1):
        words.append(re.findall(r"(?=([\u4e00-\ufaff]{%d}))" % (i), str, re.UNICODE))
    return words

def English(str):
    regex = r"[a-zA-Z]+\'*[a-z]*"
    matches = re.findall(regex, str, re.UNICODE)
    if matches:
        return True
    else:
        return False

class searchEngine:
    def __init__(self, n):
        self.dicts = []
        self.dictAll = dict()
        for i in range(n):
            self.dicts.append(dict())
    
    def put(self, n, word, index):
        if n >= len(self.dicts):
            return
        if word not in self.dicts[n]:
            self.dicts[n][word] = set([index])
        else:
            self.dicts[n][word].add(index)
    
    def putAll(self, word, index):
        if word not in self.dictAll:
            self.dictAll[word] = set([index])
        else:
            self.dictAll[word].add(index)
    
    def query(self, word):
        if English(word):
            return self.dicts[0].get(word, set())
        else:
            return self.dicts[len(word) - 1].get(word, set())
    
    def queryAll(self, word):
        return self.dictAll.get(word, set())

n_words = 3

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

    # TODO load source data, build search engine
    source = pd.read_csv(args.source, header=None)
    
    sourceData = source.iloc[:,1].values

    engine = searchEngine(n_words)
    for index, title in enumerate(sourceData):
        terms = splitKeyWordByRE(title,n_words)
        for i in range(n_words):
            for term in terms[i]:
                engine.putAll(term, index+1)
    
    # TODO compute query result
    with open(args.query, 'r') as queryfile:
        querys = queryfile.readlines()

    answer1 = []

    for query in querys:
        keywords, op = parseQuery(query)

        answer = engine.queryAll(keywords[0])
        for keyword in keywords[1:]:
            if op == "and":
                answer = answer & engine.queryAll(keyword)
            if op == "or":
                answer = answer | engine.queryAll(keyword)
            if op == "not":
                answer = answer - engine.queryAll(keyword)

        answer = list(answer)
        answer.sort()
        if len(answer) == 0:
            answer = '0'
        else:
            answer = ','.join(str(num) for num in answer)

        answer1.append(answer)
  
    # TODO output result
    with open(args.output, "w") as ouputfile:
        for i in range(len(answer1)):
            if i!=0:
                ouputfile.write('\n')
            ouputfile.write(answer1[i])