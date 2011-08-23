from tokenizer import Tokenizer, TokenType
import logger

class CompilerOverrides(object):
    def __init__(self):
        self.CCompiler = ""
        self.CPreProcessor = ""
        self.CXXCompiler = ""
        self.FCompiler = ""
        self.F77Compiler = ""
        self.OBJCCompiler = ""
        self.OBJCPreProcessor = ""
        self.OBJCXXCompiler = ""
        self.OBJCXXPreProcessor = ""

class OptimizationOverrides(object):
    def __init__(self):
        self.optimizationLevel = ""
        self.debugInfo = False

class ParallelOverrides(object):
    def __init__(self):
        self.library = ""

class OverrideGroup(object):
    def __init__(self):
        self.compiler = "", None
        self.optimization = "", None
        self.parallel = "", None

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
        if tokens[i].type == TokenType.Identifier or (tokens[i].type == TokenType.Symbol and tokens[i].value == '*'):
            overrideGroup = OverrideGroup()
            overrideGroup.compiler = tokens[i].value, CompilerOverrides()
        else:
            logger.writeError("Expected either Compiler Override group name or '*' got '" + tokens[i].value + "'", filePath=filename, exitProgram=True)
        i += 1
        if i >= lengthOfTokens:
            logger.writeError("Parsing ended inside of Override group. Please finish file and re-run MixDown.", filePath=filename, exitProgram=True)

        if not (tokens[i].type == TokenType.Symbol and tokens[i].value == ','):
            logger.writeError("Expected ',' got '" + tokens[i].value + "'", filePath=filename, exitProgram=True)
        i += 1
        if i >= lengthOfTokens:
            logger.writeError("Parsing ended inside of Override group. Please finish file and re-run MixDown.", filePath=filename, exitProgram=True)

        if tokens[i].type == TokenType.Identifier or (tokens[i].type == TokenType.Symbol and tokens[i].value == '*'):
            overrideGroup.optimization = tokens[i].value, OptimizationOverrides()
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
            overrideGroup.parallel = tokens[i].value, ParallelOverrides()
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
                overrideGroup.compiler[1].CCompiler = overrideString
            elif overrideName == "cpreprocessor":
                overrideGroup.compiler[1].CPreProcessor = overrideString
            elif overrideName == "cxxcompiler":
                overrideGroup.compiler[1].CXXCompiler = overrideString
            elif overrideName == "fcompiler":
                overrideGroup.compiler[1].FCompiler = overrideString
            elif overrideName == "f77compiler":
                overrideGroup.compiler[1].F77Compiler = overrideString
            elif overrideName == "objcCompiler":
                overrideGroup.compiler[1].OBJCCompiler = overrideString
            elif overrideName == "objcpreprocessor":
                overrideGroup.compiler[1].OBJCPreProcessor = overrideString
            elif overrideName == "objcxxcompiler":
                overrideGroup.compiler[1].OBJCXXCompiler = overrideString
            elif overrideName == "objcxxpreprocessor":
                overrideGroup.compiler[1].OBJCXXPreProcessor = overrideString
            #Optimization Overrides
            elif overrideName == "optimizationlevel":
                overrideGroup.optimization[1].optimizationLevel = overrideString
            elif overrideName == "debuginfo":
                overrideGroup.optimization[1].debugInfo = overrideString
            #Syntax end
            else:
                logger.writeError("Unknown override pair:\n\t" + overrideNameOriginal + " = " + overrideString, filePath=filename, exitProgram=True)

        #Syntax end

        groups.append(overrideGroup)
    return groups
