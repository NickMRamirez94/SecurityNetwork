import mysql.connector
from mysql.connector import errorcode
from cryptography.fernet import Fernet
from prettytable import PrettyTable

#Create a connection to the local database
cnx = mysql.connector.connect(user='root', password='smackdown2', database='security')

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
    cursor.execute(query)
    result = cursor.fetchone()
    cursor.close()

    print
    print("----------------------Welcome----------------------")
    print("Hello " + result[0] + " " + result[1] + "\nYour home is: " + result[2] + "\nYour address is: " + result[3])
    print("---------------------------------------------------")

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
            CreateCameraNetwork(username)
        elif (choice == 5):
            ViewIncidentsAdmin()
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
    print
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
    print
    choice = input("Enter your choice [0-9]: ")
    print
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
    print
    choice = input("Enter your choice [0-3]: ")
    print
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
        print("Sorry you are not a Supervisor!\n")

##################################################################################################################
## Will quiery all Incidents based on usernames address. Will not print anything unless there is an instrusion  ##
##################################################################################################################
def ViewIncidents(username):
    cursor = cnx.cursor()

    query = ("SELECT * FROM incident NATURAL JOIN home NATURAL JOIN homeowner WHERE homeowner.username=")
    query = query + "'" + username + "'"
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()

    if len(results) > 0:
        tab = PrettyTable(['Incident Type', 'Amount Lost'])
        for row in results:
            tab.add_row([row[1], row[2]])
        print(tab)
    else:
        print("There are no Incidents at your address at this time.\n")

##############################################################################################
##Used to add or create a camera. The customer must have all pertinent information         ##
##                        for the camera to be added or created.                           ##
##############################################################################################
def AddCameras(username):
    print
    print("----------------------Add Cameras----------------------")
    print("Here is where we will be able to add cameras to a home")
    print("OR network. You will need to enter all the pertinent")
    print("information so that a user can be added to the system.")
    print("-------------------------------------------------------")
    print

    #Retrieve street address. Every user will have an address
    cursor = cnx.cursor()
    query = ("SELECT street_address FROM homeowner WHERE username=")
    query = query + "'" + username + "'"
    cursor.execute(query)
    result = cursor.fetchone()
    cursor.close()
    street_address = result[0]

    #show the user their exisiting cameras
    cursor = cnx.cursor()
    query = ("SELECT IP, cam_name, network_id FROM outdoor_camera WHERE street_address=")
    query = query + "'" + street_address + "'"
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()

    #Check to see if user already has some Cameras.
    if len(results) > 0:
        tab = PrettyTable(['IP', 'Camera Name', 'Network ID'])
        for row in results:
            tab.add_row([row[0], row[1], row[2]])
        print("Here are the Cameras currently at your home.")
        print(tab)
        print
    else:
        print("It looks like you do not have any cameras at this time. Lets add some!\n")

    choice = 2
    while (choice != 1):
        camera_IP = raw_input("Camera IP ** ###.###.##.## **: ")
        camera_name = raw_input("Camera Name: ")
        network_ID = raw_input("Network ID: ")
        if (len(network_ID) != 8):
            print
            print("**Network ID must be 8 characters long. Try again.**")
            print
            continue

        print("\n_____________Please confirm this information_________________\n")
        print
        print("Camera IP: " + camera_IP)
        print("Camera Name: " + camera_name)
        print("Network ID: " + network_ID)
        print

        choice = input("1 to confirm. 0 to reenter information.\n")

    cursor = cnx.cursor()

    add_camera = ("INSERT outdoor_camera VALUES (")
    add_camera = add_camera + "'" + camera_IP + "', "
    add_camera = add_camera + "'" + camera_name + "', "
    add_camera = add_camera + "'" + street_address + "', "
    add_camera = add_camera + "'" + network_ID + "');"
    
    try:
        print("Entering Cameras into system.....")
        print
        cursor.execute(add_camera)
        cnx.commit()
        print("...Done..")
        print
    except mysql.connector.Error as err:
        print("Sorry an error occured. Most likely that Camera Network is not in the system yet!\n")

    cursor.close()

################################################################################
##Used to delete a camera. The customer must have all pertinent information   ##
##                        for the camera to be added or created.             ##
##############################################################################
def DeleteCameras(username):
    print
    print("----------------------Camera Deletion----------------------")
    print("    Here is where we will be able to delete a camera    ")
    print("You will need to enter all the pertinent information so")
    print("that a camera can be removed from the system. Thank you.")
    print("---------------------------------------------------------")
    print
    print

    #Retrieve street address. Every user will have a street address.
    cursor = cnx.cursor()
    query = ("SELECT street_address FROM homeowner WHERE username=")
    query = query + "'" + username + "'"
    cursor.execute(query)
    result = cursor.fetchone()
    cursor.close()
    street_address = result[0]

    #show the user their exisiting cameras
    cursor = cnx.cursor()
    query = ("SELECT IP, cam_name, network_id FROM outdoor_camera WHERE street_address=")
    query = query + "'" + street_address + "'"
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()

    if len(results) > 0:
        tab = PrettyTable(['IP', 'Camera Name', 'Network ID'])
        for row in results:
            tab.add_row([row[0], row[1], row[2]])
        print("Here are the Cameras currently at your home.")
        print(tab)
        print

        choice = 2
        while (choice != 1):
            camera_IP = raw_input("Camera IP: ")

            print("\n_____________Please confirm this information_________________\n")
            print
            print("Camera IP: " + camera_IP)
            print

            choice = input("1 to confirm. 0 to go back.")

        cursor = cnx.cursor()

        delete_camera = ("DELETE c FROM outdoor_camera as c ")
        delete_camera = delete_camera + "WHERE c.IP="
        delete_camera = delete_camera + "'" + camera_IP + "' "
        
        try:
            print("Deleting camera from system.....")
            print
            cursor.execute(delete_camera)
            cnx.commit()
            print("...Done..")
            print
        except mysql.connector.Error as err:
            print("Sorry an error occured. Most likely that camera is not in the system or is not in your network!\n")

        cursor.close()
    else:
        print("It looks like you do not have any cameras at this time. Lets add some!\n")
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
        if (len(customer_id) != 8):
            print
            print("**Sorry. The customer ID is not the correct length. Please try again**")
            print
            continue
        street_address = raw_input("Street Address: ")
        username = raw_input("Username: ")
        password = raw_input("Temp Password: ")

        print("\n_____________Please confirm this information_________________\n")
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

    #Retrieve network number. Every employee will have a network number.
    cursor = cnx.cursor()
    query = ("SELECT network_num FROM security_network NATURAL JOIN ")
    query = query + "employee WHERE employee.username="
    query = query + "'" + username + "'"
    cursor.execute(query)
    result = cursor.fetchone()
    cursor.close()
    network_num = result[0]

    choice = 2
    while (choice != 1):
        home_name = raw_input("Home Name: ")
        contact = raw_input("Phone Number ** (###) ###-#### **: ")
        street_address = raw_input("Street Address: ")

        print("\n_____________Please confirm this information_________________\n")
        print
        print("Home Name: " + home_name)
        print("Phone Number: " + contact)
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
    print("----------------------Home Deletion----------------------")
    print("    Here is where we will be able to delete a home    ")
    print("You will need to enter all the pertinent information so")
    print("that a home can be removed from the system. Thank you.")
    print("**CAUTION. THIS ACTION CANNNOT BE UNDONE. THIS WILL REMOVE**")
    print("**ALL SECURITY DEVICES, HOMEOWNERS, AND OUTDOOR CAMERAS**")
    print("**                ASSOCIATED WITH THE HOME             **")
    print("---------------------------------------------------------")
    print
    print

    #Retrieve network number. All employees have a network number.
    cursor = cnx.cursor()
    query = ("SELECT network_num FROM security_network NATURAL JOIN ")
    query = query + "employee WHERE employee.username="
    query = query + "'" + username + "'"
    cursor.execute(query)
    result = cursor.fetchone()
    cursor.close()
    network_num = result[0]

    #Show admin a list of all current homes.
    cursor = cnx.cursor()
    query = ("SELECT home_name, contact, street_address ")
    query = query + "FROM home "
    query = query + "WHERE network_num="
    query = query + "'" + network_num + "'"
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()
    
    if (len(results) > 0):
        tab = PrettyTable(['Home Name', 'Contact #', 'Street Address'])
        for row in results:
            tab.add_row([row[0], row[1], row[2]])
        print("Here are the Homes currently in your network.")
        print(tab)
        print

        choice = 2
        while (choice != 1):
            street_address = raw_input("Street Address: ")

            print("\n_____________Please confirm this information_________________\n")
            print
            print("Street Address: " + street_address)
            print

            choice = input("1 to confirm. 0 to go back.")

        cursor = cnx.cursor()

        delete_home = ("DELETE h FROM home as h NATURAL JOIN security_network as s ")
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
    
    else:
        print("Sorry there are no homes in your network at this time.")

##############################################################################################
##Used to delete a Camera Network. The employee must have all pertinent information for     ##
##                           the Camera Network to be deleted from the system.              ##
##############################################################################################
def DeleteCameraNetwork():
    print
    print("-------------------Delete Camera Network-------------------")
    print("Here is where we will be able to delete a Camera")
    print("Network.You will need to enter all the pertinent information")
    print("so that a Camera Network can be removed from the system. Thank you.")
    print("**Caution. This action is permanent and cannot be undone**")
    print("-----------------------------------------------------------")
    print
    print

    choice = 2
    while (choice != 1):
        network_id = raw_input("Camera Network ID: ")
        if (len(network_id) != 8):
            print
            print("**Sorry. The Network ID is not the correct length. Please try again**")
            print
            continue

        print("\n_____________Please confirm this information_________________\n")
        print
        print("Camera Network ID: " + network_id)
        print

        choice = input("1 to confirm. 0 to reenter information.\n")

    cursor = cnx.cursor()

    delete_camera_network = ("DELETE c FROM camera_network as c ")
    delete_camera_network = delete_camera_network + "WHERE c.network_id="
    delete_camera_network = delete_camera_network + "'" + network_id + "';"
    
    try:
        print("Deleting Camera Network from system.....")
        print
        cursor.execute(delete_camera_network)
        cnx.commit()
        print("...Done..")
        print
    except mysql.connector.Error as err:
        print("Sorry an error occured. Most likely that Camera Network is not in the system!\n")

    cursor.close()

##############################################################################################
##Used to create a Camera Network. The employee must have all pertinent information for     ##
##                           the Camera Network to be entered into the system.              ##
##############################################################################################
def CreateCameraNetwork(username):
    print
    print("-------------------Create Camera Network-------------------")
    print("Here is where we will be able to create a Camera")
    print("Network.You will need to enter all the pertinent information")
    print("so that a Camera Network can be added to the system. Thank you.")
    print("**The Security Network must be in system before the Camera Network**")
    print("-----------------------------------------------------------")
    print
    print

    choice = 2
    while (choice != 1):
        server_IP = raw_input("Server IP: ")
        network_id = raw_input("Camera Network ID: ")
        if (len(network_id) != 8):
            print
            print("**Sorry. The Camera Network ID is not the correct length. Please try again**")
            print
            continue

        print("\n_____________Please confirm this information_________________\n")
        print
        print("Server IP: " + server_IP)
        print("Camera Network ID: " + network_id)
        print

        choice = input("1 to confirm. 0 to reenter information.\n")
    
    cursor = cnx.cursor()

    query = ("SELECT DISTINCT network_num FROM employee WHERE username=")
    query = query + "'" + username + "'"

    network_num = " "

    try:
        cursor.execute(query)
        result = cursor.fetchone()
        network_num = result[0]
    except mysql.connector.Error as err:
        print("Sorry. There seems to be a problem with your Security Network number.")

    cursor.close()
    cursor = cnx.cursor()

    add_camera_network = ("INSERT camera_network VALUES (")
    add_camera_network = add_camera_network + "'" + server_IP + "', "
    add_camera_network = add_camera_network + "'" + network_id + "', "
    add_camera_network = add_camera_network + "'" + network_num + "');"
    
    try:
        print("Entering Camera Network into system.....")
        print
        cursor.execute(add_camera_network)
        cnx.commit()
        print("...Done..")
        print
    except mysql.connector.Error as err:
        print("Sorry an error occured. Most likely that Security Network is not in the system yet!\n")

    cursor.close()

##################################################################################################################
##Will quiery all instrutions based on street address. Will not print anything unless there is an instrusion    ##
##                        The street address will need to be supplied                                           ##
##################################################################################################################
def ViewIncidentsAdmin():
    print
    print("-------------------View Incidents Admin-------------------")
    print("Here is where we will be able to view incidents at a home")
    print("You will need to enter all the pertinent information")
    print("so that a the incidents can be viewed. Thank you.")
    print("**The home must be in the system in order to view its incidents**")
    print("-----------------------------------------------------------")
    print
    print

    choice = 2
    while (choice != 1):
        street_address = raw_input("Street Address: ")

        print("\n_____________Please confirm this information_________________\n")
        print
        print("Street Address: " + street_address)
        print

        choice = input("1 to confirm. 0 to reenter information.\n")
    cursor = cnx.cursor()

    query = ("SELECT * FROM incident NATURAL JOIN home NATURAL JOIN homeowner WHERE homeowner.street_address=")
    query = query + "'" + street_address + "'"
    try:
        cursor.execute(query)
    except mysql.connector.Error as err:
        print("Sorry an error has occured. Check Street Address!")

    results = cursor.fetchall()
    cursor.close()

    if len(results) > 0:
        tab = PrettyTable(['Instrusion Type', 'Amount Lost'])
        for row in results:
            tab.add_row([row[1], row[2]])
        print(tab)
    else:
        print("There are no instrusions at that address at this time.\n")

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
        device_IP = raw_input("Device IP ** ###.###.##.## **: ")
        street_address = raw_input("Street Address: ")

        print("\n_____________Please confirm this information_________________\n")
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
        if (len(incident_id) != 8):
            print
            print("**Sorry. The Incident ID is not the correct length. Please try again**")
            print
            continue
        street_address = raw_input("Street Address: ")

        print("\n_____________Please confirm this information_________________\n")
        print
        print("Instrusion Type: " + instrusion_type)
        print("Lost Equity: " + lost_equity)
        print("Occured Time: " + occured_time)
        print("Day Occured: " + current_day)
        print("Incident ID: " + incident_id)
        print("Street Address: " + street_address)
        print

        choice = input("1 to confirm. 0 to reenter information.\n")

    cursor = cnx.cursor()

    query = ("SELECT distinct network_id FROM outdoor_camera WHERE street_address=")
    query = query + "'" + street_address + "'"

    try:
        cursor.execute(query)
        result = cursor.fetchone()
        network_id = result[0]
    except mysql.connector.Error as err:
        print("Sorry that home is not part of a network yet!")

    cursor.close()
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
        print("Sorry an error occured.!\n")

    cursor.close()

##############################################################################################
##Used to create an employee. The Supervisor must have all pertinent information and       ##
##                         give the employee a temporary password.                         ##
##############################################################################################
def AddEmployee():
    print
    print("--------------------ADD employee---------------------")
    print("This will add an employee to the system")
    print("The menu following will prompt you on what is needed")
    print("-----------------------------------------------------")
    print

    print("enter in which security nework will this employee work under?")
    NET_ID = raw_input("Network Identification number: ")

    cursor = cnx.cursor()
    query = ("SELECT loc FROM security_network where network_num =")
    query = query + "'" + NET_ID + "'"

    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()

    try:
        if (len(result) == 0):
            print("The network you entered was not found")
        else:
            print("enter in the new name of the employee you wish to add\n")
            EMP_FNAME = raw_input("New employee first name: ")
            EMP_LNAME = raw_input("New employee last name: ")
            print("enter in the new Login name and Password \n")
            EMP_USERN = raw_input("New employee login name: ")
            EMP_PASS  = raw_input("New employee user password ")


            print("enter in the id of the employee")
            EMP_ID = raw_input("New employee ID: ")

            ADD_EMP = "INSERT employee VALUES ("
            ADD_EMP = ADD_EMP + "'" + EMP_ID + "', "
            ADD_EMP = ADD_EMP + "false, "
            ADD_EMP = ADD_EMP + "'" + EMP_LNAME + "', "
            ADD_EMP = ADD_EMP + "'" + EMP_FNAME + "', "
            ADD_EMP = ADD_EMP + "'" + EMP_USERN + "', "
            ADD_EMP = ADD_EMP + "'" + EMP_PASS + "', "
            ADD_EMP = ADD_EMP + "'" + NET_ID + "');"

            cursor = cnx.cursor()
            cursor.execute(ADD_EMP)
            cursor.close()

            cnx.commit()
    except mysql.connector.Error as err:
        print("Sorry an error occured.!\n")   

##############################################################################################
##Used to create a Security network for a city. The Supervisor must have all pertinent     ##
##             information for the Security Network to be added to the system              ##
##############################################################################################
def AddSecurityNetwork():
    print
    print("-------------------Add network---------------------")
    print("This will expand your Network into a new city")
    print("Information needed to perform this operation")
    print("will be prompted")
    print("-----------------------------------------------------")
    print

    choice = 2
    while (choice != 1):
        NET_LOC = raw_input("Network Location: ")
        NET_ID = raw_input("Network ID number (8 digit format): ")
        if (len(NET_ID) != 8):
            print
            print("**Sorry. The Network ID is not the correct length. Please try again**")
            print
            continue

        print("\n_____________Please confirm this information_________________\n")
        print
        print("Network Location: " + NET_LOC)
        print("Network ID: " + NET_ID)
        print

        choice = input("1 to confirm. 0 to reenter information.\n")

    query = (" select* from security_network Where network_num ='")
    query = query + NET_ID + "'"
    try:
        cursor = cnx.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()

        if (len(result) > 0):
            print("**It appears the the network ID you are adding already exist**")
            print("**Please check you ID number and reattempt if necessary**")
        else:
            print("OK, adding this network to the system")

            ADD_NET = "INSERT security_network VALUES ("
            ADD_NET = ADD_NET + "'" + NET_LOC + "', "
            ADD_NET = ADD_NET + "'" + NET_ID + "');"

            cursor = cnx.cursor()
            cursor.execute(ADD_NET)
            cursor.close()
            cnx.commit()
    except mysql.connector.Error as err:
        print("Sorry an error occured.!\n")
    

##############################################################################################
##Used to delete an employee. The Supervisor must have all pertinent information to         ##
##                         remove the employee from the system.                             ##
##############################################################################################
def DeleteEmployee():

    print
    print("----------------Employee Deletion--------------------")
    print("This will perminantly delete an employee from the system")
    print("You will need the Employee ID to execute")
    print("This is permentant, pleese check before you can people")
    print("-----------------------------------------------------")
    print

    query = "SELECT employee_id, lname, fname FROM employee;"

    cursor = cnx.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()

    if len(results) > 0:
        tab = PrettyTable(['Employee ID', 'First Name', 'Last Name'])
        for row in results:
            tab.add_row([row[0], row[1], row[2]])
        print(tab)
        print

        choice = 2
        while (choice != 1):
            EMP_ID = raw_input("Employee ID: ")
            if (len(EMP_ID) != 8):
                print
                print("**Sorry. The Employee ID is not the correct length. Please try again**")
                print
                continue

            print("\n_____________Please confirm this information_________________\n")
            print
            print("Employee ID: " + EMP_ID)
            print

            choice = input("1 to confirm. 0 to reenter information.\n")

        query = ("Select * from employee where employee_id = ")
        query = query + "'" + EMP_ID + "'"

        cursor = cnx.cursor()
        try:
            cursor.execute(query)
            result = cursor.fetchone()
            if (len(result) == 0):
                print("Well.. it looks like that employee doesn't exit\n")
                print("thats embarassing, come back when you know what you are doing")
            else:
                delete_employee = "DELETE e FROM employee as e WHERE employee_id="
                delete_employee = delete_employee + "'" + EMP_ID + "'"

                cursor.execute(delete_employee)
                cnx.commit()
                print("you have sucessfully Fired Somone! rest easy tonight.")        
                cursor.close()
        except mysql.connector.Error as err:
            print("Sorry an error occured.!\n")
        
    else:
        print("**Sorry there are no employees in the system yet! Add some first.**")


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