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

def installPackage():
    downloadrpkfileList()
    print(f'Plugin repository: {Fore.LIGHTBLUE_EX}{rpkURL}{Style.RESET_ALL}')
    print(f'Attempting to find {Fore.LIGHTGREEN_EX}{commandArgs}{Style.RESET_ALL}...')

    with open('assets/plugins.rpk', 'r') as f:
        lines = len(f.readlines())

    with open('assets/plugins.rpk', 'r') as f:
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
            print(f'Found Package {Fore.LIGHTGREEN_EX}{commandArgs}{Style.RESET_ALL}!')
            foundPackage = True
            break

    if foundPackage is True:
        print('-' * terminalX)
        confInput = input(f'Are you sure you want to install {Fore.LIGHTGREEN_EX}{commandArgs}{Style.RESET_ALL}? y/n: ')

        if confInput == 'y':
            print(f'Installing {Fore.LIGHTGREEN_EX}{commandArgs}{Style.RESET_ALL}...')
            fileDownloader()
            if '.zip' in fileName:
                extractZip(fileName)
        else:
            print(f'{Fore.YELLOW}Install Canceled{Style.RESET_ALL}')
    else:
        print(f'{Fore.LIGHTGREEN_EX}{commandArgs}{Style.RESET_ALL} was not found.')

# Downloads file
def fileDownloader():
    global fileName
    fileName = os.path.basename(fileURL)

    print(Fore.MAGENTA + 'Downloading...')

    # Checks for invalid url data
    try:
        r = requests.get(fileURL)
        open(f'{installLoc}/{fileName}', 'wb').write(r.content)
        print(f'{Fore.LIGHTMAGENTA_EX}Install Complete!{Style.RESET_ALL}')
    except FileNotFoundError:
        errorHandle('Invalid install directory', 3)

def extractZip(zip):
    with zipfile.ZipFile(f'{installLoc}/{zip}', 'r') as zip_ref:
        zip_ref.extractall(installLoc)

readArgsFile()
loadConfig()
installPackage()