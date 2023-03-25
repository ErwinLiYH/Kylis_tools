import pyperclip
import argparse
import Kkit
import json
import os
import hashlib
import base64
import getpass
# from cryptography.fernet import Fernet
from Kkit import encryption

def read_config(config_path):
    return json.loads(Kkit.load(config_path, "utf-8"))

def gen_key(pin):
    bytes_key = pin.encode('utf-8')
    hash_object = hashlib.sha256(bytes_key)
    hex_dig = hash_object.hexdigest()
    key_bytes = bytes.fromhex(hex_dig)[:32]
    key = base64.urlsafe_b64encode(key_bytes)
    return key

def get_passwd(conf_dict, pin):
    while True:
        key  = input("input a password key: ")
        if key == "q()":
            print("Thank you!")
            break
        elif key == "h()":
            print("q() for leaving\ns() for showing all password keys")
        elif key == "s()":
            Kkit.print_list(list(conf_dict["passwds"].keys()), 5, verbose=False)
        else:
            try:
                # encrypted_passwd = conf_dict["passwds"][key].encode("utf-8")
                encrypted_passwd = conf_dict["passwds"][key]
                # cipher_suite = Fernet(gen_key(pin))
                # password = cipher_suite.decrypt(encrypted_passwd).decode("utf-8")
                password = encryption.decrypt_string(encrypted_passwd, pin)
                pyperclip.copy(password)
                print("copied password for %s to clipborad."%key)
            except KeyError:
                print("Can't find password for %s, please input again, using s() to show all keys"%key)

def store_passwd(conf_dict, conf_path, pin):
    key = input("input a password key: ")
    prompt = "please input password for %s: "%key
    if key in conf_dict["passwds"]:
        x = input("key '%s' already added, do you want to modify?(yes/no): "%key)
        if x == "yes" or x == "y" or x == "Y":
            prompt = "please input the new password for %s: "%key
        else:
            exit(1)
    # cipher_suite = Fernet(gen_key(pin))
    while True:
        passwd = getpass.getpass(prompt)
        passwd2 = getpass.getpass("please input again: ")
        if passwd==passwd2:
            break
        else:
            print("password should be same as the first one!")
    # conf_dict["passwds"][key] = cipher_suite.encrypt(passwd.encode("utf-8")).decode("utf-8")
    conf_dict["passwds"][key] = encryption.encrypt_string(passwd, pin)
    Kkit.store(conf_path, json.dumps(conf_dict, indent=4, ensure_ascii=False), encoding="utf-8")
    print("password added/modified to %s"%conf_path)

def main():

    home_directory = os.environ["HOME"]

    parser = argparse.ArgumentParser(description='secure password holder')
    parser.add_argument("--config", "-c", default=os.path.join(home_directory, "ktools_conf/passwd_holder.conf"), type=str, action="store", help="the config file path, default is ~/Myscripts/Conf/scphelper.conf")
    parser.add_argument('--add', '-a', action='store_true', help="add a password")
    parser.set_defaults(add=False)

    args = parser.parse_args()

    if os.path.exists(args.config) == False:
        conf_dict = {}
        while True:
            pin = getpass.getpass("Initialize your pin: ")
            pin2 = getpass.getpass("please input again: ")
            if pin==pin2:
                break
            else:
                print("password should be same as the first one!")
        conf_dict["pin"] = base64.b64encode(pin.encode("utf-8")).decode('utf-8')
        conf_dict["passwds"] = {}
        Kkit.store(args.config, json.dumps(conf_dict, indent=4, ensure_ascii=False), encoding="utf-8")
        print("initialize conf file in %s"%args.config)
        print("You can add a password now")
        store_passwd(conf_dict, args.config, pin)
    else:
        pin = getpass.getpass("password: ")
        conf_dict = read_config(args.config)
        base64_pin = base64.b64encode(pin.encode("utf-8")).decode('utf-8')
        right_base64_pin = conf_dict["pin"]
        if right_base64_pin == base64_pin:
            pass
        else:
            print("password ERROR!")
            exit(1)

        if args.add:
            print("You can add or modify a password now")
            store_passwd(conf_dict, args.config, pin)
        else:
            get_passwd(conf_dict, pin)

if __name__=="__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Force quit")