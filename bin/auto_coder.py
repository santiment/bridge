class Commands:
    pass

class ProgramResult:
    pass


def generate_code():
    pass

def format_code():
    pass

def fix_code():
    pass

def run_program() -> ProgramResult:
    pass

if __name__ == "__main__":
    COMMANDS = []
    generate_code(COMMANDS)
    format_code()


    result = run_program()

    while (result.failed()):
        fix_code(result)
        result = run_program()