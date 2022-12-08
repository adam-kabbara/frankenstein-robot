import socketio

sio = socketio.Client()

@sio.event
def connect():
    print("I'm connected!")

@sio.event
def message(data):
    print(f'I received a message!\n{data}')

def start():
    sio.connect('http://localhost:5000')
    sio.emit('message', {'foo': 'bar'})

if __name__=="__main__":
    start()
    print("hai")
