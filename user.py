import json
from language import default_lang

users = {}

class User:
    id = 0
    lang = ""
    mode = "none"
    login = ""
    name = ""
    last_name = ""
    email = ""
    callback = ""
    promos = []

    def __init__(self, id, lang=default_lang, login="", name="", last_name="", email="", callback="", promos=[]) -> None:
        self.id = id
        self.lang = lang
        self.login = login
        self.name = name
        self.last_name = last_name
        self.email = email
        self.callback = callback
        self.promos = promos


def get_user(id: int) -> User:
    global users

    for id in users.keys():
        return users[id]
    
    config = {}
    with open("users.json", encoding="utf8") as f:
        config = json.load(f)
        if str(id) in config.keys():
            users[id] = User(id, config[str(id)]["lang"], config[str(id)]["login"], config[str(id)]["name"],
                            config[str(id)]["last_name"], config[str(id)]["email"], config[str(id)]["callback"], config[str(id)]["promos"])
            return users[id]
        
        users[id] = User(id)
        user = {id: {"lang": users[id].lang, "login": users[id].login, "name": users[id].name, "last_name": users[id].last_name,
                     "email": users[id].email, "callback": users[id].callback, "promos": users[id].promos}}
        config.update(user)
    
    with open("users.json", "w") as f:
        json.dump(config, f, indent=2)

    return users[id]


def update_user(id, lang=None, login=None, name=None, last_name=None, email=None, callback=None, promos=None):
    user = get_user(id)
    if lang != None:
        user.lang = lang
    if login != None:
        user.login = login
    if name != None:
        user.name = name
    if last_name != None:
        user.last_name = last_name
    if email != None:
        user.email = email
    if callback != None:
        user.callback = callback
    if promos != None:
        user.promos = promos
    
    with open("users.json", "r+") as f:
        data = json.load(f)
        data[str(id)]["lang"] = user.lang
        data[str(id)]["login"] = user.login
        data[str(id)]["name"] = user.name
        data[str(id)]["last_name"] = user.last_name
        data[str(id)]["email"] = user.email
        data[str(id)]["callback"] = user.callback
        data[str(id)]["promos"] = user.promos
        f.seek(0)
        json.dump(data, f, indent=2)
        f.truncate()