#!/usr/bin/env python3
"""
Name: Hritish Mahajan
Date: 19 April 2023
"""

import os
import subprocess
from time import sleep


def clear_screen():
    """Clear the screen"""
    os.system('clear' if os.name == 'posix' else 'cls')


def check_file_exists(file_path):
    """Check if file exists"""
    return os.path.exists(file_path)


def create_shortcut_file(file_path):
    """Create a shortcut file in the home directory"""
    shortcut_name = os.path.basename(file_path)
    home_dir = os.path.expanduser('~')
    shortcut_path = os.path.join(home_dir, shortcut_name)
    # check if shortcut already exists
    if os.path.islink(shortcut_path) is False:
        os.symlink(file_path, shortcut_path)
        return True
    return False


def remove_shortcut_file(shortcut_name):
    """Remove the shortcut file from the home directory"""
    home_dir = os.path.expanduser('~')
    shortcut_path = os.path.join(home_dir, shortcut_name)
    # check if shortcut exists
    if os.path.islink(shortcut_path):
        os.unlink(shortcut_path)
        return True
    return False


def create_shortcut():
    """Menu for creating a shortcut file in the home directory"""
    clear_screen()
    file_path = input(
        "Please enter the file name to create a shortcut: ")
    # check if file exists
    if not check_file_exists(file_path):
        print(f"\nSorry, couldn't find {colorize(file_path, 'red')}!")
        input("\nPress " + colorize("Enter") +
              " to return to the main menu.")

    else:
        confirm = input(
            f"Found {colorize(file_path)}. Select Y/y to create shortcut. ")
        if confirm.lower() == "y":
            if create_shortcut_file(file_path):
                print("Creating Shortcut, please wait.")
                sleep(2)
                print()
                print_shortcut_report()
                return
            else:
                print(f"\nLink {colorize(file_path, 'red')} already exists!\n")

        else:
            input("Press " + colorize("Enter") +
                  " to return to the main menu.")


def remove_shortcut():
    """Menu for removing a shortcut file from the home directory"""
    clear_screen()
    shortcut_name = input("Please enter the shortcut/link to remove: ")
    home_dir = os.path.expanduser('~')
    shortcut_path = os.path.join(home_dir, shortcut_name)
    # check if shortcut exists
    if os.path.islink(shortcut_path) is False:
        print(f"\nSorry, couldn't find {colorize(shortcut_name, 'red')}!")
        input("\nPress " + colorize("Enter") +
              " to return to the main menu.")
        return

    confirm = input(
        f"Are you sure you want remove {colorize(shortcut_name)}? Press {colorize('Y/y')} to confirm: ")
    if confirm.lower() == "y":
        if remove_shortcut_file(shortcut_name):
            print("\nRemoving link, please wait...")
            sleep(2)
        else:
            print(f"\nSorry, couldn't find {colorize(shortcut_name, 'red')}!")
            sleep(2)

    input("\nPress " + colorize("Enter") +
          " to return to the main menu.")


def print_shortcut_report():
    """Print a report of all the shortcut files in the home directory"""
    home_dir = os.path.expanduser('~')
    os.chdir(home_dir)

    print(f"""**************************************
********** {colorize("Shortcut Report")} ***********
**************************************""")
    print()
    print(f"You current directory is {colorize(cwd, 'yellow')}.")
    links = [entry for entry in os.scandir() if entry.is_symlink()]
    print(f"\nThe number of links is {colorize(str(len(links)), 'yellow')}.\n")
    print(colorize("Symbolic Link", "underline"),
          colorize("Target", "underline"), sep="\t\t")
    # print links by scanning the home directory and printing the name and link
    for link in links:
        target = os.path.realpath(link)
        print(link.name, target, sep="\t\t")
    choice = input(
        f"\n\nTo return to the {colorize('Main Menu', 'yellow')}, press {colorize('Enter', 'yellow')}. Or select {colorize('R/r', 'yellow')} to remove a link. ")
    if choice == "r" or choice == "R":
        remove_shortcut()


def colorize(text, color="green"):
    """Colorize text"""
    color = {'green': '\033[92m', 'red': '\033[91m',
             'yellow': '\033[93m', 'underline': '\033[4m\033[33m'}[color]
    return color + text + '\033[0m'


def main_menu():
    global cwd
    cwd = os.getcwd()
    while True:
        clear_screen()
        print(f"""**************************************
********** {colorize("Shortcut Creator")} **********
**************************************

Enter Selection:

1 - Create a shortcut in your home directory.
2 - Remove a shortcut from your home directory.
3 - Run shortcut report.
""")
        choice = input("Please enter a " + colorize("number (1-4)") +
                       " or " + colorize('"Q/q"') + " to quit the program: ")
        if choice == "1":
            create_shortcut()
        elif choice == "2":
            remove_shortcut()
        elif choice == "3":
            clear_screen()
            print_shortcut_report()
        elif choice == "q" or choice == "Q" or choice == "quit":
            clear_screen()
            print("Quitting program: Returning to shell.\n\n")
            print(colorize("Have a wonderful day!", 'yellow'))
            input()
            break
        else:
            print("Invalid choice. Please try again.")
            sleep(2)


if __name__ == "__main__":

    main_menu()
