import os
import sys

class chunkFile():
    def chunking(filename):
        chunkfilename = filename.split(".")
        max_size = 4*1024*1024  # 일단 5kb
        buffer = 1024
        with open(filename, 'r+b') as src:
            suffix = 1
            while True:
                with open(chunkfilename[0] + '.%s' % suffix, 'w+b') as tgt:
                    written = 0
                    while written < max_size:
                        data = src.read(buffer)
                        if data:
                            tgt.write(data)
                            written += buffer
                        else:
                            return suffix
                    suffix += 1




