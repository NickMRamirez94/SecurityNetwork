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

    while (choice != 9):
        choice = MenuAdmin()

        if (choice == 0):
            CreateUser()
        elif (choice == 1):
            CreateHome(username)
        elif (choice ==2):
            DeleteHome(username)
        elif (choice == 3):
            DeleteCameraNetwork()
        elif (choice == 4):
            CreateCameraNetwork()
        elif (choice == 5):
            ViewIncidents()
        elif (choice == 6):
            AddSecurityDevices()
        elif (choice == 7):
            AddIncidents()
        elif (choice == 8):
            SupervisorFunctions(username)
        elif (choice == 9):
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
    print("1. Add Cameras to a Home")
    print("2. Delete a Camera from a Home")
    print("3. Exit")
    print("--------------------------------------------")
    choice = input("Enter your choice [0-3]: ")
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
    print("3. Delete Camera Network")
    print("4. Create Camera Network")
    print("5. View Incidents associated with user")
    print("6. Add security devices associated with user")
    print("7. Add incidents associated with user")
    print("8. Supervisor Functions")
    print("9. Exit")
    print("--------------------------------------------")
    choice = input("Enter your choice [0-9]: ")
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
    choice = input("Enter your choice [0-3]: ")
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

##############################################################################################
##Used to create a home. The employee must have all pertinent information for the home to be##
##                                        added to the system.                              ##
##############################################################################################
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

##############################################################################################
##Used to delete a home. The employee must have all pertinent information for the home to be##
##                                    deleted from the system.                              ##
##############################################################################################
def DeleteHome(username):
    print
    print("--------------------Home Deletion--------------------")
    print("Here is where we will be able to delete a home")
    print("You will need to enter all the pertinent information so")
    print("that a home can be removed from the system. Thank you.")
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
        street_address = raw_input("Street Address: ")

        print("Please confirm this information.")
        print
        print("Street Address: " + street_address)
        print

        choice = input("1 to confirm. 0 to go back.")

    cursor = cnx.cursor()

    delete_home = ("DELETE h FROM home as h NATURAL JOIN security_network as s")
    delete_home = delete_home + "WHERE h.network_num="
    delete_home = delete_home + "'" + network_num + "' "
    delete_home = delete_home + "AND h.street_address="
    delete_home = delete_home + "'" + street_address + "'"
    
    try:
        print("Deleting home from system.....")
        print
        cursor.execute(delete_home)
        cnx.commit()
        print("...Done..")
        print
    except mysql.connector.Error as err:
        print("Sorry an error occured. Most likely that home is not in the system or is not in your network!\n")

    cursor.close()

##############################################################################################
##Used to delete a Camera Network. The employee must have all pertinent information for     ##
##                           the Camera Network to be deleted from the system.              ##
##############################################################################################
def DeleteCameraNetwork():
    pass

##############################################################################################
##Used to create a Camera Network. The employee must have all pertinent information for     ##
##                           the Camera Network to be entered into the system.              ##
##############################################################################################
def CreateCameraNetwork():
    print
    print("-----------------Create Camera Network----------------")
    print("Here is where we will be able to create a Camera")
    print("Network.You will need to enter all the pertinent information")
    print("so that a Camera Network can be added to the system. Thank you.")
    print("**The Security Network must be in system before the Camera Network**")
    print("-----------------------------------------------------")
    print
    print

    choice = 2
    while (choice != 1):
        device_type = raw_input("Device Type: ")
        device_IP = raw_input("Device IP: ")
        street_address = raw_input("Street Address: ")

        print("Please confirm this information.")
        print
        print("Device Type: " + device_type)
        print("Device IP: " + device_IP)
        print("Street Address: " + street_address)
        print

        choice = input("1 to confirm. 0 to reenter information.\n")

    cursor = cnx.cursor()

    add_security_device = ("INSERT security_device VALUES (")
    add_security_device = add_security_device + "'" + device_type + "', "
    add_security_device = add_security_device + "'" + device_IP + "', "
    add_security_device = add_security_device + "'" + street_address + "');"
    
    try:
        print("Entering security devices into system.....")
        print
        cursor.execute(add_security_device)
        cnx.commit()
        print("...Done..")
        print
    except mysql.connector.Error as err:
        print("Sorry an error occured. Most likely that home is not in the system yet!\n")

    cursor.close()

##############################################################################################
##Used to create a Security Device. The employee must have all pertinent information for    ##
##                           the Security Device to be added to a home.                     ##
##############################################################################################
def AddSecurityDevices():
    print
    print("-----------------Add Security Devices----------------")
    print("Here is where we will be able to add security devices to")
    print("a home.You will need to enter all the pertinent information")
    print("so that a user can be added to the system. Thank you.")
    print("**The home must be in system before security devices**")
    print("-----------------------------------------------------")
    print
    print

    choice = 2
    while (choice != 1):
        device_type = raw_input("Device Type: ")
        device_IP = raw_input("Device IP: ")
        street_address = raw_input("Street Address: ")

        print("Please confirm this information.")
        print
        print("Device Type: " + device_type)
        print("Device IP: " + device_IP)
        print("Street Address: " + street_address)
        print

        choice = input("1 to confirm. 0 to reenter information.\n")

    cursor = cnx.cursor()

    add_security_device = ("INSERT security_device VALUES (")
    add_security_device = add_security_device + "'" + device_type + "', "
    add_security_device = add_security_device + "'" + device_IP + "', "
    add_security_device = add_security_device + "'" + street_address + "');"
    
    try:
        print("Entering security devices into system.....")
        print
        cursor.execute(add_security_device)
        cnx.commit()
        print("...Done..")
        print
    except mysql.connector.Error as err:
        print("Sorry an error occured. Most likely that home is not in the system yet!\n")

    cursor.close()

##############################################################################################
##Used to add an Incident to a home. The employee must have all pertinent information for   ##
##                           the Incident to be added to a home.                            ##
##############################################################################################
def AddIncidents():
    print
    print("---------------------Add Incidents-------------------")
    print("Here is where we will be able to add incidents to")
    print("a home.You will need to enter all the pertinent information")
    print("so that an incident can be added to the system. Thank you.")
    print("**The home must be in system before the incident**")
    print("-----------------------------------------------------")
    print
    print

    choice = 2
    while (choice != 1):
        instrusion_type = raw_input("Intrusion Type: ")
        lost_equity = raw_input("Lost Equity: ")
        occured_time = raw_input("Occured Time **hh:mm:ss**: ")
        current_day = raw_input("Day Occured **yyyy:mm:dd**: ")
        incident_id = raw_input("Incident ID: ")
        street_address = raw_input("Street Address: ")
        network_id = raw_input("Network ID: ")

        print("Please confirm this information.")
        print
        print("Instrusion Type: " + instrusion_type)
        print("Lost Equity: " + lost_equity)
        print("Occured Time: " + occured_time)
        print("Day Occured: " + current_day)
        print("Incident ID: " + incident_id)
        print("Street Address: " + street_address)
        print("Network ID: " + network_id)
        print

        choice = input("1 to confirm. 0 to reenter information.\n")

    cursor = cnx.cursor()

    add_incident = ("INSERT incident VALUES (")
    add_incident = add_incident + "'" + instrusion_type + "', "
    add_incident = add_incident + "'" + lost_equity + "', "
    add_incident = add_incident + "'" + occured_time + "', "
    add_incident = add_incident + "'" + current_day + "', "
    add_incident = add_incident + "'" + incident_id + "', "
    add_incident = add_incident + "'" + street_address + "', "
    add_incident = add_incident + "'" + network_id + "');"
    
    try:
        print("Entering security devices into system.....")
        print
        cursor.execute(add_incident)
        cnx.commit()
        print("...Done..")
        print
    except mysql.connector.Error as err:
        print("Sorry an error occured. Most likely that home is not in the system yet!\n")

    cursor.close()

##############################################################################################
##Used to create an employee. The Supervisor must have all pertinent information and       ##
##                         give the employee a temporary password.                         ##
##############################################################################################
def AddEmployee():
    pass

##############################################################################################
##Used to create a Security network for a city. The Supervisor must have all pertinent     ##
##             information for the Security Network to be added to the system              ##
##############################################################################################
def AddSecurityNetwork():
    pass

##############################################################################################
##Used to delete an employee. The Supervisor must have all pertinent information to         ##
##                         remove the employee from the system.                             ##
##############################################################################################
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