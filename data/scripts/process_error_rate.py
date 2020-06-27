from __future__ import division

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

def process(src_file,trg_file,src_out,trg_out,error_rate):
 arr=[]
 error_num=0
 sum_num=0
 with open(src_file,'r') as f1:
  with open(trg_file,'r') as f2:
   for l1,l2 in zip(f1,f2):
    l1=l1.strip()
    t1=l1.split(' ')
    l2=l2.strip()
    t2=l2.split(' ')
    re=levenshtein(t1,t2)
    error_num+=re
    sum_num+=len(t2)
    arr.append([l1,l2,re,len(t2),re/len(t2)])

   def itm(a):
    return a[4]

   arr=sorted(arr,key=itm)

   i=0
   for item in arr:
    if error_num/sum_num >= error_rate:
     break
    error_num-=item[2]
    sum_num-=item[3]
    i+=1

 with open(src_out,'w') as f1:
  with open(trg_out,'w') as f2:
   for item in arr[i:]:
    f1.write(item[0]+'\n')
    f2.write(item[1]+'\n')
    
import sys
if not len(sys.argv)==6:
 exit()
process(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4],float(sys.argv[5]))

