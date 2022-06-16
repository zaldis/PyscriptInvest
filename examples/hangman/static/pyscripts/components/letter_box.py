CORRECT_LETTER = 'correct-letter'
INCORRECT_LETTER = 'incorrect-letter'
EMPTY_LETTER = 'empty-letter'


class LetterBox:

    def __init__(self, position: int, letter: str) -> None:
        self._position = position
        self._letter = letter

        correct_letter_theme = PyWidgetTheme("letter-box__correct")
        incorrect_letter_theme = PyWidgetTheme("letter-box__incorrect")
        empty_theme = PyWidgetTheme("empty")
        self._theme_map = {
            CORRECT_LETTER: correct_letter_theme,
            INCORRECT_LETTER: incorrect_letter_theme,
            EMPTY_LETTER: empty_theme
        }
        self.py_element = None

    def build(self, status: str):
        letter_box = create("div", classes="word-box__letter-box")   
        theme = self._theme_map[status]
        theme.theme_it(letter_box.element)

        position_label = create("div", id_=f"letter-position-{self._position}", classes="letter-box__position")
        position_label.element.innerHTML = self._position
        letter_box.element.appendChild(position_label.element)

        letter_label = create("div", classes="letter-box__letter")
        letter_label.element.innerHTML = "?" if status == EMPTY_LETTER else self._letter
        letter_box.element.appendChild(letter_label.element)
        
        self.py_element = letter_box

    @property
    def onclick(self):
        return self.py_element.element.onclick

    @onclick.setter
    def onclick(self, new_handler):
        self.py_element.element.onclick = new_handler
