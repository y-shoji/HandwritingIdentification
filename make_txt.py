import argparse

from os.path import join
from glob import glob


def create_txt(text):
    f1 = open(text,'r')
    new_txt = []
    count = 0
    for line in f1:
        if line == '-1,-1\n':
            name = text.lstrip(args.input).rstrip('.txt')
            text_path = '{}/{}{}.txt'.format(args.output,name,count)
            f2 = open(text_path,'w')
            for line2 in new_txt:
                f2.write(line2)
            f2.close()
            count += 1
            new_txt = []

        else:
            new_txt.append(line)
    f1.close()

def main():
    texts = glob(join(args.input,'*.txt'))
    for text in texts:
        create_txt(text)

        
if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input',type=str,default='log')
    parser.add_argument('--output',type=str,default='logs')
    args = parser.parse_args()

    main()
