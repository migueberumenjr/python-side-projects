'''
Simple calculator program
Author: Miguel Berumen
Date: 1/15/2017
'''

import re

print("Our Magical Calculator")
print("Type 'quit' to exit\n")

prev = 0
run = True

def performMath():
    global run
    global prev
    equation = ""

    # If there has been a previous calculation, use that result as the prompt
    if prev == 0:
        equation = input("Enter equation: ")
    else:
        equation = input(str(prev))

    # if user quits ->
    if equation == 'quit':
        print("Goodbye")
        run = False
    else:
        equation = re.sub('[a-zA-Z,.:()" "]', '', equation)
        if prev == 0:
            prev = eval(equation)
        else:
            prev = eval(str(prev) + equation)

while run:
    performMath()
