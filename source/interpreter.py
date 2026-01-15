import mathPiege
import os
import time

# Hardcoded math operator syntaxes
mathSyntax = ["sum(", "dif(", "sub(", "pro(", "rat(",
              "quo(", "pow(", "mod(", "fact(", "abs(",
              "log(", "sqrt(", "root(", "floor(", "ceil(",
              "round(", "floorRat(", "ceilRat(", "sin(", "cos(",
              "tan(", "cot(", "sec(", "csc(", "asin(",
              "acos(", "atan(", "acot(", "asec(", "acsc(",
              "sinh(", "cosh(", "tanh(", "coth(", "sech(",
              "csch(", "detMtrx(", "lenVect(", "dotVect(", "exp(",
              "ln(", "rand(", "randInt(", "sign(", "squareSum(",
              "cubeSum(", "max(", "min(", "aMean(", "gMean(",
              "agMean(", "median(", "mode(", "quart1(", "quart3(",
              "iqr(", "meanAbsDev(", "medianAbsDev(", "modeAbsDev(",
              "popVar(", "popStdDev(", "samVar(", "samStdDev("]

compSyntax = ["less(", "more(", "equal(",
              "notless(", "notmore(", "notequal("]

# Hardcoded characters to check for each type of data
numberType = "0123456789.+-e"
charType = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

def foundSyntax(data, mainIndex, string):
    if all(data[mainIndex + i] == string[i] for i in range(len(string))):
        return True

def lineByIndex(charIndex, tempLineBreak):
    lineIndex = 0
    for i, x in enumerate(tempLineBreak):
        if tempLineBreak[i-1] < charIndex and charIndex < x:
            return i

def executeCode(data):
    
    # Temporary lists for variable-value, line break indices, and ignored index pairs
    tempVariable     = ["NullValue", "ComplexInfinity", "pi"]
    tempValue        = [float("0"), float("inf"), 3.1415926535897932]
    tempLineBreak    = [0]
    tempIgnoreIndex1 = []
    tempIgnoreIndex2 = []

    # Default output mode
    outputMode = "none"

    # Start executing code

    for charIndex in range(len(data)):
        if data[charIndex] == "\n":
            tempLineBreak.append(charIndex)

    for charIndex in range(len(data)):
        
        # Detect call for input-output interpreter
        if foundSyntax(data, charIndex, "io{"):

            charIndex2 = charIndex+len("io{")
            while charIndex2 < len(data):

                # Detect input
                if foundSyntax(data, charIndex2, "input[\""):
                    destinationList = []
                    for charIndex3 in range(charIndex2+len("input[\""), len(data)):
                        if foundSyntax(data, charIndex3, "\"]"):
                            charIndex2 = charIndex3+1
                            break
                        else: destinationList.append(data[charIndex3])
                    inputDir = ''.join(destinationList)
                    inputList = open(inputDir, "r").readlines()
                    for line in inputList:
                        assignIndex = line.find("=")
                        varNameList = [line[i] for i in range(assignIndex) if line[i] != " "]
                        valueList = [line[i] for i in range(assignIndex + 1, len(line)) if line[i] != " " and line[i] != "\n"]
                        tempVariable.append(''.join(varNameList))
                        tempValue.append(float(''.join(valueList)))

                # Detect output type (to interpreter / to file destination)
                elif foundSyntax(data, charIndex2, "output[interpreter];"):
                    outputMode = "interpreter"
                    
                elif foundSyntax(data, charIndex2, "output[directory; \""):
                    outputMode = "directory"
                    destinationList = []
                    for charIndex3 in range(charIndex2+len("output[directory; \""), len(data)):
                        if foundSyntax(data, charIndex3, "\"]"):
                            charIndex2 = charIndex3+1
                            break
                        else: destinationList.append(data[charIndex3])
                    outputDir = ''.join(destinationList)
                    with open(outputDir, "w", encoding="utf-8") as file:
                        file.write("")

                # Detect end of io{} function
                elif foundSyntax(data, charIndex2, "};"):
                    charIndex = charIndex2+1
                    char = data[charIndex2+1]
                    break

                charIndex2 += 1

        # Detect call for math operator
        if foundSyntax(data, charIndex, "op{"):

            charIndex2 = charIndex+len("op{")
            while charIndex2 < len(data):

                # Detect for ignored character indices
                if len(tempIgnoreIndex1) != 0:
                    try:
                        index = tempIgnoreIndex1.index(charIndex2)
                        if any(charIndex2 == indexToIgnore for indexToIgnore in range(tempIgnoreIndex1[index], tempIgnoreIndex2[index])):
                            charIndex2 = tempIgnoreIndex2[index]
                    except Exception:
                        pass

                # Detect do[] function
                if foundSyntax(data, charIndex2, "do["):

                    # Preparation
                    
                    indentLevel = 0
                    tempOp = []
                    tempIndentOp = []
                    tempFreqOp = []

                    # Read from code to write to tempCommand

                    endCodeIndex = tempLineBreak[lineByIndex(charIndex2, tempLineBreak)]
                    tempCode = ''.join([x for i, x in enumerate(data) if i >= charIndex2 + len("do[") and i < endCodeIndex])

                    endCommandIndex = tempCode.find(";")
                    tempCommand = ''.join([x for i, x in enumerate(tempCode) if i < endCommandIndex])

                    charIndex2 += len(tempCommand) + len("do[;")

                    for charIndex3, char in enumerate(tempCommand):
                        if tempCommand.find("(") == -1:
                            break
                        for syntax in mathSyntax:
                            if foundSyntax(tempCommand, charIndex3, syntax):
                                tempOp.append(syntax)
                                indentLevel += 1
                                tempIndentOp.append(indentLevel)
                                tempFreqOp.append(tempOp.count(syntax))
                                break
                        if char == ")":
                            indentLevel -= 1

                    # Run tempCommand while # of operators left is not 0
                    while len(tempOp) != 0:

                        # Find operator whose indentLevel is highest
                        maxIndent = max(tempIndentOp)
                        maxIndex = tempIndentOp.index(maxIndent)
                        functionIndex = 0
                        tempFreqIndex = 0
                        for charIndex3 in range(len(tempCommand)):
                            if tempFreqIndex == tempFreqOp[maxIndex] + 1: break
                            elif all(tempCommand[charIndex3+i] == tempOp[maxIndex][i] for i in range(len(tempOp[maxIndex]))):
                                functionIndex = charIndex3
                                tempFreqIndex += 1

                        # Read tempCommand and run said operator
                        indentLevel = 0
                        for charIndex3 in range(functionIndex+len(tempOp[maxIndex]), len(tempCommand)):

                            # Get literal input
                            if tempCommand[charIndex3] == ")": break
                            
                            lastInstance = 0
                            tempValueOp = []
                            tempValueList = []
                            
                            for charIndex4 in range(charIndex3, len(tempCommand)):
                                if tempCommand[charIndex4] == ")":
                                    tempValueOp.append(''.join(tempValueList))
                                    lastInstance = charIndex4 + 1
                                    break
                                elif tempCommand[charIndex4] == " ":
                                    continue
                                elif tempCommand[charIndex4] == ",":
                                    tempValueOp.append(''.join(tempValueList))
                                    tempValueList = []
                                else: tempValueList.append(tempCommand[charIndex4])

                            # Translate to float if input is of numberType or get values from variable if input is of text
                            tempValueOp2 = []

                            for index in range(len(tempValueOp)):
                                if all(tempValueOp[index][i] in numberType for i in range(len(tempValueOp[index]))):
                                    tempValueOp2.append(float(tempValueOp[index]))
                                else:
                                    try:
                                        varValue = tempValue[tempVariable.index(tempValueOp[index])]
                                        tempValueOp2.append(varValue)
                                    except Exception:
                                        errorAtLine = lineByIndex(charIndex2, tempLineBreak)
                                        print(f"NoVariable, line {errorAtLine}: Variable \"{''.join(tempValueOp)}\" does not exist.")
                                        return None                                        

                            # Detect function and run
                            code = getattr(mathPiege, tempOp[maxIndex][:-1])
                            try:
                                answer = code(tempValueOp2)
                            except Exception:
                                errorAtLine = lineByIndex(charIndex2, tempLineBreak)
                                print(f"InvalidCommand, line {errorAtLine}: Cannot execute command \"{tempCommand}\".")
                                return None

                            # Remove part of tempCommand which has been executed                                
                            for charIndex4 in range(charIndex3, lastInstance):
                                tempCommand = tempCommand[:charIndex3] + tempCommand[charIndex3 + 1:]
                            tempCommand = tempCommand[:charIndex3-len(tempOp[maxIndex])] + str(answer) + tempCommand[charIndex3:]

                            tempOp.pop(maxIndex)
                            tempIndentOp.pop(maxIndex)
                            tempFreqOp.pop(maxIndex)
                            break

                    # Get variable name
                    tempVarList = []
                    
                    for charIndex3 in range(charIndex2, len(data)):
                        if foundSyntax(data, charIndex3, "];"):
                            charIndex2 = charIndex3 + 2
                            break
                        elif data[charIndex3] == " ": continue
                        else: tempVarList.append(data[charIndex3])

                    varName = ''.join(tempVarList)
                    if varName not in tempVariable:
                        tempVariable.append(''.join(tempVarList))
                        if all(tempCommand[i] in numberType for i in range(len(tempCommand))):
                            tempValue.append(float(tempCommand))
                        else:
                            varValue = tempValue[tempVariable.index(tempCommand)]
                            tempValue.append(float(varValue))
                    else:
                        if all(tempCommand[i] in numberType for i in range(len(tempCommand))):
                            tempValue[tempVariable.index(varName)] = float(tempCommand)
                        else:
                            try:
                                varValue = tempValue[tempVariable.index(tempCommand)]
                                tempValue[tempVariable.index(varName)] = float(varValue)
                            except Exception:
                                errorAtLine = lineByIndex(charIndex2, tempLineBreak)
                                print(f"InvalidAssignment, line {errorAtLine}: Cannot assign \"{tempCommand}\" to variable \"{varName}\".")
                                return None
                        
                # Detect return[] function
                elif foundSyntax(data, charIndex2, "return["):
                    tempVarList = []
                    for charIndex3 in range(charIndex2+len("return["), len(data)):
                        if foundSyntax(data, charIndex3, "];"):
                            break
                        elif data[charIndex3] == " ": continue
                        else: tempVarList.append(data[charIndex3])
                    if outputMode == "interpreter":
                        print(f"{''.join(tempVarList)} = {tempValue[tempVariable.index(''.join(tempVarList))]}")
                    elif outputMode == "directory":
                        with open(outputDir, "a+", encoding="utf-8") as file:
                            file.write(f"{''.join(tempVarList)} = {tempValue[tempVariable.index(''.join(tempVarList))]}\n")

                # Detect print[] function
                elif foundSyntax(data, charIndex2, "print["):
                    tempPrint = []
                    tempVarList = []
                    for charIndex3 in range(charIndex2+len("print["), len(data)):
                        if foundSyntax(data, charIndex3, "];"):
                            tempPrint.append(''.join(tempVarList))
                            break
                        elif data[charIndex3] == ";":
                            tempPrint.append(''.join(tempVarList))
                            tempVarList = []
                        else: tempVarList.append(data[charIndex3])

                    for index in range(len(tempPrint)):
                        if "\"" in tempPrint[index]:
                            tempPrint[index] = ''.join([x for x in tempPrint[index] if x != "\""])
                        elif "\"" not in tempPrint[index] and " " in tempPrint[index][0]:
                            tempPrint[index] = str(tempValue[tempVariable.index(tempPrint[index][1:])])

                    if outputMode == "interpreter":
                        print(''.join(tempPrint))
                    elif outputMode == "directory":
                        with open(outputDir, "a+", encoding="utf-8") as file:
                            file.write(''.join(tempPrint) + "\n")

                # Detect deleteVar[] function
                elif foundSyntax(data, charIndex2, "deleteVar["):
                    tempVarList = []
                    for charIndex3 in range(charIndex2+len("deleteVar["), len(data)):
                        if foundSyntax(data, charIndex3, "];"):
                            break
                        elif data[charIndex3] == " ": continue
                        else: tempVarList.append(data[charIndex3])
                    tempValue.pop(tempVariable.index(''.join(tempVarList)))
                    tempVariable.pop(tempVariable.index(''.join(tempVarList)))

                # Detect setCursor[] function
                elif foundSyntax(data, charIndex2, "setCursor["):

                    # Get type                    
                    indexToGo = charIndex2
                    tempTypeList = []
                    tempIndexList = []
                    tempCompList = []
                    
                    charIndex3 = charIndex2+len("setCursor[")

                    while charIndex3 < len(data):
                        if data[charIndex3] == ";":
                            typeToUse = ''.join(tempTypeList)
                            break
                        else: tempTypeList.append(data[charIndex3])
                        charIndex3 += 1

                    # Get index                    
                    charIndex3 += 2
                    while charIndex3 < len(data):
                        if data[charIndex3] == ";": break
                        else: tempIndexList.append(data[charIndex3])
                        charIndex3 += 1

                    if all(''.join(tempIndexList)[i] in numberType for i in range(len(tempIndexList))):
                        indexToGo = int(''.join(tempIndexList))
                    else:
                        varValue = tempValue[tempVariable.index(''.join(tempIndexList))]
                        indexToGo = varValue
                        
                    # Get condition
                    lastInstance = 0
                    charIndex3 += 2
                    while charIndex3 < len(data):
                        if foundSyntax(data, charIndex3, "];"):
                            tempComparator = ''.join(tempCompList)
                            lastInstance = charIndex3
                            break
                        else: tempCompList.append(data[charIndex3])
                        charIndex3 += 1

                    for index in compSyntax:
                        if all(tempComparator[i] == index[i] for i in range(len(index))):
                            tempCompOp = index
                            break

                    tempValueComp = []
                    tempInputList = []
                    
                    for charIndex3 in range(len(tempCompOp), len(tempComparator)):
                        if tempComparator[charIndex3] == ")":
                            tempValueComp.append(''.join(tempInputList))
                            break
                        elif tempComparator[charIndex3] == " ":
                            continue
                        elif tempComparator[charIndex3] == ",":
                            tempValueComp.append(''.join(tempInputList))
                            tempInputList = []
                        else: tempInputList.append(tempComparator[charIndex3])

                    tempValueComp2 = []

                    for index in range(len(tempValueComp)):
                        if all(tempValueComp[index][i] in numberType for i in range(len(tempValueComp[index]))):
                            tempValueComp2.append(float(tempValueComp[index]))
                        else:
                            varValue = tempValue[tempVariable.index(tempValueComp[index])]
                            tempValueComp2.append(varValue)

                    verdict = False

                    # Detect function and run
                    code = getattr(mathPiege, tempCompOp[:-1])
                    try:
                        verdict = code(tempValueComp2)
                    except Exception:
                        errorAtLine = lineByIndex(charIndex2, tempLineBreak)
                        str(input(f"InvalidComparator, line {errorAtLine}: Cannot execute comparison \"{tempComparator}\"."))
                        return None

                    if verdict == True:
                        if typeToUse == "char":
                            charIndex2 = indexToGo - 1
                        elif typeToUse == "line":
                            charIndex2 = tempLineBreak[indexToGo - 1]
                    elif verdict == False:
                        charIndex2 = lastInstance

                # Detect moveCursor[] function
                elif foundSyntax(data, charIndex2, "moveCursor["):

                    # Get type                    
                    indexToGo = charIndex2
                    tempTypeList = []
                    tempIndexList = []
                    tempCompList = []
                    
                    charIndex3 = charIndex2+len("moveCursor[")

                    while charIndex3 < len(data):
                        if data[charIndex3] == ";":
                            typeToUse = ''.join(tempTypeList)
                            break
                        else: tempTypeList.append(data[charIndex3])
                        charIndex3 += 1

                    # Get amount                    
                    charIndex3 += 2
                    while charIndex3 < len(data):
                        if data[charIndex3] == ";": break
                        else: tempIndexList.append(data[charIndex3])
                        charIndex3 += 1

                    if all(''.join(tempIndexList)[i] in numberType for i in range(len(tempIndexList))):
                        indexToGo = int(''.join(tempIndexList))
                    else:
                        varValue = tempValue[tempVariable.index(''.join(tempIndexList))]
                        indexToGo = varValue                   
                        
                    # Get condition
                    lastInstance = 0
                    charIndex3 += 2
                    while charIndex3 < len(data):
                        if foundSyntax(data, charIndex3, "];"):
                            tempComparator = ''.join(tempCompList)
                            lastInstance = charIndex3
                            break
                        else: tempCompList.append(data[charIndex3])
                        charIndex3 += 1

                    for index in compSyntax:
                        if all(tempComparator[i] == index[i] for i in range(len(index))):
                            tempCompOp = index
                            break

                    tempValueComp = []
                    tempInputList = []
                    
                    for charIndex3 in range(len(tempCompOp), len(tempComparator)):
                        if tempComparator[charIndex3] == ")":
                            tempValueComp.append(''.join(tempInputList))
                            break
                        elif tempComparator[charIndex3] == " ":
                            continue
                        elif tempComparator[charIndex3] == ",":
                            tempValueComp.append(''.join(tempInputList))
                            tempInputList = []
                        else: tempInputList.append(tempComparator[charIndex3])

                    tempValueComp2 = []

                    for index in range(len(tempValueComp)):
                        if all(tempValueComp[index][i] in numberType for i in range(len(tempValueComp[index]))):
                            tempValueComp2.append(float(tempValueComp[index]))
                        else:
                            varValue = tempValue[tempVariable.index(tempValueComp[index])]
                            tempValueComp2.append(varValue)

                    # Detect function and run
                    code = getattr(mathPiege, tempCompOp[:-1])
                    try:
                        verdict = code(tempValueComp2)
                    except Exception:
                        errorAtLine = lineByIndex(charIndex2, tempLineBreak)
                        print(f"InvalidComparator, line {errorAtLine}: Cannot execute comparison \"{tempComparator}\".")
                        return None

                    if verdict == True:
                        if typeToUse == "char":
                            charIndex2 += indexToGo
                        elif typeToUse == "line":
                            tempLineBreakValue = 0
                            for charIndex3 in range(0, charIndex2):
                                if data[charIndex3] == "\n":
                                    tempLineBreakValue += 1
                            charIndex2 = tempLineBreak[tempLineBreakValue + indexToGo]
                    elif verdict == False:
                        charIndex2 = lastInstance
                
                # Detect getIndex[] function
                elif foundSyntax(data, charIndex2, "getIndex["):
                    tempVarList = []
                    
                    for charIndex3 in range(charIndex2+len("getIndex["), len(data)):
                        if foundSyntax(data, charIndex3, "];"):
                            for charIndex4 in range(charIndex3+len("];"), len(data)):
                                if data[charIndex4] in charType:
                                    indexToGet = charIndex4
                                    break
                            break
                        elif data[charIndex3] == " ": continue
                        else: tempVarList.append(data[charIndex3])

                    varName = ''.join(tempVarList)
                    if varName not in tempVariable:
                        tempVariable.append(''.join(tempVarList))
                        tempValue.append(indexToGet)
                    else:
                        tempValue[tempVariable.index(varName)] = indexToGet

                # Detect ignoreIndex[] function
                elif foundSyntax(data, charIndex2, "ignoreIndex["):
                    
                    tempIndexList = []

                    # Get index1
                    charIndex3 = charIndex2 + len("ignoreIndex[")
                    while data[charIndex3] != ";":
                        if data[charIndex3] == " ": continue
                        else: tempIndexList.append(data[charIndex3])
                        charIndex3 += 1

                    if all(tempIndexList[i] in numberType for i in range(len(tempIndexList))):
                        tempIgnoreIndex1.append(int(''.join(tempIndexList)))
                    else:
                        varValue = tempValue[tempVariable.index(''.join(tempIndexList))]
                        tempIgnoreIndex1.append(int(varValue))
                    tempIndexList = []

                    # Get index2
                    charIndex3 += 2
                    while data[charIndex3] != "]":
                        if data[charIndex3] == " ": continue
                        else: tempIndexList.append(data[charIndex3])
                        charIndex3 += 1

                    if all(tempIndexList[i] in numberType for i in range(len(tempIndexList))):
                        tempIgnoreIndex2.append(int(''.join(tempIndexList)))
                    else:
                        varValue = tempValue[tempVariable.index(''.join(tempIndexList))]
                        tempIgnoreIndex2.append(int(varValue))
                    tempIndexList = []

                    # Check if [index1, index2] in other elements of tempIgnore
                    currentLen = len(tempIgnoreIndex1) - 1
                    if any(tempIgnoreIndex1[i] == tempIgnoreIndex1[currentLen] and tempIgnoreIndex2[i] == tempIgnoreIndex2[currentLen]  for i in range(currentLen+1) for j in range(2) if i != currentLen):
                        tempIgnoreIndex1.pop(currentLen)
                        tempIgnoreIndex2.pop(currentLen)

                # Detect endCode[] function
                elif foundSyntax(data, charIndex2, "endCode["):
                    charIndex2 = len(data) - 1
                
                # Detect end of op{} function
                elif foundSyntax(data, charIndex2, "};"):
                    break

                charIndex2 += 1

if __name__ == "__main__":
    piegeFiles = [f for f in os.listdir('.') if f.endswith('.piege')]
    for fileName in piegeFiles:
        print("* Running", fileName)
        file = open(fileName, "r")
        data = ''.join(file.read())
        timeStart = time.time()
        executeCode(data)
        timeEnd = time.time()
        file.close()
        print(f"Program \"{fileName}\" finished. Total runtime: {round(timeEnd - timeStart, 5)}s.\n")
    str(input(""))
