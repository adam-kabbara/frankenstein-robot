let wave_btn = document.getElementById("wave-btn");
let flex_btn = document.getElementById("flex-btn");
let reset_btn = document.getElementById("reset-btn");
let sit_btn = document.getElementById("sit-btn");
let control_left_btn = document.getElementById("control-left-btn");
let both_btn = document.getElementById("both-btn");
let control_right_btn = document.getElementById("control-right-btn");

let arm_up_btn = document.getElementById("arm-up-btn");
let arm_down_btn = document.getElementById("arm-down-btn");
let next_scene_btn = document.getElementById("next-scene-btn");
let prev_scene_btn = document.getElementById("prev-scene-btn");
let rotation_up_btn = document.getElementById("rotation-up-btn");
let rotation_down_btn = document.getElementById("rotation-down-btn");
let step_btn = document.getElementById("step-btn");

let move_right_btn = document.getElementById("move-right-btn");
let move_down_btn = document.getElementById("move-down-btn");
let move_left_btn = document.getElementById("move-left-btn");
let move_up_btn = document.getElementById("move-up-btn");

let left_hand_btn = document.getElementById("left-hand-btn");
let right_hand_btn = document.getElementById("right-hand-btn");

let hold_press_btns = [
    arm_down_btn, arm_up_btn, rotation_down_btn, rotation_up_btn, 
    move_right_btn, move_down_btn, move_left_btn, move_up_btn];
let click_press_btns = [
    flex_btn, reset_btn, sit_btn, control_left_btn, both_btn, control_right_btn,
    prev_scene_btn, next_scene_btn, step_btn, left_hand_btn, right_hand_btn, wave_btn]

hold_press_btns.concat(click_press_btns).forEach((btn)=>{
    let timerID;
    let counter = 0;

    btn.addEventListener("mousedown", pressingDown, false);
    btn.addEventListener("mouseup", notPressingDown, false);
    btn.addEventListener("mouseleave", notPressingDown, false);
    btn.addEventListener("touchstart", pressingDown, false);
    btn.addEventListener("touchend", notPressingDown, false);

    function pressingDown(e) {
        requestAnimationFrame(timer);
        e.preventDefault();
    }

    function notPressingDown(e) {
        cancelAnimationFrame(timerID);
        counter = 0;
        if (btn.classList.contains("glow")){//if the button has been pressed (mouse down)
            console.log("logic");
            if (hold_press_btns.includes(btn)){
                send_btn_command("released", btn.id);
                console.log("sent released message");
            }
            else if (click_press_btns.includes(btn)) {
                send_btn_command("clicked", btn.id);
                console.log("sent click message");
            }
            btn.classList.remove("glow");
            update_html_btn_click(btn.id);
        }
    }

    function timer() {
        if (counter === 1){
            btn.classList.add("glow");
            if (hold_press_btns.includes(btn)){
                send_btn_command("pressed", btn.id);
                console.log("sent pressed message")
            }
        }
        timerID = requestAnimationFrame(timer);
        counter++;
    }
});

function send_btn_command(status, elem_id){
    if (elem_id == right_hand_btn.id){ // robot can only contract right hand rn 
        if (right_hand_btn.children[1].innerText.toLowerCase() == "open right"){
            elem_id = "open-right-hand"
        }
        else{
            elem_id = "close-right-hand"
        }
    }

    fetch("/control", {
        method: "POST",
        headers: {"Content-type": "application/json"},
        body: JSON.stringify({status:status, id:elem_id})
      }).then(res => {
        console.log("Request complete! response:", res.status);
    });
}

function update_html_btn_click(elem_id){
    let txt;
    let icon;

    if (elem_id == sit_btn.id){
        txt = sit_btn.children[1]; icon = sit_btn.children[0];
        if (txt.innerText.toLowerCase() == "sit"){
            txt.innerText = "Stand";
            icon.classList.add("fa-arrow-up"); icon.classList.remove("fa-chair");
        }
        else{
            txt.innerText = "Sit";
            icon.classList.add("fa-chair"); icon.classList.remove("fa-arrow-up");
        }
    }
    else if (elem_id == left_hand_btn.id){
        txt = left_hand_btn.children[1];
        if (txt.innerText.toLowerCase() == "close left"){
            txt.innerText = "Open Left";
        }
        else{
            txt.innerText = "Close Left";
        }
    }
    else if (elem_id == right_hand_btn.id){
        txt = right_hand_btn.children[1];
        if (txt.innerText.toLowerCase() == "close right"){
            txt.innerText = "Open Right";
        }
        else{
            txt.innerText = "Close Right";
        }
    }
    else if (elem_id == control_right_btn.id){
        control_right_btn.classList.add("selected");
        both_btn.classList.remove("selected");
        control_left_btn.classList.remove("selected");
    }
    else if (elem_id == both_btn.id){
        both_btn.classList.add("selected");
        control_right_btn.classList.remove("selected");
        control_left_btn.classList.remove("selected");
    }    
    else if (elem_id == control_left_btn.id){
        control_left_btn.classList.add("selected");
        both_btn.classList.remove("selected");
        control_right_btn.classList.remove("selected");
    }
}
