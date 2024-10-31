import configparser

config = configparser.ConfigParser()

def username ():
    config.read("settings.ini")
    name = config["UserSettings"]["username"]
    return name
def update_username(n_username):
    config.read("settings.ini")
    config["UserSettings"]["username"] = n_username
    with open("settings.ini", "w") as configfile:
        config.write(configfile)
