import argparse

def main(args):
    output=open(args.o,'w')
    with open(args.i,'r') as f:
        for line in f:
            temp=line.strip().split()
            if len(temp)>=args.min and len(temp)<=args.max:
                output.write(line)

if __name__ == "__main__":
    # Define and parse program input
    parser = argparse.ArgumentParser()
    parser.add_argument("--i", help="The path to an input m2 file.")
    parser.add_argument("--min", help="A path to where we save the output same text file.", required=True,type=int)
    parser.add_argument("--max", help="A path to where we save the output same text file.", required=True,type=int)
    parser.add_argument("--o", help="A path to where we save the output same text file.", required=True)
    args = parser.parse_args()
    main(args)
