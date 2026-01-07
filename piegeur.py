
### PYTHON INTERPRETER FOR PIÈGE
### VERSION 0.1.5 (07 JANUARY 2026)
### AUTHOR: RANDOMMAERKS (BAO NGUYEN)
###
### LICENSED UNDER THE MIT LICENSE
### CHECK OUT LICENSE.TXT FOR MORE INFORMATION

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
              "ln("]

compSyntax = ["less(", "more(", "equal(",
              "notless(", "notmore(", "notequal("]

# Hardcoded characters to check for each type of data
numberType = "0123456789.+-e"
charType = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

piegeFiles = [f for f in os.listdir('.') if f.endswith('.piege')]

for fileIndex in piegeFiles:
    
    # Temporary lists for variables and values through related index
    tempVariable = ["NullValue", "ComplexInfinity", "pi"]
    tempValue    = [float("0"), float("inf"), 3.1415926535897932]

    # Temporary list for position of line breaks
    tempLineBreak = [0]

    # Temporary lists for indices to ignore
    tempIgnoreIndex1 = []
    tempIgnoreIndex2 = []

    # Default input, output
    inputMode = "none"
    outputMode = "none"

    print("* Running", fileIndex)
    data = ''.join(open(fileIndex, "r").read())
    timeStart = time.time()

    for charIndex in range(len(data)):
        if data[charIndex] == "\n":
            tempLineBreak.append(charIndex)

    for charIndex in range(len(data)):
        
        # Detect call for input-output interpreter
        if all(data[charIndex+i] == "io{"[i] for i in range(len("io{"))):

            charIndex2 = charIndex+len("io{")
            while charIndex2 < len(data):

                # Detect output type (to interpreter / to file destination)
                if all(data[charIndex2+i] == "output[interpreter];"[i] for i in range(len("output[interpreter];"))):
                    outputMode = "interpreter"
                    
                elif all(data[charIndex2+i] == "output[directory; \""[i] for i in range(len("output[directory; \""))):
                    outputMode = "directory"
                    destinationList = []
                    for charIndex3 in range(charIndex2+len("output[directory; \""), len(data)):
                        if data[charIndex3] == "\"" and data[charIndex3+1] == "]":
                            charIndex2 = charIndex3+1
                            char = data[charIndex3+1]
                            break
                        else: destinationList.append(data[charIndex3])
                    outputDir = ''.join(destinationList)
                    with open(outputDir, "w", encoding="utf-8") as file:
                        file.write("")

                # Detect end of io{} function
                if data[charIndex2] == "}" and data[charIndex2+1] == ";":
                    charIndex = charIndex2+1
                    char = data[charIndex2+1]
                    break

                charIndex2 += 1

        # Detect call for math operator
        if all(data[charIndex+i] == "op{"[i] for i in range(len("op{"))):

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
                if all(data[charIndex2+i] == "do["[i] for i in range(len("do["))):

                    # Preparation
                    
                    indentLevel = 0
                    tempOp = []
                    tempIndentOp = []
                    tempCommandList = []
                    tempFreqOp = []

                    # Read from code to write to tempCommand

                    charIndex3 = charIndex2+len("do[")
                    while charIndex3 < len(data):
                        if data[charIndex3] == ";":
                            charIndex2 = charIndex3 + 1
                            break
                        else:
                            foundOp = ""
                            for syntax in mathSyntax:
                                if all(data[charIndex3+i] == syntax[i] for i in range(len(syntax))):
                                    foundOp = syntax
                                    tempOp.append(syntax)
                                    indentLevel += 1
                                    tempIndentOp.append(indentLevel)
                                    tempFreqOp.append(tempOp.count(syntax))
                                    break
                            if data[charIndex3] == ")":
                                indentLevel -= 1
                        if foundOp == "": 
                            tempCommandList.append(data[charIndex3])
                            charIndex3 += 1
                        else:
                            tempCommandList.append(foundOp)
                            charIndex3 += len(foundOp)

                    tempCommand = ''.join(tempCommandList)

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
                                        for index in range(len(tempLineBreak)):
                                            if charIndex2 > tempLineBreak[index] and charIndex2 < tempLineBreak[index+1]:
                                                errorAtLine = index + 1
                                                break
                                        str(input(f"NoVariable, line {errorAtLine}: Variable \"{''.join(tempValueOp)}\" does not exist, returning 0."))
                                        tempValueOp2.append(0)
                                        

                            # Detect function and run

                            code = f"answer = mathPiege.{tempOp[maxIndex]}{tempValueOp2})"
                            try:
                                exec(code)
                            except Exception:
                                for index in range(len(tempLineBreak)):
                                    if charIndex2 > tempLineBreak[index] and charIndex2 < tempLineBreak[index+1]:
                                        errorAtLine = index + 1
                                        break
                                str(input(f"InvalidCommand, line {errorAtLine}: Cannot execute command \"{tempCommand}\"."))

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
                        if all(data[charIndex3+i] == "];"[i] for i in range(len("];"))):
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
                                for index in range(len(tempLineBreak)):
                                    if charIndex2 > tempLineBreak[index] and charIndex2 < tempLineBreak[index+1]:
                                        errorAtLine = index + 1
                                        break
                                str(input(f"InvalidAssignment, line {errorAtLine}: Cannot assign \"{tempCommand}\" to variable \"{varName}\", assigning NullValue."))
                                tempValue[tempVariable.index(varName)] = tempValue[0]
                        
                # Detect return[] function
                elif all(data[charIndex2+i] == "return["[i] for i in range(len("return["))):
                    tempVarList = []
                    for charIndex3 in range(charIndex2+len("return["), len(data)):
                        if all(data[charIndex3+i] == "];"[i] for i in range(len("];"))):
                            break
                        elif data[charIndex3] == " ": continue
                        else: tempVarList.append(data[charIndex3])
                    if outputMode == "interpreter":
                        print(f"{''.join(tempVarList)} = {tempValue[tempVariable.index(''.join(tempVarList))]}")
                    elif outputMode == "directory":
                        with open(outputDir, "a+", encoding="utf-8") as file:
                            file.write(f"{''.join(tempVarList)} = {tempValue[tempVariable.index(''.join(tempVarList))]}\n")

                # Detect print[] function
                elif all(data[charIndex2+i] == "print["[i] for i in range(len("print["))):
                    tempPrint = []
                    tempVarList = []
                    for charIndex3 in range(charIndex2+len("print["), len(data)):
                        if all(data[charIndex3+i] == "];"[i] for i in range(len("];"))):
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
                elif all(data[charIndex2+i] == "deleteVar["[i] for i in range(len("deleteVar["))):
                    tempVarList = []
                    for charIndex3 in range(charIndex2+len("deleteVar["), len(data)):
                        if all(data[charIndex3+i] == "];"[i] for i in range(len("];"))):
                            break
                        elif data[charIndex3] == " ": continue
                        else: tempVarList.append(data[charIndex3])
                    tempValue.pop(tempVariable.index(''.join(tempVarList)))
                    tempVariable.pop(tempVariable.index(''.join(tempVarList)))

                # Detect setCursor[] function
                elif all(data[charIndex2+i] == "setCursor["[i] for i in range(len("setCursor["))):

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
                        if all(data[charIndex3+i] == "];"[i] for i in range(len("];"))):
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

                    code = f"verdict = mathPiege.{tempCompOp}{tempValueComp2})"
                    try:
                        exec(code)
                    except Exception:
                        for index in range(len(tempLineBreak)):
                            if charIndex2 > tempLineBreak[index]:
                                errorAtLine = index + 1
                                break
                        str(input(f"InvalidComparator, line {errorAtLine}: Cannot execute comparison \"{tempComparator}\"."))

                    if verdict == True:
                        if typeToUse == "char":
                            charIndex2 = indexToGo - 1
                        elif typeToUse == "line":
                            charIndex2 = tempLineBreak[indexToGo - 1]
                    elif verdict == False:
                        charIndex2 = lastInstance

                # Detect moveCursor[] function
                elif all(data[charIndex2+i] == "moveCursor["[i] for i in range(len("moveCursor["))):

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
                        if all(data[charIndex3+i] == "];"[i] for i in range(len("];"))):
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

                    code = f"verdict = mathPiege.{tempCompOp}{tempValueComp2})"
                    try:
                        exec(code)
                    except Exception:
                        for index in range(len(tempLineBreak)):
                            if charIndex2 > tempLineBreak[index]:
                                errorAtLine = index + 1
                                break
                        str(input(f"InvalidComparator, line {errorAtLine}: Cannot execute comparison \"{tempComparator}\"."))

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
                elif all(data[charIndex2+i] == "getIndex["[i] for i in range(len("getIndex["))):
                    tempVarList = []
                    
                    for charIndex3 in range(charIndex2+len("getIndex["), len(data)):
                        if all(data[charIndex3+i] == "];"[i] for i in range(len("];"))):
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
                elif all(data[charIndex2+i] == "ignoreIndex["[i] for i in range(len("ignoreIndex["))):
                    
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
                elif all(data[charIndex2+i] == "endCode["[i] for i in range(len("endCode["))):
                    charIndex2 = len(data) - 1
                
                # Detect end of op{} function
                elif data[charIndex2] == "}" and data[charIndex2+1] == ";":
                    break

                charIndex2 += 1
           
    timeEnd = time.time()
    print(f"Program {fileIndex} finished. Total runtime: {round(timeEnd - timeStart, 5)}s.\n")
    
str(input(""))
