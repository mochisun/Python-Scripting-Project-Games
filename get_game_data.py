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
#pattern of game executables
GAME_CODE_EXTENSION = ".go"
#to aid in compile command creation
GAME_COMPILE_COMMAND_BASE = ["go", "build"]

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

def create_dir(path):
    if not os.path.exists(path):
        os.mkdir(path)

def get_name_from_paths(paths, to_strip):
    new_names = []
    #iterate through each path name and 
    for path in paths:
        #.split to return last aspect of path
        _, dir_name = os.path.split(path)
        #strip off "game"
        new_dir_name = dir_name.replace(to_strip, "")
        new_names.append(new_dir_name)
    return new_names

def copy_and_overwrite(source, dest):
    #remove directory if already exists to allow new data
    if os.path.exists(dest):
        shutil.rmtree(dest)
    
    #copy everything from source to dest
    shutil.copytree(source, dest)

#create json file containing data regarding <game_dirs> at path <path>
def make_json_metadata_file(path, game_dirs):
    #json formatting
    data = {
        "gameNames" : game_dirs,
        "numberOfGames" : len(game_dirs)
    }
    #open "w" for write, as f for file. use of context manager so file closes/cleans up auto
    with open(path, "w") as f:
        #dump <data> into f for file, not s for string
        json.dump(data, f)

#compile game
def compile_game_code(path):
    code_file_name = None
    #walk through once to access <files>
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(GAME_CODE_EXTENSION):
                code_file_name = file
            break
        break
    if code_file_name is None:
        return
    #build command to run 
    command = GAME_COMPILE_COMMAND_BASE + [code_file_name]
    run_command(command, path)

def run_command(command, path):
    #get current working directory to go back to it later
    cwd = os.getcwd()
    #change directory
    os.chdir(path)

    #run command. PIPE allows for process communication
    result = run(command, stdout=PIPE, stdin=PIPE, universal_newlines=True)
    print("compile result", result)
    #change back to cwd for good practice
    os.chdir(cwd)


def main(source, target):
    #get current working directory
    cwd = os.getcwd()
    #get full source path by joining with base cwd
    source_path = os.path.join(cwd, source)
    #get full target path by joining with base cwd
    target_path = os.path.join(cwd, target)
    #get game paths from function
    game_paths = find_all_game_paths(source_path)
    #strip pattern off paths to get new directories
    new_game_dirs = get_name_from_paths(game_paths, GAME_DIR_PATTERN)
    
    #create the directory for target
    create_dir(target_path)

    #iterate through tuple pulled from zip: which matches indicies of both paths
    for src, dest in zip(game_paths, new_game_dirs):
      
        #create the new path per src
        dest_path = os.path.join(target_path, dest)
        copy_and_overwrite(src, dest_path)
        compile_game_code(dest_path)

    #create neat json file for data reading
    json_path = os.path.join(target_path, "metadata.json")
    make_json_metadata_file(json_path, new_game_dirs)




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

