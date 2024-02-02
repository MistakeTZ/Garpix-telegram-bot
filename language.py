import glob, os
import json


languages = {}
default_lang = ""
languages_list = []

def start(lang):
    global languages_list, default_lang

    languages_list = get_all_languages()
    default_lang = lang

    if not load_lang(default_lang):
        print("Default language not found")
        

def get_all_languages() -> list:
    arr = []
    for file in glob.glob("lang\*.json"):
        arr.append(file.replace(".json", "").replace("lang\\", ""))

    return arr


def load_lang(lang) -> bool:
    global languages

    if lang in languages.keys():
        return True

    if not lang in languages_list:
        return False
    if not os.path.exists("lang/{}.json".format(lang)):
        return False
    
    with open("lang/{}.json".format(lang), encoding="utf8") as f:
        languages[lang] = json.load(f)

    return True


def get_list() -> list:
    return languages_list


def text(key, lang=default_lang, *args):
    if not lang in languages.keys():
        if not load_lang(lang):
            lang = default_lang

    if key in languages[lang].keys():
        return languages[lang][key].format(*args)
    
    if key in languages[default_lang].keys():
        return languages[default_lang][key].format(args)
    return languages[lang]["NOT_FOUND"]
    

start("ru")