import sqlite3
import operations


# Connect to SQLite
db = sqlite3.connect("space_missions.db")

# Cursor is used to send SQL commands to SQLite
cursor = db.cursor()

print("-----------------------------------------")
print("        SPACE MISSION DATABASE")
print("-----------------------------------------")
print()
operations.print_menu()

list_countries = [
    "Usa", "Ussr", "Uk", "Russia", "China", "Japan",
    "India", "France", "Germany", "Iran", "South korea",
    "North korea", "Brazil", "Argentina", "Mexico", "Spain",
    "Netherlands", "Sweden", "Switzerland", "Ukraine",
    "International"
]


# Create the two tables
operations.creating_countries_database(cursor, db, list_countries)
operations.creating_missions_database(cursor, db)


# 0 = CSV has not been imported yet
# 1 = CSV has already been imported so i can print the data
check = 0

while True:
    # Import CSV only once
    if check == 0:
        operations.import_missions_from_csv(cursor, db, check)
        check = 1

    try:
        choice = int(input("\nEnter your choice (write a number): "))
        if choice > 8 or choice <= 0:
            print("\nWrong number! Try again.")
            continue

    except ValueError:
        print("\nPlease enter a number!")
        continue


    # Menu cases
    match choice:
        case 1:
            operations.show_all_missions(cursor)
        case 2:
            print("\n-----SEARCH MISSION BY NAME-----")

            search_mission_name = input(
                "\nWrite the name of the mission you want to search: "
            ).capitalize()

            while search_mission_name == "":
                print("Empty name. That is invalid. Try again.")

                search_mission_name = input(
                    "\nWrite the name of the mission you want to search: "
                ).capitalize()

            operations.search_by_name(cursor,db,search_mission_name)


        case 3:
            print("\n-----SEARCH MISSION BY COUNTRY-----")

            search_mission_country = input(
                "\nWrite the country of the mission you want to search: ").capitalize()

            while search_mission_country == "":
                print("Empty country name. That is invalid. Try again.")

                search_mission_country = input(
                    "\nWrite the country of the mission you want to search: ").capitalize()

            cursor.execute("""
                SELECT id
                FROM countries
                WHERE name = ?
            """, (search_mission_country,))

            country = cursor.fetchone()

            while country is None:
                print("Country not found. Try again.")

                search_mission_country = input(
                    "\nWrite the country of the mission you want to search: ").capitalize()

                cursor.execute("""
                    SELECT id
                    FROM countries
                    WHERE name = ?
                """, (search_mission_country,))

                country = cursor.fetchone()

            operations.search_by_country(cursor,db,search_mission_country,list_countries)


        case 4:
            print("\n-----SEARCH MISSION AFTER A YEAR-----")

            while True:
                try:
                    search_mission_after_year = int(input("\nEnter a year to find missions launched after it: "))
                    if search_mission_after_year <= 0:
                        print("Year must be greater than 0.")
                    else:
                        break

                except ValueError:
                    print("Please enter a valid year.")

            operations.search_after_year(cursor,db,search_mission_after_year)


        case 5:
            operations.insert_mission(cursor, db)

        case 6:
            print("\n-----UPDATE MISSION-----")
            old_mission_name = input(
                "Write the name of the mission you want to update:").strip()


            while old_mission_name == "":
                print("Empty name. That is invalid. Try again.")
                old_mission_name = input(
                    "Write the name of the mission you want to update:")

            operations.update(cursor, db, list_countries, old_mission_name)

        case 7:
            print("\n-----DELETE MISSION-----")
            delete_mission = input(
                "\nEnter the name of mission you want to delete:").capitalize()

            while delete_mission == "":
                print("Empty name. That is invalid. Try again.")
                delete_mission = input("\nEnter the name of mission you want to delete:")

            operations.delete(cursor, db, delete_mission)

        case 8:
            print("EXIT")
            db.close()
            exit()

    Continue = input("\nIf you want to continue, enter 'Y'. Otherwise enter 'N'. If you enter anything else, the program will exit.)").upper()
    if Continue == "Y":
        print()
        operations.print_menu()

    else:
        print("\nExiting...")
        db.close()
        exit()


