from time import time
from decimal import *

# Preset constant

pi = Decimal('3.1415926535897932384626433832795')
e = Decimal('2.7182818284590452353602874713527')


# Sorting algorithms

def selectionSort(value):
    for i in range(len(value) - 1):
        minIndex = i
        for j in range(i+1, len(value)):
            if value[j] < value[minIndex]:
                minIndex = j
        if minIndex != i:
            tempValue = value[i]
            value[i] = value[minIndex]
            value[minIndex] = tempValue
    return value

def insertionSort(value):
    n = len(value)
    if n <= 1:
        return value
    for i in range(1, n):
        temp = value[i]         
        j = i - 1
        while j >= 0 and temp < value[j]: 
            value[j + 1] = value[j]
            j -= 1
        value[j + 1] = temp
    return value


# Arithmetical operators

def sum(value):
    sum = Decimal(0)
    for index in value:
        sum += index
    return sum

def sub(value):
    sub = value[0]
    for index in range(1, len(value)):
        sub -= value[index]
    return sub

def pro(value):
    pro = Decimal(1)
    for index in value:
        pro *= index
    return pro

def rat(value):
    if value[1] != 0: return value[0] / value[1]
    else: return Decimal("NaN")

def quo(value):
    quo = value[0]
    for index in range(1, len(value)):
        quo /= value[index]
    return quo

def pow(value):
    return value[0] ** value[1]

def exp(value):
    return e ** value[0]

def mod(value):
    return value[0] % value[1]

def fact(value):
    value = value[0]
    if value == 0: return 1.0
    fact = 1
    for index in range(1, int(value)+1):
        fact *= index
    return fact

def abs(value):
    if value[0] < 0: return -value[0]
    else: return value[0]

def sign(value):
    value = value[0]
    if value < 0: return -1
    elif value > 0: return 1
    else: return 0

def dif(value):
    return abs([value[0] - value[1]])

def log(value):
    if value[1] == value[0]: return 1
    elif value[1] == 1: return 0
    elif value[1] == 0: return Decimal("NaN")
    if value[0] > 1: a = -100
    else: a = 100
    b = -a
    loopIndex = 1000
    while loopIndex != 0:
        meanExp = (a + b) / 2
        if value[0] ** Decimal(meanExp) < value[1]: a = meanExp
        elif value[0] ** Decimal(meanExp) > value[1]: b = meanExp
        else: break
        loopIndex -= 1
    return meanExp

def ln(value):
    if value[0] == e: return 1
    elif value[0] == 1: return 0
    elif value[0] == 0: return Decimal("NaN")
    a = -100
    b = -a
    loopIndex = 1000    
    while loopIndex != 0:
        meanExp = (a + b) / 2
        if e ** Decimal(meanExp) < value[0]: a = meanExp
        elif e ** Decimal(meanExp) > value[0]: b = meanExp
        else: break
        loopIndex -= 1
    return meanExp

def sqrt(value):
    return Decimal(value[0]) ** Decimal(0.5)

def root(value):
    return Decimal(value[1]) ** 1/value[0]

def neg(value):
    return -Decimal(value[0])


# Rounding operators

def floor(value):
    value = value[0]
    if value >= 0: return int(value)
    return int(value) - 1

def ceil(value):
    value = value[0]
    if value > 0: return int(value) + 1
    return int(value)

def round(value):
    valueSign = sign([value[0]])
    newValue = value[0] * 10**(value[1])
    decimalPart = abs([newValue - int(newValue)])
    if decimalPart >= 0.5: newValue = (int(newValue) + valueSign) / 10**(value[1])
    else: newValue = int(newValue) / 10**(value[1])
    return newValue
    
def floorRat(value):
    return floor([rat(value)])

def ceilRat(value):
    return ceil([rat(value)])


# Trigonometric operators

def sin(value):
    value = value[0]
    step = 0
    threshold = pow([10, -16])
    value %= 2*pi
    mainResult = Decimal((-1)**step / fact([2*step + 1])) * value**(2*step + 1)
    while True:
        step += 1
        nextResult = Decimal((-1)**step / fact([2*step + 1])) * value**(2*step + 1)
        tempResult = mainResult + nextResult
        if dif([mainResult, tempResult]) <= threshold:
            break
        mainResult += nextResult
    return mainResult

def cos(value):
    value = value[0]
    step = 0
    threshold = pow([10, -16])
    value %= 2*pi
    if value == 0: return 1
    mainResult = Decimal((-1)**step / fact([2*step])) * value**(2*step)
    while True:
        step += 1
        nextResult = Decimal((-1)**step / fact([2*step])) * value**(2*step)
        tempResult = mainResult + nextResult
        if dif([mainResult, tempResult]) <= threshold:
            break
        mainResult += nextResult
    return mainResult

def tan(value):
    value = value[0] % pi
    return rat([sin([value]), cos([value])])

def cot(value):
    value = value[0] % pi
    return rat([cos([value]), sin([value])])

def sec(value):
    value = value[0]
    return rat([1, cos([value])])

def csc(value):
    value = value[0] % 2*pi
    return rat([1, sin([value])])

def asin(value):
    value = value[0]
    if abs([value]) > 1: return Decimal("NaN")
    loopIndex = 1000
    a = -pi/2
    b = pi/2
    if value == 1: return pi/2
    elif value == 0: return 0
    elif value == -1: return -pi/2
    while loopIndex != 0:
        meanVal = (a + b) / 2
        if sin([meanVal]) < value: a = meanVal
        elif sin([meanVal]) > value: b = meanVal
        else: break
        loopIndex -= 1
    return meanVal

def acos(value):
    value = value[0]
    if value == 1: return 0
    return pi/2 - asin([value])

def atan(value):
    value = value[0]
    loopIndex = 1000
    a = -pi/2
    b = pi/2
    while loopIndex != 0:
        meanVal = (a + b) / 2
        if tan([Decimal(meanVal)]) < value: a = meanVal
        elif tan([Decimal(meanVal)]) > value: b = meanVal
        else: return meanVal
        loopIndex -= 1
    return meanVal

def acot(value):
    return pi/2 - atan(value)

def asec(value):
    value = value[0]
    if abs([value]) < 1: return Decimal("NaN")
    loopIndex = 1000
    a = 0
    b = pi
    if value == 1: return 0
    elif value == -1: return pi
    while loopIndex != 0:
        meanVal = (a + b) / 2
        if sec([meanVal]) < abs([value]): a = meanVal
        elif sec([meanVal]) > abs([value]): b = meanVal
        else: break
        loopIndex -= 1
    if value >= 1: return meanVal
    else: return pi - meanVal

def acsc(value):
    return pi/2 - asec(value)


# Hyperbolic operators

def sinh(value):
    value = value[0]
    return (exp([2*value]) - 1) / (2 * exp([value]))

def cosh(value):
    value = value[0]
    return (exp([2*value]) + 1) / (2 * exp([value]))

def tanh(value):
    value = value[0]
    return rat([sinh([value]), cosh([value])])

def coth(value):
    value = value[0]
    return rat([cosh([value]), sinh([value])])

def sech(value):
    value = value[0]
    return rat([1, cosh([value])])

def csch(value):
    value = value[0]
    return rat([1, sinh([value])])

def asinh(value):
    value = value[0]
    return ln([value + sqrt([value**2 + 1])])

def acosh(value):
    value = value[0]
    if value < 1: return Decimal("NaN")
    return ln([value + sqrt([value**2 - 1])])

def atanh(value):
    value = value[0]
    if abs([value]) > 1: return Decimal("NaN")
    elif value == 1: return Decimal("Infinity")
    elif value == -1: return Decimal("-Infinity")
    return 0.5 * ln([rat([1 + value, 1 - value])])

def acoth(value):
    value = value[0]
    if abs([value]) < 1: return Decimal("NaN")
    elif value == 1: return Decimal("Infinity")
    elif value == -1: return Decimal("-Infinity")
    return 0.5 * ln([rat([value + 1, value - 1])])

def asech(value):
    value = value[0]
    if value < 0 or value > 1: return Decimal("NaN")
    elif value == 0: return Decimal("Infinity")
    return ln([rat([1, value]) + sqrt([rat([1, value**2]) - 1])])

def acsch(value):
    value = value[0]
    if value == 0: return Decimal("NaN")
    return ln([rat([1, value]) + sqrt([rat([1, value**2]) + 1])])


# Randomiser opeators

def randInt(value):
    time1 = time() - int(time())
    time1 = int(time1 * 10**15)
    time1 = time1 << 7
    time1 = time1 >> 11
    valueDif = dif([value[0], value[1]]) + Decimal(1)
    return time1 % valueDif + value[0]

def rand(value):
    time1 = time() - int(time())
    time1 = int(time1 * 10**15)
    time1 = time1 << 7
    time1 = time1 >> 11
    valueDif = dif([value[0], value[1]]) + Decimal(10**-16)
    return time1 % valueDif + value[0]


# Vector operators

def lenVect(value):
    lenVect = 0
    for index in value:
        lenVect += index**2
    return sqrt([lenVect])

def dist(value):
    dist = 0
    halfLength = int(len(value) / 2)
    for index in range(halfLength):
        dist += (value[index] - value[index + halfLength])**2
    return sqrt([dist])

def dotVect(value):
    dotVect = 0
    halfLength = int(len(value) / 2)
    for index in range(halfLength):
        dotVect += value[index] * value[index + halfLength]
    return dotVect

def angle(value):
    dotVect12 = dotVect(value)
    halfLength = int(len(value) / 2)
    vect1 = [value[i] for i in range(len(value)) if i < halfLength]
    vect2 = [x for x in value if x not in vect1]
    lenVect1 = 0
    for index in range(halfLength):
        lenVect1 += value[index]**2
    lenVect2 = 0
    for index in range(halfLength, len(value)):
        lenVect2 += value[index]**2
    return acos([rat([dotVect12, (lenVect1*lenVect2)**0.5])])


# Statistical operators

def squareSum(value):
    sum = 0
    for index in value:
        sum += index**2
    return sum

def cubeSum(value):
    sum = 0
    for index in value:
        sum += index**3
    return sum

def aMean(value):
    mean = 0
    for index in value:
        mean += index
    return mean / len(value)

def gMean(value):
    mean = 1
    for index in value:
        mean *= index
    return root([len(value), mean])

def agMean(value):
    a = value[0]
    g = value[1]
    for i in range(10):
        aNew = (a + g)/2
        gNew = sqrt([a*g])
        a = aNew
        g = gNew
    return aNew

def max(value):
    maxValue = value[0]
    for index in value:
        if maxValue < index: maxValue = index
    return maxValue

def min(value):
    minValue = value[0]
    for index in value:
        if minValue > index: minValue = index
    return minValue

def mode(value):
    maxFrequency = 0
    maxValue = value[0]
    for index in value:
        frequency = [x for x in value if x == index]
        if maxFrequency < len(frequency):
            maxFrequency = len(frequency)
            maxValue = index
    return maxValue

def popVar(value):
    mean = Decimal(aMean(value))
    sum = Decimal(squareSum(value))
    return Decimal(1/len(value)) * sum - mean**Decimal(2)

def popStdDev(value):
    return popVar(value)**Decimal(0.5)

def samVar(value):
    mean = Decimal(aMean(value))
    sum = Decimal(0)
    for index in value:
        sum += (index - mean)**Decimal(2)
    return Decimal(1/(len(value)-1)) * sum

def samStdDev(value):
    return samVar(value)**Decimal(0.5)

def median(value):
    value = insertionSort(value)
    halfLength = int(len(value) / 2)
    if len(value) % 2 == 1:
        return value[halfLength]
    else:
        return (value[halfLength - 1] + value[halfLength]) / 2

def meanAbsDev(value):
    meanValue = aMean(value)
    sum = 0
    for index in value:
        sum += dif([index, meanValue])
    return sum / len(value)

def medianAbsDev(value):
    medianValue = median(value)
    sum = 0
    for index in value:
        sum += dif([index, medianValue])
    return sum / len(value)

def modeAbsDev(value):
    modeValue = mode(value)
    sum = 0
    for index in value:
        sum += dif([index, modeValue])
    return sum / len(value)

def quart1(value):
    value = insertionSort(value)
    halfLength = int(len(value) / 2)
    tempList = [x for i, x in enumerate(value) if i < halfLength]
    return median(tempList)

def quart3(value):
    value = insertionSort(value)
    halfLength = int(len(value) / 2)
    if len(value) % 2 == 1: halfLength += 1
    tempList = [x for i, x in enumerate(value) if i >= halfLength]
    return median(tempList)

def iqr(value):
    return quart3(value) - quart1(value)


# Algebraic operators

def constant(value):
    value = value[0]
    return value

def linear(value):
    if value[0] == 0: return ["All"]
    else: return [-value[1] / value[0]]

def quadratic(value):
    if value[0] == 0: return linear([value[1], value[2]])
    else:
        delta = value[1] ** 2 - 4 * value[0] * value[2]
        if delta > 0:
            x1 = (- value[1] + sqrt([delta])) / (2 * value[0])
            x2 = (- value[1] - sqrt([delta])) / (2 * value[0])
            return [x1, x2]
        if delta == 0:
            x = (-value[1]) / (2 * value[0])
            return [x]
        if delta < 0:
            return [Decimal("NaN")]

def ratioNum(value):
    return [(value[0] / value[1]) * value[2]]

def ratioDenom(value):
    return [(value[1] / value[0]) * value[2]]


# Comparison operators

def less(value):
    return all(a < b for a, b in zip(value, value[1:]))

def more(value):
    return all(a > b for a, b in zip(value, value[1:]))

def equal(value):
    return all(a == b for a, b in zip(value, value[1:]))

def notless(value):
    return all(a >= b for a, b in zip(value, value[1:]))

def notmore(value):
    return all(a <= b for a, b in zip(value, value[1:]))

def notequal(value):
    return all(a != b for a, b in zip(value, value[1:]))
