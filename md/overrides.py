from tokenizer import Tokenizer, TokenType
import defines, logger

class Overrides(object):
    def __init__(self):
        self.CCompiler = None
        self.CPreProcessor = None
        self.CXXCompiler = None
        self.FCompiler = None
        self.F77Compiler = None
        self.OBJCCompiler = None
        self.OBJCPreProcessor = None
        self.OBJCXXCompiler = None
        self.OBJCXXPreProcessor = None
        self.optimize = None
        self.CFlags = None
        self.CDefines = None
        self.CXXFlags = None
        self.CPPFlags = None
        self.FFlags = None
        self.FLibs = None
        self.F77Flags = None
        self.F77Libs = None
        self.LinkerFlags = None
        self.LinkerFlagsEXE = None
        self.LinkerFlagsShared = None
        self.LinkerFlagsModule = None
        self.OBJCFlags = None
        self.OBJCXXFlags = None

    def combine(self, child):
        if child.CCompiler != None:
            self.CCompiler = child.CCompiler
        if child.CPreProcessor != None:
            self.CPreProcessor = child.CPreProcessor
        if child.CXXCompiler != None:
            self.CXXCompiler = child.CXXCompiler
        if child.FCompiler != None:
            self.FCompiler = child.FCompiler
        if child.F77Compiler != None:
            self.F77Compiler = child.F77Compiler
        if child.OBJCCompiler != None:
            self.OBJCCompiler = child.OBJCCompiler
        if child.OBJCPreProcessor != None:
            self.OBJCPreProcessor = child.OBJCPreProcessor
        if child.OBJCXXCompiler != None:
            self.OBJCXXCompiler = child.OBJCXXCompiler
        if child.OBJCXXPreProcessor != None:
            self.OBJCXXPreProcessor = child.OBJCXXPreProcessor
        if child.optimize != None:
            self.optimize = child.optimize
        if child.CFlags != None:
            self.CFlags = child.CFlags
        if child.CDefines != None:
            self.CDefines = child.CDefines
        if child.CXXFlags != None:
            self.CXXFlags = child.CXXFlags
        if child.CPPFlags != None:
            self.CPPFlags = child.CPPFlags
        if child.FFlags != None:
            self.FFlags = child.FFlags
        if child.FLibs != None:
            self.FLibs = child.FLibs
        if child.F77Flags != None:
            self.F77Flags = child.F77Flags
        if child.F77Libs != None:
            self.F77Libs = child.F77Libs
        if child.LinkerFlags != None:
            self.LinkerFlags = child.LinkerFlags
        if child.LinkerFlagsEXE != None:
            self.LinkerFlagsEXE = child.LinkerFlagsEXE
        if child.LinkerFlagsShared != None:
            self.LinkerFlagsShared = child.LinkerFlagsShared
        if child.LinkerFlagsModule != None:
            self.LinkerFlagsModule = child.LinkerFlagsModule
        if child.OBJCFlags != None:
            self.OBJCFlags = child.OBJCFlags
        if child.OBJCXXFlags != None:
            self.OBJCXXFlags = child.OBJCXXFlags

class OverrideGroup(object):
    def __init__(self):
        self.compiler = ""
        self.optimization = ""
        self.parallel = ""
        self.overrides = Overrides()

def readGroups(filename):
    groups = list()
    overrideGroup = None
    tokenizer = Tokenizer(filename)
    tokenizer.tokenize()
    tokens = tokenizer.tokens
    i = 0
    lengthOfTokens = len(tokens)

    while i < lengthOfTokens:
        #Syntax start: <compiler group name>, <optimization group name>, <parallel group name>
        if tokens[i].type == TokenType.Identifier:
            overrideGroup = OverrideGroup()
            overrideGroup.compiler = tokens[i].value
        else:
            logger.writeError("Expected Compiler Override group name '" + tokens[i].value + "'", filePath=filename, exitProgram=True)
        i += 1
        if i >= lengthOfTokens:
            logger.writeError("Parsing ended inside of Override group. Please finish file and re-run MixDown.", filePath=filename, exitProgram=True)

        if not (tokens[i].type == TokenType.Symbol and tokens[i].value == ','):
            logger.writeError("Expected ',' got '" + tokens[i].value + "'", filePath=filename, exitProgram=True)
        i += 1
        if i >= lengthOfTokens:
            logger.writeError("Parsing ended inside of Override group. Please finish file and re-run MixDown.", filePath=filename, exitProgram=True)

        if tokens[i].type == TokenType.Identifier or (tokens[i].type == TokenType.Symbol and tokens[i].value == '*'):
            overrideGroup.optimization = tokens[i].value
        else:
            logger.writeError("Expected either Optimization Override group name or '*' got '" + tokens[i].value + "'", filePath=filename, exitProgram=True)
        i += 1
        if i >= lengthOfTokens:
            logger.writeError("Parsing ended inside of Override group. Please finish file and re-run MixDown.", filePath=filename, exitProgram=True)

        if not (tokens[i].type == TokenType.Symbol and tokens[i].value == ','):
            logger.writeError("Expected ',' got '" + tokens[i].value + "'", filePath=filename, exitProgram=True)
        i += 1
        if i >= lengthOfTokens:
            logger.writeError("Parsing ended inside of Override group. Please finish file and re-run MixDown.", filePath=filename, exitProgram=True)

        if tokens[i].type == TokenType.Identifier or (tokens[i].type == TokenType.Symbol and tokens[i].value == '*'):
            overrideGroup.parallel = tokens[i].value
        else:
            logger.writeError("Expected either Parallel Override group name or '*' got '" + tokens[i].value + "'", filePath=filename, exitProgram=True)
        i += 1
        if i >= lengthOfTokens:
            logger.writeError("Parsing ended inside of Override group. Please finish file and re-run MixDown.", filePath=filename, exitProgram=True)
        #Syntax end

        #Syntax start:
        #{
        #  <Identifier> = <string>
        #   ...
        #  <Identifier> = <string>
        #}
        if not (tokens[i].type == TokenType.Symbol and tokens[i].value == '{'):
            logger.writeError("Expected '{' got '" + tokens[i].value + "'", filePath=filename, exitProgram=True)
        i += 1
        if i >= lengthOfTokens:
            logger.writeError("Parsing ended inside of Override group. Please finish file and re-run MixDown.", filePath=filename, exitProgram=True)

        while True:
            if tokens[i].type == TokenType.Symbol and tokens[i].value == '}':
                i += 1
                break
            overrideName = ""
            overrideValue = ""

            #Syntax start:  <Identifier> = <string>
            if not tokens[i].type == TokenType.Identifier:
                logger.writeError("Expected Override identifier got '" + tokens[i].value + "'", filePath=filename, exitProgram=True)
            overrideNameOriginal = tokens[i].value
            overrideName = tokens[i].value.lower()
            i += 1
            if i >= lengthOfTokens:
                logger.writeError("Parsing ended inside of Override group. Please finish file and re-run MixDown.", filePath=filename, exitProgram=True)

            if not (tokens[i].type == TokenType.Symbol and tokens[i].value == '='):
                logger.writeError("Expected '=' got '" + tokens[i].value + "'", filePath=filename, exitProgram=True)
            i += 1
            if i >= lengthOfTokens:
                logger.writeError("Parsing ended inside of Override group. Please finish file and re-run MixDown.", filePath=filename, exitProgram=True)

            if not tokens[i].type == TokenType.String:
                logger.writeError("Expected Override value string got '" + tokens[i].value + "'", filePath=filename, exitProgram=True)
            overrideString = tokens[i].value
            i += 1
            if i >= lengthOfTokens:
                logger.writeError("Parsing ended inside of Override group. Please finish file and re-run MixDown.", filePath=filename, exitProgram=True)

            #Compiler Overrides
            if overrideName == "ccompiler":
                overrideGroup.overrides.CCompiler = overrideString
            elif overrideName == "cpreprocessor":
                overrideGroup.overrides.CPreProcessor = overrideString
            elif overrideName == "cxxcompiler":
                overrideGroup.overrides.CXXCompiler = overrideString
            elif overrideName == "fcompiler":
                overrideGroup.overrides.FCompiler = overrideString
            elif overrideName == "f77compiler":
                overrideGroup.overrides.F77Compiler = overrideString
            elif overrideName == "objccompiler":
                overrideGroup.overrides.OBJCCompiler = overrideString
            elif overrideName == "objcxxcompiler":
                overrideGroup.overrides.OBJCXXCompiler = overrideString
            elif overrideName == "objcxxpreprocessor":
                overrideGroup.overrides.OBJCXXPreProcessor = overrideString
            #Optimization Overrides
            elif overrideName == "optimize":
                lowered = overrideString.lower()
                if lowered == "true" or lowered == "false":
                    overrideGroup.overrides.optimize = lowered
                else:
                    logger.writeError("Optimize pair expected either 'True' or 'False' got '" + overrideString + "'", filePath=filename, exitProgram=True)
            elif overrideName == "cflags":
                overrideGroup.overrides.CFlags = overrideString
            elif overrideName == "cdefines":
                overrideGroup.overrides.CDefines = overrideString
            elif overrideName == "cpreprocessorflags":
                overrideGroup.overrides.CPPFlags = overrideString
            elif overrideName == "cxxflags":
                overrideGroup.overrides.CXXFlags = overrideString
            elif overrideName == "fflags":
                overrideGroup.overrides.FFlags = overrideString
            elif overrideName == "flibs":
                overrideGroup.overrides.FLibs = overrideString
            elif overrideName == "f77flags":
                overrideGroup.overrides.F77Flags = overrideString
            elif overrideName == "f77libs":
                overrideGroup.overrides.F77Libs = overrideString
            elif overrideName == "linkerflags":
                overrideGroup.overrides.LinkerFlags = overrideString
            elif overrideName == "linkerflagsexe":
                overrideGroup.overrides.LinkerFlagsEXE = overrideString
            elif overrideName == "linkerflagsmodule":
                overrideGroup.overrides.LinkerFlagsModule = overrideString
            elif overrideName == "linkerflagsshared":
                overrideGroup.overrides.LinkerFlagsShared = overrideString
            elif overrideName == "objcflags":
                overrideGroup.overrides.OBJCFlags = overrideString
            elif overrideName == "objcxxflags":
                overrideGroup.overrides.OBJCXXFlags = overrideString
            #Syntax end
            else:
                logger.writeError("Unknown override pair:\n\t" + overrideNameOriginal + " = " + overrideString, filePath=filename, exitProgram=True)

        #Syntax end

        groups.append(overrideGroup)
    return groups

def selectGroups(groups, options):
    compilerGroupSet = False
    optimizationGroupSet = False
    parallelGroupSet = False
    overrides = Overrides()

    for group in groups:
        if group.compiler.lower() == options.compilerGroupName and group.optimization == '*' and group.parallel == '*':
            if compilerGroupSet:
                logger.writeError("Duplicate override group found: " + group.compiler + ",* ,*", filePath=options.overrideFile, exitProgram=True)
            overrides = group.overrides
            compilerGroupSet = True
    for group in groups:
        if group.optimization.lower() == options.optimizationGroupName:
            if optimizationGroupSet:
                logger.writeError("Duplicate override group found: " + group.compiler + ", " + group.optimization + ",*", filePath=options.overrideFile, exitProgram=True)
            overrides.combine(group.overrides)
            optimizationGroupSet = True
    for group in groups:
        if group.parallel.lower() == options.parallelGroupName:
            if parallelGroupSet:
                logger.writeError("Duplicate override group found: " + group.compiler + ", " + group.optimization + group.parallel, filePath=options.overrideFile, exitProgram=True)
            overrides.combine(group.overrides)
            parallelGroupSet = True

    defines.setOverrideDefines(options, overrides)
