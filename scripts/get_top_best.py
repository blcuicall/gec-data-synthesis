def get_top_best(checkpoint_dir,top_num,log_file,out_file):
 sz=[]
 with open(checkpoint_dir+'/'+out_file,'w') as f1:
  with open(checkpoint_dir+'/'+log_file,'r') as f2:
   for line in f2:
    line=line.split('| ')
    if len(line)>2 and line[2].find('valid') != -1:
     va=line[3].strip()
     va=va.split(' ')
     if len(va)>1 and va[0].find('loss') != -1:
      va_f=float(va[1])
      e_i=int(line[1].strip().split(' ')[1])
      sz.append([e_i,va_f])
   sz=sorted(sz,key=lambda x:x[1])
   for i in range(top_num):
    f1.write(checkpoint_dir+'/checkpoint%d.pt\n' % sz[i][0])

import sys
if not len(sys.argv) == 5:
 exit()
get_top_best(sys.argv[1],int(sys.argv[2]),sys.argv[3],sys.argv[4])
