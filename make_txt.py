import argparse

parser = argparse.ArgumentParser()
parser.add_argument('txt',help='*.txt',type=str)
args = parser.parse_args()

with open(args.txt,'r') as f:
    new_txt = []
    count = 0
    for line in f:
        if line == '-1,-1\n':
            f2 = open('{}{}.txt'.format(args.txt[:-4],count),'w')
            for line2 in new_txt:
                f2.write(line2)
            f2.close()
            count += 1
            new_txt = []

        else:
            new_txt.append(line)
    
        
