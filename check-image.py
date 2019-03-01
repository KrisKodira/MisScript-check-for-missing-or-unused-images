#TODO: Get directory the file is in and search there

import requests # dependency
import re
import os
import os.path
import sys

cwd = os.getcwd()

missingImages = 0
unusedImages = 0
unusedImagesSize = 0

allImagesInDir = []
allImagesInFile = []
allMissingImages = []
allUnusedImages = []

toCheckFileOrFolder = input("Do you want to check a file or a directory? (file/dir) ")

import math

def convert_size(size_bytes):
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return "%s %s" % (s, size_name[i])

def checkFile(file):
    try:
        f = open(fileToCheck)

        global allImagesInDir
        global allImagesInFile
        global allMissingImages

        fileCheckingDir = os.path.dirname(os.path.realpath(file))

        if fileCheckingDir[len(str(fileCheckingDir)) - 1] != "/":
            fileCheckingDir = str(fileCheckingDir) + "/"

        def checkUrl(urlToCheck):
            request = requests.get(urlToCheck)
            if request.status_code == 200:
                return True
            else:
                return False


        # match any image
        for line in f:
            result = re.search(r'(http(s?):)?([/|.|\w|\s|-])*\.(?:jpg|gif|png)', line)
            if result:
                matchURL = line[result.start():result.end()]
                if re.search(r'(http(s?):)', matchURL):
                    if checkUrl(matchURL) == False:
                        allMissingImages.append(matchURL)
                else:
                    allImagesInFile.append(cwd + matchURL)
                    if os.path.isfile(fileCheckingDir + matchURL) == False:
                        allMissingImages.append(fileCheckingDir + matchURL)

        # check all existing images
        for path, subdirs, files in os.walk(fileCheckingDir+""):
            for name in files:
                fullpath = os.path.join(path, name)
                matches = re.search(r'([/|.|\w|\s|-])*\.(?:jpg|gif|png)',fullpath)
                if matches:
                    allImagesInDir.append(fullpath[matches.start():matches.end()])
                    fstat = os.stat(fullpath[matches.start():matches.end()])

                    global unusedImagesSize
                    unusedImagesSize += fstat.st_size

        # All images that are not used in directory
        global allUnusedImages
        allUnusedImages = list(set(allImagesInDir) - set(allImagesInFile))
    except: 
        pass

def tellUserStatus():
    global missingImages
    global unusedImages
    missingImages += len(set(allMissingImages))
    unusedImages += len(set(allUnusedImages))
    print("Missing images: " + str(missingImages))
    print("Unused images: " + str(unusedImages))
    print("---- Unnecessary used space: " + convert_size(unusedImagesSize))
    toListAllFiles = input("List missing or unused images? (both/miss/unused/n) ")

    if toListAllFiles == "both":
        print("")
        print("---------- Missing Images ----------")
        for image in list(set(allMissingImages)):
            cleanPath = re.sub(r'(?<!(https:))(?<!(http:))//', '/', image)
            cleanPath = cleanPath.replace(str(cwd), '')
            print(cleanPath)
        
        print("")
        print("")
        print("---------- Unused Images ----------")
        for image in list(set(allUnusedImages)):
            image = str(image)
            image = image.replace(str(cwd), '')
            print(image)
    elif toListAllFiles == "miss":
        print("")
        print("---------- Missing Images ----------")
        for image in list(set(allMissingImages)):
            cleanPath = re.sub(r'(?<!(https:))(?<!(http:))//', '/', image)
            cleanPath = cleanPath.replace(str(cwd), '')
            print(cleanPath)
    elif toListAllFiles == "unused":
        print("")
        print("---------- Unused Images ----------")
        for image in list(set(allUnusedImages)):
            image = str(image)
            image = image.replace(str(cwd), '')
            print(image)
    
    saveToFile = input("Do you want to save the missing and unused images to a file? (y/n) ")
    if saveToFile == "y":
        file = open("IMAGE_REPORT.txt","w") 
 
        file.write("---------- Missing Images ----------\n")
        for image in list(set(allMissingImages)):
            cleanPath = re.sub(r'(?<!(https:))(?<!(http:))//', '/', image)
            cleanPath = cleanPath.replace(str(cwd), '')
            file.write(cleanPath+"\n")
        
        file.write("\n")
        file.write("\n")
        file.write("---------- Unused Images ----------\n")
        for image in list(set(allMissingImages)):
            cleanPath = re.sub(r'(?<!(https:))(?<!(http:))//', '/', image)
            cleanPath = cleanPath.replace(str(cwd), '')
            file.write(cleanPath+"\n")
        file.close()
    else:
        print("Ok goodbye")
        sys.exit()

if toCheckFileOrFolder == "file":
    fileToCheck = input("Which File do you want to check? ")

    if os.path.isfile(fileToCheck):
        checkFile(fileToCheck)
        tellUserStatus()        
    else:
        print("ERROR: The file doesn't exist")
elif toCheckFileOrFolder == "dir":
    filesToCheckInDir = []

    toCheckCurrOrCustom = input("Do you want to check the current directory or a custom directory? (curr/ABSOLUTE_PATH_TO_DIR) ")
    if toCheckCurrOrCustom != "curr":
        cwd = toCheckCurrOrCustom
    elif toCheckCurrOrCustom == "curr":
        cwd = cwd
    else:
        print("ERROR: You didn't type curr or ABSOLUTE_PATH_TO_DIR. Please try again.")
        sys.exit()

    for path, subdirs, files in os.walk(cwd+""):
        for name in files:
            fullpath = os.path.join(path, name)
            matches = re.search(r'([/|.|\w|\s|-])*\.(?:html|php|js)',fullpath)
            if matches:
                filesToCheckInDir.append(fullpath[matches.start():matches.end()])
    
    if len(filesToCheckInDir) == 0:
        print("No .html or .php files to check")
    else:
        for fileToCheck in filesToCheckInDir:
            checkFile(fileToCheck)
        tellUserStatus()
else:
    print("ERROR: You didn't type file or dir. Please try again.")