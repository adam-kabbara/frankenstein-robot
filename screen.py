import socketio
import os
import cv2
import time
 
sio = socketio.Client()
 
# ---------------- socket io ----------------
@sio.event
def connect():
   sio.emit('message', {"device-name": "screen"})
   print("I'm connected!")
 
@sio.event
def messages(data):
   print(f'Received: {data}')
 
   if "text" in data:
       say(data['text'])
 
def say(txt):
   os.system(f'echo "{txt}"|espeak')
 
def main():
   font = cv2.FONT_HERSHEY_SIMPLEX
   fontScale = 1
   color = (0, 0, 255)
   thickness = 2
   cap = cv2.VideoCapture("speak.mp4")
   fps = cap.get(cv2.CAP_PROP_FPS)
   fps /= 1000
   framerate = time.time()
   elapsed = 0
   while(cap.isOpened()):
       ret, frame = cap.read()
       if ret:
           scale_percent = 50 # percent of original size (the higher it is, the slower the fps)
           width = int(frame.shape[1] * scale_percent / 100)
           height = int(frame.shape[0] * scale_percent / 100)
           dim = (width, height)
           frame = cv2.resize(frame, dim, interpolation = cv2.INTER_AREA)
 
 
           elapsed += 1
           frame = cv2.putText(frame, f"{elapsed / (time.time() - framerate):.2f} FPS", (2, 530), font, fontScale, color, thickness, cv2.LINE_AA)           
           cv2.imshow("Face", frame)
           if cv2.waitKey(1) & 0xFF == ord('q'):
               break
       else:
           print('cap')
           cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
 
 
   cap.release()
   cv2.destroyAllWindows()
 
if __name__=="__main__":
   sio.connect('http://192.168.2.14:5000')
   print("hai")
   main()
 