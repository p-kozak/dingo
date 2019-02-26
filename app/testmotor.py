import hardwarecontrol

motor = StepMotor()
cont = True
while(cont = True)
{
    print("Specify number of steps. 1 step = 0.9 degrees")
    innum = input("Specify number of steps, only integers. 1 step = 0.9 degrees.")
    stepnum = int(innum)

    print("Moved")
    val = input("Do you want to continue? (y/n)")
    if(val == y):
        cont = True
    else:
        cont = False
}