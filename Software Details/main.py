from machine import Pin, PWM
import bluetooth
import time

in1 = Pin(22, Pin.OUT)
in2 = Pin(23, Pin.OUT) 
in3 = Pin(19, Pin.OUT)
in4 = Pin(18, Pin.OUT)

servo1 = PWM(Pin(4), freq=50)
servo2 = PWM(Pin(5), freq=50)

def move_forward():
    in1.value(1)
    in2.value(0)
    in3.value(1)
    in4.value(0)

def move_backward():
    in1.value(0)
    in2.value(1)
    in3.value(0)
    in4.value(1)

def turn_left():
    in1.value(0)
    in2.value(1)
    in3.value(1)
    in4.value(0)

def turn_right():
    in1.value(1)
    in2.value(0)
    in3.value(0)
    in4.value(1)

def stop_motors():
    in1.value(0)
    in2.value(0)
    in3.value(0)
    in4.value(0)

def lock_motors():
    in1.value(1)
    in2.value(1)
    in3.value(1)
    in4.value(1)

def arms_attack():
    servo1.duty(115)
    servo2.duty(115)
    time.sleep(0.1)
    servo1.duty(35)
    servo2.duty(35)
    time.sleep(0.1)


conn = [-1]

name = "Geeta"
ble = bluetooth.BLE()
ble.active(False)
time.sleep(0.5)
ble.active(True)
ble.config(gap_name=name)

service_UUID = bluetooth.UUID("6e400001-b5a3-f393-e0a9-e50e24dcca9e")
char_UUID    = bluetooth.UUID("6e400002-b5a3-f393-e0a9-e50e24dcca9e")

char    = (char_UUID, bluetooth.FLAG_WRITE | bluetooth.FLAG_NOTIFY)
service = (service_UUID, (char,),)
((char_handle,),) = ble.gatts_register_services((service,))

def event_occured(event, data):
    if event == 1:
        conn[0] = data[0]
        print("Connected")
    elif event == 2:
        conn[0] = -1
        print("Disconnected")
        advertise(name)
    elif event == 3:
        print("Data received")

def advertise(device_name):
    nb  = device_name.encode()
    adv = bytearray([0x02, 0x01, 0x06]) + bytearray([len(nb) + 1, 0x09]) + nb
    ble.gap_advertise(50, adv_data=adv)
    print("Advertising:", device_name)


advertise(name)
ble.irq(event_occured)
stop_motors()


while True:
    raw_msg = ble.gatts_read(char_handle).rstrip(b'\x00')
    cmd = raw_msg.decode().strip()

    if cmd == "F":
        move_forward()
        print("Moved Forward")
        time.sleep(0.1)
    elif cmd == "B":
        move_backward()
        print("Moved Backward")
        time.sleep(0.1)
    elif cmd == "L":
        turn_left()
        print("Moved Left")
        time.sleep(0.1)
    elif cmd == "R":
        turn_right()
        print("Moved Right")
        time.sleep(0.1)
    elif cmd == "S":
        stop_motors()
        print("Stopped")
        time.sleep(0.1)
    elif cmd == "A":
        arms_attack()
        print("Attatcked")
        time.sleep(2)

    time.sleep(0.05)
