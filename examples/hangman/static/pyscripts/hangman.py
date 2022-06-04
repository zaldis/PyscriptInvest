import json
from js import console, document


step = 1
next_btn = Element("next-btn")
status_img = Element("status-img")
new_letter_input = Element("new-letter")
selected_position_input = Element("selected-position")
word_input = Element("load-word")
word_box = document.getElementsByClassName("word-box")[0]


def select_letter(letter, position):
    def select_letter_(evt, *args, **kwargs):
        new_letter_input.element.value = letter
        selected_position_input.element.innerHTML = position
        console.log("Active position", position)
    return select_letter_


def load_word(*args, **kwargs):
    console.log(word_input)
    letters = json.loads(
        word_input.element.getAttribute("word")
    )
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


word_input.element.onclick = load_word
