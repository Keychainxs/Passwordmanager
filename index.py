from cryptography.fernet import Fernet 
import base64 
import hashlib 
import msvcrt
import getpass
import os 


def getpass(prompt="Password: "):
    print(prompt, end='', flush=True)
    password = b''
    while True:
        char = msvcrt.getch()
        if char in b'\r\n':
            print('')
            break
        password += char
        print('*', end='', flush=True)
    return password.decode()



master_password = getpass("What is the master password: ")



def load_key(): 
    with open("key.key", 'rb') as file: 
        key= file.read()
   
    return key 
loaded_key = load_key()
combined_key = loaded_key + master_password.encode()

hashed_key = hashlib.sha256(combined_key).digest()
key = base64.urlsafe_b64encode(hashed_key)
fer = Fernet(key)


def view (): 
    try:
        with open('passwords.txt', 'r') as f: 
             for line in f.readlines(): 
           
                data = line.strip()
                if "|" in data:
                    user, passw = data.split("|", 1)
                    try:
                        decrypted_password = fer.decrypt(passw.encode()).decode()
                        print("User:", user , " | Password:", decrypted_password)
                    except Exception as e: 
                        print(f"error decrypting password for user {user}: {e}")
                else:
                    print(f"Skipping line: {data}")
    except FileNotFoundError: 
        print(f"The file password.txt was not found" )
    except Exception as e:
        print(f"An error occurred:{e}")


def add (): 
        name = input("Acount name: ")
        pwd = input("password: ")
        try:
            encrypted_password = fer.encrypt(pwd.encode()).decode()
            with open('passwords.txt', 'a') as f: 
                f.write(name + "|"+ encrypted_password + "\n")
            print("password added successfully")
        except Exception as e: 
            print(f"An error occured while add the password: {e}")

def delete():

    name = input("Enter the account name to delete: ")
    try: 
        with open('password.txt', 'r') as f: 
            lines= f.readlines()
        with open ('password.txt', 'w') as f:
            for line in lines: 
                if line.strip().split("|")[0] != name: 
                    f.write(line)
        print(f"Password deleted successfully: {name}")
    except Exception as e:
        print(f"An error occured while deleting the password: {e}") 

def update(): 
    name = input("Enter the account name to update: ")
    new_pwd = getpass("Enter the new password: ")

    try: 
        encrypted_password = fer.encrypt(new_pwd.encode()).decode()
        with open('passwords.txt', 'r') as f:
            lines = f.readlines()
        with open('passwords.txt', 'w') as f: 
            for line in lines: 
                user, passw = lines.strip().split("|",1)

                if user ==name: 
                    f.write(f"{user}|{encrypted_password}\n")
                else:
                    f.write(line) 
                print(f"password updated successfully: {name}")
    except Exception as e:
        print(f"an error occurred while updating the password: {e}")
while True:
    mode = input("would you like to add an existing password or view an existing password(view, add, delete, update)? Press q to quit: ")

    if mode == "q" : 
        break

    elif mode == "view": 
        view()
    elif mode == "add": 
        add()
    elif mode =="delete": 
        delete()
    elif mode == "update": 
        update()
    else: 
        print("Invalid, try again")
        continue