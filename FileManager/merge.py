import os
import sys
import shutil
import glob

class mergeFile():
    def merging(filename,extension):
        outfilename = filename+'.'+extension
        #print(filename)
        globfile = outfilename+'.'+'*'
        with open(outfilename,'wb') as outfile:
            for filename in glob.glob('test.*'):
                if filename == outfilename:
                    continue
                with open(filename,'rb') as readfile:
                    shutil.copyfileobj(readfile,outfile)



