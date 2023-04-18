#!/usr/bin/env python3
"""
Name: Hritish Mahajan
Date: 18 February 2023
"""

import os
import sys
import subprocess
from time import sleep


def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')


def get_cwd():
    return os.getcwd()


def check_file_exists(file_path):
    return os.path.exists(file_path)


def create_shortcut(file_path):
    shortcut_name = os.path.basename(file_path)
    home_dir = os.path.expanduser('~')
    shortcut_path = os.path.join(home_dir, shortcut_name)
    subprocess.run(['ln', '-s', file_path, shortcut_path])


def remove_shortcut(shortcut_name):
    home_dir = os.path.expanduser('~')
    shortcut_path = os.path.join(home_dir, shortcut_name)
    if os.path.islink(shortcut_path):
        os.unlink(shortcut_path)
        return True
    return False


def print_shortcut_report():
    home_dir = os.path.expanduser('~')
    os.chdir(home_dir)

    print("********************")
    print("** Shortcut Report")
    print("*****************")
    print()
    print(f"You current directory is {get_cwd()}.")
    links = [entry for entry in os.scandir() if entry.is_symlink()]
    print(f"The number of links is {len(links)}.")
    print("Symbolic Link | Target Path")
    for link in links:
        target = os.readlink(link.path)
        print(f"{link.name} | {target}")


def main_menu():
    clear_screen()
    print("# Main Menu\n")
    print("****************")
    print("********* Shortcut Creator")
    print("****************\n")
    print("Enter Selection:")
    print("1 - Create a shortcut in your home directory.")
    print("2 - Remove a shortcut from your home directory.")
    print("3 - Run shortcut report.")
    print("Please enter a number (1-3) or '/q' to quit the program.")
    choice = input()

    if choice == "1":
        clear_screen()
        file_path = input("Please enter the file name to create a shortcut: ")
        if not check_file_exists(file_path):
            print("File not found.")
        else:
            confirm = input(
                f"Found {file_path}. Select Y/y to create shortcut. ")
            if confirm.lower() == "y":
                create_shortcut(file_path)
                print("Creating Shortcut, please wait.")
                sleep(2)
                print_shortcut_report()
    elif choice == "2":
        clear_screen()
        shortcut_name = input("Please enter the shortcut/link to remove: ")
        confirm = input(
            f"Are you sure you want remove {shortcut_name}? Press Y/y to confirm: ")
        if confirm.lower() == "y":
            if remove_shortcut(shortcut_name):
                print("Removing link, please wait...")
                sleep(2)
                clear_screen()
            else:
                print(f"Sorry, couldn't find {shortcut_name}!")
                sleep(2)
    elif choice == "3":
        clear_screen()
        print_shortcut_report()
    elif choice == "/q":
        sys.exit(0)
    else:
        print("Invalid choice. Please try again.")
        sleep(2)

    input("\nTo return to the Main Menu, press Enter.")
    main_menu()


if __name__ == "__main__":
    main_menu()
