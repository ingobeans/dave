import os

os.system("color")

class colors:
    PURPLE = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def purple(inp):
    inp = str(inp)
    return colors.PURPLE + inp + colors.ENDC
def blue(inp):
    inp = str(inp)
    return colors.BLUE + inp + colors.ENDC
def cyan(inp):
    inp = str(inp)
    return colors.CYAN + inp + colors.ENDC
def green(inp):
    inp = str(inp)
    return colors.GREEN + inp + colors.ENDC
def yellow(inp):
    inp = str(inp)
    return colors.YELLOW + inp + colors.ENDC
def red(inp):
    inp = str(inp)
    return colors.RED + inp + colors.ENDC