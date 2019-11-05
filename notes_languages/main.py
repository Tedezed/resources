# Python 3.5.2
# By Tedezed

import json, random

def menu(mode, input_msg, input_list):
    print(chr(27) + "[2J")
    print(input_msg)
    for i,o in enumerate(input_list):
        if mode == "menu":
            print("[%s] %s" % (i, o))
        else:
            print("%s" % (o))

    ok_option = False
    option = -1
    if mode == "menu":
        while not ok_option:
            option = int(input("> "))
            if option <= len(input_list)-1 \
              and option >= 0:
                ok_option = True
    return option

def query(mode, input_msg, input_list, mode_select_answer, mode_select):
    print(chr(27) + "[2J")
    print(input_msg)
    for i,o in enumerate(input_list):
        if mode == "select_correct":
            print("  [%s] %s" % (i, o[mode_select]))
        elif mode == "write_correct":
            print("  - %s" % (o[mode_select]))
        else:
            print("%s" % (o))

    correct_id = random.randrange(0,len(input_list),1)
    if mode == "select_correct":
        print("Word: %s" % (input_list[correct_id][mode_select_answer]))
    elif mode == "write_correct":
        print("Write Word in %s: %s" % (mode_select_answer, input_list[correct_id][mode_select_answer]))

    ok_option = False
    option = -1
    while not ok_option:
        if mode == "select_correct":
            try:
                option = int(input("> "))
                if correct_id == option:
                    ok_option = True
            except ValueError as e:
                print("[ERROR] Input number")
        elif mode == "write_correct":
            option = input("> ")
            if input_list[correct_id][mode_select] == option:
                ok_option = True
    return option

def found_in_list(mother_language, input_word, input_list):
    found = False
    for i in input_list:
        if i[mother_language] == input_word[mother_language]:
            found = True
    return found

def select_correct(options_num, data, mother_language, language_to_learn):
    print(1)
    len_langs = len(data["dic_langs"])
    list_words = []
    for i in range(0,options_num,1):
        random_word_ok = False
        while not random_word_ok:
            random_word = data["dic_langs"][random.randrange(0,len_langs,1)]
            if not found_in_list(mother_language, random_word, list_words) \
               and not random_word_ok:
                list_words.append(random_word)
                random_word_ok = True

    mode_select = random.choice([True, False])
    if mode_select:
        mode_select = mother_language
        mode_select_answer = language_to_learn
    else:
        mode_select = language_to_learn
        mode_select_answer = mother_language

    if random.choice([True, False]):
        query("select_correct", "Words:", list_words, mode_select_answer, mode_select)
    else:
        query("write_correct", "Words:", list_words, mode_select_answer, mode_select)
    print("Correct!")


with open('langs.json', encoding='utf-8') as json_file:
    data = json.load(json_file)

    language_to_learn = menu("menu", "Language to learn:", data["list_langs"])
    mother_language = menu("menu", "Mother language:", data["list_langs"])

    print(language_to_learn)

    while True:
        select_correct(
            4, 
            data, 
            data["list_langs"][mother_language], 
            data["list_langs"][language_to_learn]
            )