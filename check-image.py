import requests # dependency, needs to be installed
import re
import os
import os.path
import sys
import shutil
import math

global cwd
cwd = os.getcwd()

missingImages = 0
unusedImages = 0
unusedImagesSize = 0

allImagesInDir = []
allImagesInFile = []
allMissingImages = []
allUnusedImages = []

if sys.version_info[0] < 3:
    raise Exception("ERROR: Version 3 of Python required")

toCheckFileOrFolder = input("Do you want to check a file or a directory? (file/dir) ")

# Function for size conversion of unused images
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
        for num, line in enumerate(f, 1):
            #result = re.findall(r'<!--[\s\S]*?-->|(?P<url>(http(s?):)?/?/.+?\.(jpg|gif|png))', line)
            
            
            regexp = r'<!--[\s\S]*?-->|(?P<url>(http(s?):)?\/?\/?[^,;\'" \n\t>)(\\]+?\.(jpg|gif|png))'
            result = [item[0] for item in re.findall(regexp, line) if item[0]]
            if result:

                num = str(num)
                
                matchURL = result[0]
                if re.search(r'(http(s?):)', matchURL):
                    if checkUrl(matchURL) == False:
                        allMissingImages.append(matchURL + " on line number " + num)
                else:
                    if matchURL[0] != "/":
                        allImagesInFile.append(cwd + matchURL)
                        if os.path.isfile(fileCheckingDir + matchURL) == False:
                            allMissingImages.append(fileCheckingDir + matchURL + " on line number " + num + " in file " + f.name)
                    else:
                        allImagesInFile.append(cwd + matchURL)
                        if os.path.isfile(cwd + matchURL) == False:
                            allMissingImages.append(cwd + matchURL + " on line number " + num + " in file " + f.name)

        # check all existing images
        for path, subdirs, files in os.walk(fileCheckingDir+""):
            for name in files:
                fullpath = os.path.join(path, name)
                matches = re.search(r'([/|.|\w|\s|-])*\.(?:jpg|gif|png)',fullpath)
                if matches:
                    if(any(substring in fullpath for substring in dirsToExclude) is not True):
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
    else:
        pass
    
    saveToFile = input("Do you want to save the missing and unused images to a .txt file? (y/n) ")
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
        for image in list(set(allUnusedImages)):
            cleanPath = re.sub(r'(?<!(https:))(?<!(http:))//', '/', image)
            cleanPath = cleanPath.replace(str(cwd), '')
            file.write(cleanPath+"\n")
        file.close()
    else:
        pass
    
    moveToFolderForDeletion = input("Do you want to place all unused files inside a folder (" + cwd +"/MOVED_FILES_FROM_CHECK_IMAGE_SCRIPT" + ")? (y/n) ")
    if moveToFolderForDeletion == "y":
        newpath = r""+ cwd +"/MOVED_FILES_FROM_CHECK_IMAGE_SCRIPT"
        if not os.path.exists(newpath):
            os.makedirs(newpath)
            for image in allUnusedImages:
                shutil.move(str(image), cwd +"/MOVED_FILES_FROM_CHECK_IMAGE_SCRIPT/"+os.path.basename(image))
    else:
        print("Ok goodbye!")
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
    if toCheckCurrOrCustom != "curr" and toCheckCurrOrCustom != "":
        cwd = toCheckCurrOrCustom.strip().replace("\\","")
        print("CWD: " + cwd)
    elif toCheckCurrOrCustom == "curr":
        cwd = cwd
    else:
        print("ERROR: You didn't type 'curr' or 'ABSOLUTE_PATH_TO_DIR'. Please try again.")
        sys.exit()

    global dirsToExclude
    dirsToExclude = []
    
    toExcludeDir = input("Do you want to exclude any directories in (" + cwd + ") from being checked? (y/n) ")
    if toExcludeDir == "y":

        toStopExclusion = False
        while toStopExclusion == False:
            whichToExclude = input("Please type the pathname or exit if you're done. (RELATIVE_PATH_TO_DIR/exit) ")

            if whichToExclude != "exit":
                dirsToExclude.append(whichToExclude)
                print("TO EXLCUDE: " + str(dirsToExclude))
            else:
                toStopExclusion = True

    for path, subdirs, files in os.walk(str(cwd)):
        for name in files:
            fullpath = os.path.join(path, name)
            if(any(substring in fullpath for substring in dirsToExclude) is not True):
                matches = re.search(r'([/|.|\w|\s|-])*\.(?:html|php|js|css)',fullpath)
                if matches:
                    filesToCheckInDir.append(fullpath[matches.start():matches.end()])
    
    if len(filesToCheckInDir) == 0:
        print("No .html, .css, .js or .php files to check in " + cwd)
    else:
        for fileToCheck in filesToCheckInDir:
            checkFile(fileToCheck)
        tellUserStatus()
else:
    print("ERROR: You didn't type 'file' or 'dir'. Please try again.")