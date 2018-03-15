import os
import glob
from os.path import basename

def main():
    h=[]
    for file in glob.glob("*.mp3"):
        pos = file.rfind(".mp3")
        pos2 = file.rfind(" - ")
        no = int(file[pos2+3:pos])
        newFile = file[:pos2] + ".mp3"
        d=(no,file, newFile)
        h.append(d)
    hs = sorted(h, key=lambda a: a[0])
    i=0
    for o in hs:
        i=i+1
        # TODO use : "{:02}".format(1)
        newFile=str(i) + " " + o[2]
        print(newFile)
        os.rename(o[1], newFile)

if __name__ == "__main__":
    main()