#!/usr/bin/env python3
"""
Name: Hritish Mahajan
Date: 18 February 2023
"""


import csv
import os
import pwd
import sys
import subprocess
import grp


def read_csv_file(filename):
    """Read the CSV file and return a list of dictionaries"""
    with open(filename) as csv_file:
        csv_reader = csv.DictReader(csv_file)
        return list(csv_reader)


def check_user(user):
    """Check if the user details are valid"""
    if not user['Department']:
        print('Cannot process employee ID {}.\t'.format(user['EmployeeID']) +
              colorize('Not a valid department.', 'red'))
        return False
    if not user['FirstName'] or not user['LastName'] or not user['Office'] or not user['Phone']:
        print('Cannot process employee ID {}.\t'.format(user['EmployeeID']) +
              colorize('Insufficient data.', 'red'))
        return False
    return True


def get_shell(user):
    """Return the shell for the user"""
    if user['Department'] == 'office':
        return '/bin/csh'
    return '/bin/bash'


def get_userid(user):
    """Return the user ID for the user"""
    # Get the first initial of the first name
    first_initial = user['FirstName'][0].lower()
    # Get the last name
    last_name = user['LastName'].lower()
    # Get the user ID
    user_id = first_initial + last_name
    # Check for special characters
    for char in user_id:
        if not char.isalnum():
            user_id = user_id.replace(char, '')
    # Check if the user ID exists
    if user_id in [u.pw_name for u in pwd.getpwall()]:
        # Get the number of users with the same ID
        num_users = len([u for u in pwd.getpwall()
                         if u.pw_name.startswith(user_id)])
        # Append the number to the user ID
        user_id = user_id + str(num_users)
    return user_id


def get_group(user):
    """Return the group for the user"""
    # Get the group name
    group_name = user['Department'].lower()
    # Check if the group exists
    if group_name not in [g.gr_name for g in grp.getgrall()]:
        # Create the group
        subprocess.call(['groupadd', group_name])
    return group_name


def create_user(user):
    """Create the user"""
    # Check if the user details are valid
    if not check_user(user):
        return
    # Get the user ID
    user_id = get_userid(user)
    # Print a message
    print('Processing employee ID {}.'.format(user['EmployeeID']), end='\t\t')
    # Get the group
    group = get_group(user)
    # Get the shell
    shell = get_shell(user)

    # Get and create the home directory
    home_dir = '/home/' + group + '/' + user_id
    if not os.path.exists(home_dir):
        os.makedirs(home_dir)
    # Create the user
    subprocess.call(['useradd', '-m', '-s', shell, '-d', home_dir,
                     '-g', group, '-p', 'password', user_id], stderr=subprocess.DEVNULL)
    # Expire the password and do not show output
    subprocess.call(['passwd', '-e', user_id], stdout=subprocess.DEVNULL)

    print(colorize(user_id) + ' added to system.')


def colorize(text, color="green"):
    color = {'green': '\033[92m', 'red': '\033[91m',
             'yellow': '\033[93m'}[color]
    return color + text + '\033[0m'


def main():
    # Clear the terminal
    os.system('clear')
    # Check if the script is run as root
    if os.geteuid() != 0:
        print(colorize('This script must be run as root.', 'red'))
        sys.exit(1)
    # Print the header
    print('Adding new users to the system.')
    print('Please Note: The default password for new users is ' +
          colorize('password') + '.')
    print('For testing purposes. Change the password to ' +
          colorize('1$4pizz@') + '.\n')
    # Read the CSV file
    users = read_csv_file('linux_users.csv')
    # Create the users
    for user in users:
        create_user(user)
        print()


if __name__ == '__main__':
    main()
