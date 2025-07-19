import csv
import os
import hashlib
import getpass  # For secure password input
import re  # For email validation
from datetime import datetime

# Security enhancements
PEPPER = b's3cr3t_p3pp3r'  # Add this to passwords before hashing
HASH_ITERATIONS = 100000

def clear_screen():
    """Cross-platform screen clearing"""
    os.system('cls' if os.name == 'nt' else 'clear')

def hash_password(password):
    """Securely hash password with salt and pepper"""
    salt = os.urandom(16)  # Unique salt per user
    return hashlib.pbkdf2_hmac(
        'sha256',
        password.encode() + PEPPER,
        salt,
        HASH_ITERATIONS
    ).hex(), salt.hex()

def verify_password(stored_hash, salt_hex, password_attempt):
    """Verify password against stored hash"""
    salt = bytes.fromhex(salt_hex)
    attempt_hash = hashlib.pbkdf2_hmac(
        'sha256',
        password_attempt.encode() + PEPPER,
        salt,
        HASH_ITERATIONS
    ).hex()
    return attempt_hash == stored_hash

def is_valid_email(email):
    """Basic email validation"""
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

def load_users():
    """Load users from CSV file"""
    users = {}
    try:
        with open("users.csv", "r") as f:
            reader = csv.reader(f)
            for row in reader:
                if len(row) == 4:  # email, salt, hash, timestamp
                    users[row[0]] = {
                        'salt': row[1],
                        'hash': row[2],
                        'timestamp': row[3]
                    }
    except FileNotFoundError:
        pass
    return users

def save_user(email, salt, password_hash):
    """Save new user to CSV file"""
    with open("users.csv", "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            email, 
            salt, 
            password_hash,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ])

def register_user():
    """Handle secure user registration"""
    print("\n=== REGISTRATION ===")
    email = input("E-mail: ").strip().lower()
    
    if not is_valid_email(email):
        clear_screen()
        print("Invalid email format. Please try again.")
        return
    
    users = load_users()
    if email in users:
        clear_screen()
        print("Email already registered. Please login or use a different email.")
        return
    
    while True:
        password = getpass.getpass("Password (min 8 chars): ")
        if len(password) < 8:
            print("Password must be at least 8 characters")
            continue
            
        password2 = getpass.getpass("Confirm password: ")
        if password == password2:
            break
        print("Passwords don't match. Please try again.")
    
    password_hash, salt = hash_password(password)
    save_user(email, salt, password_hash)
    clear_screen()
    print("Registration successful! You can now login.")

def login_user():
    """Handle secure user login"""
    print("\n=== LOGIN ===")
    email = input("E-mail: ").strip().lower()
    password = getpass.getpass("Password: ")
    clear_screen()
    
    users = load_users()
    if email in users:
        user = users[email]
        if verify_password(user['hash'], user['salt'], password):
            print(f"Welcome back! Last login: {user['timestamp']}")
            return True
    
    print("Invalid credentials. Please try again.")
    return False

def main_menu():
    """Display main menu and handle navigation"""
    active = True
    logged_in = False
    
    while active:
        print("\n=== MAIN MENU ===")
        if logged_in:
            print("1. Account Settings")
            print("2. Logout")
            print("3. Quit")
        else:
            print("1. Login")
            print("2. Register")
            print("3. Quit")
        
        choice = input("\nChoose an option: ").strip()
        clear_screen()
        
        if choice == "1":
            if logged_in:
                print("Account Settings (Coming Soon!)")
            else:
                logged_in = login_user()
                
        elif choice == "2":
            if logged_in:
                logged_in = False
                print("You have been logged out successfully.")
            else:
                register_user()
                
        elif choice == "3":
            active = False
            print("Thank you for using our service. Goodbye!")
            
        else:
            print("Invalid option. Please choose 1-3")

if __name__ == "__main__":
    clear_screen()
    print("=== SECURE LOGIN SYSTEM ===")
    main_menu()