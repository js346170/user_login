import csv
import os  # For cross-platform screen clearing

def clear_output():
    """Cross-platform screen clearing"""
    os.system('cls' if os.name == 'nt' else 'clear')

def registerUser():
    """Handle user registration"""
    with open("users.csv", mode="a", newline="") as f:
        writer = csv.writer(f, delimiter=",")
        print("To register, please enter your information:")
        email = input("E-mail: ")
        password = input("Password: ")
        password2 = input("Re-type password: ")
        clear_output()
        if password == password2:
            writer.writerow([email, password])
            print("You are now registered!")
        else:
            print("Passwords don't match. Please try again.")

def loginUser():
    """Handle user login"""
    print("To login, please enter your information:")
    email = input("E-mail: ")
    password = input("Password: ")
    clear_output()
    try:
        with open("users.csv", mode="r") as f:
            reader = csv.reader(f, delimiter=",")
            for row in reader:
                if row == [email, password]:
                    print("You are now logged in!")
                    return True
    except FileNotFoundError:
        print("No users registered yet.")
    print("Invalid credentials. Please try again.")
    return False

# Main application state
active = True
logged_in = False

# Main loop
while active:
    if logged_in:
        print("1. Logout\n2. Quit")
    else:
        print("1. Login\n2. Register\n3. Quit")
    
    choice = input("What would you like to do? ").lower().strip()
    clear_output()
    
    if choice == "2" or choice == "register":
        if not logged_in:
            registerUser()
        else:
            print("Please logout before registering.")
    elif choice == "1" or choice == "login":
        if not logged_in:
            logged_in = loginUser()
        else:
            print("You're already logged in.")
    elif choice == "3" or choice == "quit":
        active = False
        print("Have a nice day!")
    elif choice == "1" or choice == "logout":  # Only shown when logged in
        if logged_in:
            logged_in = False
            print("You have been logged out")
    else:
        print("Invalid option. Please try again!")
