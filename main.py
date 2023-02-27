from datetime import date, datetime
import json

file = "notes.json"

def conclusion(data):
    if type(data) is str:
        print(data)
    if type(data) is dict:
        print(f"\nID - {data['identifier']}\nНазвание - {data['title']}\nТело заметки - {data['frame']}\nДата-создания - {data['created']}\nДата-обновления заметки - {data['dateUpdate']}\n")
    if type(data) is list:
        for i in data:
            print(f"\nID - {i['identifier']}\nНазвание - {i['title']}\nТело заметки- {i['frame']}\nДата-создания - {i['created']}\nДата-обновления заметки - {i['dateUpdate']}\n")

def readID(identifier:int):
    try:
        get_all_todo = readAll() if readAll() is not None else []
        if 'нет' in get_all_todo:
            return get_all_todo
        get_all_ids = [__id["identifier"] for __id in get_all_todo]
        if identifier not in get_all_ids:
            return 'Запись с таким идентификатором остсутствуют'
        with open(file,'r') as f:
            todo = json.loads(f.read())
            for _ in todo:
                if identifier == _['identifier']:
                    return _
    except FileNotFoundError:
        return "Запиcи отсутствуют\n"

def readAll():
    try:
        with open(file,'r') as f:
            return sorted(
                json.loads(f.read()),
                key=lambda x: (x["created"] == "null", x["created"] == "", x["created"]), 
                reverse=True
            )
    except json.JSONDecodeError:
        return None
    except FileNotFoundError:
        return "Записи отсутствуют"
    
def getlastId():
    try:
        with open(file,'r') as f:
            lastId = [_id['identifier'] for _id in json.loads(f.read())]
            return max(lastId) if len(lastId) != 0 else 0
    except json.JSONDecodeError:
        return None
    except FileNotFoundError:
        with open(file,'a') as f:
            return None

def addNote(title,frame):
    Date = datetime.now().strftime("%d-%m-%Y, %H:%M:%S")
    lastId = getlastId() if getlastId() is not None else 0
    new_todo = {
        "identifier": lastId + 1 , 
        "title": title, 
        "frame": frame, 
        "created": Date, 
        "dateUpdate": Date
    }
    get_all_todo = readAll() if readAll() is not None else []
    all_todo = list(get_all_todo)
    all_todo.append(new_todo)
    with open(file, "w") as f:
        f.write(json.dumps(all_todo, ensure_ascii=False))
    return f"Сохранено"

def update(identifier:int, title, frame):
    try:
        get_all_todo = readAll() if readAll() is not None else []
        if 'нет' in get_all_todo:
            return get_all_todo
        get_all_ids = [__id["identifier"] for __id in get_all_todo]
        if identifier not in get_all_ids:
            return 'Данный идентификатор отсутствует'
        new_todo = [todo for todo in get_all_todo if todo['identifier'] != identifier]
        todo = {}
        for i in get_all_todo:
            if identifier == i['identifirer']:
                todo.update(
                        {
                            "id": i['identidier'], 
                            "title": title, 
                            "body": frame, 
                            "created_at": i['created'], 
                            "date_update": datetime.now().strftime("%m-%d-%Y, %H:%M:%S")
                        }               
                    )
                break
        new_todo.append(todo)
        with open(file, 'w') as f:
            f.write(json.dumps(new_todo, ensure_ascii=False))
        return f"Обновлено"
    except FileNotFoundError:
        return "Пусто"
    
def deleteNote(identifier:int):
    try:
        get_all_todo = readAll() if readAll() is not None else []
        if 'нет' in get_all_todo:
            return get_all_todo
        get_all_ids = [__id["identifier"] for __id in get_all_todo]
        if identifier not in get_all_ids:
            return 'Запись с таким идентификатором не найдена'
        new_all_todo = [todo for todo in get_all_todo if todo['identifier'] != identifier]
        with open(file, "w") as f:
            f.write(json.dumps(new_all_todo, ensure_ascii=False))
        return f'Удалено'
    except FileNotFoundError:
        return "Пусто"
    
print('Выполните командку "help", что бы ознакомиться со всеми командами!')
while True:
    command = str(input("Ввод строки: ")).replace(" ","")
    match command:
        case "help":
            print("Полный список команд, выполняющий в приложении заметки:\n"+
                  "------------------------------------------\n"+
                  "read = чтение заметки по идентификатору\n"+
                  "add = добавление заметки\n"+
                  "update = изменение заметки\n"+
                  "delete = удаление заметки\n"+
                  "quit = выход из приложения\n"+
                  "------------------------------------------")
        case "read":
            identifier = int(input("Введите идентификатор: "))
            conclusion(readID(identifier))
        case "add":
            title = str(input("Заголовок заметки: "))
            frame = str(input("Тело заметки: "))
            conclusion(addNote(title, frame))
        case "update":
            identifier = int(input("Введите идентификатор заметки, котороый необходимо заменить: "))
            title = str(input("Введите новый заголовок: "))
            frame = str(input("Введите новый текст: "))
            conclusion(update(identifier,title,frame))
        case "delete":
            identifier = int(input("Введите идентификатор, который хотите удалить: "))
            conclusion(deleteNote(identifier))
        case "quit":
            break