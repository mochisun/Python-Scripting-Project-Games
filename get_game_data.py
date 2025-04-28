#operating sys
import os
#work with json files
import json
#copy/overwrite operations
import shutil
#run terminal command -> compile/run go code
from subprocess import PIPE, run
#access to command line args
import sys

#pattern to match search results with
GAME_DIR_PATTERN = "game"

#find and return all game paths based on <source>
def find_all_game_paths(source):
    #path list var
    game_paths = []
    #walk recursively through source directory. only iterate once for use of dirs variable
    for root, dirs, files in os.walk(source):
        #iterate through found dirs
        for directory in dirs: 
            #check dir against pattern, lowercase for ease
            if GAME_DIR_PATTERN in directory.lower():
                path = os.path.join(source, directory)
                game_paths.append(path)

        break
    return game_paths

def main(source, target):
    #get current working directory
    cwd = os.getcwd()
    #get full source path by joining with base cwd
    source_path = os.path.join(cwd, source)
    #get full target path by joining with base cwd
    target_path = os.path.join(cwd, target)



#determines if script is run directly or imported as module
#if we run this code on cl -> "python get_game_data.py data new_data", then args is list carrying [0]=file name [1]=data [2]=new_data
if __name__ == "__main__":
    args = sys.argv
    #we only want 2 args (data, new_data) + our file name = 3 args total
    if (len(args) != 3):
        raise Exception("must pass source and target directory only")
    #get the data from user entry. "[1:]" cuts off python file [0]
    source, target = args[1:]
    #call to main with entered data variables
    main(source, target)
