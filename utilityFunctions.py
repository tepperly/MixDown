import os, Queue, shutil, sys, tarfile, tempfile, urllib2, subprocess

def executeCommand(command, args = "", workingDirectory = "", verbose = False, exitOnError = False):
    try:
        lastcwd = os.getcwd()
        if workingDirectory != "":
            os.chdir(workingDirectory)
        fullCommand = command + args
        if verbose:
            print "Executing: " + fullCommand + ": Working Directory: " + workingDirectory
        errorCode = os.system(fullCommand)
        if exitOnError and errorCode != 0:
            printErrorAndExit("Command '" + fullCommand + "': exited with error code " + str(errorCode))
    finally:
        os.chdir(lastcwd)

def executeSubProcess(args, workingDirectory = "", outFileHandle = 1, verbose = False, exitOnError = False):
    fullCommand = " ".join(args)
    if verbose:
        print "Executing: " + fullCommand + ": Working Directory: " + workingDirectory
    process = subprocess.Popen(args, stdout=outFileHandle, stderr=outFileHandle, cwd=workingDirectory)
    process.wait()
    if exitOnError and process.returncode != 0:
        printErrorAndExit("Command '" + fullCommand + "': exited with error code " + str(process.returncode))
        
def findShallowestFile(startPath, fileList):
    q = Queue.Queue()
    q.put(startPath)
    while not q.empty():
        currPath = includeTrailingPathDelimiter(q.get())
        for item in os.listdir(currPath):
            itemPath = currPath + item
            if os.path.isdir(itemPath):
                q.put(itemPath)
            elif item in fileList:
                return currPath + item # success
            
def getBasename(path):
    basename = os.path.basename(path)
    if not os.path.isdir(path):
        i = 0
        for c in basename:
            if (c == '.') and (not i == 0):
                break
            i += 1
        basename = basename[:i]    
    return basename

def includeTrailingPathDelimiter(path):
    if (not path[len(path)-1:] == '/') and (not os.path.isfile(path)):
        return path + '/'
    return path

def isURL(url):
    try:
        f = urllib2.urlopen(url)
        return True
    except:
        return False
    
def prettyPrintList(list, header = "", headerIndent = "", itemIndent = ""):
    retStr = headerIndent + header
    listLen = len(list)
    if listLen == 1:
        retStr = retStr + list[0]
    elif listLen > 0:
        for currItem in list:
            retStr = retStr  + "\n" + itemIndent + currItem
    return retStr
            
def printErrorAndExit(errorStr, filePath = "", lineNumber = 0):
    sys.stdin.flush()
    if filePath == "" and lineNumber == 0:
        sys.stderr.write("Error: %s\n" % (errorStr))
    elif lineNumber == 0:
        sys.stderr.write("Error: %s: %s\n" % (filePath, errorStr))
    else:
        sys.stderr.write("Error: %s (line %d): %s\n" % (filePath, lineNumber, errorStr))
    sys.stderr.flush()
    sys.exit()

def removeDir(path):
    if (path[len(path)-1:] == '/') and os.path.isfile(path[:len(path)-1]):
        raise IOError("Error: Cannot clean directory '" + path + "' : File exists by the same name.")
    if os.path.exists(path):
        shutil.rmtree(path)
        
def splitFileName(fileName):
    basename = fileName
    version = ""
    
    if basename.endswith(".tar.gz"):
        basename = basename[:-7]
    elif basename.endswith(".tar.bz2"):
        basename = basename[:-8]
    elif basename.endswith(".tar") or basename.endswith(".tgz") or basename.endswith(".tbz") or basename.endswith(".tb2"):
        basename = basename[:-4]
    
    basename = os.path.basename(basename)
        
    i = 0
    for c in basename:
        if c in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']:
            version = basename[i:]
            basename = basename[:i]
            if basename[-1] == '-':
                basename = basename[:-1]
            break
        i += 1
        
    return basename, version
        
def stripItemsInList(value):
    retList = []
    for item in value[:]:
        retList.append(str.strip(item))
    return retList

def untar(tarPath, outPath = "", stripDir=False):
    if stripDir:
        unTarOutpath = tempfile.mkdtemp()
    else:
        unTarOutpath = outPath
        
    tar = tarfile.open(tarPath, "r")
    for item in tar:
        #TODO: check for relative path's
        tar.extract(item, unTarOutpath)
        
    if stripDir:
        dirList = os.listdir(unTarOutpath)
        if len(dirList) == 1:
            src = includeTrailingPathDelimiter(unTarOutpath) + dirList[0]
        else:
            src = includeTrailingPathDelimiter(unTarOutpath)
        shutil.move(src, outPath)
        
def URLToFilename(url):
    filename = url[(str.rfind(url, "/")+1):]
    if url == "" or file == "":
        return "_"
    return filename
    
