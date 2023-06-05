import os
import subprocess
import importlib
from subprocess import PIPE
from pathlib import Path
#from clickhouse_driver import Client

SEPARATOR = "##### This is a new file#####\n"

# class Commands:
#     read_file
#     wirte_file
    

class ProgramResult:
    pass

def go_parent_dir():
    curr_path = os.getcwd()
    dirs = os.listdir(curr_path)
    if 'bin' not in dirs:
        os.chdir("..")  # Change the current directory

def generate_code(bash_script):
    os.system(bash_script)

def format_code(gpt_file, project_name):
    
    SEPARATOR = "#####This is a new file#####\n"
    # Locate files and dest folders
    go_parent_dir()
    gpt_file_path = Path('./bin') / gpt_file
    dest_path = Path('./lib') / project_name
    if not dest_path.exists():
        dest_path.mkdir()
    print ("Creating dest folders!")

    # Split the gpt result file into separate files
    with open(gpt_file_path, 'r') as f:
        data = f.read()
        code_split = data.split(SEPARATOR)
        code_split = [x for x in code_split if x]
    
    FILES = ['constants.py', 'process.py', 'query.py', f'{project_name}.py']
    for i, filename in enumerate(FILES):
        file_path = dest_path / filename
        with open(file_path, 'w') as f:
            f.write(code_split[i])

def fix_code():
    pass

def import_module_with_alias(module_name, alias):
    try:
        module = importlib.import_module(module_name)
        globals()[alias] = module
        print(f"Successfully imported module '{module_name}' with alias '{alias}'")
    except ImportError:
        print(f"Failed to import module: {module_name}")

def get_clickhouse_result(project_name):

    import_module_with_alias(f"lib.{project_name}.query", "query")
    host = 'clickhouse.stage.san'
    port = '30900'
    compression = 'lz4'

    # create a client
    #client = Client(host=host, port=port, compression=compression)

    sql = ...

def run_program(project_name=None):
    go_parent_dir()
    output = subprocess.run(["bash", "bin/run.sh", project_name], stdout=PIPE, stderr=PIPE)

    print (output)
    return output

def re_run(k=1):
    while k:
        generate_code()

if __name__ == "__main__":
    bash_script = './gpt_write_code'
    gpt_file = 'new_exporter.py'
    project_name = 'stargate'
    log_file = 'bridge.log'
    

    generate_code(bash_script)
    format_code(gpt_file, project_name)



    #result, log = run_program(project_name)

    # while (result.failed()):
    #     fix_code(result)
    #     result = run_program(project_name)