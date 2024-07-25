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

foundPackages = []
terminalX = os.get_terminal_size().columns

# Load config
def loadConfig():
    f = open("assets/config.json", "r")
    tmp_j = f.read()
    cfginfo = json.loads(tmp_j)

    global pluginRepo
    global installLoc
    installLoc = (cfginfo['installLocation'])
    pluginRepo = (cfginfo['pluginRepo'])

    if '@HOME' in installLoc:
        installLoc = installLoc.replace('@HOME', os.path.expanduser('~'))

def readArgsFile():
    with open('assets/.args', 'r') as f:
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
        open('assets/plugins.rpk', 'wb').write(r.content)
    except:  # noqa: E722
        errorHandle("Invalid URL", 1)

def searchPackages():
    downloadrpkfileList()
    print(f'Plugin repository: {Fore.LIGHTBLUE_EX}{rpkURL}{Style.RESET_ALL}')
    print(f'Attempting to find {Fore.LIGHTBLUE_EX}{commandArgs}{Style.RESET_ALL}...')

    with open('assets/plugins.rpk', 'r') as f:
        lines = len(f.readlines())

    with open('assets/plugins.rpk', 'r') as f:
        file = f.readlines()

    for i in range(lines):
        fileList = file[i]
        fileItem = fileList.split(';')
        global fileURL
        fileURL = fileItem[1].replace('\n', '')
        fileItem = fileItem[0].replace('\n', '')
        
        if commandArgs in fileItem:
            global foundPackages
            foundPackages.append(fileItem)

    if len(foundPackages) != 0:
        print('-' * terminalX)
        print(f'{Fore.LIGHTBLUE_EX}{len(foundPackages)}{Style.RESET_ALL} package(s) found with the search term "{Fore.LIGHTBLUE_EX}{commandArgs}{Style.RESET_ALL}".')

        for i in range(len(foundPackages)):
            print(f'{i + 1}: {Fore.LIGHTBLUE_EX}{foundPackages[i]}{Style.RESET_ALL}')
    else:
        print(f'No packages with the term "{Fore.LIGHTBLUE_EX}{commandArgs}{Style.RESET_ALL}" were found.')

readArgsFile()
loadConfig()
searchPackages()