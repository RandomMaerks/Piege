
### MATH LIBRARY FOR PIÈGE
### VERSION 0.1.5 (07 JANUARY 2026)
### AUTHOR: RANDOMMAERKS (BAO NGUYEN)
###
### LICENSED UNDER THE MIT LICENSE
### CHECK OUT LICENSE.TXT FOR MORE INFORMATION


# Preset constant
pi = 3.1415926535897932384626433832795
eConst = 2.7182818284590452353602874713527


# Arithmetical operators

def sum(value):
    sum = 0
    for index in value:
        sum += index
    return sum

def sub(value):
    sub = value[0]
    for index in range(1, len(value)):
        sub -= value[index]
    return sub

def pro(value):
    pro = 1
    for index in value:
        pro *= index
    return pro

def rat(value):
    try:
        rat = value[0] / value[1]
    except ZeroDivisionError:
        return "ComplexInfinity"
    return rat

def quo(value):
    quo = value[0]
    for index in range(1, len(value)):
        quo /= value[index]
    return quo

def pow(value):
    return value[0] ** value[1]

def exp(value):
    return eConst ** value[0]

def mod(value):
    return value[0] % value[1]

def fact(value):
    value = value[0]
    if int(value) == 0: return 1.0
    elif int(value) == 1: return 1.0
    else:
        fact = 1
        for index in range(1, int(value)+1):
            fact *= index
        return float(fact)

def abs(value):
    value = value[0]
    if value < 0: return -value
    elif value >= 0: return value

def dif(value):
    return abs([value[0] - value[1]])

def log(value):
    if value[0] == value[1]: return 1
    elif value[1] == 1: return 0
    loopIndex = 1000
    a = -100
    b = 100
    temp1 = 0
    temp2 = 0
    while loopIndex != 0:
        temp1 = value[0] ** a
        temp2 = value[0] ** b
        meanExp = (a + b) / 2
        if value[0] ** meanExp < value[1]: a = meanExp
        elif value[0] ** meanExp > value[1]: b = meanExp
        else: break
        loopIndex -= 1
    return meanExp

def ln(value):
    if value[0] == eConst: return 1
    elif value[0] == 1: return 0
    loopIndex = 1000
    a = -100
    b = 100
    temp1 = 0
    temp2 = 0
    while loopIndex != 0:
        temp1 = eConst ** a
        temp2 = eConst ** b
        meanExp = (a + b) / 2
        if eConst ** meanExp < value[0]: a = meanExp
        elif eConst ** meanExp > value[0]: b = meanExp
        else: break
        loopIndex -= 1
    return meanExp

def sqrt(value):
    value = value[0]
    return value ** 0.5

def root(value):
    return value[1] ** (1/value[0])


# Rounding operators

def floor(value):
    value = value[0]
    if value != int(value):
        if value > 0:
            return int(value)
        return int(value) - 1
    return value

def ceil(value):
    value = value[0]
    if value != int(value):
        if value > 0:
            return int(value) + 1
        return int(value)
    return value

def round(value):
    newValue = float(int(value[0] * (10 ** (int(value[1]) + 1))))
    newValue /= 10
    if newValue >= float(int(newValue) + 0.5):
        return ceil([newValue]) / (10 ** int(value[1]))
    return floor([newValue]) / (10 ** int(value[1]))
    
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
    mainResult = ((-1)**step / fact([2*step + 1])) * value**(2*step + 1)
    while True:
        step += 1
        nextResult = ((-1)**step / fact([2*step + 1])) * value**(2*step + 1)
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
    mainResult = ((-1)**step / fact([2*step])) * value**(2*step)
    while True:
        step += 1
        nextResult = ((-1)**step / fact([2*step])) * value**(2*step)
        tempResult = mainResult + nextResult
        if dif([mainResult, tempResult]) <= threshold:
            break
        mainResult += nextResult
    return mainResult

def tan(value):
    value = value[0]
    value %= pi
    return rat([sin([value]), cos([value])])

def cot(value):
    value = value[0]
    value %= pi
    return rat([cos([value]), sin([value])])

def sec(value):
    value = value[0]
    value %= 2*pi
    return rat([1, cos([value])])

def csc(value):
    value = value[0]
    value %= 2*pi
    return rat([1, sin([value])])

def asin(value):
    value = value[0]
    if abs([value]) > 1: return "NullValue"
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
    return pi/2 - asin(value)

def atan(value):
    value = value[0]
    loopIndex = 1000
    a = -pi/2
    b = pi/2
    while loopIndex != 0:
        meanVal = (a + b) / 2
        if tan([meanVal]) < value: a = meanVal
        elif tan([meanVal]) > value: b = meanVal
        else: return meanVal
        loopIndex -= 1
    return meanVal

def acot(value):
    return pi/2 - atan(value)

def asec(value):
    value = value[0]
    if abs([value]) < 1: return "NullValue"
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
    if value < 1: return "NullValue"
    return ln([value + sqrt([value**2 - 1])])

def atanh(value):
    value = value[0]
    if abs([value]) >= 1: return "NullValue"
    return 0.5 * ln([rat([1 + value, 1 - value])])

def acoth(value):
    value = value[0]
    if abs([value]) <= 1: return "NullValue"
    return 0.5 * ln([rat([value + 1, value - 1])])

def asech(value):
    value = value[0]
    if value <= 0 or value > 1: return "NullValue"
    return ln([rat([1, value]) + sqrt([rat([1, value**2]) - 1])])

def acsch(value):
    value = value[0]
    if value == 0: return "NullValue"
    return ln([rat([1, value]) + sqrt([rat([1, value**2]) + 1])])

        
# Algebraic operators

def constant(value):
    value = value[0]
    return value

def linear(value):
    if value[0] == 0: return "All"
    else: return -value[1] / value[0]

def quadratic(value):
    if value[0] == 0: return linear([value[1], value[2]])
    else:
        delta = value[1] ** 2 - 4 * value[0] * value[2]
        if delta > 0:
            x1 = (- value[1] + sqrt([delta])) / (2 * value[0])
            x2 = (- value[1] - sqrt([delta])) / (2 * value[0])
            solution = [x1, x2]
            return solution
        if delta == 0:
            x = (-value[1]) / (2 * value[0])
            return x
        if delta < 0:
            return "NullValue"

def ratioNum(value):
    return (value[0] / value[1]) * value[2]

def ratioDenom(value):
    return (value[1] / value[0]) * value[2]


# Comparison operators

def less(value):
    for index in range(len(value)-1):
        if not value[index] < value[index+1]: return False
    return True

def more(value):
    for index in range(len(value)-1):
        if not value[index] > value[index+1]: return False
    return True

def equal(value):
    for index in range(len(value)-1):
        if not value[index] == value[index+1]: return False
    return True

def notless(value):
    for index in range(len(value)-1):
        if not value[index] >= value[index+1]: return False
    return True

def notmore(value):
    for index in range(len(value)-1):
        if not value[index] <= value[index+1]: return False
    return True

def notequal(value):
    for index in range(len(value)-1):
        if not value[index] != value[index+1]: return False
    return True
