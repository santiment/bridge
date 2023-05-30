import os
import subprocess
from subprocess import PIPE
from pathlib import Path

# class Commands:
#     read_file
#     wirte_file
    

class ProgramResult:
    pass

def go_parent_dir():
    curr_path = os.getcwd()
    dirs = os.listdir(curr_path)
    if 'bin' not in dirs:
        os.system("cd ..")

def generate_code(bash_script):
    os.system(bash_script)

def format_code(gpt_file, project_name):
    
    # Locate files and dest folders
    go_parent_dir()
    gpt_file_path = Path('./bin') / gpt_file
    dest_path = Path('./lib') / project_name
    if not dest_path.exists():
        dest_path.mkdir()
    print ("Creating dest folders!")

    # Split the gpt result file into separate files
    with open(gpt_file_path, 'r') as f:
        data = f.readlines()
        print (data)
    

def fix_code():
    pass

def run_program(project_name=None):
    go_parent_dir()
    output = subprocess.run(["bash", "bin/run.sh", project_name], stdout=PIPE, stderr=PIPE)

    print (output)
    return output

if __name__ == "__main__":
    bash_script = './gpt_write_code'
    gpt_file = 'new_exporter.py'
    project_name = 'polygon_bridge'
    
    result = run_program(project_name)

    #generate_code(bash_script)
    
    format_code(gpt_file, project_name)

    result = run_program(project_name)

    while (result.failed()):
        fix_code(result)
        result = run_program(project_name)