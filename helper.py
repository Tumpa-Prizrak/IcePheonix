import sqlite3, datetime, json
from time import sleep

json_data = json.load(open("settings.json"))

def create_log(mess: str, code: str = "ok"):
    file = open("log.txt", "a")
        
    out = f"[{code}][{datetime.datetime.now()}]: {mess}"
        
    print(out)
    
    file.write(out + "\n")

    file.close()

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