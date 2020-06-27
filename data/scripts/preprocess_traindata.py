from __future__ import division

commoncharacter=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','!','$','%','&','(',')','\'','\"','.',',','?','+','=','-','*','/','0','1','2','3','4','5','6','7','8','9',':',';','#','{','}','[',']','<','>','|','_','\\','^','@','~']
special=['`']
specialcharacter={"\xef\xbc\xa1" : 'A',
    "\xef\xbc\xa2" : 'B',
    "\xef\xbc\xa3" : 'C',
    "\xef\xbc\xa4" : 'D',
    "\xef\xbc\xa5" : 'E',
    "\xef\xbc\xa6" : 'F',
    "\xef\xbc\xa7" : 'G',
    "\xef\xbc\xa8" : 'H',
    "\xef\xbc\xa9" : 'I',
    "\xef\xbc\xaa" : 'J',
    "\xef\xbc\xab" : 'K',
    "\xef\xbc\xac" : 'L',
    "\xef\xbc\xad" : 'M',
    "\xef\xbc\xae" : 'N',
    "\xef\xbc\xaf" : 'O',
    "\xef\xbc\xb0" : 'P',
    "\xef\xbc\xb1" : 'Q',
    "\xef\xbc\xb2" : 'R',
    "\xef\xbc\xb3" : 'S',
    "\xef\xbc\xb4" : 'T',
    "\xef\xbc\xb5" : 'U',
    "\xef\xbc\xb6" : 'V',
    "\xef\xbc\xb7" : 'W',
    "\xef\xbc\xb8" : 'X',
    "\xef\xbc\xb9" : 'Y',
    "\xef\xbc\xba" : 'Z',
    "\xef\xbd\x81" : 'a',
    "\xef\xbd\x82" : 'b',
    "\xef\xbd\x83" : 'c',
    "\xef\xbd\x84" : 'd',
    "\xef\xbd\x85" : 'e',
    "\xef\xbd\x86" : 'f',
    "\xef\xbd\x87" : 'g',
    "\xef\xbd\x88" : 'h',
    "\xef\xbd\x89" : 'i',
    "\xef\xbd\x8a" : 'j',
    "\xef\xbd\x8b" : 'k',
    "\xef\xbd\x8c" : 'l',
    "\xef\xbd\x8d" : 'm',
    "\xef\xbd\x8e" : 'n',
    "\xef\xbd\x8f" : 'o',
    "\xef\xbd\x90" : 'p',
    "\xef\xbd\x91" : 'q',
    "\xef\xbd\x92" : 'r',
    "\xef\xbd\x93" : 's',
    "\xef\xbd\x94" : 't',
    "\xef\xbd\x95" : 'u',
    "\xef\xbd\x96" : 'v',
    "\xef\xbd\x97" : 'w',
    "\xef\xbd\x98" : 'x',
    "\xef\xbd\x99" : 'y',
    "\xef\xbd\x9a" : 'z'}
specialsymbol={"\xef\xb9\x9e" : ')',
     "\xef\xb9\x9d" : '(',
     "\xef\xbd\x9d" : '}',
     "\xef\xb9\x90" : ',',
     "\xef\xbd\x80" : '\'',
     "\xef\xb9\xa5" : '>',
     "\xef\xbc\x9c" : '<',
     "\xef\xbc\x9d" : '=',
     "\xef\xbc\x9e" : '>',
     "\xef\xbc\x82" : '\"',
     "\xef\xbc\x84" : '$',
     "\xef\xbc\x86" : '&',
     "\xef\xbc\x87" : '\'',
     "\xef\xbc\x8a" : '*',
     "\xef\xbc\x8b" : '+',
     "\xef\xbc\x8d" : '-',
     "\xef\xbc\x8f" : '/',
     "\xef\xbc\xbb" : '[',
     "\xef\xbc\xbc" : '\\',
     "\xef\xbc\xbd" : ']',
     "\xef\xbc\xbe" : '^',
     "\xef\xbc\xbf" : '_',
     "\xef\xbc\xa0" : '@',
     "\xef\xbc\x83" : '#'}
specialunit3=['\xef\xbf\xa5','\xef\xbf\xa1','\xef\xbf\xa0']
specialunit2=[]#'\xc2\xb0'

def processline(line):
    line=line.split(' ')
    if 'http' in line and ':' in line:
     return "",True
    skip=False
    for j,word in enumerate(line):
        word=word.replace('\\/','/')
        line[j]=word
        for i in range(len(word)):
            if not word[i] in commoncharacter:
               if word[i] in special:
                re=line[j]
                re=re[0:i]+'\''+re[i+1:]
                line[j]=re
               elif len(word)>=2+i:
                 if word[i:i+2] in specialunit2:
                  pass
                 elif len(word)>=3+i:
                  if word[i:i+3] in specialcharacter:
                   re=line[j]
                   re=re[0:i]+specialcharacter[word[i:i+3]]+re[i+3:]
                   line[j]=re
                  #elif word[i:i+3] in specialsymbol:
                  # re=line[j]
                  # re=re[0:i]+specialsymbol[word[i:i+3]]+re[i+3:]
                  # line[j]=re
                  # print l2
                  elif word[i:i+3] in specialunit3:
                   pass
                  else:
                   skip=True
               else:
                skip=True
            else:
               pass
    return line,skip

def preprocess(src_dir,trg_dir,out_dir,out_file_name,abandon_same_corpus=True):
 s=set()
 with open(src_dir,'r') as f:
  with open(trg_dir,'r') as f1:
   with open(out_dir+out_file_name+'.src.p','w') as f2:
    with open(out_dir+out_file_name+'.trg.p','w') as f3:
     with open(out_dir+out_file_name+'.src.q','w') as f4:
      with open(out_dir+out_file_name+'.trg.q','w') as f5:
       for l1,l2 in zip(f.readlines(),f1.readlines()):
           l1=l1[:-1]
           l2=l2[:-1]
           if abandon_same_corpus and l1==l2:
              continue

           line1,skip=processline(l1)
           if skip:
              f4.write(l1+'\n')
              f5.write(l2+'\n')
              continue
          
           line2,skip=processline(l2)
           if skip:
              f4.write(l1+'\n')
              f5.write(l2+'\n')
              continue
           
           line1=' '.join(line1)
           line2=' '.join(line2)
           if line1+line2 in s:
              continue
           else:
              s.add(line1+line2)

           f2.write(line1+'\n')
           f3.write(line2+'\n')

import sys
if not len(sys.argv)==6:
 exit()
b=False
if sys.argv[5]=='True':
 b=True
preprocess(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4],b)
