from hardwarecontrol import *

motor = StepMotor()
cont = True
while cont == True:
    print("Specify number of steps, only integers. 1 step = 0.9 degrees. \n If you want to exit input: exit")    
    innum = input(">> ")

    if innum == "exit":
        cont = False
    else:
        stepnum = int(innum)
        
        motor.turnbystep(stepnum)
        print("Moved")
        # print("Do you want to continue? (y/n)")
        # val = input(">> ")
        # if val == "y":
        #     cont = True
        # else:
        #     cont = False