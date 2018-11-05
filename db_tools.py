import json


def get_banned_list():
    file = open('banlist.json', 'r')
    banned_list = json.load(file)
    return banned_list


def is_in_list(check_id):
    if check_id in get_banned_list():
        return True
    return False


def renew_banned_list(banned_list):
    file = open('banlist.json', 'w')
    json.dump(banned_list, file)


def add_id_to_banned_list(new_id):
    current_list = get_banned_list()
    if new_id not in current_list:
        current_list.append(new_id)
    renew_banned_list(current_list)


def del_from_banned_list(del_id):
    current_list = get_banned_list()
    if del_id in current_list:
        current_list.remove(del_id)
    renew_banned_list(current_list)
