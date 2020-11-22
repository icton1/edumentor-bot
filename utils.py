from storage import get_user_info, set_user_info


def create_new_user_document(message):
    return {
        "userinfo": {
            "id": message.from_user.id,
            "name": message.from_user.first_name,
            "username": message.from_user.username,
        },
        "current_state": "default",
        "scenario_state": {}
    }


def get_scenario_state(user_document):
    scenario_name = user_document["current_state"]
    if scenario_name == "default":
        return None
    scenario_element = user_document.get(scenario_name)
    if scenario_element is None:
        print("Error: Запрос стейта несуществующего сценария: " + scenario_name)
        return None
    return scenario_element.get("current_state")


def set_scenario(user_document, scenario_name, doc={}):
    user_document["current_state"] = scenario_name
    user_document[scenario_name] = doc
    set_user_info(user_document["userinfo"]["id"], user_document)


def set_scenario_state(user_document, scenario_state):
    scenario_name = user_document.get("current_state")
    scenario_element = user_document.get(scenario_name)
    if scenario_element is None:
        user_document[scenario_name] = {
            "current_state": scenario_state
        }
    else:
        scenario_element["current_state"] = scenario_state
    set_user_info(user_document["userinfo"]["id"], user_document)


def get_current_scenario(message):
    user_document = get_user_info(message.from_user.id)
    if user_document is None:
        return "on_start_scenario"
    return user_document.get("current_state")
