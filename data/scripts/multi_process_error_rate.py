import argparse
import multiprocessing

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

def thread_main(src,trg,i,d):
    error_num=0
    sum_num=0
    arr=[]
    for l1,l2 in zip(src,trg):
       r=levenshtein(l1.split(),l2.split())
       arr.append([l1,l2,r,len(l2.split()),r/len(l2.split())])
    d[i]=arr
   
def main(args):
    src=[]
    trg=[]

    with open(args.si,'r') as f1:
     with open(args.ti,'r') as f2:
      for l1,l2 in zip(f1,f2):
       l1=l1.strip()
       src.append(l1)
       l2=l2.strip()
       trg.append(l2)

    mgr = multiprocessing.Manager()
    d = mgr.dict()
    num=len(src)//args.c
    threads=[]
    for i in range(args.c):
       if i==args.c-1:
        threads.append(multiprocessing.Process(target=thread_main,args=(src[num*i:],trg[num*i:],i,d)))
       else:
        threads.append(multiprocessing.Process(target=thread_main,args=(src[num*i:num*(i+1)],trg[num*i:num*(i+1)],i,d)))
       threads[-1].start()

    for t in threads:
     t.join()
    
    arr=[]
    for i in range(args.c):
     arr.extend(d[i])

    def itm(a):
     return a[4]

    arr=sorted(arr,key=itm)

    error_num=0
    sum_num=0
    for a in arr:
     error_num+=int(a[2])
     sum_num+=int(a[3])

    i=0
    for item in arr:
     if error_num/sum_num >= args.er:
      break
     error_num-=item[2]
     sum_num-=item[3]
     i+=1

    with open(args.so,'w') as f1:
     with open(args.to,'w') as f2:
      for item in arr[i:]:
       f1.write(item[0]+'\n')
       f2.write(item[1]+'\n')
 
if __name__ == "__main__":
    # Define and parse program input
    parser = argparse.ArgumentParser()
    parser.add_argument("-si", help="The path to an input m2 file.",required=True)
    parser.add_argument("-so", help="The path to an input m2 file.",required=True)
    parser.add_argument("-ti", help="The path to an input m2 file.",required=True)
    parser.add_argument("-to", help="The path to an input m2 file.",required=True)
    parser.add_argument("-er", help="The path to an input m2 file.",required=True,type=float)
    parser.add_argument("-c", help="A path to where we save the output same text file.", type=int,default=1)
    args = parser.parse_args()
    main(args)
