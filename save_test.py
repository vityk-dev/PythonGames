import json, os

FILE = "life.json"
def Save(level,life, filepath=FILE):
    data ={}
    if os.path.exists(filepath):
        with open(filepath, "r",encoding="utf-8") as file:
            try:
                data = json.load(file)
            except json.JSONDecodeError:
                data = {}

            
    data[f"level{level}"] = {
        "level": level,
        "life": life
    }
    
    with open(filepath, "w", encoding="utf-8") as file:    
        json.dump(data, file, ensure_ascii=False, indent=4) 
        


def Load(level, filepath="life.json"):
    if os.path.exists(filepath):
        with open(filepath, "r",encoding="utf-8") as file:
            try: 
                data = json.load(file)
            except json.JSONDecodeError:
                return None
        return data.get(f"level{level}")
    return None

