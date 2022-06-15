import json
from js import console, document, window, STATIC_BASE, createWebSocket, alert


step = 1
next_btn = Element("next-btn")
start_btn = Element("start-btn")
check_btn = Element("next-btn")
status_img = Element("status-img")
new_letter_input = Element("new-letter")
selected_position_input = Element("selected-position")
word_input = Element("load-word")
word_box = document.getElementsByClassName("word-box")[0]
check_block = Element("check-block")
spent_time_label = Element("spent-time")


socket = None


def select_letter(letter, position):
    def select_letter_(evt, *args, **kwargs):
        new_letter_input.element.value = letter
        selected_position_input.element.innerHTML = position
        console.log("Active position", position)
    return select_letter_


def load_word(letters: list):
    console.log(word_input)
    word_box.innerHTML = "" 
    for pos, letter_obj in enumerate(letters, start=1):
        status = letter_obj["status"]
        letter = letter_obj["letter"] 

        letter_box = create("div", classes="word-box__letter-box")   
        if status == "correct":
            letter_box.element.classList.add("letter-box__correct")
        elif status == "incorrect":
            letter_box.element.classList.add("letter-box__incorrect")

        position_label = create("div", classes="letter-box__position")
        position_label.element.innerHTML = pos
        letter_box.element.appendChild(position_label.element)

        letter_label = create("div", classes="letter-box__letter")
        letter_label.element.innerHTML = "?" if status == "empty" else letter
        letter_box.element.appendChild(letter_label.element)

        if status != "correct":
            letter_box.element.onclick = select_letter(letter, pos)
        word_box.appendChild(letter_box.element)


def check_letter(letter: str, position: int) -> None:
    if (
        not letter
        or not ('а' <= letter <= 'я')
    ):
        alert("U can check only Ukrainian alphabet")
        return

    if not position:
        alert("U must select letter position before check")
        return

    console.log("Sending check event", position, letter);
    global socket
    socket.send(json.dumps({
        'hangman game': 'check',
        'position': position,
        'letter': letter
    }))


def handle_check_letter(evt):
    letter = new_letter_input.value;
    position = int(selected_position_input.element.innerHTML);
    check_letter(letter, position)


def handle_socket_message(evt):
    console.log('Handle event', evt)
    global socket

    if not socket:
        console.log("Socket is closed")
        return

    data = json.loads(evt.data)
    check_block.element.classList.remove("none");
    if 'event' in data and data['event'] == 'game initialized':
        socket.send(
            json.dumps({
                'hangman game': 'connect'
            }
        ))

    if "word" in data:
        word = data["word"]
        load_word(word)

        attempt = data["attempt"]
        status_img.element.src = f"{STATIC_BASE}/assets/step{attempt}.svg"

        if attempt == 5:
            check_block.element.classList.add("none")
            console.log("Stop game")

    if "time" in data:
        spent_time_label.element.innerHTML = data["time"];


def run_game(*args, **kwargs):
    global socket
    socket and socket.close()
    socket = createWebSocket(
         'ws://'
         + window.location.host
         + '/ws/hangman/'
    )
    socket.onmessage = handle_socket_message


start_btn.element.onclick = run_game
check_btn.element.onclick = handle_check_letter

