def goto(linenum):
    global line
    line = linenum

line = 1
while True:
    if line == 1:
        response = input("yes or no? ")
        if response == "yes":
            goto(2)
        elif response == "no":
            goto(3)
        else:
            goto(100)
    elif line == 2:
        print ("Thank you for the yes!")
        goto(20)
    elif line == 3:
        print ("Thank you for the no!")
        goto(20)
    elif line == 20:
        break
    elif line == 100:
        print( "You're annoying me - answer the question!")
        goto(1)
