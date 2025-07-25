import json
import os

default_data = {
    "Level": 0,
    "Life": 3,
    "Guards": 1,
}

data = {}

def defaultSave():
    with open("save.json", "w", encoding="utf-8") as file:
        json.dump(default_data, file, indent=4, ensure_ascii=False)

def save():
    with open("save.json", "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

def loadSave():
    global data
    if not os.path.exists("save.json"):
        defaultSave()
    with open("save.json", "r", encoding="utf-8") as file:
        data = json.load(file)

def increaseGuards():
    data["Guards"] += 1
    save()

def newLevel(score):
    if score == 0:
        data["Level"] += 1
        increaseGuards()
        handleLife(2)
        save()

def handleLife(user_input):
    if user_input == 2:
        data["Life"] -= 1
        if data["Life"] <= 0:
            data["Смертей"] += 1
            print("Игрок умер. Перезапуск.")
            defaultSave()
        save()

loadSave()
newLevel(0)
print(data)


