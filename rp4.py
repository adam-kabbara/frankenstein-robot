import socketio
from adafruit_servokit import ServoKit
import threading
import time


# ---------------- servo control ----------------
kit = ServoKit(channels=16)
left_knee = kit.servo[10]
right_knee = kit.servo[6]
left_hip = kit.servo[8]
right_hip = kit.servo[4]
left_arm_rot = kit.servo[2]
right_arm_rot = kit.servo[14]
left_arm_arc = kit.servo[0]
right_arm_arc = kit.servo[15]
left_elbow = kit.servo[3]
right_elbow = kit.servo[12]
right_hand = kit.servo[13]

right_elbow.set_pulse_width_range(700, 2700)
left_elbow.set_pulse_width_range(1100, 2800)
right_arm_arc.set_pulse_width_range(380, 1200)
left_arm_arc.set_pulse_width_range(1100, 2700)
right_arm_rot.set_pulse_width_range(800, 2700)
left_arm_rot.set_pulse_width_range(500, 2200)

left_hip.angle= 130
right_hip.angle = 20
left_knee.angle = 60

def init_motors():
    right_hand.angle=0
    right_arm_arc.angle = 165
    left_arm_arc.angle = 58
    right_hand.angle=0
    left_elbow.angle=180
    right_elbow.angle=0


init_motors()


left_arm_lifting = False
right_arm_lifting = False
control = "both"

# ---------------- socket io ----------------
sio = socketio.Client()

@sio.event
def connect():
    sio.emit('message', {"device-name": "rp4"})
    print("I'm connected!")

@sio.event
def message(data):
    print(f'Received: {data}')
    handle_motors(data)

def handle_motors(call):
    global left_arm_lifting, right_arm_lifting, control
    if "clicked" in call:
        if call["clicked"] == "open-right-hand":
            right_hand.angle = 0
        elif call["clicked"] == "close-right-hand":
            right_hand.angle = 55
        elif call["clicked"] == "reset-btn":
            left_arm_arc.angle = None
            right_arm_arc.angle = None
            left_elbow.angle=None
            right_elbow.angle=None

            print("reset")
        elif call["clicked"] == "step-btn":
            init_motors()#temp function for step button as it doesnt work for intended use
        elif call["clicked"] == "control-left-btn":
            control = "left"
        elif call["clicked"] == "control-right-btn":
            control = "right"
        elif call["clicked"] == "both-btn":
            control = "both"
        elif call["clicked"] == "flex-btn":
            ll = threading.Thread(target=flex_left)
            lr = threading.Thread(target=flex_right)
            if control == "both":
                ll.start()
                lr.start()
            elif control == "left":
                ll.start()
            elif control == 'right':
                lr.start()

    if "pressed" in call:
        if call["pressed"] == "arm-up-btn":
            ll = threading.Thread(target=lift_left_arm, args=[1])
            lr = threading.Thread(target=lift_right_arm, args=[1])
            if control == "both":
                left_arm_lifting = True
                right_arm_lifting = True
                ll.start()
                lr.start()
            elif control == "left":
                left_arm_lifting = True
                ll.start()
            elif control == 'right':
                right_arm_lifting = True
                lr.start()

    if "released" in call:
        if call["released"] == "arm-up-btn" or call["released"] == "arm-down-btn":
            if control == "both":
                left_arm_lifting = False
                right_arm_lifting = False
            elif control == "left":
                left_arm_lifting = False
            elif control == "right":
                right_arm_lifting = False


def lift_left_arm(mult):
    while (left_arm_lifting):
        print(f"left arm arc: {left_arm_arc.angle}")
        if left_arm_arc.angle >= 154:
            break
        left_arm_arc.angle +=5*mult
        time.sleep(0.05)

def lift_right_arm(mult):
    while (right_arm_lifting):
        print(f"right arm arc: {right_arm_arc.angle}")
        if right_arm_arc.angle < 6:
            break
        right_arm_arc.angle -=5*mult
        time.sleep(0.05)

def flex_left():
    left_elbow.angle=50
    time.sleep(5)
    left_elbow.angle=180

def flex_right():
    right_elbow.angle=150
    time.sleep(5)
    left_elbow.angle=0

            

if __name__=="__main__":
    sio.connect('http://192.168.2.14:5000')
