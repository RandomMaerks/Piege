from decimal import *

# --------------------
# Magnitude / quantity
# --------------------

def magnitude(options, inputValues):
    # Get character display, position of value, and the input values
    charDisplay = str(options[0])
    position = "after" if len(options) < 2 else str(options[1])
    value = int(inputValues[0])

    # Make the display
    display = [charDisplay for _ in range(value)]
    if position == "after": display = f"{''.join(display)} {value}"
    else: display = f"{inputValues[0]} {''.join(display)}"

    # Return display
    return display


# ------
# Matrix
# ------

def matrix(options, inputValues):
    # Get notation style and row quantity
    matrixNotation = str(options[0])
    rowQuantity = int(options[1])

    # Prepare left and right brackets/parentheses for later
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

    # Make display
    display = []
    columnQuantity = int(len(inputValues) / rowQuantity)
    for rowIndex in range(rowQuantity):
        tempDisplay = []
        tempDisplay.append(leftNotation[rowIndex])
        for columnIndex in range(columnQuantity):
            element = inputValues[rowIndex * columnQuantity + columnIndex]
            space = ''.join([" " for _ in range(len(str(element)), maxLength)])
            tempDisplay.append(f"{element}{space}")
            if columnIndex != columnQuantity - 1:
                tempDisplay.append("  ")
        tempDisplay.append(rightNotation[rowIndex])
        display.append(''.join(tempDisplay))

    # Return display
    return '\n'.join(display)


# -----
# Graph
# -----

def graph(options, inputValues):
    # Get type, scale type, padding and scale factor
    graphType = str(options[0])
    scaleType = str(options[1])
    padding = "all" if len(options) < 3 else str(options[2])
    scaleFactor = 40 if len(options) < 4 else Decimal(options[3])

    # Add additional empty string if inputValues <= 1
    if len(inputValues) == 0: inputValues = ["", 0]
    elif len(inputValues) == 1: inputValues = [""] + inputValues

    # Limit scaleFactor
    if scaleFactor > 100: scaleFactor = Decimal(100)
    elif scaleFactor <= 0: scaleFactor = Decimal(0.1)
    
    # Get max length and max value of input values
    maxLength = len(str(inputValues[0]))
    maxValue = inputValues[1]
    for i in range(int(len(inputValues) / 2)):
        if maxLength < len(str(inputValues[2*i])): maxLength = len(str(inputValues[2*i]))
        if maxValue < inputValues[2*i + 1]: maxValue = inputValues[2*i + 1]

    # Prepare for display
    if graphType == "bar":
        decimalSection = ["", "▏", "▎", "▍", "▌", "▋", "▊", "▉", "█"]
    elif graphType == "dot":
        decimalSection = ["•", "•", "•", "•", "•", "•", "•", "•", " "]
    scalar = maxValue / scaleFactor

    # Make display
    display = []
    if padding in ["all", "noBetween"]:
        display.append(f"{''.join([" " for _ in range(maxLength)])}▕")
    for i in range(int(len(inputValues) / 2)):
        label = str(inputValues[2*i])
        space = ''.join([" " for _ in range(len(label), maxLength)])
        value = inputValues[2*i + 1]
        if scaleType == "literal":
            if graphType == "bar":
                graphDisplay = ''.join([decimalSection[4] for _ in range(int(value))])
            elif graphType == "dot":
                lastDot = decimalSection[4] if value != 0 else ""
                graphDisplay = ''.join([decimalSection[8] for _ in range(int(value)-1)]) + lastDot
        elif scaleType == "scaled":
            scaledValue = value / scalar
            decimal = scaledValue - int(scaledValue)
            secIndex = int(decimal * 8)
            graphDisplay = ''.join([decimalSection[-1] for _ in range(int(scaledValue))]) + decimalSection[secIndex]
        display.append(f"{label}{space}▕{graphDisplay} {value}")
        if padding in ["all", "noOuter"] and i != int(len(inputValues) / 2) - 1:
            display.append(f"{''.join([" " for _ in range(maxLength)])}▕")
    if padding in ["all", "noBetween"]:
        display.append(f"{''.join([" " for _ in range(maxLength)])}▕")

    # Return display
    return '\n'.join(display)


# -----
# Table
# -----
        
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
        labelBar = ''.join(["━" for _ in range(maxLabelLength+2)])
        valueBar = ''.join(["━" for _ in range(maxValueLength+2)])
    elif orientation == "column":
        labelBar = ''.join(["━" for _ in range(maxLength+2)])
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
                    space = ''.join([" " for _ in range(len(str(element)), maxLabelLength)])
                else:
                    space = ''.join([" " for _ in range(len(str(element)), maxValueLength)])
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
                    space = ''.join([" " for _ in range(len(str(element)), maxLength)])
                    tempDisplay.append(f"│ {element}{space} ")
            tempDisplay.append("│")
            display.append(''.join(tempDisplay))
            if rowIndex != rowQuantity - 1:
                display.append(''.join(middleBorder))
        display.append(''.join(bottomBorder)) 
        return '\n'.join(display)