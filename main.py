LOW_ATT_LIST=[
    "i", "me", "my", "myself", "we", "our","ours", "ourselves", "you", "your", "yours","yourself", "yourselves", "he", "him", "his","himself", "she", "her", "hers", "herself","it", "its",
    "itself", "they", "them", "their","theirs", "themselves", "what", "which", "who","whom", "this", "that", "these", "those", "am","is", "are", "was", "were", "be", "been", "being",
    "have", "has", "had", "having", "do", "does","did", "doing", "a", "an", "the", "and", "but","if", "or", "because", "as", "until", "while","of", "at", "by", "for", "with", "about", "against",
    "between", "into", "through", "during", "before","after", "above", "below", "to", "from", "up","down", "in", "out", "on", "off", "over", "under","again", "further", "then", "once", "here", "there",
    "when", "where", "why", "how", "all", "any", "both","each", "few", "more", "most", "other", "some","such", "no", "nor", "not", "only", "own", "same","so", "than", "too", "very", "s", "t", "can", "will",
    "just", "don", "should", "now"
]
DEFAULT_QUA=4

def att_pt(sen:list,qua:int=DEFAULT_QUA):
    same_list=same_word(sen=sen,qua=qua)
    pt = []
    down = [round(100 / ((i + 1) ** 1.2), qua) for i in range(len(sen))]
    for i in range(1, len(sen) + 1):
        pt.append([round(j / sum(down[i - 1::-1]) * (sen[:i].count(sen[i - 1]) ** 2), qua) for j in down[i - 1::-1]])
    temp = []
    for i in range(len(pt)):
        if sen[i] not in LOW_ATT_LIST:
            temp.append(round((sum([pt[j][i] for j in range(i, len(pt))])), qua))
        else:
            temp.append(round((sum([pt[j][i] for j in range(i, len(pt))])**-sum([pt[j][i] for j in range(i, len(pt))])), qua))
    temp_copy=temp.copy()
    for n in same_list:
        t=[]
        for name,j in same_list[n]:
            value=0
            idx = [i for i, x in enumerate(sen) if x == name]
            for k in idx:
                value+=temp_copy[k]
            t.append(round(value*j,qua))
        idx = [i for i, x in enumerate(sen) if x == n]
        for k in idx:
            temp[k]=round(temp[k]+sum(t),qua)
    return [round(i / sum(temp), qua) for i in temp]

def same_word(sen:list,kill_line:float=0,qua:int=DEFAULT_QUA):
    sen=list(set(sen))
    temp={i:list() for i in sen}
    for i in sen:
        for j in sen:
            if i!=j:
                same_value=int(len(i)-len(j) if len(j)>len(i) else len(j)-len(i))
                for k in range(len(j) if len(i)>len(j) else len(i)):
                    if i[k]==j[k]:
                        same_value+=1
                    else:
                        same_value-=round(abs(same_value)/(k+1),qua)
                score=round(same_value / max(len(i), len(j)), qua)
                if score>kill_line:
                    temp[i].append([j,score])
    pt={}
    for i,j in temp.items():
        if j!=[]:
            pt[i]=j
    return pt

if __name__ == '__main__':
    sen='The Matthew effect sometimes called the Matthew principle' \
        ' or cumulative advantage is the tendency of individuals ' \
        'to accrue social or economic success in proportion to their ' \
        'initial level of popularity friends and wealth It is sometimes ' \
        'summarized by the adage or platitude the rich get richer and ' \
        'the poor get poorer'.lower().split()
    print(att_pt(sen))