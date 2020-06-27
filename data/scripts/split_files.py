def split_file(src_file,trg_file,src_out,trg_out,same_out):
 with open(src_file,'r') as f1:
  with open(trg_file,'r') as f2:
   with open(src_out,'w') as f3:
    with open(trg_out,'w') as f4:
     with open(same_out,'w') as f5:
      for l1,l2 in zip(f1,f2):
       if l1==l2:
        f5.write(l1)
       else:
        f3.write(l1)
        f4.write(l2)

import sys
if not len(sys.argv)==4:
 exit()
split_file(sys.argv[1],sys.argv[2],sys.argv[3]+'.notsame.src',sys.argv[3]+'.notsame.trg',sys.argv[3]+'.same')
