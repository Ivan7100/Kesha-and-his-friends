import json
import os
import datetime

class PlayerData:
    """
    Класс PlayerData содержит данные о персонажах и их состоянии.
    """
    def __init__(self, file_name):
        """
        Инициализирует класс PlayerData, загружает данные из файла.
        """
        self.file_name = os.path.join("data/saves", file_name)
        self.data = {}
        try:
            with open(self.file_name, "r", encoding="utf-8") as file:
                self.data = json.load(file)
        except FileNotFoundError:
            self.data = {
                "kesha": {
                    "money": 0,
                    "mood": 100.0,
                    "satiety": 50.0,
                    "energy": 100.0,
                    "purity": 50.0,
                    "is_sleeping": True,
                    "bg_kitchen": "bg_kitchen.jpg",
                    "bg_bathroom": "bg_bathroom.jpg",
                    "bg_playroom": "bg_playroom.jpg",
                    "bg_bedroom": "bg_bedroom.jpg",
                    "character_image": "kesha_image.webp",
                    "last_room": "kitchen",
                    "games": [
                        "Тенис",
                        "Бомбы и пончики",
                        "Лабиринт"
                    ],
                    "shop": {
                        "classic_skin": ["kesha_image.webp", 0],
                        "other_skin": ["other_kesha_image.png", 600],
                        "classic_bg_skin": [["bg_kitchen.jpg", "bg_bathroom.jpg",
                                             "bg_playroom.jpg", "bg_bedroom.jpg"], 0],
                        "other_bg_skin": [["other_bg_kitchen.jpg", "bg_bathroom.jpg",
                                           "other_bg_playroom.jpg", "other_bg_bedroom.jpg"], 600],
                        "cola": [250, 70],
                        "porridge": [150, 30],
                        "cutlet": [200, 50],
                        "chocolate": [100, 25]
                    }
                },
                "monkey": {
                    "money": 0,
                    "mood": 100.0,
                    "satiety": 50.0,
                    "energy": 100.0,
                    "purity": 50.0,
                    "is_sleeping": True,
                    "bg_kitchen": "bg_kitchen.jpg",
                    "bg_bathroom": "bg_bathroom.jpg",
                    "bg_playroom": "bg_playroom.jpg",
                    "bg_bedroom": "bg_bedroom.jpg",
                    "character_image": "monkey_image.jpg",
                    "last_room": "kitchen",
                    "games": [
                        "Змейка",
                        "Обезьяна и чайник",
                        "Кубопад"
                    ],
                    "shop": {
                        "classic_skin": ["monkey_image.jpg", 0],
                        "other_skin": ["other_monkey_image.png", 600],
                        "classic_bg_skin": [["bg_kitchen.jpg", "bg_bathroom.jpg",
                                             "bg_playroom.jpg", "bg_bedroom.jpg"], 0],
                        "other_bg_skin": [["other_bg_kitchen.jpg", "bg_bathroom.jpg",
                                           "other_bg_playroom.jpg", "other_bg_bedroom.jpg"], 600],
                        "cola": [250, 70],
                        "porridge": [150, 30],
                        "cutlet": [200, 50],
                        "chocolate": [100, 25]
                    }
                },
                "elephant": {
                    "money": 0,
                    "mood": 100.0,
                    "satiety": 50.0,
                    "energy": 100.0,
                    "purity": 50.0,
                    "is_sleeping": True,
                    "bg_kitchen": "bg_kitchen.jpg",
                    "bg_bathroom": "bg_bathroom.jpg",
                    "bg_playroom": "bg_playroom.jpg",
                    "bg_bedroom": "bg_bedroom.jpg",
                    "character_image": "elephant_image.jpg",
                    "last_room": "kitchen",
                    "games": [
                        "Тетрис",
                        "Circle clicker",
                        "Flappy Elephant"
                    ],
                    "shop": {
                        "classic_skin": ["elephant_image.jpg", 0],
                        "other_skin": ["other_elephant_image.png", 600],
                        "classic_bg_skin": [["bg_kitchen.jpg", "bg_bathroom.jpg",
                                             "bg_playroom.jpg", "bg_bedroom.jpg"], 0],
                        "other_bg_skin": [["other_bg_kitchen.jpg", "bg_bathroom.jpg",
                                           "other_bg_playroom.jpg", "other_bg_bedroom.jpg"], 600],
                        "cola": [250, 70],
                        "porridge": [150, 30],
                        "cutlet": [200, 50],
                        "chocolate": [100, 25]
                    }
                },
                "last_session_time": str(datetime.datetime.now()),
                "last_character": "kesha"
            }

    def save(self):
        """
        Сохраняет данные в файл.
        """
        with open(self.file_name, "w", encoding="utf-8") as file:
            json.dump(self.data, file, ensure_ascii=False, indent=4)
    
    def add_money(self, amount: int, character: str):
        """
        Добавляет деньги персонажу и обновляет его настроение.
        """
        self.data[character]["money"] += amount
        self.data[character]["mood"] = min(max(self.data[character]["mood"] + (amount / 10), 0), 100)
        self.save()
    
    def update_stats(self):
        """
        Обновляет состояние персонажей.
        """
        now = datetime.datetime.now()
        time = datetime.datetime.strptime(self.data["last_session_time"], '%Y-%m-%d %H:%M:%S.%f')
        self.data["last_session_time"] = str(now)
        time = now - time
        delta_time = time.seconds + time.days * 24 * 60 * 60 + time.microseconds / 1000000
        for i in ["kesha", "monkey", "elephant"]:
            self.data[i]["mood"] = max(min(self.data[i]["mood"] - delta_time * 0.00154, 100), 0)
            if not self.data[i]["is_sleeping"]:
                self.data[i]["energy"] = max(min(self.data[i]["energy"] + delta_time * 0.00347, 100), 0)
            else:
                self.data[i]["energy"] = max(min(self.data[i]["energy"] - delta_time * 0.00154, 100), 0)
            self.data[i]["satiety"] = max(min(self.data[i]["satiety"] - delta_time * 0.00154, 100), 0)
            self.data[i]["purity"] = max(min(self.data[i]["purity"] - delta_time * 0.00154, 100), 0)

        self.save()



if __name__ == "__main__":
    data = PlayerData("save1.json")
    data.update_stats()