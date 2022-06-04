var chatSocket, step;
const wordInput = document.getElementById("load-word");
const statusImg = document.getElementById("status-img");
const newLetterInput = document.getElementById("new-letter");
const letterPositionLabel = document.getElementById("selected-position");
const checkButton = document.getElementById("next-btn");
const startButton = document.getElementById("start-btn");
const spentTimeLabel = document.getElementById("spent-time");
const checkBlock = document.getElementById("check-block");


checkButton.onclick = function(evt) {
    const letter = newLetterInput.value;
    const position = parseInt(letterPositionLabel.innerHTML);

    if (!letter || !('а' <= letter && letter <= 'я')) {
        alert('U can check only ukrainian alphabet');
        return;
    }

    if (!position) {
        alert('U must select letter position before check');
        return;
    }

    console.log("Sending check event", position, letter);
    chatSocket.send(JSON.stringify({
        'hangman game': 'check',
        'position': position,
        'letter': letter
    }));
};


startButton.onclick = function(evt) {
    chatSocket && chatSocket.close();
    chatSocket = new WebSocket(
        'ws://'
        + window.location.host
        + '/ws/hangman/'
    );
    checkBlock.classList.remove("none");

    chatSocket.onmessage = function(evt) {
        const data = JSON.parse(evt.data);
        
        console.log(data)
        if (data['event'] == 'game initialized') {
            chatSocket.send(JSON.stringify({
                'hangman game': 'connect'
            }));
        }

        if ("word" in data) {
            const word = data.word;
            wordInput.setAttribute("word", JSON.stringify(word));
            wordInput.click();

            const attempt = data.attempt;
            statusImg.src = `${STATIC_BASE}/assets/step${attempt}.svg`

            if (attempt == '5') {
                checkBlock.classList.add("none");
            }
        }

        if ("time" in data) {
            spentTimeLabel.innerHTML = data.time;
        }
    };
}
