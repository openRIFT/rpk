#!/usr/bin/env python3

#############################################################
#                                                           #
# File created by 0hStormy                                  #
#                                                           #
#############################################################

from colorama import Fore, Style
import requests
import os
import json
import zipfile

foundPackage = False
terminalX = os.get_terminal_size().columns
homeFolder = os.path.expanduser('~')

# Load config
def loadConfig():
    f = open(f"{homeFolder}/.rpk/config.json", "r")
    tmp_j = f.read()
    cfginfo = json.loads(tmp_j)

    global pluginRepo
    global removeLoc
    removeLoc = (cfginfo['installLocation'])
    pluginRepo = (cfginfo['pluginRepo'])

    if '@HOME' in removeLoc:
        removeLoc = removeLoc.replace('@HOME', os.path.expanduser('~'))

def readArgsFile():
    with open(f'{homeFolder}/.args', 'r') as f:
        global commandArgs
        commandArgs = f.read()
        f.close()

def errorHandle(message, code):
    print(f'{Fore.RED}Error:{Style.RESET_ALL} {message}')
    exit(code)

# Repo downloader
def downloadrpkfileList():
    global rpkURL
    rpkURL = pluginRepo

    try:
        r = requests.get((rpkURL), allow_redirects=True)
        open(f'{homeFolder}/.rpk/plugins.rpk', 'wb').write(r.content)
    except:  # noqa: E722
        errorHandle("Invalid URL", 1)

def removePackage():
    downloadrpkfileList()
    print(f'Plugin repository: {Fore.LIGHTBLUE_EX}{rpkURL}{Style.RESET_ALL}')
    print(f'Attempting to find {Fore.LIGHTRED_EX}{commandArgs}{Style.RESET_ALL}...')

    with open(f'{homeFolder}/.rpk/plugins.rpk', 'r') as f:
        lines = len(f.readlines())

    with open(f'{homeFolder}/.rpk/plugins.rpk', 'r') as f:
        file = f.readlines()

    for i in range(lines):
        global foundPackage
        if foundPackage is not True:
            fileList = file[i]
            fileItem = fileList.split(';')
            global fileURL
            fileURL = fileItem[1].replace('\n', '')
            fileItem = fileItem[0].replace('\n', '')

        if fileItem == commandArgs:
            print(f'Found Package {Fore.LIGHTRED_EX}{commandArgs}{Style.RESET_ALL}!')
            foundPackage = True
            break

    if foundPackage is True:
        print('-' * terminalX)
        confInput = input(f'Are you sure you want to remove {Fore.LIGHTRED_EX}{commandArgs}{Style.RESET_ALL}? y/n: ')

        if confInput == 'y':
            print(f'Removing {Fore.LIGHTRED_EX}{commandArgs}{Style.RESET_ALL}...')
            try:
                fileName = os.path.basename(fileURL)

                if '.zip' in fileName:
                    zip = zipfile.ZipFile(f'{removeLoc}/{fileName}')
                    for i in range(len(zip.namelist())):
                        os.remove(f'{removeLoc}/{zip.namelist()[i]}')
                    os.remove(f'{removeLoc}/{fileName}')

                print(f'{Fore.LIGHTMAGENTA_EX}Remove Complete!{Style.RESET_ALL}')

            except FileNotFoundError:
                print(f'{Fore.YELLOW}{commandArgs}{Style.RESET_ALL} is not present in Plugins folder, finshing...')
        else:
            print(f'{Fore.YELLOW}Remove Canceled{Style.RESET_ALL}')
    else:
        print(f'{Fore.LIGHTRED_EX}{commandArgs}{Style.RESET_ALL} was not found.')

readArgsFile()
loadConfig()
removePackage()
