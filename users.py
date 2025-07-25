import json, os

userfile = "users.json"
    
def loadUsers(userfile):
    if os.path.exists(userfile) and os.path.getsize(userfile) > 0:
        with open(userfile, "r", encoding="utf-8") as file:
            try:
                data = json.load(file)
                return data if isinstance(data,list) else[]
            except json.JSONDecodeError:
                return []
    else:
        return []
    
def saveUser(users):
    with open(userfile, "w", encoding="utf-8") as file:
        json.dump(users, file, indent=4, ensure_ascii=False)

    
def registerUser():
    name = input("Введите имя: ").lower()
    email = input("Введите email: ").lower()
    password = input("Введите пароль: ").strip()

    users = loadUsers(userfile)

    if any(user["email"] == email for user in users):
        print("Этот email уже занят")
        return False
    
    newUsers = {
        "email": email,
        "password": password,
        "name": name,
        "balance": 0,
        "banned": False
        }
    users.append(newUsers)

    with open(userfile, "w", encoding="utf-8") as file:
        json.dump(users, file, indent=4, ensure_ascii=False)
    print("Пользователь зарегистрирован успешно")
    return True

def addBalance():
    email = input("Введите ваш email: ").lower()
    users = loadUsers(userfile)
    for user in users:
        if user["email"] == email:
            try :
                amount = float(input("Введите сумму:"))
                if amount > 0:
                    user["balance"] += amount
                    saveUser(users)
                    print(f"Баланс пополнен, ваш текуший баланс {user['balance']}")
                    return
                else:
                    print("Введите коректную сумму")
                    return
            except ValueError:
                print("Введите коректную сумму: ")
                return
            
def banUser():
    admin = input("Логин админа:").lower()
    if admin == "admin":
        email = input("Email для блокировки: ").lower().strip()
        users = loadUsers(userfile)
        for user in users:
            if user["email"] == email:
                if user.get("banned", False):
                    print("Юзер уже забанен")
                else:
                    user["banned"] = True
                    saveUser(users)
                    print(f"Пользователь {email} был забанен ")
            else:
                print("Пользователь не найден")
                return

        
def main():
    while True:
        print("Что вы хотите сделать")
        print("1. Зарегистрироватся")
        print("2. Добавить баланс")
        print("3. Забанить Юзера")
        print("4. Выйти")

        choice = input("Ваш выбор: ")
        if choice == "1":
            registerUser()
        elif choice == "2":
            addBalance()
        elif choice == "3":
            banUser()
        elif choice == "4":
            break
        else:
            print("Неверный выбор")

main()