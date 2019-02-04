#!/usr/bin/env python
import os


class FileData:
    def __init__(self, absPath, filename):
        self.filename = filename
        self.absPath = absPath


def isBackUpFile(inputFileName):
    # must end with .rvt
    # an actual file name must be at lease one char long, which means the file must be at lease 10 long a.0001.rvt
    # chars from end-7 to end-4 must be digits
    # char end-4 to end-8 must be '.'
    numDigits = 4
    if inputFileName.endswith('.rvt') and len(inputFileName) >= (2 + numDigits + 4):
        numbersSection = inputFileName[len(inputFileName) - (numDigits + 4):-4]
        if numbersSection.isdigit() and inputFileName[len(inputFileName) - 4] == '.' and inputFileName[len(inputFileName) - (1 + numDigits + 4)] == '.':
            return True
    return False


def tryDeleteFile(file):
    try:
        os.remove(file.absPath)
        print("Deleted: " + file.filename)
    except OSError as e:  # if failed, report it back to the user
        print ("Error: %s - %s." % (e.filename, e.strerror))



def deleteAll():
    totalSize = 0;
    foundFiles = []

    for root, dirs, files in os.walk('.'):
        for filename in files:
            abpath = os.path.abspath(os.path.join(root,filename))
            if isBackUpFile(filename):
                foundFiles.append(FileData(abpath, filename))
                totalSize = totalSize + os.path.getsize(abpath)


    if(len(foundFiles) == 0):
        raw_input("No REVIT backup-files found in folder. Press any 'Enter' to exit.")
        return
    print("Found the following REVIT backup-files in this folder:")
    print("Total size is: " +str(totalSize/1000) + "mb")
    print
    count = 1
    for file in foundFiles:
        print(str(count) + ". " + file.filename)
        count += 1
    print
    answer = raw_input(
        "Press 'Y' then 'Enter' to delete these " + str(count - 1) + " files or just press 'Enter' to exit.   ")
    if answer == "Y" or answer == "y":
        print
        for file in foundFiles:
            tryDeleteFile(file)
        print
        raw_input("Done. Press 'Enter' to exit.")

deleteAll()
