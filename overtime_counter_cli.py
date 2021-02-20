import sqlite3

ERORR_MSG = "\nERROR: Špatné zadány hodnoty! Zkuste to znovu..."
db_name = "data.db"


def create_table(db_name, sql):
    with sqlite3.connect(db_name) as db:
        cursor = db.cursor()
        cursor.execute(sql)
        db.commit()
        print("*** Databáze byla vytvořena ***")


def drop_table(db_name):
    with sqlite3.connect(db_name) as db:
        cursor = db.cursor()
        cursor.execute("drop table Data")
        db.commit()
        print("\n*** Databáze byla smazána ***\n")


def insert_data(db_name):
    first_name = input("\nZadejte křestní jméno: ")
    last_name = input("Zadejte příjmení: ")
    while True:
        hours = input("Zadejte počet hodin: ")
        if hours.isnumeric():
            break
        else:
            print(ERORR_MSG)
    while True:
        perhour = input("Zadejte hodinovku: ")
        if perhour.isnumeric():
            break
        else:
            print(ERORR_MSG)
    with sqlite3.connect(db_name) as db:
        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO Data (First, Last, Hours, PerHour) VALUES(?,?,?,?)",
            (first_name, last_name, hours, perhour),
        )
        db.commit()
    print("\n*** Uživatel přidán ***\n")


def print_all(db_name):
    with sqlite3.connect(db_name) as db:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM Data")
        rows = cursor.fetchall()
        if len(rows) == 0:
            print("\n*** V databázi nejsou žádní uživatelé ***\n")
        db.commit()
        for row in rows:
            print("-" * 60)
            print(
                row[0],
                "  |  ",
                row[1],
                "  |  ",
                row[2],
                "  |  ",
                row[3],
                "  |  ",
                row[4],
            )


def search(db_name):
    name = input("Hledat uživatele: ")
    splits = name.split()
    if len(splits) == 1:
        with sqlite3.connect(db_name) as db:
            cursor = db.cursor()
            cursor.execute("SELECT * FROM Data WHERE First=?", [name])
            rows = cursor.fetchall()
            db.commit()
            cursor.execute("SELECT * FROM Data WHERE Last=?", [name])
            rows += cursor.fetchall()
            db.commit()
            for row in rows:
                print("———————————————————")
                print("ID: ", row[0])
                print("Jméno: ", row[1])
                print("Příjmení: ", row[2])
                print("Počet hodin: ", row[3])
                print("Hodinovka: ", row[4])
                print("———————————————————")

    elif len(splits) > 0 and len(splits) != 1:
        name2 = [name]
        with sqlite3.connect(db_name) as db:
            cursor = db.cursor()
            cursor.execute("SELECT * FROM Data WHERE First || ' ' || Last=?", name2)
            rows = cursor.fetchall()
            db.commit()
            for row in rows:
                print("———————————————————")
                print("ID: ", row[0])
                print("Jméno: ", row[1])
                print("Příjmení: ", row[2])
                print("Počet hodin: ", row[3])
                print("Hodinovka: ", row[4])
                print("———————————————————")

    if len(rows) == 1:
        print("\n*** Nalezen jeden uživatel ***\n")
        return row

    elif len(rows) >= 2:
        print("\n*** Nalezeno více uživatelů ***\n")
        id = input("Zadejte ID uživatele: ")
        cursor.execute("SELECT * FROM Data WHERE UserID =?", id)
        rows = cursor.fetchall()
        db.commit()

        if len(rows) == 0:
            print("\n*** Nenalezen žádny uživatel s tímto ID ***\n")
            return

        for row in rows:
            print("———————————————————")
            print("ID: ", row[0])
            print("Jméno: ", row[1])
            print("Příjmení: ", row[2])
            print("Počet hodin: ", row[3])
            print("Hodinovka: ", row[4])
            print("———————————————————")
        return row

    elif len(rows) == 0:
        print("\n*** Nenalezen žádný uživatel ***\n")
    print("≡" * 60)


def purchase(db_name):
    found = search(db_name)
    if found == None:
        return
    hours = float(found[3])
    perhour = int(found[4])
    id = str(found[0])
    print(
        f"\nAktuální počet hodin uživatele {found[1]} {found[2]} je {hours}h a hodinovka je {perhour}Kč\n"
    )
    while True:
        print("\n   1 - Nákup na firmu\n   2 - Půjčení auta")
        pur_type = input("\n   Vyberte možnost: ")
        if pur_type == "1" or pur_type == "2":
            break
        else:
            print(ERORR_MSG)

    while True:
        if pur_type == "1":
            price = input("\nZadejte cenu nákupu zaokrouhlednou na koruny: ")
            if price.isdecimal():
                price = int(price)
                break
            else:
                print(ERORR_MSG)
        elif pur_type == "2":
            price = input("\nZadejte počet kilometrů: ")
            if price.isdecimal():
                price = int(price)
                break
            else:
                print(ERORR_MSG)

    while pur_type == "2":
        price_per_km = input("Zadejte cenu za jeden kilometr: ")
        if price_per_km.isnumeric():
            price = price * float(price_per_km)
            break
        else:
            print(ERORR_MSG)

    price_hours = round(price / perhour, 1)
    hours_new = str(round(hours - price_hours, 1))

    with sqlite3.connect(db_name) as db:
        cursor = db.cursor()
        cursor.execute("UPDATE Data SET Hours = ? WHERE UserID = ?", (hours_new, id))
        db.commit()
        print(
            "\n*** Počet hodin uživatele {} {} byl aktualizaván na {}h\n".format(
                found[1], found[2], hours_new
            )
        )


def process():
    print("≡" * 60)
    print(
        "\n1 - Přidat uživatele\n2 - Vypsat všechny uživatele\n3 - Hledat\n4 - Nákup nebo půjčení auta\n5 - Vytvořit databázi\n6 - Smazat databázi\n"
    )
    print("≡" * 60)
    op = input("Zadejte číslo operace: ")

    if op == "1":
        insert_data(db_name)
    elif op == "2":
        print_all(db_name)
    elif op == "3":
        search(db_name)
    elif op == "4":
        purchase(db_name)
    elif op == "5":
        sql = """create table Data
                (UserID integer,
                First text,
                Last text,
                Hours real,
                PerHour integer,
                primary key(UserID))"""
        create_table(db_name, sql)
    elif op == "6":
        drop_table(db_name)
    else:
        print("\n** Nesprávné číslo operace ***\n")


if __name__ == "__main__":
    while True:
        process()

