#!/usr/bin/env python3

#############################################################
#                                                           #
# File created by 0hStormy                                  #
#                                                           #
#############################################################

# Packages
import sys
import os
import subprocess
from colorama import Fore, Style

def errorHandle(message, code):
    print(f'{Fore.RED}Error:{Style.RESET_ALL} {message}')
    exit(code)

def writeArgsFile():
    with open('assets/.args', 'w') as f:
        try:
            f.write(sys.argv[2])
        except IndexError:
            errorHandle(f'No Sub-argument found, try something like: {Fore.LIGHTMAGENTA_EX}rpk install [PACKAGE]{Style.RESET_ALL}', 2)
        f.close()

if len(sys.argv) == 1:
    with open('assets/help.txt', 'r') as f:
        helpFile = f.read()
        f.close()
    print(f'\n{helpFile}')

else:
    command = sys.argv[1]
    writeArgsFile()
    commandsList = os.listdir('assets/')
    for commands in commandsList:
        if commands == f'{command}.py':
            subprocess.run(['python', f'assets/{command}.py'])