import mathPiege
import visualiser
from decimal import *

# -------------------------------
# |     INITIALISE SYNTAXES     |
# -------------------------------

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
              "popVar(", "popStdDev(", "samVar(", "samStdDev(", "neg(",
              "asinh(", "acosh(", "atanh(", "acoth(", "asech(", "acsch("]

compSyntax = ["less(", "more(", "equal(",
              "notless(", "notmore(", "notequal("]

# Hardcoded characters to check for each type of data
numberType = "0123456789.+-Ee"
charType = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

# -----------------------------------
# |     USEFUL STRING FUNCTIONS     |
# -----------------------------------

def foundSyntax(data, mainIndex, string):
    try: return all(data[mainIndex + i] == string[i] for i in range(len(string)))
    except IndexError: return None

def lineByIndex(charIndex, tempLineBreak):
    lineIndex = 0
    for i, x in enumerate(tempLineBreak):
        if tempLineBreak[i-1] <= charIndex and charIndex < x:
            return i

def isNumber(string):
    try:
        Decimal(string)
    except InvalidOperation:
        return False
    verdict = all(string[i] in numberType for i in range(len(string)))
    return verdict

def isChar(string):
    verdict = all(string[i] in charType for i in range(len(string)))
    return verdict

# --------------------------
# |     CODE EXECUTION     |
# --------------------------

def executeCode(data):
    
    # Temporary lists for variable-value, line break indices, and ignored index pairs
    tempVariable     = ["NullValue", "ComplexInfinity", "pi"]
    tempValue        = [Decimal('NaN'), Decimal('Infinity'), Decimal('3.1415926535897932384626433832795')]
    tempLineBreak    = [0]
    tempIgnoreLine   = []

    # Default output mode
    outputMode = "none"

    # Add an additional just-in-case line break at the end
    if data[-1] != "\n":
        data = data + "\n"

    # Find all instances of line break
    for charIndex in range(len(data)):
        if data[charIndex] == "\n":
            tempLineBreak.append(charIndex)
    

    # Start executing code
    charIndex = 0

    while charIndex in range(len(data)):

        # ------------------------
        # Check if line is ignored
        # ------------------------

        if len(tempIgnoreLine) != 0:
            try:
                line = lineByIndex(charIndex, tempLineBreak)
                if line in tempIgnoreLine:
                    charIndex = tempLineBreak[line]
            except Exception as e:
                pass
    

        # ---------------------
        # Detect INPUT function
        # ---------------------

        if foundSyntax(data, charIndex, "INPUT "):

            # Get directory from code
            charIndex2 = charIndex + len("INPUT ")
            while charIndex2 in range(len(data)):
                if data[charIndex2] == "\n":
                    break
                elif foundSyntax(data, charIndex2, "directory"):
                    inputMode = "directory"
                    charIndex2 += len("directory")
                    charIndex3 = charIndex2
                    detectDir = False
                    while charIndex3 in range(len(data)):
                        if data[charIndex3] == ("\"" or "'"):
                            if detectDir == False:
                                detectDir = True
                                firstInstance = charIndex3+1
                            else:
                                detectDir = False
                                lastInstance = charIndex3
                                break
                        charIndex3 += 1
                    inputDir = data[firstInstance:lastInstance]
                charIndex2 += 1
            
            # Read, process and save variable-value pair
            try:
                inputList = open(inputDir, "r").readlines()
            except UnboundLocalError:
                errorAtLine = lineByIndex(charIndex, tempLineBreak)
                print(f"Line {errorAtLine}: Missing input directory (syntax: INPUT `type` = `directory`).")
                return
            except FileNotFoundError:
                errorAtLine = lineByIndex(charIndex, tempLineBreak)
                print(f"Line {errorAtLine}: '{inputDir}' does not exist.")
                return
            for line in inputList:
                if "=" not in line:
                    continue
                line = line.replace(" ", "").replace("\n", "")
                assignIndex = line.find("=")
                variable = line[:assignIndex]
                try:
                    value = Decimal(line[assignIndex+1:])
                except InvalidOperation:
                    errorAtLine = lineByIndex(charIndex, tempLineBreak)
                    print(f"Line {errorAtLine}: Could not read value of variable '{variable}' when trying to read '{inputDir}'.")
                    return
                tempVariable.append(variable)
                tempValue.append(value)

            charIndex = charIndex2


        # ----------------------
        # Detect OUTPUT function
        # ----------------------

        elif foundSyntax(data, charIndex, "OUTPUT "):

            # Detect type & directory
            charIndex2 = charIndex + len("OUTPUT ")
            while charIndex2 in range(len(data)):
                if data[charIndex2] == "\n":
                    break
                elif foundSyntax(data, charIndex2, "interpreter"):
                    outputMode = "interpreter"
                    charIndex2 += len("interpreter")
                    break
                elif foundSyntax(data, charIndex2, "directory"):
                    outputMode = "directory"
                    charIndex2 += len("directory")
                    charIndex3 = charIndex2
                    detectDir = False
                    while charIndex3 in range(len(data)):
                        if data[charIndex3] == "\n":
                            break
                        elif data[charIndex3] == ("\"" or "'"):
                            if detectDir == False:
                                detectDir = True
                                firstInstance = charIndex3+1
                            else:
                                detectDir = False
                                lastInstance = charIndex3
                                break
                        charIndex3 += 1
                    try:
                        outputDir = data[firstInstance:lastInstance]
                    except UnboundLocalError:
                        errorAtLine = lineByIndex(charIndex, tempLineBreak)
                        print(f"Line {errorAtLine}: Missing output directory (syntax: OUTPUT `type` = `directory`).")
                        return

                    # Clear previous data
                    try:
                        with open(outputDir, "w+", encoding="utf8") as file:
                            file.write("")
                    except PermissionError:
                        errorAtLine = lineByIndex(charIndex, tempLineBreak)
                        print(f"Line {errorAtLine}: Cannot write to '{outputDir}' due to permission failure.")
                        return
                charIndex2 += 1

            charIndex = charIndex2


        # ------------------
        # Detect DO function
        # ------------------

        elif foundSyntax(data, charIndex, "DO "):
            
            # Read through code
            charIndex2 = charIndex + len("DO ")
            firstInstance = charIndex2
            while charIndex2 in range(len(data)):
                if data[charIndex2] == "\n":
                    lastInstance = charIndex2
                    break
                charIndex2 += 1
            code = data[firstInstance:lastInstance].replace(" ", "").split(";")

            # Get command and variable to write to
            try:
                tempCommand = code[0]
                foundVariable = code[1]
            except IndexError:
                errorAtLine = lineByIndex(charIndex, tempLineBreak)
                print(f"Line {errorAtLine}: Cannot read variable name.")
                return
            if len(tempCommand) == 0:
                errorAtLine = lineByIndex(charIndex, tempLineBreak)
                print(f"Line {errorAtLine}: No operation found (syntax: DO operation; output).")
                return
            elif len(foundVariable) == 0:
                errorAtLine = lineByIndex(charIndex, tempLineBreak)
                print(f"Line {errorAtLine}: No output found (syntax: DO operation; output).")
                return
            elif isNumber(foundVariable):
                errorAtLine = lineByIndex(charIndex, tempLineBreak)
                print(f"Line {errorAtLine}: Variable '{foundVariable}' must not be all numbers.")
                return

            # Separate every object of tempCommand for easier analysis
            separated = tempCommand.replace("(", "(#").replace(",", "#").replace(")", "#)#").split("#")
            tempCommand = [x for x in separated if x != ""]

            # Preparation for executing tempCommand
            indentLevel = 0
            operatorList  = [] # List of found operators in tempCommand
            indentList    = [] # List of indentation levels
            frequencyList = [] # List of frequencies (from leftmost to current location)

            # Process all objects in tempCommand
            for index, object in enumerate(tempCommand):
                if "(" in object and object in mathSyntax:
                    indentLevel += 1
                    operatorList.append(object)
                    frequencyList.append(operatorList.count(object))
                    indentList.append(indentLevel)
                elif isNumber(object):
                    tempCommand[index] = Decimal(object)
                    frequencyList.append(int(-1))
                    indentList.append(indentLevel)
                elif object in tempVariable:
                    variable = object
                    try:
                        value = tempValue[tempVariable.index(variable)]
                    except UnboundLocalError:
                        errorAtLine = lineByIndex(charIndex, tempLineBreak)
                        print(f"Line {errorAtLine}: Variable '{variable}' does not exist.")
                        return
                    tempCommand[index] = Decimal(value)
                    frequencyList.append(int(-1))
                    indentList.append(indentLevel)
                elif object == ")":
                    indentList.append(indentLevel)
                    indentLevel -= 1
                    frequencyList.append(int(-1))
                else:
                    indentList.append(indentLevel)
                    frequencyList.append(int(-1))
            
            # Run tempCommand while # of operators left is not 0
            while len(operatorList) != 0:

                # Find all objects whose indentLevel is highest
                indexStart = indentList.index(max(indentList))
                operatorOfMax = tempCommand[indexStart]
                opIndexInOpList = operatorList.index(operatorOfMax)
                indentOfMax = indentList[indexStart]
                frequencyOfMax = frequencyList[indexStart]

                # Get entire operation
                listOfEndIndices = [
                    index for index, object in enumerate(tempCommand) 
                    if object == ")" and indentList[index] == indentOfMax
                    ]
                try:
                    indexEnd = listOfEndIndices[0]
                except IndexError:
                    errorAtLine = lineByIndex(charIndex, tempLineBreak)
                    print(f"Line {errorAtLine}: Operator '{operatorOfMax}' has no closing syntax.")
                    return
                fullOperator = tempCommand[indexStart:indexEnd+1]

                # Get calculable objects
                valueList = fullOperator[1:-1]

                # Run operation
                code = getattr(mathPiege, operatorOfMax[:-1])
                try:
                    answer = Decimal(code(valueList))
                except TypeError:
                    errorAtLine = lineByIndex(charIndex, tempLineBreak)
                    print(f"Line {errorAtLine}: Operator '{operatorOfMax}' includes illegal input values: {valueList}.")
                    return
                except Exception as e:
                    errorAtLine = lineByIndex(charIndex, tempLineBreak)
                    print(f"Line {errorAtLine}: Cannot execute operator '{operatorOfMax}'.")
                    return
                
                # Remove part of tempCommand and other stuff which has been executed
                tempCommand = tempCommand[:indexStart] + [answer] + tempCommand[indexEnd+1:]
                indentList = indentList[:indexStart] + [int(indentOfMax - 1)] + indentList[indexEnd+1:]
                frequencyList = frequencyList[:indexStart] + [int(-1)] + frequencyList[indexEnd+1:]
                operatorList.pop(opIndexInOpList)

            # Return to string
            tempCommand = ''.join([str(x) for x in tempCommand])

            # Write to variable
            if foundVariable not in tempVariable:
                tempVariable.append(foundVariable)
                try:
                    tempValue.append(Decimal(tempCommand))
                except InvalidOperation:
                    errorAtLine = lineByIndex(charIndex, tempLineBreak)
                    print(f"Line {errorAtLine}: Cannot assign '{tempCommand}' to '{foundVariable}'.")
                    return
            else:
                try:
                    tempValue[tempVariable.index(foundVariable)] = Decimal(tempCommand)
                except Exception as e:
                    errorAtLine = lineByIndex(charIndex, tempLineBreak)
                    print(f"Line {errorAtLine}: Cannot assign '{tempCommand}' to variable '{foundVariable}'.")
                    return

            charIndex = charIndex2


        # ----------------------
        # Detect RETURN function
        # ----------------------

        elif foundSyntax(data, charIndex, "RETURN "):
            
            # Read variable name
            charIndex2 = charIndex + len("RETURN ")
            firstInstance = charIndex2
            while charIndex2 in range(len(data)):
                if data[charIndex2] == "\n":
                    lastInstance = charIndex2
                    break
                charIndex2 += 1
            variable = data[firstInstance:lastInstance]

            # Find respective value
            try:
                value = tempValue[tempVariable.index(variable)]
            except Exception as e:
                errorAtLine = lineByIndex(charIndex, tempLineBreak)
                print(f"Line {errorAtLine}: Variable '{variable}' does not exist.")
                return

            # Find integer ratio if possible
            ratioDisplay = ""
            try:
                ratio = Decimal(value).as_integer_ratio()
                if len(str(ratio[0])) < 10 and len(str(ratio[1])) < 10 and ratio[1] != 1:
                    ratioDisplay = f" ({ratio[0]}/{ratio[1]})"
            except Exception as e:
                pass
                
            # Write to selected output
            if outputMode == "interpreter":
                print(f"{variable} = {value}{ratioDisplay}")
            elif outputMode == "directory":
                with open(outputDir, "a+", encoding="utf8") as file:
                    file.write(f"{variable} = {value}{ratioDisplay}\n")

            charIndex = charIndex2


        # ---------------------
        # Detect PRINT function
        # ---------------------

        elif foundSyntax(data, charIndex, "PRINT "):

            # Read through code for display objects
            charIndex2 = charIndex + len("PRINT ")
            firstInstance = charIndex2
            separatorIndices = [0]
            inQuotes = False
            while charIndex2 in range(len(data)):
                if data[charIndex2] == "\n":
                    separatorIndices.append(charIndex2-firstInstance)
                    lastInstance = charIndex2
                    break
                if data[charIndex2] == "\"" and data[charIndex2-1] != "\\":
                    inQuotes = not inQuotes
                if data[charIndex2] == "," and not inQuotes:
                    separatorIndices.append(charIndex2-firstInstance)
                charIndex2 += 1
            inputString = data[firstInstance:lastInstance]

            # Separate string and variable names to put into display
            display = []
            for index in range(len(separatorIndices)-1):
                index1 = separatorIndices[index] if index == 0 else separatorIndices[index] + 1
                index2 = separatorIndices[index+1]
                string = inputString[index1:index2]
                if "\"" not in string: string = string.replace(" ", "")
                else:
                    if string.startswith(" "):
                        quoteIndex = string.find("\"")
                        string = string[quoteIndex:]
                    if string.endswith(" "):
                        quoteIndex = len(string) - string[::-1].find("\"")
                        string = string[:quoteIndex]
                display.append(string)

            # Process all objects in display (replace variable by value, remove quotes)
            for index, object in enumerate(display):
                if "\"" in object:
                    display[index] = display[index][1:-1]
                    continue
                variable = object
                try:
                    value = tempValue[tempVariable.index(variable)]
                except Exception as e:
                    errorAtLine = lineByIndex(charIndex, tempLineBreak)
                    print(f"Line {errorAtLine}: Variable '{variable}' does not exist.")
                    return
                display[index] = str(value)

            # Write to selected output
            if outputMode == "interpreter":
                print(''.join(display))
            elif outputMode == "directory":
                with open(outputDir, "a+", encoding="utf8") as file:
                    file.write(''.join(display) + "\n")

            charIndex = charIndex2


        # ----------------------
        # Detect VISUAL function
        # ----------------------

        elif foundSyntax(data, charIndex, "VISUAL "):

            # Read through code
            charIndex2 = charIndex + len("VISUAL ")
            firstInstance = charIndex2
            while charIndex2 in range(len(data)):
                if data[charIndex2] == "\n":
                    lastInstance = charIndex2
                    break
                charIndex2 += 1
            code = data[firstInstance:lastInstance].replace(" ", "").split(";")

            # Get visual type, options and data
            foundType = code[0].split("=")
            type = foundType[0]
            if type == "quantity": type = "magnitude"
            options = foundType[1].split(",")
            values = code[1].split(",")

            # Process all objects in values (replace variable by value)
            for index, object in enumerate(values):
                if "\"" in object:
                    values[index] = object.replace("\"", "").replace("'", "")
                    continue
                if isNumber(object):
                    values[index] = Decimal(object)
                    continue
                variable = object
                try:
                    value = tempValue[tempVariable.index(variable)]
                except Exception as e:
                    errorAtLine = lineByIndex(charIndex, tempLineBreak)
                    print(f"Line {errorAtLine}: Variable '{variable}' does not exist.")
                    return
                values[index] = Decimal(value)
            
            # Run code to visualise
            code = getattr(visualiser, type)
            try:
                display = code(options, values)
            except Exception as e:
                errorAtLine = lineByIndex(charIndex, tempLineBreak)
                print(f"Line {errorAtLine}: Cannot visualise '{type}'.")
                return
            
            # Print out display to selected output
            if outputMode == "interpreter":
                print(display)
            elif outputMode == "directory":
                with open(outputDir, "a+", encoding="utf8") as file:
                    file.write(f"{display}\n")


        # ----------------------
        # Detect DELETE function
        # ----------------------

        elif foundSyntax(data, charIndex, "DELETE "):

            # Read variable name
            charIndex2 = charIndex + len("DELETE ")
            firstInstance = charIndex2
            while charIndex2 in range(len(data)):
                if data[charIndex2] == "\n":
                    lastInstance = charIndex2
                    break
                charIndex2 += 1
            variable = data[firstInstance:lastInstance]

            # Find respective value
            try:
                value = tempValue[tempVariable.index(variable)]
            except Exception as e:
                errorAtLine = lineByIndex(charIndex, tempLineBreak)
                print(f"Line {errorAtLine}: Variable '{variable}' does not exist.")
                return
                
            # Remove
            tempValue.pop(tempVariable.index(variable))
            tempVariable.pop(tempVariable.index(variable))

            charIndex = charIndex2


        # ----------------------
        # Detect SETCUR function
        # ----------------------

        elif foundSyntax(data, charIndex, "SETCUR "):

            # Read through code for type, index and condition
            charIndex2 = charIndex + len("SETCUR ")
            firstInstance = charIndex2
            while charIndex2 in range(len(data)):
                if data[charIndex2] == "\n":
                    lastInstance = charIndex2
                    break
                charIndex2 += 1
            comparator = data[firstInstance:lastInstance].replace(" ", "").split(";")

            # Get type and index
            typeIndex = comparator[0].split("=")
            typeToUse = typeIndex[0]
            indexToGo = int(typeIndex[1])

            # Get condition
            condition = comparator[1]
            openParen = condition.find("(")
            closeParen = condition.find(")")
            operator = condition[:openParen]
            values = condition[openParen+1:closeParen].split(",")

            # Process all objects in values (replace variable by value)
            for index, object in enumerate(values):
                if isNumber(object):
                    values[index] = Decimal(object)
                    continue
                variable = object
                try:
                    value = tempValue[tempVariable.index(variable)]
                except Exception as e:
                    errorAtLine = lineByIndex(charIndex, tempLineBreak)
                    print(f"Line {errorAtLine}: Variable '{variable}' does not exist.")
                    return
                values[index] = Decimal(value)

            # Check condition
            verdict = False
            code = getattr(mathPiege, operator)
            try:
                verdict = code(values)
            except Exception as e:
                errorAtLine = lineByIndex(charIndex2, tempLineBreak)
                print(f"Line {errorAtLine}: Cannot execute comparison \"{comparator}\".")
                return

            # Activate SETCUR if verdict is True
            if verdict == True:
                if typeToUse == "char":
                    charIndex = indexToGo - 1
                elif typeToUse == "line":
                    charIndex = tempLineBreak[indexToGo - 1]


        # -----------------------
        # Detect MOVECUR function
        # -----------------------

        elif foundSyntax(data, charIndex, "MOVECUR "):

            # Read through code for type, index and condition
            charIndex2 = charIndex + len("MOVECUR ")
            firstInstance = charIndex2
            while charIndex2 in range(len(data)):
                if data[charIndex2] == "\n":
                    lastInstance = charIndex2
                    break
                charIndex2 += 1
            comparator = data[firstInstance:lastInstance].replace(" ", "").split(";")

            # Get type and index
            typeIndex = comparator[0].split("=")
            typeToUse = typeIndex[0]
            indexToGo = int(typeIndex[1])

            # Get condition
            condition = comparator[1]
            openParen = condition.find("(")
            closeParen = condition.find(")")
            operator = condition[:openParen]
            values = condition[openParen+1:closeParen].split(",")

            # Process all objects in values (replace variable by value)
            for index, object in enumerate(values):
                if isNumber(object):
                    values[index] = Decimal(object)
                    continue
                variable = object
                try:
                    value = tempValue[tempVariable.index(variable)]
                except Exception as e:
                    errorAtLine = lineByIndex(charIndex, tempLineBreak)
                    print(f"Line {errorAtLine}: Variable '{variable}' does not exist.")
                    return
                values[index] = Decimal(value)

            # Check condition
            verdict = False
            code = getattr(mathPiege, operator)
            try:
                verdict = code(values)
            except Exception as e:
                errorAtLine = lineByIndex(charIndex2, tempLineBreak)
                print(f"Line {errorAtLine}: Cannot execute comparison \"{comparator}\".")
                return

            # Activate MOVECUR if verdict is True
            if verdict == True:
                if typeToUse == "char":
                    charIndex += indexToGo
                elif typeToUse == "line":
                    line = lineByIndex(charIndex, tempLineBreak) - 1
                    charIndex = tempLineBreak[line + indexToGo]


        # ----------------------
        # Detect IGNORE function
        # ----------------------

        elif foundSyntax(data, charIndex, "IGNORE "):

            # Read line index
            charIndex2 = charIndex + len("IGNORE ")
            firstInstance = charIndex2
            while charIndex2 in range(len(data)):
                if data[charIndex2] == "\n":
                    lastInstance = charIndex2
                    break
                charIndex2 += 1
            line = data[firstInstance:lastInstance]
            if not isNumber(line):
                try:
                    value = tempValue[tempVariable.index(line)]
                except Exception as e:
                    errorAtLine = lineByIndex(charIndex, tempLineBreak)
                    print(f"Line {errorAtLine}: Variable '{line}' does not exist.")
                    return
                line = int(value)
            else:
                line = int(line)

            # Insert line if not ignored previously
            if line not in tempIgnoreLine: tempIgnoreLine.append(line)

            charIndex = charIndex2


        # -------------------
        # Detect END function
        # -------------------

        elif foundSyntax(data, charIndex, "END"):
            break

        charIndex += 1