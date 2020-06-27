import argparse
import sys
import difflib

def main(args):
    src=open(args.s,'r')
    trg=open(args.t,'r')
    output=open(args.o,'w')

    for i, (err,cor) in enumerate(zip(src,trg)):
        weights = []
        matcher = difflib.SequenceMatcher(None, cor.split(), err.split())
        for tag, i1, i2, j1, j2 in matcher.get_opcodes():
            if tag == "equal":
                for x in range(i2, i1, -1):
                    weights.append("0")
            elif tag != "insert":
                for x in range(i2, i1, -1):
                    weights.append("1")
        output.write(" ".join(weights)+'\n')
    src.close()
    trg.close()
    output.close()
    vocabulary=open(args.v,'w')
    vocabulary.write('0 1\n1 1')
    vocabulary.close()

if __name__ == "__main__":
    # Define and parse program input
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", help="The path to an input m2 file.")
    parser.add_argument("-o", help="A path to where we save the output same text file.", required=True)
    parser.add_argument("-v", help="A path to where we save the output same text file.", required=True)
    parser.add_argument("-t", help="A path to where we save the output same text file.", required=True)
    args = parser.parse_args()
    main(args)
