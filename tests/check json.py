import json

dataDef = {
    "Level": 0,
    "Life": 3,
    "Guards": 1
}

data = {}

def defaultSave():
    with open("save.json", "w", encoding="utf-8") as file:
        json.dump(dataDef, file, indent=4, ensure_ascii=False)

def save():
    global data
    with open("save.json", "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

def loadSave():
    global data
    with open("save.json", "r", encoding="utf-8") as file:
        data = json.load(file)

def guards():
    global data
    i = data["Level"]
    if data["Level"] == i:
        data["Guards"] += 1
        save()
    else:
        return False

def newLevel(score):
    global data
    if score == 0:
        data["Level"] += 1
        save()
        guards()
        Life()
    else:
        return False
    
def Life():
    global data
    user = int(input())
    x = 0
    if user == 2:
        data["Life"] -= 1
        save()
        if data["Life"] == 0:
            x += 1
            dataDef["Смертей"] = x
            defaultSave()
            x += 1
            return x

loadSave()             
newLevel(0)
print(data)




