#import sys
#import codecs
#sys.stdin = codecs.getreader('UTF-8')(sys.stdin)
#s=set()
#for line in sys.stdin:
# a=int(line)
# if a==0:
#  exit()
# if not line in s:
#  s.add(line)
#  print line,
import argparse
import os

def main(args):
    if not os.path.exists(args.i):
        return 1
    file_list=[]
    for f in os.listdir(args.i):
         if args.name in f:
              file_list.append(args.i+'/'+f)
    
    s=set()
    output=open(args.o,'w')
    for f in file_list:
     with open(f,'r') as f1:
         for line in f1:
          if not line in s:
              s.add(line)
              output.write(line)
    output.close()  

if __name__ == "__main__":
    # Define and parse program input
    parser = argparse.ArgumentParser()
    parser.add_argument("--i", help="The path to an input m2 file.")
    parser.add_argument("--name", help="A path to where we save the output same text file.", required=True)
    parser.add_argument("--o", help="A path to where we save the output same text file.", required=True)
    args = parser.parse_args()
    main(args)

