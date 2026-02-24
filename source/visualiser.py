# Magnitude / quantity

def magnitude(options, inputValues):
    charDisplay = str(options[0])
    display = [charDisplay for a in range(int(inputValues[0]))]
    return f"{inputValues[0]} {''.join(display)}"


# Matrix

def matrix(options, inputValues):
    matrixNotation = str(options[0])
    rowQuantity = int(options[1])

    maxLength = len(str(inputValues[0]))
    for i in inputValues:
        if maxLength < len(str(i)): maxLength = len(str(i))
    leftNotation = []
    rightNotation = []
    if rowQuantity == 1:
        if matrixNotation == "brackets":
            leftNotation.append("[ ")
            rightNotation.append(" ]")
        elif matrixNotation == "parentheses":
            leftNotation.append("( ")
            rightNotation.append(" )")
    else:
        if matrixNotation == "brackets":
            leftNotation.append("⎡ ")
            rightNotation.append(" ⎤")
            if rowQuantity >= 2:
                for i in range(2, rowQuantity):
                    leftNotation.append("⎢ ")
                    rightNotation.append(" ⎥")
            leftNotation.append("⎣ ")
            rightNotation.append(" ⎦")
        elif matrixNotation == "parentheses":
            leftNotation.append("⎛ ")
            rightNotation.append(" ⎞")
            if rowQuantity >= 2:
                for i in range(2, rowQuantity):
                    leftNotation.append("⎢ ")
                    rightNotation.append(" ⎥")
            leftNotation.append("⎝ ")
            rightNotation.append(" ⎠")

    display = []
    columnQuantity = int(len(inputValues) / rowQuantity)
    for rowIndex in range(rowQuantity):
        tempDisplay = []
        tempDisplay.append(leftNotation[rowIndex])
        for columnIndex in range(columnQuantity):
            element = inputValues[rowIndex * columnQuantity + columnIndex]
            space = ''.join([" " for a in range(len(str(element)), maxLength)])
            tempDisplay.append(f"{element}{space}")
            if columnIndex != columnQuantity - 1:
                tempDisplay.append("  ")
        tempDisplay.append(rightNotation[rowIndex])
        display.append(''.join(tempDisplay))
    return '\n'.join(display)


# Graph

def graph(options, inputValues):
    graphType = str(options[0])

    maxLength = len(str(inputValues[0]))
    maxValue = inputValues[1]
    for i in range(int(len(inputValues) / 2)):
        if maxLength < len(str(inputValues[2*i])): maxLength = len(str(inputValues[2*i]))
        if maxValue < inputValues[2*i + 1]: maxValue = inputValues[2*i + 1]

    display = []
    #scalar = 10**(len(str(int(maxValue)))-2)
    scalar = maxValue / 40
    decimalSection = ["", "▏", "▎", "▍", "▌", "▋", "▊", "▉", "█"]
    for i in range(int(len(inputValues) / 2)):
        label = str(inputValues[2*i])
        space = ''.join([" " for a in range(len(label), maxLength)])
        value = inputValues[2*i + 1]
        if graphType == "quantity":
            barDisplay = ''.join(["▌" for a in range(int(value))])
        elif graphType == "bar":
            scaledValue = value / scalar
            decimal = scaledValue - int(scaledValue)
            secIndex = int(decimal * 8)
            barDisplay = ''.join(["█" for a in range(int(scaledValue))]) + decimalSection[secIndex]
        display.append(f"{''.join([" " for a in range(maxLength)])}▕")
        display.append(f"{label}{space}▕{barDisplay} {value}")
    display.append(f"{''.join([" " for a in range(maxLength)])}▕")
    return '\n'.join(display)


# Table
        
def table(options, inputValues):
    orientation = options[0]
    if orientation == "row":
        rowQuantity = int(options[1])
        columnQuantity = int(len(inputValues) / rowQuantity)

        maxLabelLength = len(str(inputValues[0]))
        maxValueLength = len(str(inputValues[1]))
        for elementIndex, element in enumerate(inputValues):
            columnIndex = elementIndex % columnQuantity
            rowIndex = int(elementIndex * rowQuantity / len(inputValues))
            if columnIndex == 0:
                if maxLabelLength < len(str(element)): maxLabelLength = len(str(element))
            else:
                if maxValueLength < len(str(element)): maxValueLength = len(str(element))
                
    elif orientation == "column":
        columnQuantity = int(options[1])
        rowQuantity = int(len(inputValues) / columnQuantity)

        maxLength = len(str(inputValues[0]))
        for i in inputValues:
            if maxLength < len(str(i)): maxLength = len(str(i))

    topBorder = []
    middleBorder = []
    bottomBorder = []
    if orientation == "row":
        labelBar = ''.join(["━" for a in range(maxLabelLength+2)])
        valueBar = ''.join(["━" for a in range(maxValueLength+2)])
    elif orientation == "column":
        labelBar = ''.join(["━" for a in range(maxLength+2)])
        valueBar = labelBar
    topBorder.append("┍" + labelBar)
    middleBorder.append("┝" + labelBar)
    bottomBorder.append("┕" + labelBar)
    for columnIndex in range(1, columnQuantity):
        topBorder.append("┯" + valueBar)
        middleBorder.append("┿" + valueBar)
        bottomBorder.append("┷" + valueBar)
    topBorder.append("┑")
    middleBorder.append("┥")
    bottomBorder.append("┙")
            
    display = []
    display.append(''.join(topBorder))
    if orientation == "row":
        for rowIndex in range(rowQuantity):
            tempDisplay = []
            for columnIndex in range(columnQuantity):
                element = inputValues[rowIndex * columnQuantity + columnIndex]
                if columnIndex == 0:
                    space = ''.join([" " for a in range(len(str(element)), maxLabelLength)])
                else:
                    space = ''.join([" " for a in range(len(str(element)), maxValueLength)])
                tempDisplay.append(f"│ {element}{space} ")
            tempDisplay.append("│")
            display.append(''.join(tempDisplay))
            if rowIndex != rowQuantity - 1:
                display.append(''.join(middleBorder))
        display.append(''.join(bottomBorder))
        return '\n'.join(display)
    
    elif orientation == "column":
        rowQuantityByColumn = int(len(inputValues) / columnQuantity)
        for rowIndex in range(rowQuantityByColumn):
            tempDisplay = []
            for elementIndex, element in enumerate(inputValues):
                if elementIndex % rowQuantityByColumn == rowIndex:
                    space = ''.join([" " for a in range(len(str(element)), maxLength)])
                    tempDisplay.append(f"│ {element}{space} ")
            tempDisplay.append("│")
            display.append(''.join(tempDisplay))
            if rowIndex != rowQuantity - 1:
                display.append(''.join(middleBorder))
        display.append(''.join(bottomBorder)) 
        return '\n'.join(display)
