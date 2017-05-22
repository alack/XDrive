import os
import sys
import shutil
import glob

class mergeFile():
    def merging(inputfilename,extension):
        outfilename = inputfilename+'.'+extension

        with open(outfilename,'wb') as outfile:
            counter = 1
            while True:
                partfilename = inputfilename+'.'+str(counter)
                if (os.path.isfile(partfilename)==False):
                    break
                with open(partfilename,'rb') as readfile:
                    shutil.copyfileobj(readfile,outfile)
                counter += 1


