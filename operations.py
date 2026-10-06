import csv

def creating_countries_database(cursor, db, list_countries):
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS countries
        (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL UNIQUE
        )
    """)

    db.commit()

    for country in list_countries:
        cursor.execute("""
            INSERT OR IGNORE INTO countries(name)
            VALUES (?)
        """, (country,))

    db.commit()


def creating_missions_database(cursor, db):

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS missions
        (
            id INTEGER PRIMARY KEY,
            mission_name TEXT NOT NULL UNIQUE,
            year INTEGER NOT NULL,
            country_id INTEGER NOT NULL,
            mission_type TEXT NOT NULL,
            status TEXT NOT NULL,
            launch_site TEXT NOT NULL,
            FOREIGN KEY (country_id) REFERENCES countries(id)
        )
    """)

    db.commit()


def import_missions_from_csv(cursor, db, check):

    with open("missions.csv", "r") as file:
        reader = csv.reader(file)
        # Skip CSV header
        next(reader)

        if check == 0:
            for line in reader:
                mission_name, year, country_id, mission_type, status, launch_site = line
                year = int(year)
                country_id = int(country_id)
                cursor.execute("""
                    INSERT OR IGNORE INTO missions
                    (
                        mission_name,
                        year,
                        country_id,
                        mission_type,
                        status,
                        launch_site
                    )
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    mission_name,
                    year,
                    country_id,
                    mission_type,
                    status,
                    launch_site
                ))

    db.commit()


def show_all_missions(cursor):
    cursor.execute("""
        SELECT
            mission_name,
            year,
            country_id,
            mission_type,
            status,
            launch_site
        FROM missions
    """)

    missions = cursor.fetchall()
    print("\n----------SHOW ALL MISSIONS----------")

    if not missions:
        print("No missions found.")
        return

    for mission in missions:
        print(f"""
Mission Name: {mission[0]}
Year: {mission[1]}
Country ID: {mission[2]}
Mission Type: {mission[3]}
Status: {mission[4]}
Launch Site: {mission[5]}
""")


def print_menu():
    print("1.Show all missions")
    print("2.Search mission by name")
    print("3.Search mission by country")
    print("4.Search mission after a year")
    print("5.Insert a mission")
    print("6.Update a mission")
    print("7.Delete a mission")
    print("8.Exit")


def search_by_name(cursor, db, search_mission_name):

    cursor.execute("""
        SELECT
            mission_name,
            year,
            country_id,
            mission_type,
            status,
            launch_site
        FROM missions
        WHERE mission_name = ?
    """, (search_mission_name,))

    mission = cursor.fetchone()

    if mission:
        print(f"""
Mission Name: {mission[0]}
Year: {mission[1]}
Country ID: {mission[2]}
Mission Type: {mission[3]}
Status: {mission[4]}
Launch Site: {mission[5]}
""")

    else:
        print("Mission with this name not found.")


def search_by_country(cursor, db, search_mission_country, list_countries):

    cursor.execute("""
        SELECT
            missions.mission_name,
            missions.year,
            missions.country_id,
            missions.mission_type,
            missions.status,
            missions.launch_site
        FROM missions
        JOIN countries
            ON missions.country_id = countries.id
        WHERE countries.name = ?
    """, (search_mission_country,))

    missions = cursor.fetchall()

    if not missions:
        print("No missions found for this country.")
        return

    for mission in missions:
        print(f"""
Mission Name: {mission[0]}
Year: {mission[1]}
Country ID: {mission[2]}
Mission Type: {mission[3]}
Status: {mission[4]}
Launch Site: {mission[5]}
""")


def search_after_year(cursor, db, search_mission_year):
    cursor.execute("""
        SELECT
            mission_name,
            year,
            country_id,
            mission_type,
            status,
            launch_site
        FROM missions
        WHERE year > ?
    """, (search_mission_year,))

    missions = cursor.fetchall()

    if not missions:
        print("No missions found after this year.")
        return

    for mission in missions:
        print(f"""
Mission Name: {mission[0]}
Year: {mission[1]}
Country ID: {mission[2]}
Mission Type: {mission[3]}
Status: {mission[4]}
Launch Site: {mission[5]}
""")


def insert_mission(cursor, db):
    print("\n----------INSERT NEW MISSION----------")
    while True:
        mission_name = input("Enter mission name: ").strip()
        if mission_name == "":
            print("Mission name cannot be empty.")
            continue

        cursor.execute("""
            SELECT mission_name
            FROM missions
            WHERE mission_name = ?
        """, (mission_name,))

        if cursor.fetchone():
            print("A mission with this name already exists. Try again.")
            continue

        break

    while True:
        try:
            year = int(input("Enter mission year: "))
            if year <= 0:
                print("Year must be greater than 0.")
            else:
                break

        except ValueError:
            print("Please enter a valid year.")

    while True:
        country = input("Enter country: ").capitalize()
        cursor.execute("""
            SELECT id
            FROM countries
            WHERE name = ?
        """, (country,))

        country_result = cursor.fetchone()
        if country_result:
            country_id = country_result[0]
            break

        print("Country not found. Try again.")

    while True:
        mission_type = input("Enter mission type: ").strip()
        if mission_type:
            break
        print("Mission type cannot be empty.")

    accepted_status = [
        "Successful",
        "Failed",
        "Partial"
    ]

    while True:
        status = input("Enter mission status (Successful/Failed/Partial): ").strip().capitalize()
        if status in accepted_status:
            break
        print("Status not accepted. Try again.")

    while True:
        launch_site = input("Enter launch site: ").strip()
        if launch_site:
            break
        print("Launch site cannot be empty.")

    cursor.execute("""
        INSERT INTO missions
        (
            mission_name,
            year,
            country_id,
            mission_type,
            status,
            launch_site
        )
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        mission_name,
        year,
        country_id,
        mission_type,
        status,
        launch_site
    ))

    db.commit()
    print("\nMission inserted successfully.")


def update(cursor, db, list_countries, old_mission_name):
    cursor.execute("""
        SELECT
            mission_name,
            year,
            country_id,
            mission_type,
            status,
            launch_site
        FROM missions
        WHERE mission_name = ?
    """, (old_mission_name,))

    mission = cursor.fetchone()
    if not mission:
        print("Mission with this name not found.")
        return
    print(f"""
Mission Name: {mission[0]}
Year: {mission[1]}
Country ID: {mission[2]}
Mission Type: {mission[3]}
Status: {mission[4]}
Launch Site: {mission[5]}
""")

    print("""
What do you want to update?
1. Mission name
2. Year
3. Country
4. Mission type
5. Status
6. Launch site
""")

    while True:
        try:
            answer = int(input("Write a number: "))
            if 1 <= answer <= 6:
                break
            print("Wrong number! Choose a number from 1 to 6.")

        except ValueError:
            print("Please enter a number.")

    if answer == 1:
        while True:
            new_mission_name = input("Write the new mission name: ")
            if new_mission_name == "":
                print("Please enter a new mission name.")
                continue

            cursor.execute("""
                SELECT mission_name
                FROM missions
                WHERE mission_name = ?
            """, (new_mission_name,))

            existing_mission = cursor.fetchone()
            if existing_mission:
                print(f"There is already a mission with this name: ")
                print(f"{existing_mission[0]}. Try again.")
                continue
            break

        cursor.execute("""
            UPDATE missions
            SET mission_name = ?
            WHERE mission_name = ?
        """, (new_mission_name, old_mission_name))

        db.commit()
        print("Mission name updated successfully.")

    elif answer == 2:
        while True:
            try:
                new_mission_year = int(input("Write the new mission year: "))
                if new_mission_year <= 0:
                    print("Year must be greater than 0.")
                else:
                    break

            except ValueError:
                print("Please enter a valid number.")

        cursor.execute("""
            UPDATE missions
            SET year = ?
            WHERE mission_name = ?
        """, (new_mission_year, old_mission_name))

        db.commit()
        print("Year updated successfully.")

    elif answer == 3:
        while True:
            new_mission_country = input("Write the new country: ").capitalize()

            cursor.execute("""
                SELECT id
                FROM countries
                WHERE name = ?
            """, (new_mission_country,))

            country = cursor.fetchone()
            if country:
                break

            print("Country not found. Try again.")

        new_country_id = country[0]

        cursor.execute("""
            UPDATE missions
            SET country_id = ?
            WHERE mission_name = ?
        """, (new_country_id, old_mission_name))

        db.commit()

        print("Country updated successfully.")

    elif answer == 4:
        while True:
            new_mission_type = input("Write the new mission type: ").capitalize()
            if new_mission_type:
                break

            print("Please enter a new mission type.")

        cursor.execute("""
            UPDATE missions
            SET mission_type = ?
            WHERE mission_name = ?
        """, (new_mission_type, old_mission_name))

        db.commit()
        print("Mission type updated successfully.")

    elif answer == 5:
        accepted_status = [
            "Successful",
            "Failed",
            "Partial"
        ]

        new_status = input("Write the new mission status: ").strip().capitalize()
        while new_status not in accepted_status:
            print("Status not accepted. Try again.")
            new_status = input( "Write the new mission status: ").strip().capitalize()

        cursor.execute("""
            UPDATE missions
            SET status = ?
            WHERE mission_name = ?
        """, (new_status, old_mission_name))

        db.commit()
        print("Status updated successfully.")

    elif answer == 6:
        while True:
            new_launch_site = input("Write the new launch site: ")
            if new_launch_site:
                break
            print("Launch site cannot be empty.")

        cursor.execute("""
            UPDATE missions
            SET launch_site = ?
            WHERE mission_name = ?
        """, (new_launch_site, old_mission_name))

        db.commit()
        print("Launch site updated successfully.")


def delete(cursor, db, delete_mission):
    cursor.execute("""
        SELECT id
        FROM missions
        WHERE mission_name = ?
    """, (delete_mission,))

    mission = cursor.fetchone()
    if not mission:
        print("Mission not found.")
        return

    confirmation = input(f"Are you sure you want to delete {delete_mission}? (Y/N): ").upper()

    while confirmation not in ["Y", "N"]:
        print("Please enter Y or N.")
        confirmation = input(f"Are you sure you want to delete {delete_mission}? (Y/N): ").upper()

    if confirmation == "N":
        print("Deletion cancelled.")
        return

    cursor.execute("""
        DELETE FROM missions
        WHERE mission_name = ?
    """, (delete_mission,))

    db.commit()
    print("Mission deleted successfully.")