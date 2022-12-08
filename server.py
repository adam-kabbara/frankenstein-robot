import json
from flask import Flask, render_template, request, redirect, url_for
from flask_socketio import SocketIO, emit
import openai
import private

app = Flask(__name__)
socketio = SocketIO(app)
openai.organization = private.organization
openai.api_key = private.key

# flask routes
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
        return render_template("ai.html")
    elif request.method == "POST":
        text = request.form['question']
        handle_ai_question(text) #TODO add tkinter window on server so students can see qustions and ans
        return redirect(url_for("ai"))

# event handlers
def handel_command(command):
    print(command)
    if command["status"] == "pressed":
        socketio.emit('message', {'data': 'hghgghghgh'})
    elif command["status"] == "released":
        pass
    elif command["status"] == "clicked":
        pass
    else:
        raise Exception("!!!Unidentified status call!!!")


def to_third_pov(text):
    return text.replace("your", "his").replace("you", "he").replace("are", "is")\
        .replace("you", "he").replace("do", "does").replace("he does", "he do")

def get_gpt3_response(question):
#TODO
    if question.lower().startswith("ram: "): # repeate after me
        robot_response = question[5:]
    else:                                   # format question to send to openai
        converted_question = f"ask Frankenstein's monster {to_third_pov(question[8:])}" #todo
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

        if gpt3_response.lower().contains("frankenstein's monster"):
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
    socketio.emit('message', {'data': 'hghgghghgh'})

# SOCKET ROUTS  
@socketio.on('message')
def handle_message(data):
    print(f"received message: {data}")

@socketio.on('connect')
def connect():
    print("got a connection")
    emit('message', {'data': 'Connected'})


if __name__ == "__main__":
    socketio.run(app, port=5000, debug=True, host="localhost")
