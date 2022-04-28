import sqlite3, datetime, json, nextcord
from time import sleep

json_data = json.load(open("settings.json"))

def create_log(message: str, code: str="ok"):
    out = f"[{code}][{datetime.datetime.now()}]: {message}"
    
    print(out)
    with open(f"logs/log_{datetime.date.today()}.txt", "a", encoding="UTF-8") as file:
        file.write("\n" + out)

def do_to_database(command: str, *options):
    dbFilename = json_data["db"]
    while True:
        try:
            conn = sqlite3.connect(dbFilename, timeout=1)
            cursor = conn.cursor()
            if options == []:
                returnStr = list(cursor.execute(command))
            else:
                returnStr = list(cursor.execute(command, options))
            conn.commit()
            cursor.close()
            conn.close()
            egg = []
            for i in returnStr:
                egg.append(list(map(lambda x: eval(x) if "startswith" in dir(x) and x.startswith('[') and x.endswith(']') else x, i)))
            return egg
        except sqlite3.OperationalError as e:
            create_log(e, code="error")
            sleep(1)
            continue

def fix_long_embed(description):
    return([description[i:i+1024] for i in range(0, len(description), 1024)])