# Scientific Space Mission Database

A Python and SQLite application for storing, searching, managing, and modifying information about scientific space missions from different countries and space programs.

The project was developed to explore practical database programming through **Python**, **SQL**, and **SQLite**, with a focus on relational database design, CRUD operations, data validation, CSV data import, database relationships, and parameterized queries.

---

## Features

- Store scientific space mission information in an SQLite database
- Maintain related country and mission tables
- Import mission data from a CSV file
- Display all stored missions
- Search for a mission by name
- Search for missions by country
- Search for missions launched after a specified year
- Insert new missions
- Update existing mission information
- Delete missions with confirmation
- Validate user input before database operations
- Prevent duplicate mission names
- Validate mission status values
- Use parameterized SQL queries for database operations

---

## Database Design

The application uses a relational database containing two main tables:

- `countries`
- `missions`

The tables are connected through a foreign-key relationship.

### Countries Table

```sql
CREATE TABLE countries (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE
);
```

Each country has:

- A unique ID
- A unique country name

---

### Missions Table

```sql
CREATE TABLE missions (
    id INTEGER PRIMARY KEY,
    mission_name TEXT NOT NULL UNIQUE,
    year INTEGER NOT NULL,
    country_id INTEGER NOT NULL,
    mission_type TEXT NOT NULL,
    status TEXT NOT NULL,
    launch_site TEXT NOT NULL,
    FOREIGN KEY (country_id) REFERENCES countries(id)
);
```

Each mission stores:

| Field | Description |
|---|---|
| `id` | Unique mission identifier |
| `mission_name` | Name of the mission |
| `year` | Mission year |
| `country_id` | Country associated with the mission |
| `mission_type` | Type or purpose of the mission |
| `status` | Mission outcome |
| `launch_site` | Location from which the mission was launched |

The `country_id` field creates a relationship between the `missions` and `countries` tables.

---

## Relational Model

The database relationship can be represented as:

```text
countries
+----------------+
| id             | <----------------+
| name           |                  |
+----------------+                  |
                                    |
                                    |
missions                            |
+----------------+                  |
| id             |                  |
| mission_name   |                  |
| year           |                  |
| country_id     | -----------------+
| mission_type   |
| status         |
| launch_site    |
+----------------+
```

One country can therefore be associated with multiple missions.

---

## CRUD Operations

The application implements the four fundamental database operations:

### Create

New missions can be inserted into the database.

Before insertion, the application validates:

- Mission name is not empty
- Mission name does not already exist
- Year is a valid positive integer
- Country exists in the database
- Mission type is not empty
- Mission status is valid
- Launch site is not empty

Accepted mission statuses are:

```text
Successful
Failed
Partial
```

---

### Read

Mission records can be retrieved in several ways.

#### Show All Missions

Displays all missions currently stored in the database.

#### Search by Mission Name

Searches for an exact mission name.

Example:

```text
Voyager 1
```

#### Search by Country

Retrieves missions belonging to a specified country using a SQL `JOIN` between the `missions` and `countries` tables.

Conceptually:

```sql
SELECT ...
FROM missions
JOIN countries
    ON missions.country_id = countries.id
WHERE countries.name = ?;
```

#### Search After a Year

Retrieves missions whose mission year is greater than a specified value.

Example:

```text
Search after year: 2000
```

returns missions satisfying:

```sql
WHERE year > 2000
```

---

### Update

Existing mission records can be modified.

The application allows the user to update:

1. Mission name
2. Mission year
3. Country
4. Mission type
5. Mission status
6. Launch site

Validation is performed before changes are committed to the database.

For example, when updating the country, the new country must already exist in the `countries` table.

When updating the mission status, the value must be one of:

```text
Successful
Failed
Partial
```

---

### Delete

Missions can be removed from the database by mission name.

Before deleting a record, the application:

1. Verifies that the mission exists
2. Requests confirmation from the user
3. Accepts only `Y` or `N`
4. Deletes the mission only after confirmation

Example:

```text
Are you sure you want to delete Voyager 1? (Y/N):
```

This helps prevent accidental deletion.

---

## CSV Data Import

Mission information can be loaded from:

```text
missions.csv
```

The CSV importer reads each row and inserts mission data into the database.

Expected fields are:

```text
mission_name, year, country_id, mission_type, status, launch_site
```

Example:

```csv
mission_name,year,country_id,mission_type,status,launch_site
Voyager 1,1977,1,Outer Planet Exploration,Successful,Cape Canaveral
Apollo 11,1969,1,Lunar Mission,Successful,Kennedy Space Center
```

Duplicate mission names are ignored during CSV import using:

```sql
INSERT OR IGNORE
```

---

## Search Menu

The application supports the following operations:

```text
1. Show all missions
2. Search mission by name
3. Search mission by country
4. Search mission after a year
5. Insert a mission
6. Update a mission
7. Delete a mission
8. Exit
```

This provides a simple command-line interface for interacting with the database.

---

## Parameterized SQL Queries

Database operations use parameterized SQL statements rather than constructing SQL commands directly from user input.

For example:

```python
cursor.execute("""
    SELECT mission_name
    FROM missions
    WHERE mission_name = ?
""", (mission_name,))
```

This keeps user-provided values separate from the SQL statement itself and is safer than manually constructing SQL queries using string concatenation.

---

## Input Validation

The project performs validation throughout the application.

Examples include:

### Mission Name

```text
Mission name cannot be empty.
```

Duplicate names are also rejected.

### Mission Year

The year must:

- Be an integer
- Be greater than zero

### Country

The country must already exist in the `countries` table.

### Mission Status

Only the following values are accepted:

```text
Successful
Failed
Partial
```

### Launch Site

The launch site cannot be empty.

### Delete Confirmation

Deletion requires an explicit:

```text
Y
```

or:

```text
N
```

response.

---

## Technologies Used

| Technology | Purpose |
|---|---|
| Python | Application logic |
| SQLite | Relational database |
| SQL | Database queries and CRUD operations |
| Python `csv` module | CSV data import |

The project uses Python's standard library and does not require third-party packages for its core functionality.

---

## SQL Concepts Demonstrated

The project uses several important SQL concepts:

- `CREATE TABLE`
- Primary keys
- Foreign keys
- `UNIQUE` constraints
- `NOT NULL` constraints
- `INSERT`
- `INSERT OR IGNORE`
- `SELECT`
- `WHERE`
- `JOIN`
- `UPDATE`
- `DELETE`
- Parameterized queries
- Relational table design

---

## Python Concepts Demonstrated

The project also demonstrates practical Python concepts including:

- Functions
- Loops
- Conditional statements
- Exception handling
- File processing
- CSV parsing
- User input
- String processing
- Database cursors
- Database transactions
- Structured validation logic

---

## Example Workflow

A typical user session could involve:

```text
1. Start the application

2. Import the initial mission dataset from CSV

3. Display all available missions

4. Search for a specific mission

5. Search for missions belonging to a country

6. Search for missions after a particular year

7. Insert a new mission

8. Update one of its fields

9. Delete a mission

10. Exit the application
```

This demonstrates the complete lifecycle of records stored in a relational database.

---

## Example Search

A search by country might produce results similar to:

```text
Mission Name: Apollo 11
Year: 1969
Country ID: 1
Mission Type: Lunar Mission
Status: Successful
Launch Site: Kennedy Space Center
```

A year-based query can be used to retrieve all missions launched after a particular date.

For example:

```text
Search for missions after: 2000
```

will return records where:

```sql
year > 2000
```

---

## Database Transactions

Changes to the database are committed after operations such as:

- Creating tables
- Importing CSV data
- Inserting missions
- Updating missions
- Deleting missions

For example:

```python
db.commit()
```

ensures that successful database modifications are persisted.

---

## Project Goals

This project was created to develop practical experience with:

- Python database programming
- Relational database design
- SQL queries
- Database relationships
- CRUD operations
- Data validation
- CSV data processing
- User-driven database applications
- Error handling
- Data integrity

Rather than using SQLite only as simple storage, the project applies relational concepts through separate country and mission entities connected by a foreign key.

---

## Potential Improvements

Possible future extensions include:

- Case-insensitive mission searching
- Partial-name searching
- Search by mission type
- Search by mission status
- Search within a range of years
- Sorting search results
- Adding new countries dynamically
- Additional database constraints
- Improved CSV validation
- Import error reporting
- Exporting database results to CSV
- Automated unit tests
- Logging database operations
- A graphical user interface
- A web-based interface
- Command-line arguments using `argparse`
- More advanced reports and statistics

For example, future versions could provide queries such as:

```text
Show all successful missions after 1990
```

or:

```text
Show all lunar missions launched by a selected country
```

---

## Possible Future Architecture

As the application grows, the project could be separated into dedicated modules:

```text
project/
├── database.py
├── operations.py
├── validation.py
├── main.py
├── missions.csv
└── README.md
```

This would separate:

- Database initialization
- CRUD operations
- Validation
- User-interface logic
- Data import

and make the application easier to test and maintain.

---

## About

The **Scientific Space Mission Database** is a Python and SQLite project designed to apply relational database concepts through a practical scientific dataset.

It combines database schema design, SQL queries, CSV importing, CRUD operations, relational joins, input validation, and database transactions in an interactive application for managing information about space missions.