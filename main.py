import jieba
import argparse
import pandas as pd
import json
import codecs

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
    jieba.set_dictionary('./dict.txt.big.txt')
    jieba.initialize()

    # TODO load source data, build search engine
    source = pd.read_csv(args.source, header=None)
    querylist = pd.read_csv(args.query, header=None)

    engine = dict()
    for index,row in source.iterrows():
        #print(row[0])
        title = row[1]
        #terms = jieba.cut(title)
        terms = jieba.cut_for_search(title)
        #print(", ".join(terms))
        for term in terms:
            #print(term)
            if engine.get(term) == None:
                engine[term] = set()
            engine[term].add(row[0])
        
    
    print('build engine finish')
    # TODO compute query result
    

  
    # TODO output result
    ouputfile = open(args.output, "w")

    for index,row in querylist.iterrows():
        querys, op = parseQuery(row[0])
        #print('query : ', querys)
        #print('op : ', op)
        answer = None
        for i in querys:
            if answer == None:
                answer = engine.get(i, set())
            else:
                if op == "and":
                    answer = answer & engine.get(i, set())
                if op == "or":
                    answer = answer | engine.get(i, set())
                if op == "not":
                    answer = answer - engine.get(i, set())
        
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

    print('query finish')