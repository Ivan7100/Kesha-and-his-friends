import json
import os

class PlayerData:
    def __init__(self, file_name):
        self.file_name = os.path.join('data/saves', file_name)
        self.data = {}
        try:
            with open(self.file_name, 'r', encoding='utf-8') as file:
                self.data = json.load(file)
        except FileNotFoundError:
            self.data = {'money': 0}

    def save(self):
        with open(self.file_name, 'w', encoding='utf-8') as file:
            json.dump(self.data, file, ensure_ascii=False, indent=4)
    
    def add_money(self, amount):
        self.data['money'] += amount
        self.save()