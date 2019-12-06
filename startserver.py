import socket
import RPi.GPIO as GPIO
import time
import PiMotor

def startServer():
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = socket.gethostbyname('10.200.59.179')
    port = 1235
    
    s.bind((host, port))
    s.listen(5)
    s.settimeout(60)

    GPIO.setwarnings(False)
    servoPIN = 3 #board pin 3, second row on inside of board = bcm pin 2, PiMotor.py sets to gpio.board
#    GPIO.setmode(GPIO.BCM)
    GPIO.setup(servoPIN, GPIO.OUT)
    
    #mapping motors 
    m1 = PiMotor.Motor("MOTOR1",1)
    m2 = PiMotor.Motor("MOTOR2",1)
    motorAll = PiMotor.LinkedMotors(m1,m2)
    
    
    #mapping arrows on motor controller
    aBack = PiMotor.Arrow(1)
    aLeft = PiMotor.Arrow(2)
    aForward = PiMotor.Arrow(3) 
    aRight = PiMotor.Arrow(4)
    
    
    
    p = GPIO.PWM(servoPIN, 50)
    p.start(0)
    
    while True:
        c, addr = s.accept()
        print(f"Connected to: {addr}")
        c.send(bytes("Connected to server DAWG!", "utf-8"))
    
        while True: #loop on input from controller 
            aForward.off()
            aBack.off()
            msg = c.recv(128)
            if not msg: 
                break
            readableMsg = msg.decode("utf-8")
            
            allWheels = False
            if "4WDrive" in readableMsg:
                print("4WD Enabled")
                allWheels = True
                
            elif "2WDrive" in readableMsg:
                print("4WD Disabled")
                allWheels = False
                
            elif "Move" in readableMsg:#move forward
                value = ''.join(x for x in readableMsg if x.isdigit())
                valueInt = int(value)
                print("Move for -- ", valueInt)
                if (valueInt < 100):
                    aForward.on()
                    if allWheels is True:
                        motorAll.forward(valueInt)
                    else:
                        m1.forward(valueInt)
               
            elif "moveback" in readableMsg:#move backward
                value = ''.join(x for x in readableMsg if x.isdigit())
                valueInt = int(value)
                print("Move back -- ", valueInt)
                if (valueInt < 100):
                    aBack.on()
                    if allWheels is True:
                        motorAll.reverse(valueInt)
                    else:
                        m1.reverse(valueInt)
                
            elif "turn" in readableMsg:#turn
                value = ''.join(x for x in readableMsg if x.isdigit())
                valueInt = int(value)/10
                print("Turn Received -- ", valueInt)
                if(valueInt<100):
                    p.ChangeDutyCycle(valueInt)
                    
            
        
    c.close()
    print("Client Disconnected")
    
startServer()
