import json, os
# TODO1 login system for users in one file(how much intetnet used, ban for different amount of time, if ban is forever then time == inf and you cannot access to system)

# TODO3 make better security for admin(email 2 step)

# TODO2 graphical ui using turtle or pygame



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
    
def saveUser(userfile, users):
    with open(userfile, "w", encoding="utf-8") as file:
        json.dump(users, file, indent=4, ensure_ascii=False)
    
    file.close()

    
def registerUser():
    name = input("Введите имя: ").lower()
    email = input("Введите email: ").lower().strip()
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
                    saveUser(userfile, users)
                    print(f"Баланс пополнен, ваш текуший баланс {user['balance']}")
                    return
                else:
                    print("Введите коректную сумму")
                    return
            except ValueError:
                print("Введите коректную сумму: ")
                return
            
# def banUser():
#     users = loadUsers(userfile)
#     admin = input("Логин админа:").lower()
#     if admin == "admin":
#         email = str(input("Email для блокировки: ").lower())
#         for user in users:
#             if user["email"] == email:
#                 if user.get("banned", True):
#                     print("Юзер уже забанен")
#                 else:
#                     user["banned"] = True
#                     saveUser(userfile, users)
#                     print(f"Пользователь {email} был забанен ")
#             else:
#                 print("Пользователь не найден")
#                 return
    
def banUser():
    #TODO0 add admin password 
    users = loadUsers(userfile)
    admin = input("Логин админа:").lower()
    if admin == "admin":
        email = str(input("Email для блокировки: ").lower())
        user_found = False
        
        for user in users:
            if user["email"] == email:
                user_found = True
                if user.get("banned", False):
                    print("Юзер уже забанен")
                else:
                    user["banned"] = True
                    saveUser(userfile, users)
                    print(f"Пользователь {email} был забанен")
                break  # Exit the loop once user is found
        
        if not user_found:
            print("Пользователь не найден")
    else:
        print("Неверный логин админа")
        
# TODO0 write a func to delete the whole json

        
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
