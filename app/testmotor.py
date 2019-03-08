#testmotor.py
from hardwarecontrol import HardwareControl

hardware = HardwareControl()
cont = True
while cont == True:
    print("Specify number of steps, only integers. 1 step = 0.05625 degrees.\
         \n If you want to set current angle to absolute 0, input: cal\
         \n If you want to toggle the laser, input: l\
         \n If you want to exit input: exit")    
    innum = input(">> ")

    if innum == "exit":
        cont = False
    elif innum == "cal":
        hardware.calibrateMotor()
        print("Calibrated")
    elif innum == 'l':
        hardware.toggleLaser()
    else:
        stepnum = int(innum)
        if hardware.Laser.value == 1:
            hardware.Laser.off()
        hardware.turnMotor(stepnum, True)
        print("Moved")
