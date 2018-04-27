import mysql.connector
from mysql.connector import errorcode
from cryptography.fernet import Fernet

cnx = mysql.connector.connect(user='root', password='password', database='security')

########################################################################################
##Initial function called in main(). Will return the username and password of the user##
####################################################################################### 
def Login():
    username = raw_input("Username: ")
    password = raw_input("Password: ")

    return username, password

#############################################################################
##Used to verify that user is a Client. Returns TRUE if so. FALSE otherwise##
############################################################################
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

#############################################################################
##Used to verify that user is an Admin. Returns TRUE if so. FALSE otherwise##
#############################################################################
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

########################################################################################
##Displays a welcome message to the client and calls MenuClient() to find their choice##
########################################################################################
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

######################################################################################
##Displays a welcome message to the admin and calls MenuAdmin() to find their choice##
######################################################################################
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

    while (choice != 10):
        choice = MenuAdmin()

        if (choice == 0):
            CreateUser()
        elif (choice == 1):
            CreateHome(username)
        elif (choice ==2):
            DeleteHome()
        elif (choice == 3):
            DeleteUser()
        elif (choice == 4):
            DeleteNetwork()
        elif (choice == 5):
            CreateNetwork()
        elif (choice == 6):
            ViewIncidents()
        elif (choice == 7):
            AddSecurityDevices()
        elif (choice == 8):
            AddIncidents()
        elif (choice == 9):
            SupervisorFunctions(username)
        elif (choice == 10):
            pass
        else:
            print("Sorry that is an invalid choice!\n")  

#########################################
##Main menu for the client (homeowners)##
#########################################
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

############################
##Main menu for the admin##
###########################
def MenuAdmin():
    print
    print("--------------------Menu--------------------")
    print("0. Create new user")
    print("1. Create Home")
    print("2. Delete Home")
    print("3. Delete User")
    print("4. Delete Network")
    print("5. Create Network")
    print("6. View Incidents associated with user")
    print("7. Add security devices associated with user")
    print("8. Add incidents associated with user")
    print("9. Supervisor Functions")
    print("10. Exit")
    print("--------------------------------------------")
    choice = input("Enter your choice [0-10]:")
    return choice

########################################################################################################
##Menu for the supevisor. If SupervisorFunctions verifys employee is a supervisor. This will be called##
########################################################################################################
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

##################################################
##Check if supervisor. If not return immediatley##
##################################################
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

##################################################################################################################
##Will quiery all instrutions based on usernames address. Will not print anything unless there is an instrusion##
##################################################################################################################
def ViewIncidents(username):
    cursor = cnx.cursor()

    query = ("SELECT * FROM incident NATURAL JOIN home NATURAL JOIN homeowner WHERE homeowner.username=")
    query = query + "'" + username + "'"
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()

    if len(results) > 0:
        for row in results:
            print("Instrusion Type: " + row[1] + "\nAmount Lost: " + row[2])
    else:
        print("There are no instrusions at your address at this time.\n")

############################
##        DO              ##
############################

def AddCameras(username):
    pass

def DeleteCameras(username):
    pass

##############################################################################################
##Used to create a user. The employee must have all pertinent information and give the user##
##                                        a temporary password.                            ##
##############################################################################################
def CreateUser():
    print
    print("--------------------User Creation--------------------")
    print("Here is where we will be able to create a new homeowner")
    print("You will need to enter all the pertinent information so")
    print("that a user can be added to the system. Thank you.")
    print("**The home must be in system before user if new home**")
    print("-----------------------------------------------------")
    print
    print

    choice = 2
    while (choice != 1):
        homeowner_fname = raw_input("Homeowner first name: ")
        homeowner_lname = raw_input("Homeowner last name: ")
        customer_id = raw_input("Customer id: ")
        street_address = raw_input("Street Address: ")
        username = raw_input("Username: ")
        password = raw_input("Temp Password: ")

        print("Please confirm this information.")
        print
        print("Homeowner first name: " + homeowner_fname)
        print("Homeowner last name: " + homeowner_lname)
        print("Customer id: " + customer_id)
        print("Street Address: " + street_address)
        print("Username: " + username)
        print("Temp Password: " + password)
        print

        choice = input("1 to confirm. 0 to reenter information.\n")

    cursor = cnx.cursor()

    add_customer = ("INSERT homeowner VALUES (")
    add_customer = add_customer + "'" + homeowner_lname + "', "
    add_customer = add_customer + "'" + homeowner_fname + "', "
    add_customer = add_customer + "'" + customer_id + "', "
    add_customer = add_customer + "'" + street_address + "', "
    add_customer = add_customer + "'" + username + "', "
    add_customer = add_customer + "'" + password + "');"
    
    try:
        print("Entering user into system.....")
        print
        cursor.execute(add_customer)
        cnx.commit()
        print("...Done..")
        print
    except mysql.connector.Error as err:
        print("Sorry an error occured. Most likely that home is not in the system yet!\n")

    cursor.close()



def CreateHome(username):
    print
    print("--------------------Home Creation--------------------")
    print("Here is where we will be able to create a new home")
    print("You will need to enter all the pertinent information so")
    print("that a home can be added to the system. Thank you.")
    print("**The home must be in system before user if new home**")
    print("-----------------------------------------------------")
    print
    print

    #Retrieve network number
    cursor = cnx.cursor()
    query = ("SELECT network_num FROM security_network NATURAL JOIN")
    query = query + "employee WHERE employee.username="
    query = query + "'" + username + "'"
    cursor.execute(query)
    result = cursor.fetchone()
    cursor.close()
    network_num = result[0]

    choice = 2
    while (choice != 1):
        home_name = raw_input("Home Name: ")
        contact = raw_input("Phone Number: ")
        street_address = raw_input("Street Address: ")
        network_num = raw_input("Your Network Number: ")

        print("Please confirm this information.")
        print
        print("Homeowner Name: " + home_name)
        print("Homeowner last name: " + contact)
        print("Street Address: " + street_address)
        print

        choice = input("1 to confirm. 0 to go back.")

    cursor = cnx.cursor()

    add_home = ("INSERT home VALUES (")
    add_home = add_home + "'" + home_name + "', "
    add_home = add_home + "'" + contact + "', "
    add_home = add_home + "'" + street_address + "', "
    add_home = add_home + "'" + network_num + "');"
    
    try:
        print("Entering home into system.....")
        print
        cursor.execute(add_home)
        cnx.commit()
        print("...Done..")
        print
    except mysql.connector.Error as err:
        print("Sorry an error occured. Most likely that security network is not in the system yet!\n")

    cursor.close()

def DeleteHome():
    pass

def DeleteUser(username):
    pass

def DeleteNetwork():
    pass

def CreateNetwork():
    pass


def AddSecurityDevices():
    pass

def AddIncidents():
    pass

#DAVID
def AddEmployee():
    pass

#DAVID
def AddSecurityNetwork():
    pass

#DAVID
def DeleteEmployee():
    pass


#########################
#########################
##                     ##
##    MAIN FUNCTION    ##
##                     ##
#########################
#########################
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