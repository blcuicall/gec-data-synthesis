import argparse
import multiprocessing

global shit
shit=[[] for _ in range(100)]

def levenshtein(str1,str2):
 temp=[[i+j for i in range(len(str2)+1)] for j in range(len(str1)+1)]
 for i in range(1,len(str1)+1):
  for j in range(1,len(str2)+1):
   if str1[i-1] == str2[j-1]:
    d=0
   else:
    d=1
   temp[i][j]=min(temp[i-1][j]+1,temp[i][j-1]+1,temp[i-1][j-1]+d)
 return temp[-1][-1]

def thread_main(src,trg,i,lock):
    error_num=0
    sum_num=0
    for l1,l2 in zip(src,trg):
       r=levenshtein(l1.split(),l2.split())
       error_num+=r
       sum_num+=len(l2.split())
    with open("temp.%d"%i,'w') as f:
     f.write('%d %d'%(error_num,sum_num))
 
def main(args):
    src=[]
    trg=[]
    
    with open(args.s,'r') as f1:
     with open(args.t,'r') as f2:
      for l1,l2 in zip(f1,f2):
       l1=l1.strip()
       src.append(l1)
       l2=l2.strip()
       trg.append(l2)
    
    lock=multiprocessing.Lock()
    num=len(src)//args.c
    threads=[]
    for i in range(args.c):
       if i==args.c-1:
        threads.append(multiprocessing.Process(target=thread_main,args=(src[num*i:],trg[num*i:],i,lock)))
       else:
        threads.append(multiprocessing.Process(target=thread_main,args=(src[num*i:num*(i+1)],trg[num*i:num*(i+1)],i,lock)))
       threads[-1].start()
    
    for t in threads:
     t.join()
    a=0
    b=0
    import os
    for i in range(args.c):
     with open('temp.%d'%i,'r') as f:
      l=f.readline()
      l=l.split()
     os.remove('temp.%d'%i)
     a+=int(l[0])
     b+=int(l[1])
    print(a,b,a/b)

if __name__ == "__main__":
    # Define and parse program input
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", help="The path to an input m2 file.",required=True)
    parser.add_argument("-t", help="The path to an input m2 file.",required=True)
    parser.add_argument("-c", help="A path to where we save the output same text file.", type=int,default=1)
    args = parser.parse_args()
    main(args)
