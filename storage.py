from settings import SHELVE_NAME, get_filename
import shelve


def set_mentor(user_id, field, topic):
    with shelve.open(get_filename(SHELVE_NAME)) as storage:
        storage["m" + str(user_id) + topic] = {
            "user_id": user_id,
            "field": field,
            "topic": topic
        }


def get_mentors():
    with shelve.open(get_filename(SHELVE_NAME)) as storage:
        keys = []
        for key in storage.keys():
            if key.startswith("m"):
                keys.append(key)

        return [storage[k] for k in keys]


def get_user_info(user_id):
    with shelve.open(get_filename(SHELVE_NAME)) as storage:
        try:
            return storage[str(user_id)]
        except KeyError:
            return None


def set_user_info(user_id, document):
    with shelve.open(get_filename(SHELVE_NAME)) as storage:
        storage[str(user_id)] = document


def del_user_info(user_id):
    with shelve.open(get_filename(SHELVE_NAME)) as storage:
        del storage[str(user_id)]


def get_users():
    with shelve.open(get_filename(SHELVE_NAME)) as storage:
        userids = [storage[key] for key in storage.keys()]
        return userids


def clear_storage():
    with shelve.open(get_filename(SHELVE_NAME)) as storage:
        storage.clear()
