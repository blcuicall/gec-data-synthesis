import argparse
typedict={'ADJ':1, 'ADJ:FORM':2, 'ADV':3, 'CONJ':4, 'CONTR':5, 'DET':6,
          'MORPH':7, 'NOUN':8, 'NOUN:INFL':9, 'NOUN:NUM':10, 'NOUN:POSS':11,
          'ORTH':12, 'OTHER':13, 'PART':14, 'PREP':15, 'PRON':16, 'PUNCT':17,
          'SPELL':18, 'UNK':19 ,'VERB':20, 'VERB:FORM':21, 'VERB:INFL':22, 
          'VERB:SVA':23, 'VERB:TENSE':24, 'WO':25}

def readm2(m2):
    re=[]
    temp=[]
    with open(m2,'r',errors="ignore") as f:
        for line in f:
            line=line.strip()
            if len(line)==0 and len(temp) != 0:
                re.append(temp)
                temp=[]
                continue
            temp.append(line)
    return re

def count(m2,mode=1):
    re=[]
    for m in m2:
        temp=[0 for _ in range((3 if mode==1 else 25)+1)]
        temp.append(len(m[0][2:].strip().split()))
        for line in m[1:]:
            line=line.split('|||')
            t=line[1][0]#MUR
            Type=line[1][2:]#ADJ VERB
            n=line[0].split()
            n=int(n[2])-int(n[1])#待修改token数
            nn = 1 if line[2].strip().find(' ') == -1 else len(line[2].strip().split())#修改后token数
            if t=='M':
                if mode==1:
                   temp[0]+=nn
                elif mode==2:
                   if Type in typedict:
                      temp[typedict[Type]-1]+=nn
                   else:
                      print(line)
                temp[-1]+=nn
            elif t=='U':
                if mode==1:
                   temp[1]+=n
                elif mode==2:
                   if Type in typedict:
                      temp[typedict[Type]-1]+=n
                   else:
                      print(line)
                temp[-1]-=n
            elif t=='R':
                if mode==1:
                   temp[2]+=min(n,nn)
                   if nn>n:
                      temp[0]+=(nn-n)
                   elif nn<n:
                      temp[1]+=(n-nn)
                elif mode==2:
                   if Type in typedict:
                      temp[typedict[Type]-1]+=max(n,nn)
                   else:
                      print(line)
                temp[-1]+=(nn-n)
            for tt in temp[:-2]:#all error num
                temp[-2]+=tt
        re.append(temp)#temp=[each type num, all error num, target sen num]
    return re

def main(args):
    #gold = [2, 2, 1, 2, 2, 1, 1, 1, 2, 1, 2, 1, 1, 2, 1, 2, 1, 1, 2, 1, 1, 2, 1, 1, 1]
    gold = [1, 1, 1]
    threshold = 0.05

    #读取m2文件
    m2=readm2(args.i)

    #统计所有信息
    t=count(m2,args.mode)
    array=[]
    for a,b in zip(m2,t):
        temp=[a]
        temp.extend(b[i] for i in range((3 if args.mode==1 else 25) +2))
        array.append(temp)

    #排序
    def mycmp(a,b):
        if a[-2]/a[-1] < b[-2]/b[-1]:
            return -1
        elif a[-2]/a[-1] > b[-2]/b[-1]:
            return 1
        return 0
    def cmp_to_key(mycmp):
         'Convert a cmp= function into a key= function'
         class K(object):
            def __init__(self, obj, *args):
                self.obj = obj
            def __lt__(self, other):
                return mycmp(self.obj, other.obj) < 0
            def __gt__(self, other):
                return mycmp(self.obj, other.obj) > 0
            def __eq__(self, other):
                return mycmp(self.obj, other.obj) == 0
            def __le__(self, other):
                return mycmp(self.obj, other.obj) <= 0
            def __ge__(self, other):
                return mycmp(self.obj, other.obj) >= 0
            def __ne__(self, other):
                return mycmp(self.obj, other.obj) != 0
         return K

    array=sorted(array,key=cmp_to_key(mycmp))

    #统计每种错误的总和
    etnum=[0 for _ in range((3 if args.mode==1 else 25)+1)]# M U R TargetLength
    for temp in array:
        for i,et in enumerate(temp[1:-2]):
            etnum[i]+=et
        etnum[-1]+=temp[-1]

    print("Type : ",end='')
    print(etnum[:-1])
    sum_=0
    for et in etnum[:-1]:
        sum_ += et
    for et in etnum[:-1]:
        print("%f%%"%(100*et/sum_))
    print()
    print("error rate : %f" % (sum_/etnum[-1]))

    #找单位一
    tempg=999999
    tempn=999999
    for i,g in enumerate(gold):
        if tempg>g:
            tempn=etnum[i]
            tempg=g
        elif tempg==g:
            if etnum[i]<tempn:
                tempn=etnum[i]
                tempg=g
    goldnum=tempn/tempg if tempn>0 else exit()
    print(goldnum)

    #删语料
    remain=len(array)
    result=[]
    for j,temp in enumerate(array):
        b=True
        for i,et in enumerate(temp[1:-2]):
            if et!=0:
                if etnum[i]-et<gold[i]*goldnum*(1-threshold):
                    b=False
                    break
        #删除
        if b:
            for i,et in enumerate(temp[1:-2]):
                etnum[i]-=et
            etnum[-1]-=temp[-1]
            remain-=1
        else:
            result.append(array[j])
            
        #判断所有
        b=True
        if args.n<0 or remain>=args.n:
          for i,e in enumerate(etnum[:-1]):
            if e>goldnum*gold[i]*(1+threshold):
                b=False
                break
        if b:
            for ttemp in array[j+1:]:
                result.append(ttemp)
            break

    print("Type : ", end='')
    print(etnum[:-1])
    sum_ = 0
    for et in etnum[:-1]:
        sum_ += et
    for et in etnum[:-1]:
        print("%f%%"%(100*et/sum_))
    print()
    print("error rate : %f" % (sum_ / etnum[-1]))

    with open(args.o,'w') as f:
     for a in result:
      for line in a[0]:
       f.write(line+'\n')
      f.write('\n')

if __name__ == "__main__":
    # Define and parse program input
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", help="The path to an input m2 file.")
    parser.add_argument("-o", help="The path to an input m2 file.")
    parser.add_argument("-n", help="The path to an input m2 file.",default=-1,type=int)
    parser.add_argument("-mode", help="A path to where we save the output same text file.", default=1,type=int)
    #parser.add_argument("-o", help="A path to where we save the output same text file.", required=True)
    args = parser.parse_args()
    main(args)

