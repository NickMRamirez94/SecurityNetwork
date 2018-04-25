import mysql.connector
from mysql.connector import errorcode
from cryptography.fernet import Fernet

cnx = mysql.connector.connect(user='root', password='password', database='security')

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

def WelcomeClient(username):
    cursor = cnx.cursor()

    query = ("SELECT homeowner_lname, homeowner_fname, home_name, street_address FROM homeowner NATURAL JOIN home WHERE username=%s")
    cursor.execute(query, (username))

    for (homeowner_lname, homeowner_fname, home_name, street_address) in cursor:
        print
        print "--------------------Welcome--------------------"
        print("Hello" + homeowner_fname + " " + homeowner_lname + "\nYour home name is: " + home_name + " and you live on: " + street_address)
        print "-----------------------------------------------"
        
    cursor.close()

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
            print "Sorry that is an invalid choice!\n"

def WelcomeAdmin(username):
    cursor = cnx.cursor()

    print("\n" + username + "\n")
    query = ("SELECT * FROM employee WHERE username='%s'")
    cursor.execute(query, (username))

    row = cursor.fetchall()
    cursor.close()
    
    print(row)
    '''
    for (lname, fname) in cursor:
        print
        print "--------------------Welcome--------------------"
        print("Hello" + fname + " " + lname + "\n")
        print "-----------------------------------------------"
    '''
    choice = 99

    while (choice != 7):
        choice = MenuAdmin()

        if (choice == 0):
            CreateUser(username)
        elif (choice == 1):
            DeleteUser(username)
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
            pass
        else:
            print "Sorry that is an invalid choice!\n"


def MenuClient():
    print
    print "--------------------Menu--------------------"
    print "0. View Incidents on your Network"
    print "1. Add Cameras to a Network"
    print "2. Delete a Camera from a Network"
    print "3. Exit"
    print "--------------------------------------------"
    choice = input("Enter your choice [0-3]:")
    print
    return choice

def MenuAdmin():
    print
    print "--------------------Menu--------------------"
    print "0. Create new user"
    print "1. Delete User"
    print "2. Delete Network"
    print "3. Create Network"
    print "4. View Incidents associated with user"
    print "5. Add security devices associated with user"
    print "6. Add incidents associated with user"
    print "7. Exit"
    print "--------------------------------------------"
    choice = input("Enter your choice [0-7]:")
    return choice


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

def main():

    username, password = Login()

    if VerifyClient(username, password) == True:
        WelcomeClient(username)
    else:
        if VerifyAdmin(username, password) == True:
            WelcomeAdmin(username)
        else:
            print("Error. Not a client or admin!\n")

    cnx.close()

main()