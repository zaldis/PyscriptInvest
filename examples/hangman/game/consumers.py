from datetime import timedelta
import json
import time
import threading

from django.utils import timezone

from channels.generic.websocket import WebsocketConsumer


class TimerThread(threading.Thread):
    def __init__(self, call_func, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.call_func = call_func
        self._stop = threading.Event()

    def stop(self):
        self._stop.set()
        print("Thread was stopped")
    
    def stopped(self):
        return self._stop.isSet()

    def run(self):
        while not self.stopped():
            self.call_func()
            time.sleep(1)


def get_pretty_time(td: timedelta) -> str:
    minutes = td.seconds // 60
    seconds = td.seconds % 60
    return f'{minutes}m {seconds}s'


class GameConsumer(WebsocketConsumer):

    def connect(self):
        self.start_point = timezone.now()
        self.accept()
        self.timer_thread = TimerThread(
            call_func=lambda: self.send(
                text_data=json.dumps({"time": get_pretty_time(timezone.now() - self.start_point)})
            )
        )
        self.timer_thread.daemon = True
        self.send(
            text_data=json.dumps({
                'event': 'game initialized'
            })
        )
        self.attempt = 1
        
    def disconnect(self, close_code):
        print("Socket was closed", close_code)
        self.timer_thread.stop()

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
		
        if 'hangman game' in text_data_json:
            command = text_data_json['hangman game']
            if command == 'connect':
                """
                Initiate the game
                """
                self.word = "непередбачуваність"
                self.letters = [
                    {'letter': '?', 'status': 'empty'}
                    for _ in self.word
                ]
                self.send(text_data=json.dumps({
                    'message': 'New game',
                    'word': self.letters,
                    'attempt': self.attempt        
                }))
                if not self.timer_thread.is_alive():
                    self.timer_thread.start()

            elif command == 'check':
                position, letter = int(text_data_json['position'])-1, text_data_json['letter']
                is_correct = (self.word[position] == letter)
                self.letters[position]['status'] = 'correct' if is_correct else 'incorrect'
                self.letters[position]['letter'] = letter
                if not is_correct:
                    self.attempt += 1
                self.send(text_data=json.dumps({
                    'message': 'Checker result',
                    'word': self.letters,
                    'attempt': self.attempt
                }))

                if self._is_game_over():
                    self.timer_thread.stop()    

    def _is_game_over(self):
        return self.attempt == 5
