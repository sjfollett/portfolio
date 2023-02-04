import datetime
import sqlite3
"""
A simple program for viewing relationships between people

If you did not download the 'family_tree.sqlite' file you must create the database and then reset the tables. 
To do this enter database manager from the main menu and run option 4 to reset database. 
If you downloaded the example 'family_tree.sqlite' file, make sure it is in the same directory as the FamilySQLTable.py
file for the program to run properly.

NOTE: If you add new relationships in the Relationships class, you must define the reverse relationship in the
define_reverse_relationship function or you will induce an error when you assign that relationship to a person
"""


class DBbase:
    _conn = None
    _cursor = None

    def __init__(self, db_name):
        self._db_name = db_name

    def connect(self):
        self._conn = sqlite3.connect(self._db_name)
        self._cursor = self._conn.cursor()

    def execute_script(self, sql_string):
        self._cursor.executescript(sql_string)

    @property
    def get_cursor(self):
        return self._cursor

    @property
    def get_connection(self):
        return self._conn

    def reset_database(self):
        raise NotImplementedError("Must implement from the derived Class")

    def close_db(self):
        self._conn.close()


class Person(DBbase):
    def __init__(self):
        super().__init__("family_tree.sqlite")

    def add_person(self, first_name, last_name, date_of_birth, gender, middle_name=None, date_of_death=None):

        # format the inputs for consistency
        if middle_name is not None:
            middle_name = middle_name.title()
        if gender.lower() == 'm':
            gender = 'male'
        if gender.lower() == 'f':
            gender = 'female'
        date_of_birth = str(datetime.datetime.strptime(date_of_birth, "%m/%d/%Y").date())
        if date_of_death is not None:
            date_of_death = str(datetime.datetime.strptime(date_of_death, "%m/%d/%Y").date())
        # adds the Person to the Database
        try:
            super().connect()
            super().get_cursor.execute("""INSERT OR IGNORE into Person(first_name, middle_name, last_name,
            date_of_birth, date_of_death, gender) VALUES(?,?,?,?,?,?);""", (first_name.title(), middle_name,
                                                                            last_name.title(), date_of_birth,
                                                                            date_of_death, gender.title(),)).fetchall()
            super().get_connection.commit()
            super().close_db()
            print("Person added successfully")
        except Exception as ex:
            print("An error occurred", ex)
            super().close_db()

    def fetch_person(self, person_id=None):
        # if ID is null (or None), then get everything, else get by id
        try:
            super().connect()
            if person_id is not None:
                return super().get_cursor.execute("""SELECT * FROM Person WHERE id = ?;""", (person_id,)).fetchall()
            else:
                return super().get_cursor.execute("""SELECT * FROM Person;""").fetchall()
        except Exception as ex:
            print("An error occurred:", ex)
        finally:
            super().close_db()

    def fetch_relations(self, person_id):
        # takes a person ID and shows all their relations
        try:
            super().connect()
            sql = f"SELECT Person.first_name, Person.middle_name, Person.last_name, Relationships.relationship_name " \
                  f"FROM Person JOIN Relations ON Relations.person_1_id = Person.id " \
                  f"JOIN Relationships ON Relationships.relationship_id = Relations.reverse_relationship " \
                  f"WHERE Relations.person_2_id = {person_id} " \
                  f"UNION " \
                  f"SELECT Person.first_name, Person.middle_name, Person.last_name, Relationships.relationship_name " \
                  f"FROM Person " \
                  f"INNER JOIN Relations ON Relations.person_2_id = Person.id " \
                  f"INNER JOIN Relationships ON Relationships.relationship_id = Relations.relationship_id " \
                  f"WHERE Relations.person_1_id = {person_id} ;"
            return super().get_cursor.execute(sql).fetchall()

        except Exception as ex:
            print("An error occurred:", ex)
        finally:
            super().close_db()

    def update_person(self, person_id):
        # Shows person information, then choose the field by number to update
        print(Person().fetch_person(person_id))
        update_person_options = {"1": "First Name",
                                 "2": "Middle Name",
                                 "3": "Last Name",
                                 "4": "Date of Birth",
                                 "5": "Date of Death",
                                 "6": "Gender",
                                 "7": "Exit"}
        user_selection = ""
        while user_selection.lower() != "7":
            print("*** Option List ***")
            for option in update_person_options.items():
                print(option)
            user_selection = input("Select a field to update: \n")
            if user_selection != '7':
                selection_options = {"1": "first_name",
                                     "2": "middle_name",
                                     "3": "last_name",
                                     "4": "date_of_birth",
                                     "5": "date_of_death",
                                     "6": "gender"}
                updated_string = f'UPDATE Person SET {selection_options[user_selection]} = ? WHERE id = ?'
                new_value = input(f"Enter new value: ")
                new_value = new_value.title()
                try:
                    super().connect()
                    super().get_cursor.execute(updated_string, (new_value, person_id))
                    super().get_connection.commit()
                    print("Person successfully updated\n")
                except Exception as ex:
                    print("An error occurred", ex)
                finally:
                    super().close_db()

    def delete_person(self, person_id):
        try:
            super().connect()
            super().get_cursor.execute("""DELETE from Person WHERE id = ?;""", (person_id,))
            super().get_connection.commit()
            super().close_db()
            print("Person deleted successfully\n")
            return True
        except Exception as ex:
            print("An error occurred", ex)
            return False
        finally:
            super().close_db()

    def reset_database(self):
        super().connect()
        sql = """
            DROP TABLE IF EXISTS Person;

            CREATE TABLE Person (
                id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                first_name TEXT NOT NULL,
                middle_name TEXT,
                last_name TEXT NOT NULL,
                date_of_birth TEXT NOT NULL,
                date_of_death TEXT,
                gender TEXT NOT NULL);
             """
        super().execute_script(sql)
        super().close_db()
        print("successfully reset Person table")


class Relationships(DBbase):
    def __init__(self):
        super().__init__("family_tree.sqlite")

    def add(self, relationship_name):
        # adds a new relationship type ***MUST DEFINE REVERSE RELATIONSHIP OR DATABASE WILL HAVE NULLS***
        try:
            super().connect()
            super().get_cursor.execute("""INSERT OR IGNORE into Relationships(relationship_name) VALUES(?);""",
                                       (relationship_name,)).fetchall()
            super().get_connection.commit()
            super().close_db()
            print("Relationship added successfully\n")
        except Exception as ex:
            print("An error occurred", ex)

    def update(self, relationship_name, relationship_id):
        try:
            super().connect()
            super().get_cursor.execute("""UPDATE Relationships SET relationship_name = ? WHERE relationship_id = ?""",
                                       (relationship_name, relationship_id,))
            super().get_connection.commit()
            print("Relationship updated successfully\n")
        except Exception as ex:
            print("An error occurred", ex)
        finally:
            super().close_db()

    def fetch(self, relationship_id=None, relationship_name=None):
        # if ID is null (or None), then get everything, else get by id
        try:
            super().connect()
            if relationship_id is not None:
                return super().get_cursor.execute("""SELECT * FROM Relationships WHERE relationship_id = ?;""",
                                                  (relationship_id,)).fetchall()
            elif relationship_name is not None:
                return super().get_cursor.execute("""SELECT relationship_id FROM Relationships
                 WHERE relationship_name = ?;""", (relationship_name,)).fetchone()
            else:
                return super().get_cursor.execute("""SELECT * FROM Relationships;""").fetchall()
        except Exception as ex:
            print("An error occurred:", ex)
        finally:
            super().close_db()

    def delete(self, relationship_id):
        try:
            super().connect()
            super().get_cursor.execute("""DELETE from Relationships WHERE relationship_id = ?;""", (relationship_id,))
            super().get_connection.commit()
            super().close_db()
            print("Relationship deleted successfully\n")
            return True
        except Exception as ex:
            print("An error occurred", ex)
            return False
        finally:
            super().close_db()

    def reset_database(self):
        super().connect()
        sql = """
            DROP TABLE IF EXISTS Relationships;

            CREATE TABLE Relationships (
               relationship_id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
               relationship_name   TEXT NOT NULL UNIQUE
           );
             """
        super().execute_script(sql)
        super().close_db()
        print("successfully reset Relationships table")


class Relations(Person):
    def __init__(self):
        super().__init__()

    def define_reverse_relationship(self, relationship_id, person_2_id):
        # defines the relationship from Person 2 to Person 1 based on the relationship of Person 1 to Person 2
        relationship = Relationships().fetch(relationship_id=relationship_id)
        defined = Relationships().fetch()
        def_list = []
        for item in defined:
            def_list.append(item[1])
        for item in relationship:
            rel_id = item[0]
            rel_name = item[1]
            if rel_name.title() == "Cousin" or rel_name.title() == "Spouse":
                reverse_relationship = rel_id
                return reverse_relationship
            if rel_name.title() == "Father" or rel_name.title() == "Mother":
                reverse_relationship = Relationships().fetch(relationship_name="Child")[0]
                return reverse_relationship
            if rel_name.title() == "Child":
                # looks up id of person 2, determines if they are Male/Female, and then looks up relationship id
                person_2 = super().fetch_person(person_2_id)
                if person_2[0][6] == "Male":
                    reverse_relationship = Relationships().fetch(relationship_name="Father")[0]
                    return reverse_relationship
                if person_2[0][6] == "Female":
                    reverse_relationship = Relationships().fetch(relationship_name="Mother")[0]
                    return reverse_relationship
            if rel_name.title() == "Brother" or rel_name.title() == "Sister":
                person_2 = super().fetch_person(person_2_id)
                if person_2[0][6] == "Male":
                    reverse_relationship = Relationships().fetch(relationship_name="Brother")[0]
                    return reverse_relationship
                if person_2[0][6] == "Female":
                    reverse_relationship = Relationships().fetch(relationship_name="Sister")[0]
                    return reverse_relationship
            if rel_name.title() == "Hero":
                reverse_relationship = Relationships().fetch(relationship_name="Archnemesis")[0]
                return reverse_relationship
            if rel_name.title() == "Archnemesis":
                reverse_relationship = Relationships().fetch(relationship_name="Hero")[0]
                return reverse_relationship
            if rel_name.title() not in def_list:
                raise Exception("Reverse relationship not defined")

    def add_relationship(self):
        # adds a relationship between 2 people
        people = super().fetch_person()
        for person in people:
            print(person)
        person_1_id = input("Enter the ID of the person whose relationship you want to define: ")
        person_2_id = input("Enter the ID of the person to whom they are related: ")
        relationship_options = Relationships().fetch()
        for relationship in relationship_options:
            print(relationship)
        relationship_id = input("Enter relationship id of Person 1 to Person 2: ")
        rev_relationship = Relations().define_reverse_relationship(relationship_id, person_2_id)
        try:
            super().connect()
            super().get_cursor.execute("""INSERT OR IGNORE into Relations(person_1_id, person_2_id, relationship_id,
             reverse_relationship) VALUES(?,?,?,?);""", (person_1_id, person_2_id, relationship_id, rev_relationship,)
                                       ).fetchall()
            super().get_connection.commit()
            super().close_db()
            print("Relation added successfully\n")
        except Exception as ex:
            print("An error occurred", ex)

    def delete(self, relations_id):
        try:
            super().connect()
            super().get_cursor.execute("""DELETE from Relations WHERE id = ?;""", (relations_id,))
            super().get_connection.commit()
            super().close_db()
            print("Relation deleted successfully\n")
            return True
        except Exception as ex:
            print("An error occurred", ex)
            return False
        finally:
            super().close_db()

    def reset_database(self):
        super().connect()
        sql = """
                DROP TABLE IF EXISTS Relations;

                CREATE TABLE Relations (
                    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                    person_1_id INTEGER NOT NULL,
                    person_2_id INTEGER NOT NULL,
                    relationship_id INTEGER NOT NULL,
                    reverse_relationship INTEGER NOT NULL,
                    FOREIGN KEY (person_1_id) REFERENCES Person(id),
                    FOREIGN KEY (person_2_id) REFERENCES Person(id),
                    FOREIGN KEY (relationship_id) REFERENCES Relationships(relationship_id)
                    FOREIGN KEY (reverse_relationship) REFERENCES Relationships (relationship_id)
                    );
            """
        super().execute_script(sql)
        super().close_db()
        print("successfully reset Relations table")


# Creates the dynamic menu to toggle through

def main_menu():
    active = True
    main_menu_options = {"1. Person Manager": "Add, remove, update, or view people",
                         "2. Relatives Manager": "Define or remove relationships between people",
                         "3. Relationship Manager": "Add or remove relationship types from the database",
                         "4. Database Manager": "Reset Data in the Database",
                         "5. Exit": "exit the program"}
    user_selection = ""
    while active:
        print("\n*** Option List ***")
        for option in main_menu_options.items():
            print(option)
        user_selection = input("Select an option by number: \n")

        sub_menu_person = {"Add": "Add a new person",
                           "Find": "Find a person in the database, or view all people",
                           "Update": "Update information for a person",
                           "View": "See who a person is related to",
                           "Delete": "Delete a person from the database",
                           "Return": "Return to Main Menu",
                           "Exit": "Exit the Program"}

        if user_selection == "1":
            print("*** Option List ***")
            for option in sub_menu_person.items():
                print(option)
            prompt = input("Select an option: \n")

            if prompt.title() == "Add":
                first_name = input("Enter the person's first name: ")
                middle_name = input('Does the person have a middle name (Y/N): ')
                if middle_name.lower() == "y" or middle_name.lower() == "yes":
                    middle_name = input("Enter the middle name: ")
                else:
                    middle_name = None
                last_name = input("Enter Last Name: ")
                date_of_birth = input("Enter the date of birth: ")
                date_of_death = input("Is the person dead (Y/N): ")
                if date_of_death.lower() == "y" or date_of_death.lower() == "yes":
                    date_of_death = input("Enter the date of death: ")
                else:
                    date_of_death = None
                gender = input("Enter the person's gender: ")
                person = Person()
                person.add_person(first_name, last_name, date_of_birth, gender, middle_name=middle_name,
                                  date_of_death=date_of_death)

            elif prompt.title() == "Find":
                person_id = input("Enter the id of the person you want to find or press enter to view all: ")
                if person_id == "":
                    person_id = None
                else:
                    person_id = int(person_id)
                person = Person()
                x = person.fetch_person(person_id=person_id)
                for item in x:
                    print(f"Person ID: {item[0]}\n"
                          f"First Name: {item[1]}\n"
                          f"Middle Name: {item[2]}\n"
                          f"Last Name: {item[3]}\n"
                          f"Date of Birth: {item[4]}\n"
                          f"Date of Death: {item[5]}\n"
                          f"Gender: {item[6]}\n")

            elif prompt.title() == "Update":
                person_id = input("Enter the ID of the person you want to update: ")
                Person().update_person(person_id=person_id)

            elif prompt.title() == "View":
                person_id = input("Enter the ID of the person you want to see: ")
                person = Person()
                first_name = ""
                print("Person you searched for:")
                x = person.fetch_person(person_id=person_id)
                for item in x:
                    print(f"Person ID: {item[0]}\n"
                          f"First Name: {item[1]}\n"
                          f"Middle Name: {item[2]}\n"
                          f"Last Name: {item[3]}\n")
                    first_name += item[1]

                print(f"{first_name}'s Relatives:")
                x = person.fetch_relations(person_id=person_id)
                for item in x:
                    print(f"First Name: {item[0]}\n"
                          f"Middle Name: {item[1]}\n"
                          f"Last Name: {item[2]}\n"
                          f"{first_name}'s Relationship to this person: {item[3]}\n")

            elif prompt.title() == "Delete":
                person_id = input("Enter the ID of the person you want to delete: ")
                Person().delete_person(person_id=person_id)

            elif prompt.title() == "Return":
                print("\n")
                return main_menu()

            elif prompt.title() == "Exit":
                print("\n")
                active = False

            elif prompt.title() != "Add" and prompt.title() != "Find" and prompt.title() != "Update" and \
                    prompt.title() != "View" and prompt.title() != "Delete" and prompt.title() != "Return"\
                    and prompt.title() != "Exit":
                print("Invalid Input")

        sub_menu_relatives = {"Add": "Add a relationship between two people",
                              "Delete": "Delete a relationship between two people",
                              "Return": "Return to Main Menu",
                              "Exit": "Exit the Program"}

        if user_selection == "2":
            print("*** Option List ***")
            for option in sub_menu_relatives.items():
                print(option)
            prompt = input("Select an option: ")

            if prompt.title() == "Add":
                Relations().add_relationship()

            elif prompt.title() == "Delete":
                relations_id = input("Enter the ID of the relationship you want to delete: ")
                Relations().delete(relations_id)

            elif prompt.title() == "Return":
                print("\n")
                return main_menu()
            elif prompt.title() == "Exit":
                print("\n")
                active = False
            elif prompt.title() != "Add" and prompt.title() != "Delete" and prompt.title() != "Return"\
                    and prompt.title() != "Exit":
                print("Invalid Input")

        sub_menu_relationships = {"Add": "Add a relationship type to the database",
                                  "Update": "Update an existing relationship type",
                                  "Find": "Find an existing relationship type",
                                  "Delete": "Delete a relationship type",
                                  "Return": "Return to Main Menu",
                                  "Exit": "Exit the Program"}

        if user_selection == "3":
            print("*** Option List ***")
            for option in sub_menu_relationships.items():
                print(option)
            prompt = input("Select an option: ")

            if prompt.title() == "Add":
                name = input("Enter the name of the Relationship to add: ")
                Relationships().add(name)

            elif prompt.title() == "Update":
                relationship_list = Relationships().fetch()
                for relationship in relationship_list:
                    print(relationship)
                relationship_id = int(input("Enter the relationship ID you want to update: "))
                relationship_name = input("Enter the new name of the relationship: ")
                Relationships().update(relationship_name, relationship_id)

            elif prompt.title() == "Find":
                relationship_id = input("Enter the id of the relationship you want to find or press enter to view all: ")
                if relationship_id == "":
                    relationship_id = None
                else:
                    relationship_id = int(relationship_id)
                relationship_list = Relationships().fetch(relationship_id=relationship_id)
                for relationship in relationship_list:
                    print(relationship)
                print("\n")

            elif prompt.title() == "Delete":
                relationship_id = input("Enter the ID of the relationship you want to delete: ")
                Relationships().delete(relationship_id)

            elif prompt.title() == "Return":
                print("\n")
                return main_menu()

            elif prompt.title() == "Exit":
                print("\n")
                active = False

            elif prompt.title() != "Add" and prompt.title() != "Find" and prompt.title() != "Update" and\
                    prompt.title() != "Delete" and prompt.title() != "Return" and prompt.title() != "Exit":
                print("Invalid Input")

        sub_menu_database = {"1. Reset People": "Reset the Person Table",
                             "2. Reset Relatives": "Reset the Relatives Table",
                             "3. Reset Relationships": "Reset the Relationships Table",
                             "4. Reset All": "Resets all Tables and Initialize the file",
                             "5. Return": "Return to Main Menu",
                             "6. Exit": "Exit the Program"}

        if user_selection == "4":
            print("*** Option List ***")
            for option in sub_menu_database.items():
                print(option)
            prompt = input("Select a number: ")
            if prompt.title() == "1":
                warning = input("This action will delete data, do you want to continue: (Y/N) ")
                if warning.lower() == "y" or warning.lower() == "yes":
                    Person().reset_database()
                else:
                    main_menu()

            elif prompt.title() == "2":
                warning = input("This action will delete data, do you want to continue: (Y/N) ")
                if warning.lower() == "y" or warning.lower() == "yes":
                    Relations().reset_database()
                else:
                    main_menu()

            elif prompt.title() == "3":
                warning = input("This action will delete data, do you want to continue: (Y/N) ")
                if warning.lower() == "y" or warning.lower() == "yes":
                    Relationships().reset_database()
                else:
                    main_menu()

            elif prompt.title() == "4":
                print("***WARNING***WARNING***WARNING***WARNING***WARNING***WARNING***WARNING***WARNING***WARNING***\n"
                      "Continuing will delete all of your data and initialize a new family_tree.sqlite file\n"
                      "***WARNING***WARNING***WARNING***WARNING***WARNING***WARNING***WARNING***WARNING***WARNING***\n")
                warning = input("Do you want to continue: (Y/N) ")
                if warning.lower() == "y" or warning.lower() == "yes":
                    database = DBbase("family_tree.sqlite")
                    DBbase.connect(database)
                    Person().reset_database()
                    Relationships().reset_database()
                    Relations().reset_database()
                else:
                    main_menu()

            elif prompt.title() == "5":
                print("\n")
                return main_menu()
            elif prompt.title() == "6":
                print("\n")
                active = False
            elif prompt.title() != "1" and prompt.title() != "2" and prompt.title() != "3" and\
                    prompt.title() != "4" and prompt.title() != "5" and prompt.title() != "6":
                print("Invalid Input")

        if user_selection == "5":
            active = False

        if user_selection != "1" and user_selection != "2" and user_selection != "3" and user_selection != "4" and \
                user_selection != "5":
            print("invalid input")


# initializes the program
main_menu()
