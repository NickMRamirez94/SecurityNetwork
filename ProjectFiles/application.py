import mysql.connector
from mysql.connector import errorcode
from cryptography.fernet import Fernet

cnx = mysql.connector.connect(user='root', password='smackdown2', database='security')

def Login():
    username = raw_input("Username: ")
    password = raw_input("Password: ")

    return username, password

def VerifyClient(username, password):
    cursor = cnx.cursor()

    query = ("SELECT * FROM homeowner WHERE username=%s AND pass=%s")
    cursor.execute(query, (username, password))
    result = cursor.fetchall()
    cursor.close()

    if len(result) > 0:
        return True
    else:
        return False

def VerifyAdmin(username, password):
    cursor = cnx.cursor()

    query = ("SELECT * FROM employee WHERE username=%s AND pass=%s")
    cursor.execute(query, (username, password))
    
    result = cursor.fetchall()
    cursor.close()

    if len(result) > 0:
        return True
    else:
        return False

def VerifySupervisor(username, password):
    cursor = cnx.cursor()

    query = ("SELECT * FROM supervisor WHERE username=%s and pass=%s")
    cursor.execute(query, (username, password))
    result = cursor.fetchall()
    cursor.close()

    if len(result) > 0:
        return True
    else:
        return False

def WelcomeClient(username):
    cursor = cnx.cursor()

    query = ("SELECT homeowner_fname, homeowner_lname, home_name, street_address FROM homeowner NATURAL JOIN home WHERE username=")
    query = query + "'" + username + "'"
    cursor.execute(query, (username))
    result = cursor.fetchone()
    cursor.close()

    print
    print("--------------------Welcome--------------------")
    print("Hello " + result[0] + " " + result[1] + "\nYour home is: " + result[2] + "\nYour address is: " + result[3])
    print("-----------------------------------------------")

    choice = 99

    while (choice != 3):
        choice = MenuClient()

        if (choice == 0):
            ViewIncidents(username)
        elif (choice == 1):
            AddCameras(username)
        elif (choice == 2):
            DeleteCameras(username)
        elif (choice == 3):
            pass
        else:
            print("Sorry that is an invalid choice!\n")

def WelcomeAdmin(username):
    cursor = cnx.cursor()

    query = ("SELECT fname, lname FROM employee WHERE username=")
    query = query + "'" + username + "'"
    cursor.execute(query)
    result = cursor.fetchone()
    cursor.close()

    print
    print("--------------------Welcome--------------------")
    print("Hello " + result[0] + " " +  result[1])
    print("-----------------------------------------------")


    choice = 99

    while (choice != 8):
        choice = MenuAdmin()

        if (choice == 0):
            CreateUser()
        elif (choice == 1):
            DeleteUser()
        elif (choice == 2):
            DeleteNetwork()
        elif (choice == 3):
            CreateNetwork()
        elif (choice == 4):
            ViewIncidents()
        elif (choice == 5):
            AddSecurityDevices()
        elif (choice == 6):
            AddIncidents()
        elif (choice == 7):
            SupervisorFunctions(username)
        elif (choice == 8):
            pass
        else:
            print("Sorry that is an invalid choice!\n")   

def MenuClient():
    print
    print("--------------------Menu--------------------")
    print("0. View Incidents on your Network")
    print("1. Add Cameras to a Network")
    print("2. Delete a Camera from a Network")
    print("3. Exit")
    print("--------------------------------------------")
    choice = input("Enter your choice [0-3]:")
    print
    return choice

def MenuAdmin():
    print
    print("--------------------Menu--------------------")
    print("0. Create new user")
    print("1. Delete User")
    print("2. Delete Network")
    print("3. Create Network")
    print("4. View Incidents associated with user")
    print("5. Add security devices associated with user")
    print("6. Add incidents associated with user")
    print("7. Supervisor Functions")
    print("8. Exit")
    print("--------------------------------------------")
    choice = input("Enter your choice [0-8]:")
    return choice

def MenuSupervisor():
    print
    print("--------------------Menu--------------------")
    print("0. Create new Employee")
    print("1. Create new Security Network")
    print("2. Delete an Employee")
    print("3. Exit")
    print("--------------------------------------------")
    choice = input("Enter your choice [0-3]:")
    return choice

#check if supervisor. If not return immediatley
def SupervisorFunctions(username):
    cursor = cnx.cursor()

    query = ("SELECT supervisor FROM employee WHERE username=")
    query = query + "'" + username + "'"
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()

    if (result[0] == (1,)):
        choice = 99
        while (choice != 3):
            choice = MenuSupervisor()
            if (choice == 0):
                AddEmployee()
            elif (choice == 1):
                AddSecurityNetwork()
            elif (choice == 2):
                DeleteEmployee()
            elif (choice == 3):
                pass
            else:
                print("Sorry that is not a valid choice!\n")
    else:
        print("Sorry you are not a supervisor!\nThank you. Come again.\n")

def ViewIncidents(username):
    cursor = cnx.cursor()

    query = ("SELECT * FROM incident WHERE homeowner.username=%s AND homeowner.street_address=home.street_address AND incident.street_address=home.street_address")
    cursor.execute(query, (username))
    cursor.close()

    for results in cursor:
        print(results)

def AddCameras(username):
    pass

def DeleteCameras(username):
    pass

def CreateUser(username):
    pass

def DeleteUser(username):
    pass

def DeleteNetwork():
    pass

def CreateNetwork():
    pass

#for the admin so must ask admin for the users username
def ViewIncidents():
    pass

def AddSecurityDevices():
    pass

def AddIncidents():
    pass

def AddEmployee():
    pass

def AddSecurityNetwork():
    pass

def DeleteEmployee():
    pass

def main():

    username, password = Login()

    if VerifyClient(username, password) == True:
        WelcomeClient(username)
    elif VerifyAdmin(username, password) == True:
        WelcomeAdmin(username)
    else:
        print("Error. Not a client or admin!\n")

    cnx.close()

main()