
### MATH LIBRARY FOR PIÈGE
### VERSION 0.1.4 (04 JANUARY 2026)
### AUTHOR: RANDOMMAERKS (BAO NGUYEN)
###
### LICENSED UNDER THE MIT LICENSE
### CHECK OUT LICENSE.TXT FOR MORE INFORMATION

# Arithmetical operations

def sum(value):
    sum = 0
    for index in value:
        sum += index
    return sum

def subtraction(value):
    sub = value[0]
    for index in range(1, len(value)):
        sub -= value[index]
    return sub

def product(value):
    pro = 1
    for index in value:
        pro *= index
    return pro

def ratio(value1, value2):
    return value1 / value2

def quotient(value):
    quo = value[0]
    for index in range(1, len(value)):
        quo /= value[index]
    return quo

def power(value1, value2):
    return value1 ** value2

def mod(value1, value2):
    return value1 % value2

def factorial(value):
    if int(value) == 0: return 1.0
    elif int(value) == 1: return 1.0
    else:
        fact = 1
        for index in range(1, int(value)+1):
            fact *= index
        return float(fact)

def absolute(value):
    if value < 0: return -value
    elif value >= 0: return value

def difference(value1, value2):
    return absolute(value1 - value2)

def logarithm(base, value):
    if base == value: return 1
    elif value == 1: return 0
    else:
        loopIndex = 1000
        a = -100
        b = 100
        temp1 = 0
        temp2 = 0
        while loopIndex != 0:
            temp1 = base ** a
            temp2 = base ** b
            meanExp = (a + b) / 2
            if base ** meanExp < value: a = meanExp
            elif base ** meanExp > value: b = meanExp
            else: return meanExp
            loopIndex -= 1
        return meanExp

def sqrt(value):
    return value ** 0.5

def root(root, value):
    return value ** (1/root)


# Algebraic operations

def constant(value):
    return value

def linear(value1, value2):
    if value1 == 0: return "All"
    else: return - value2 / value1

def quadratic(value1, value2, value3):
    if value1 == 0: return linear(value2, value3)
    else:
        delta = value2 ** 2 - 4 * value1 * value3
        if delta > 0:
            x1 = (- value2 + sqrt(delta)) / (2 * value1)
            x2 = (- value2 - sqrt(delta)) / (2 * value1)
            solution = [x1, x2]
            return solution
        if delta == 0:
            x = (-value2) / (2 * value1)
            return x
        if delta < 0:
            xReal = (- value2) / (2 * value1)
            xIm   = sqrt(-delta) / (2 * value1)
            solution = [str(xReal) + "+" + str(xIm) + "i",
                        str(xReal) + "-" + str(xIm) + "i"]
            return solution

def ratioNum(value1, value2, value3):
    return (value1 / value2) * value3

def ratioDenom(value1, value2, value3):
    return (value2 / value1) * value3
