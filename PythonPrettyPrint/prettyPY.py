import re

# read in .txt and strip each line
with open('prettyPY_input.txt', 'r') as f:
    linesInList = f.readlines()

# basic preparations after reading text
linesInList = [_.rstrip() for _ in linesInList]
newlinesinlist = ' \n'.join(linesInList)
splitList = list(newlinesinlist)

# list where all the operation ranges are places
areaList = []

# splitList will stay unedited with our individual chars
# areaList starts with empty values of '---'
for _ in range(len(splitList)):
    areaList.append('---')

lasti = len(splitList) - 1

# label # comment areas (this one must come first!!!)
flag = False
for i, _ in enumerate(splitList):
    if areaList[i] == '---':
        openn = True
    else:
        openn = False

    if openn and flag == False and _ == '#':
        flag = True
    elif openn and flag and _ == '\n':
        areaList[i] = 'inHashComm'
        flag = False
    if openn and flag:
        areaList[i] = 'inHashComm'

# label """ comment areas
flag = False
for i, _ in enumerate(splitList):
    if areaList[i] == '---':
        openn = True
    else:
        openn = False

    if openn and i+2 <= lasti and flag == False and _ == '"' and splitList[i+1] == '"' and splitList[i+2] == '"':
        flag = True
    elif openn and i+2 <= lasti and flag and _ == '"' and splitList[i+1] == '"' and splitList[i+2] == '"':
        areaList[i] = 'inDbleComm'
        areaList[i+1] = 'inDbleComm'
        areaList[i+2] = 'inDbleComm'
        flag = False
    if openn and flag:
        areaList[i] = 'inDbleComm'

# label ''' comment areas
flag = False
for i, _ in enumerate(splitList):
    if areaList[i] == '---':
        openn = True
    else:
        openn = False

    if openn and i+2 <= lasti and flag == False and _ == "'" and splitList[i+1] == "'" and splitList[i+2] == "'":
        flag = True
    elif openn and i+2 <= lasti and flag and _ == "'" and splitList[i+1] == "'" and splitList[i+2] == "'":
        areaList[i] = "inSnglComm"
        areaList[i+1] = "inSnglComm"
        areaList[i+2] = "inSnglComm"
        flag = False
    if openn and flag:
        areaList[i] = "inSnglComm"

# label " string areas
# only works if it comes after the comment areas!!!
flag1 = False
flag2 = False
for i, _ in enumerate(splitList):
    if areaList[i] == '---':
        openn = True
    else:
        openn = False

    # doing double quote strings
    if openn and flag1 == False and flag2 == False and _ == '"':
        flag1 = True
    elif openn and i+1 <= lasti and flag1 and\
    (_ == '"' or _ == '\"' or areaList[i+1] == "inSnglComm" or areaList[i+1] == 'inDbleComm' or areaList[i+1] == "inHashComm"):
        areaList[i] = 'inDoubleStr'
        flag1 = False
    if openn and flag1:
        areaList[i] = 'inDoubleStr'

    # doing single quote strings
    if openn and flag2 == False and flag1 == False and _ == "'":
        flag2 = True
    elif openn and i+1 <= lasti and flag2 and\
    (_ == "'" or _ == "\'" or areaList[i+1] == "inSnglComm" or areaList[i+1] == 'inDbleComm' or areaList[i+1] == "inHashComm"):
        areaList[i] = "inSingleStr"
        flag2 = False
    if openn and flag2:
        areaList[i] = "inSingleStr"

# labeling python reserved words
flag = False
befores = "[^a-zA-Z]" # anything but letters
afters = "[^a-zA-Z0-9]" # anything but letters and nums
for i, _ in enumerate(splitList):
    if areaList[i] == '---':
        openn = True
    else:
        openn = False

    # 2 char words
    if openn and i>0 and i+2 <= lasti and\
    ((re.search(befores,splitList[i-1]) and _ == "a" and splitList[i+1] == "s" and re.search(afters,splitList[i+2]))\
    or(re.search(befores,splitList[i-1]) and _ == "i" and splitList[i+1] == "f" and re.search(afters,splitList[i+2]))\
    or(re.search(befores,splitList[i-1]) and _ == "i" and splitList[i+1] == "n" and re.search(afters,splitList[i+2]))\
    or(re.search(befores,splitList[i-1]) and _ == "i" and splitList[i+1] == "s" and re.search(afters,splitList[i+2]))\
    or(re.search(befores,splitList[i-1]) and _ == "o" and splitList[i+1] == "r" and re.search(afters,splitList[i+2]))):
        areaList[i-1] = 'pyWord'
        areaList[i] = 'pyWord'
        areaList[i+1] = 'pyWord'
        areaList[i+2] = 'pyWord'

    if openn and i==0 and i+2 <= lasti and\
    ((_ == "a" and splitList[i+1] == "s" and re.search(afters,splitList[i+2]))\
    or(_ == "i" and splitList[i+1] == "f" and re.search(afters,splitList[i+2]))\
    or(_ == "i" and splitList[i+1] == "n" and re.search(afters,splitList[i+2]))\
    or(_ == "i" and splitList[i+1] == "s" and re.search(afters,splitList[i+2]))\
    or(_ == "o" and splitList[i+1] == "r" and re.search(afters,splitList[i+2]))):
        areaList[i] = 'pyWord'
        areaList[i+1] = 'pyWord'
        areaList[i+2] = 'pyWord'

    # as
    # if
    # in
    # is
    # or

    elif openn and i>0 and i+3 <= lasti and\
    ((re.search(befores,splitList[i-1]) and _ == "a" and splitList[i+1] == "n" and splitList[i+2] == "d" and re.search(afters,splitList[i+3]))\
    or(re.search(befores,splitList[i-1]) and _ == "t" and splitList[i+1] == "r" and splitList[i+2] == "y" and re.search(afters,splitList[i+3]))\
    or(re.search(befores,splitList[i-1]) and _ == "d" and splitList[i+1] == "e" and splitList[i+2] == "f" and re.search(afters,splitList[i+3]))\
    or(re.search(befores,splitList[i-1]) and _ == "d" and splitList[i+1] == "e" and splitList[i+2] == "l" and re.search(afters,splitList[i+3]))\
    or(re.search(befores,splitList[i-1]) and _ == "f" and splitList[i+1] == "o" and splitList[i+2] == "r" and re.search(afters,splitList[i+3]))\
    or(re.search(befores,splitList[i-1]) and _ == "n" and splitList[i+1] == "o" and splitList[i+2] == "t" and re.search(afters,splitList[i+3]))):
        areaList[i-1] = 'pyWord'
        areaList[i] = 'pyWord'
        areaList[i+1] = 'pyWord'
        areaList[i+2] = 'pyWord'
        areaList[i+3] = 'pyWord'

    elif openn and i==0 and i+3 <= lasti and\
    ((_ == "a" and splitList[i+1] == "n" and splitList[i+2] == "d" and re.search(afters,splitList[i+3]))\
    or(_ == "t" and splitList[i+1] == "r" and splitList[i+2] == "y" and re.search(afters,splitList[i+3]))\
    or(_ == "d" and splitList[i+1] == "e" and splitList[i+2] == "f" and re.search(afters,splitList[i+3]))\
    or(_ == "d" and splitList[i+1] == "e" and splitList[i+2] == "l" and re.search(afters,splitList[i+3]))\
    or(_ == "f" and splitList[i+1] == "o" and splitList[i+2] == "r" and re.search(afters,splitList[i+3]))\
    or(_ == "n" and splitList[i+1] == "o" and splitList[i+2] == "t" and re.search(afters,splitList[i+3]))):
        areaList[i] = 'pyWord'
        areaList[i+1] = 'pyWord'
        areaList[i+2] = 'pyWord'
        areaList[i+3] = 'pyWord'

    # and
    # try
    # def
    # del
    # for
    # not

    elif openn and i>0 and i+4 <= lasti and\
    ((re.search(befores,splitList[i-1]) and _ == "e" and splitList[i+1] == "l" and splitList[i+2] == "i" and splitList[i+3] == "f" and re.search(afters,splitList[i+4]))\
    or(re.search(befores,splitList[i-1]) and _ == "e" and splitList[i+1] == "l" and splitList[i+2] == "s" and splitList[i+3] == "e" and re.search(afters,splitList[i+4]))\
    or(re.search(befores,splitList[i-1]) and _ == "f" and splitList[i+1] == "r" and splitList[i+2] == "o" and splitList[i+3] == "m" and re.search(afters,splitList[i+4]))\
    or(re.search(befores,splitList[i-1]) and _ == "N" and splitList[i+1] == "o" and splitList[i+2] == "n" and splitList[i+3] == "e" and re.search(afters,splitList[i+4]))\
    or(re.search(befores,splitList[i-1]) and _ == "p" and splitList[i+1] == "a" and splitList[i+2] == "s" and splitList[i+3] == "s" and re.search(afters,splitList[i+4]))\
    or(re.search(befores,splitList[i-1]) and _ == "T" and splitList[i+1] == "r" and splitList[i+2] == "u" and splitList[i+3] == "e" and re.search(afters,splitList[i+4]))\
    or(re.search(befores,splitList[i-1]) and _ == "w" and splitList[i+1] == "i" and splitList[i+2] == "t" and splitList[i+3] == "h" and re.search(afters,splitList[i+4]))):
        areaList[i-1] = 'pyWord'
        areaList[i] = 'pyWord'
        areaList[i+1] = 'pyWord'
        areaList[i+2] = 'pyWord'
        areaList[i+3] = 'pyWord'
        areaList[i+4] = 'pyWord'

    elif openn and i==0 and i+4 <= lasti and\
    ((_ == "e" and splitList[i+1] == "l" and splitList[i+2] == "i" and splitList[i+3] == "f" and re.search(afters,splitList[i+4]))\
    or(_ == "e" and splitList[i+1] == "l" and splitList[i+2] == "s" and splitList[i+3] == "e" and re.search(afters,splitList[i+4]))\
    or(_ == "f" and splitList[i+1] == "r" and splitList[i+2] == "o" and splitList[i+3] == "m" and re.search(afters,splitList[i+4]))\
    or(_ == "N" and splitList[i+1] == "o" and splitList[i+2] == "n" and splitList[i+3] == "e" and re.search(afters,splitList[i+4]))\
    or(_ == "p" and splitList[i+1] == "a" and splitList[i+2] == "s" and splitList[i+3] == "s" and re.search(afters,splitList[i+4]))\
    or(_ == "T" and splitList[i+1] == "r" and splitList[i+2] == "u" and splitList[i+3] == "e" and re.search(afters,splitList[i+4]))\
    or(_ == "w" and splitList[i+1] == "i" and splitList[i+2] == "t" and splitList[i+3] == "h" and re.search(afters,splitList[i+4]))):
        areaList[i] = 'pyWord'
        areaList[i+1] = 'pyWord'
        areaList[i+2] = 'pyWord'
        areaList[i+3] = 'pyWord'
        areaList[i+4] = 'pyWord'

    # elif
    # else
    # from
    # None
    # pass
    # True
    # with

    elif openn and i>0 and i+5 <= lasti and\
    ((re.search(befores,splitList[i-1]) and _ == "r" and splitList[i+1] == "a" and splitList[i+2] == "i" and splitList[i+3] == "s" and splitList[i+4] == "e" and re.search(afters,splitList[i+5]))\
    or(re.search(befores,splitList[i-1]) and _ == "F" and splitList[i+1] == "a" and splitList[i+2] == "l" and splitList[i+3] == "s" and splitList[i+4] == "e" and re.search(afters,splitList[i+5]))\
    or(re.search(befores,splitList[i-1]) and _ == "b" and splitList[i+1] == "r" and splitList[i+2] == "e" and splitList[i+3] == "a" and splitList[i+4] == "k" and re.search(afters,splitList[i+5]))\
    or(re.search(befores,splitList[i-1]) and _ == "c" and splitList[i+1] == "l" and splitList[i+2] == "a" and splitList[i+3] == "s" and splitList[i+4] == "s" and re.search(afters,splitList[i+5]))\
    or(re.search(befores,splitList[i-1]) and _ == "w" and splitList[i+1] == "h" and splitList[i+2] == "i" and splitList[i+3] == "l" and splitList[i+4] == "e" and re.search(afters,splitList[i+5]))\
    or(re.search(befores,splitList[i-1]) and _ == "y" and splitList[i+1] == "i" and splitList[i+2] == "e" and splitList[i+3] == "l" and splitList[i+4] == "d" and re.search(afters,splitList[i+5]))):
        areaList[i-1] = 'pyWord'
        areaList[i] = 'pyWord'
        areaList[i+1] = 'pyWord'
        areaList[i+2] = 'pyWord'
        areaList[i+3] = 'pyWord'
        areaList[i+4] = 'pyWord'
        areaList[i+5] = 'pyWord'

    elif openn and i==0 and i+5 <= lasti and\
    ((_ == "r" and splitList[i+1] == "a" and splitList[i+2] == "i" and splitList[i+3] == "s" and splitList[i+4] == "e" and re.search(afters,splitList[i+5]))\
    or(_ == "F" and splitList[i+1] == "a" and splitList[i+2] == "l" and splitList[i+3] == "s" and splitList[i+4] == "e" and re.search(afters,splitList[i+5]))\
    or(_ == "b" and splitList[i+1] == "r" and splitList[i+2] == "e" and splitList[i+3] == "a" and splitList[i+4] == "k" and re.search(afters,splitList[i+5]))\
    or(_ == "c" and splitList[i+1] == "l" and splitList[i+2] == "a" and splitList[i+3] == "s" and splitList[i+4] == "s" and re.search(afters,splitList[i+5]))\
    or(_ == "w" and splitList[i+1] == "h" and splitList[i+2] == "i" and splitList[i+3] == "l" and splitList[i+4] == "e" and re.search(afters,splitList[i+5]))\
    or(_ == "y" and splitList[i+1] == "i" and splitList[i+2] == "e" and splitList[i+3] == "l" and splitList[i+4] == "d" and re.search(afters,splitList[i+5]))):
        areaList[i] = 'pyWord'
        areaList[i+1] = 'pyWord'
        areaList[i+2] = 'pyWord'
        areaList[i+3] = 'pyWord'
        areaList[i+4] = 'pyWord'
        areaList[i+5] = 'pyWord'

    # raise
    # False
    # break
    # class
    # while
    # yield

    elif openn and i>0 and i+6 <= lasti and\
    ((re.search(befores,splitList[i-1]) and _ == "a" and splitList[i+1] == "s" and splitList[i+2] == "s" and splitList[i+3] == "e" and splitList[i+4] == "r" and splitList[i+5] == "t" and re.search(afters,splitList[i+6]))\
    or(re.search(befores,splitList[i-1]) and _ == "e" and splitList[i+1] == "x" and splitList[i+2] == "c" and splitList[i+3] == "e" and splitList[i+4] == "p" and splitList[i+5] == "t" and re.search(afters,splitList[i+6]))\
    or(re.search(befores,splitList[i-1]) and _ == "g" and splitList[i+1] == "l" and splitList[i+2] == "o" and splitList[i+3] == "b" and splitList[i+4] == "a" and splitList[i+5] == "l" and re.search(afters,splitList[i+6]))\
    or(re.search(befores,splitList[i-1]) and _ == "i" and splitList[i+1] == "m" and splitList[i+2] == "p" and splitList[i+3] == "o" and splitList[i+4] == "r" and splitList[i+5] == "t" and re.search(afters,splitList[i+6]))\
    or(re.search(befores,splitList[i-1]) and _ == "l" and splitList[i+1] == "a" and splitList[i+2] == "m" and splitList[i+3] == "b" and splitList[i+4] == "d" and splitList[i+5] == "a" and re.search(afters,splitList[i+6]))\
    or(re.search(befores,splitList[i-1]) and _ == "r" and splitList[i+1] == "e" and splitList[i+2] == "t" and splitList[i+3] == "u" and splitList[i+4] == "r" and splitList[i+5] == "n" and re.search(afters,splitList[i+6]))):
        areaList[i-1] = 'pyWord'
        areaList[i] = 'pyWord'
        areaList[i+1] = 'pyWord'
        areaList[i+2] = 'pyWord'
        areaList[i+3] = 'pyWord'
        areaList[i+4] = 'pyWord'
        areaList[i+5] = 'pyWord'
        areaList[i+6] = 'pyWord'

    elif openn and i==0 and i+6 <= lasti and\
    ((_ == "a" and splitList[i+1] == "s" and splitList[i+2] == "s" and splitList[i+3] == "e" and splitList[i+4] == "r" and splitList[i+5] == "t" and re.search(afters,splitList[i+6]))\
    or(_ == "e" and splitList[i+1] == "x" and splitList[i+2] == "c" and splitList[i+3] == "e" and splitList[i+4] == "p" and splitList[i+5] == "t" and re.search(afters,splitList[i+6]))\
    or(_ == "g" and splitList[i+1] == "l" and splitList[i+2] == "o" and splitList[i+3] == "b" and splitList[i+4] == "a" and splitList[i+5] == "l" and re.search(afters,splitList[i+6]))\
    or(_ == "i" and splitList[i+1] == "m" and splitList[i+2] == "p" and splitList[i+3] == "o" and splitList[i+4] == "r" and splitList[i+5] == "t" and re.search(afters,splitList[i+6]))\
    or(_ == "l" and splitList[i+1] == "a" and splitList[i+2] == "m" and splitList[i+3] == "b" and splitList[i+4] == "d" and splitList[i+5] == "a" and re.search(afters,splitList[i+6]))\
    or(_ == "r" and splitList[i+1] == "e" and splitList[i+2] == "t" and splitList[i+3] == "u" and splitList[i+4] == "r" and splitList[i+5] == "n" and re.search(afters,splitList[i+6]))):
        areaList[i] = 'pyWord'
        areaList[i+1] = 'pyWord'
        areaList[i+2] = 'pyWord'
        areaList[i+3] = 'pyWord'
        areaList[i+4] = 'pyWord'
        areaList[i+5] = 'pyWord'
        areaList[i+6] = 'pyWord'

    # assert
    # except
    # global
    # import
    # lambda
    # return

    elif openn and i>0 and i+7 <= lasti and\
    (re.search(befores,splitList[i-1]) and _ == "f" and splitList[i+1] == "i" and splitList[i+2] == "n" and splitList[i+3] == "a" and splitList[i+4] == "l" and splitList[i+5] == "l" and splitList[i+6] == "y" and re.search(afters,splitList[i+7])):
        areaList[i-1] = 'pyWord'
        areaList[i] = 'pyWord'
        areaList[i+1] = 'pyWord'
        areaList[i+2] = 'pyWord'
        areaList[i+3] = 'pyWord'
        areaList[i+4] = 'pyWord'
        areaList[i+5] = 'pyWord'
        areaList[i+6] = 'pyWord'
        areaList[i+7] = 'pyWord'

    elif openn and i==0 and i+7 <= lasti and\
    (_ == "f" and splitList[i+1] == "i" and splitList[i+2] == "n" and splitList[i+3] == "a" and splitList[i+4] == "l" and splitList[i+5] == "l" and splitList[i+6] == "y" and re.search(afters,splitList[i+7])):
        areaList[i] = 'pyWord'
        areaList[i+1] = 'pyWord'
        areaList[i+2] = 'pyWord'
        areaList[i+3] = 'pyWord'
        areaList[i+4] = 'pyWord'
        areaList[i+5] = 'pyWord'
        areaList[i+6] = 'pyWord'
        areaList[i+7] = 'pyWord'

    # finally

    elif openn and i>0 and i+8 <= lasti and\
    ((re.search(befores,splitList[i-1]) and _ == "c" and splitList[i+1] == "o" and splitList[i+2] == "n" and splitList[i+3] == "t" and splitList[i+4] == "i" and splitList[i+5] == "n" and splitList[i+6] == "u" and splitList[i+7] == "e" and re.search(afters,splitList[i+8]))\
    or(re.search(befores,splitList[i-1]) and _ == "n" and splitList[i+1] == "o" and splitList[i+2] == "n" and splitList[i+3] == "l" and splitList[i+4] == "o" and splitList[i+5] == "c" and splitList[i+6] == "a" and splitList[i+7] == "l" and re.search(afters,splitList[i+8]))):
        areaList[i-1] = 'pyWord'
        areaList[i] = 'pyWord'
        areaList[i+1] = 'pyWord'
        areaList[i+2] = 'pyWord'
        areaList[i+3] = 'pyWord'
        areaList[i+4] = 'pyWord'
        areaList[i+5] = 'pyWord'
        areaList[i+6] = 'pyWord'
        areaList[i+7] = 'pyWord'
        areaList[i+8] = 'pyWord'

    elif openn and i==0 and i+8 <= lasti and\
    ((_ == "c" and splitList[i+1] == "o" and splitList[i+2] == "n" and splitList[i+3] == "t" and splitList[i+4] == "i" and splitList[i+5] == "n" and splitList[i+6] == "u" and splitList[i+7] == "e" and re.search(afters,splitList[i+8]))\
    or(_ == "n" and splitList[i+1] == "o" and splitList[i+2] == "n" and splitList[i+3] == "l" and splitList[i+4] == "o" and splitList[i+5] == "c" and splitList[i+6] == "a" and splitList[i+7] == "l" and re.search(afters,splitList[i+8]))):
        areaList[i] = 'pyWord'
        areaList[i+1] = 'pyWord'
        areaList[i+2] = 'pyWord'
        areaList[i+3] = 'pyWord'
        areaList[i+4] = 'pyWord'
        areaList[i+5] = 'pyWord'
        areaList[i+6] = 'pyWord'
        areaList[i+7] = 'pyWord'
        areaList[i+8] = 'pyWord'

    # continue
    # nonlocal

# labeling python math chars
flag = False
operators = "[=+\-*/%&|^><~]"
for i, _ in enumerate(splitList):
    if areaList[i] == '---':
        openn = True
    else:
        openn = False

    if openn and re.search(operators,_):
        areaList[i] = 'pyMath'

# labeling numbers
flag = False
nums = "^[0-9]{1}$"
excludes = "[^a-zA-z]"
for i, _ in enumerate(splitList):
    if areaList[i] == '---':
        openn = True
    else:
        openn = False

    if openn and re.search(nums,_):
        if i == 0:
            areaList[i] = 'nums'
        elif i>0 and re.search(excludes,splitList[i-1]):
            areaList[i] = 'nums'

# labeling anything before (
# no enum, can't use _
lasti = len(splitList) - 1
includes = "^[a-zA-Z0-9]{1}$"
excludes = "[^a-zA-Z0-9]"
i = lasti
flag = False
while i >= 0:
    if areaList[i] == '---':
        openn = True
    else:
        openn = False

    if openn and i+1 <= lasti and flag == False and re.search(includes,splitList[i]) and splitList[i+1] == '(':
        flag = True
    elif openn and flag and re.search(excludes,splitList[i]):
        flag = False
    if openn and flag:
        areaList[i] = 'functions'
    # always at end!
    i -= 1

# finalize enters
openn = False
for i, _ in enumerate(splitList):
    # define condition that we change cells in
    # use areaList to find the label condition, and write to mapList
    if splitList[i] == '\n':
        areaList[i] = 'enter'

#print('initial areas and item:')
testList = []
for i, _ in enumerate(splitList):
    data = areaList[i] + ' ' + _
    testList.append(data)
#print(testList)

# copy areaList to mapList
mapList = areaList

###################################################################################################### add to prettyCSS
# label tabs that start at i==0
cntr = 0
tabflag = False
lasti = len(splitList) -1
for i, _ in enumerate(splitList):
    if i == 0 and _ == " ":
        tabflag = True
    elif tabflag and i>0 and _ != " ":
        tabflag = False
        mapList[i-1] = str(cntr)
        splitList[i-1] = 'space'
        cntr = 0
        # break
    if tabflag:
        mapList[i] = 'del'
        splitList[i] = 'del'
        cntr += 1

###################################################################################################### add to prettyCSS
# label tabs that start after 0
cntr = 1
flag = False
lasti = len(splitList) -1
for i, _ in enumerate(splitList):
    if flag == False and i>0 and _ == " " and splitList[i-1] == " ":
        flag = True
        mapList[i-1] = 'del'
        splitList[i-1] = 'del'
    elif flag and i>0 and _ != " ":
        flag = False
        mapList[i-1] = str(cntr)
        splitList[i-1] = 'space'
        cntr = 1
        # break
    if flag:
        mapList[i] = 'del'
        splitList[i] = 'del'
        cntr += 1

# remove the space: [enter space enter]
for i, _ in enumerate(splitList):
    if i>1 and mapList[i-2] == 'enter' and mapList[i-1] == ' ' and mapList[i] == 'enter':
        mapList.pop(i-1)
        splitList.pop(i-1)

#print(len(mapList))
#print(len(splitList))

# remove the space: [curly space enter]
for i, _ in enumerate(splitList):
    if (splitList[i-2] == '{' and splitList[i-1] == ' ' and splitList[i] == '\n')\
    or (splitList[i-2] == '}' and splitList[i-1] == ' ' and splitList[i] == '\n'):
        mapList.pop(i-1)
        splitList.pop(i-1)

#print("dels listed, not deleted")
testList2 = []
for i, _ in enumerate(splitList):
    data = mapList[i] + ' ' + _
    testList2.append(data)
#print(testList2)

#how many to delete
isdel = 0
for i, _ in enumerate(mapList):
    if _ == 'del':
        isdel += 1

# print()
# print("dels: "+ str(isdel))

delshene = True
while delshene:
    for i, _ in enumerate(mapList):
        if _ == 'del':
            mapList.pop(i)
            splitList.pop(i)
    isdel = 0
    for i, _ in enumerate(mapList):
        if _ == 'del':
            isdel += 1
    if isdel == 0:
        delshene = False
    else:
        delshene = True

# did we delete them all?
isdel = 0
for i, _ in enumerate(mapList):
    if _ == 'del':
        isdel += 1

# print('dels after del: ' + str(isdel))
# change maplist to colors
for i, _ in enumerate(splitList):
    if mapList[i] == 'functions':
        mapList[i] = 'green'
    elif mapList[i] == '---':
        mapList[i] = 'white'
    elif mapList[i] == 'nums':
        mapList[i] = 'red'
    elif mapList[i] == 'pyWord' or mapList[i] == 'pyMath':
        mapList[i] = 'blue'
    elif mapList[i] == "inSingleStr" or mapList[i] == 'inDoubleStr':
        mapList[i] = 'strgrn'
    elif mapList[i] == "inSnglComm" or mapList[i] == 'inDbleComm' or mapList[i] == "inHashComm":
        mapList[i] = 'gray'

# print("colored:")
testList2 = []
for i, _ in enumerate(splitList):
    data = mapList[i] + ' ' + _
    testList2.append(data)
# print(testList2)

# remove the pointless color open that's before line ends: ['color  ', 'enter' ]
for i, _ in enumerate(splitList):
    if (i+1<=(len(splitList)-1) and i>0)and (mapList[i] == 'blue' or mapList[i] == 'white' or mapList[i] == 'red'\
    or mapList[i] == 'green' or mapList[i] == 'strgrn' or mapList[i] == 'gray')\
    and _ == ' ' and mapList[i+1] == 'enter':
        mapList[i] = mapList[i-1]

# print()
# print("after pops:")
testList3 = []
for i, _ in enumerate(splitList):
    data = mapList[i] + ' ' + _
    testList3.append(data)
# print(testList3)

# replace <> with &lt; &gt; and &amp;
############################################################################################## add to cssPretty
for i, _ in enumerate(splitList):
    if _ == '<':
        splitList[i] = '&lt;'
    elif _ == '>':
        splitList[i] = '&gt;'

# print()
# print("right before it hits rulelist:")
testList3 = []
for i, _ in enumerate(splitList):
    data = mapList[i] + ' ' + _
    testList3.append(data)
# print(testList3)

################################################################################### end added from prettyPY

# empty list for final ruleset, start and stop style
ruleList = []
for i, _ in enumerate(mapList):
    ruleList.append('---')
# first round of instruction making
for i, _ in enumerate(mapList):
    # for some reason this breaks if we
    # try elfi anywhere
    if i == 0:
        ruleList[i] = 'open'
    if i>0 and _ != mapList[i-1]:
        ruleList[i-1] = 'close'
        ruleList[i] = 'open'
    if i>1 and mapList[i-2] != mapList[i-1] and _ != mapList[i-1]:
        ruleList[i-1] = 'only'
# fix index zero errors
for i, _ in enumerate(mapList):
    # for some reason this breaks if we
    # try elfi anywhere
    if i == 0:
        if i+1<=(len(mapList)-1) and mapList[i] == mapList[i+1]:
            ruleList[i] = 'open'
        else:
            ruleList[i] = 'only'

# fix final spot
for i, _ in enumerate(mapList):
    if i == len(mapList)-1:
        if mapList[i-1] == mapList[i]:
            ruleList[i] = 'close'
        elif mapList[i-1] != mapList[i]:
            ruleList[i] = 'only'

# print()
# print("after rules:")
testList4 = []
for i, _ in enumerate(ruleList):
    data = mapList[i] + ' ' + _
    testList4.append(data)
# print(testList4)
#
# blue is from next higher div
# this always goes after tab num: '">'
dict = {
    'white-open': '<span class="cw">', 'red-open': '<span class="cn">', 'green-open': '<span class="fg">',
    'strgrn-open': '<span class="sg">', 'red-open': '<span class="cn">', 'green-open': '<span class="fg">',
    'tab': '<p class="t', 'gray-open': '<span class="cg">', 'white': 'cw',  'red': 'cn', 'green': 'fg',
    'strgrn': 'sg', 'gray': 'cg', 'blue': '',
}

# put in the html
htmlList=[]
for i, _ in enumerate(splitList):
    htmlList.append('---')

for i, _ in enumerate(splitList):
    opens = mapList[i] + '-' + 'open'

    if ruleList[i] == 'open':
        if (mapList[i] == 'white' or mapList[i] == 'red' or mapList[i] == 'green' or mapList[i] == 'strgrn'\
        or mapList[i] == 'gray'):
            htmlList[i] = dict[opens] + _
        else:
            htmlList[i] = _

    elif ruleList[i] == 'close':
        if mapList[i] == 'white' or mapList[i] == 'red' or mapList[i] == 'green' or mapList[i] == 'strgrn'\
        or mapList[i] == 'gray':
            htmlList[i] = _ + '</span>'
        else:
            htmlList[i] = _
    elif ruleList[i] == 'only':
        if mapList[i] == 'white' or mapList[i] == 'red' or mapList[i] == 'green' or mapList[i] == 'strgrn'\
        or mapList[i] == 'gray':
            htmlList[i] = dict[opens] + _ + '</span>'
        else:
            htmlList[i] = _
    elif ruleList[i] == '---':
        htmlList[i] = _
    elif mapList[i] == 'enter':
        htmlList[i] = ' \n'
    if splitList[i] == 'space':
        if i+1 <= len(splitList)-1:
            htmlList[i] = '<span class="t' + mapList[i] + ' ' + dict[mapList[i+1]] + '">'
        elif i == len(splitList)-1 and i>0:
            htmlList[i] = '<span class="t' + mapList[i] + ' ' + dict[mapList[i-1]] + '">'
    if mapList[i] != 'white' and mapList[i] != 'red' and mapList[i] != 'green' and mapList[i] != 'strgrn'\
    and mapList[i] != 'blue' and mapList[i] != 'gray' and mapList[i] != 'enter' and splitList[i] != 'space':
        htmlList[i] = '<p class="t' + mapList[i] + '">'

# print()
# print(htmlList)

# prepare for inserting into <p> tags
stringsdone = "".join(htmlList).split("\n")

# fix empty lines
newlist2 = []
for _ in stringsdone:
    # normal line
    if _.startswith('<p class="t') == False and _ != '\n':
        _ = '<p>' + _ + '</p>'
    # tab line
    elif _.startswith('<p class="t') == True:
        _ = _ + '</p>'
    # enter line
    if _ == '<p></p>' or _ == '<p> </p>' or _ == '<p>   </p>':
        _ = '<p class="hidden">*</p>'
    newlist2.append(_)

# save to new file
with open('prettyPY_output.txt', 'w') as finalList:
    # this puts each list item as new line
    for _ in newlist2:
        finalList.write(_ + ' \n')
