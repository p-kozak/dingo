from hardwarecontrol import *

motor = StepMotor()
cont = True
while cont == True:
    print("Specify number of steps, only integers. 1 step = 0.05625 degrees. \n If you want to exit input: exit")    
    innum = input(">> ")

    if innum == "exit":
        cont = False
    else:
        stepnum = int(innum)
        
        motor.turnbyStep(stepnum)
        print("Moved")
