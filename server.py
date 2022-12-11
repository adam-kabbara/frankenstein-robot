import json
from flask import Flask, render_template, request, redirect, url_for
from flask_socketio import SocketIO, emit
import openai
import private

app = Flask(__name__)
socketio = SocketIO(app)
socket_ids = {}
openai.organization = private.organization
openai.api_key = private.key

# ---------------- flask routes ----------------
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/control", methods=["GET", "POST"])
def control():
    if request.method == "GET":
        return render_template("control.html")
    elif request.method == "POST":
        data = request.get_json()
        handel_command(data)
        return "Sucesss", 200

@app.route("/ai", methods=["GET", "POST"])
def ai():
    if request.method == "GET":
        return render_template("ai.html", res="null")
    elif request.method == "POST":
        text = request.form['question']
        res = handle_ai_question(text) #TODO add tkinter window on server so students can see qustions and ans
        return render_template("ai.html", res=res)

# ---------------- event handlers ----------------
def handel_command(command):
    print(command)
    if "scene-btn" in command["id"]:
        socketio.emit("messages", {"function":"scene-control", command["status"]: command["id"]}, room=socket_ids["screen"])
    else:
        socketio.emit("message", {"function":"motor-control", command["status"]: command["id"]}, room=socket_ids["rp4"])

def to_third_pov(text):
    return text.replace("your", "his").replace("you", "he").replace("are", "is")\
        .replace("do", "does").replace("he does", "he do")

def get_gpt3_response(question):
    print(f"usr quesiton: {question}\n")
    if question.lower().startswith("ram: "): # repeate after me
        robot_response = question[5:]
    else:                                   # format question to send to openai
        converted_question = f"ask Frankenstein's monster {to_third_pov(question).lower()}" #todo
        print(f"converted question: {converted_question}\n")
        # ask question
        res = json.loads(str(openai.Completion.create(
            model="text-davinci-003",
            prompt=f"{converted_question}",
            max_tokens=70, # todo change back to 70
            temperature=0.7,
            top_p=1
        )))
        gpt3_response = res['choices'][0]['text'].strip() # gpt3 response
        print(f"gpt3 response: {gpt3_response}\n")

        if "frankenstein's monster" in gpt3_response.lower():
        # Convert ans from third person to first person
            res = json.loads(str(openai.Completion.create(
                model="text-davinci-003",
                prompt=f"Convert this from third-person to first-person:\n{gpt3_response}",
                max_tokens=70,
                temperature=0,
                top_p=1
            )))
        robot_response = res['choices'][0]['text'].strip()
        print(f"\nmonster's response: {robot_response}")
    return robot_response

def handle_ai_question(question):
    ans = get_gpt3_response(question)
    print(question)
    socketio.emit("messages", {"fucnction": "speak","text": ans}, room=socket_ids["screen"])
    return ans


# ---------------- socket routes ----------------
@socketio.on('message')
def socket_message(data):
    print(f"received message: {data}")
    if "device-name" in data:
        socket_ids[data["device-name"]] = request.sid
        print(socket_ids)

@socketio.on('connect')
def socket_connection():
    print("got a connection")
    emit('message', {'data': 'Connected'})


if __name__ == "__main__":
    socketio.run(app, port=5000, debug=True, host="192.168.2.14")
