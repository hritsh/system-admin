#!/usr/bin/env python3
"""
Name: Hritish Mahajan
Date: 9 February 2023
"""

import os
import subprocess
import socket
from time import sleep

def get_gateway():
    # check for gateway using ip route command
    gateway = subprocess.check_output("ip route", shell=True).decode("utf-8")
    if "default" in gateway:
        gateway = gateway.split()[2]
        return gateway
    else:
        return ""


def test_gateway():
    # test connectivity to gateway using ping command
    clear_screen()
    print("Testing connectivity to your gateway...")
    gateway = get_gateway()
    clear_screen()
    # send 3 pings to gateway and return response
    print("Running test on gateway: " + gateway + ", please wait...\n")
    response = subprocess.call("ping -c 3 " + gateway, stdout=subprocess.PIPE, shell=True)
    # check for error and print response
    if response == 0:
        print("The gateway (" + gateway + ") is reachable and the test was " +
              colorize("SUCCESSFUL", "yellow") + "!")
    else:
        print("Your gateway is unreachable and the test has " +
              colorize("FAILED", "red") + "!")
    print("")
    press_enter()
    return response


def test_remote():
    # test connectivity to remote server using ping command
    clear_screen()
    print("Testing connectivity to remote server... Trying IP Address 129.21.3.17\n")
    # send 3 pings to remote server and return response
    response = subprocess.call("ping -c 3 129.21.3.17", stdout=subprocess.PIPE, shell=True)
    # check for error and print response
    if response == 0:
        print("The remote server (129.21.3.17) is reachable and the test was " +
              colorize("SUCCESSFUL", "yellow") + "!")
    else:
        print("The remote server was unreachable and the test has " +
              colorize("FAILED", "red") + "!")
    print("")
    press_enter()
    return response


def test_dns():
    # test DNS resolution using socket command
    clear_screen()
    print("Running DNS resolution test, please wait...\n")
    # try to resolve hostname and return response
    try:
        result = socket.gethostbyname("www.google.com")
        print("www.google.com resolved to: " + result +
              " and the test was " + colorize("SUCCESSFUL", "yellow") + "!")
    except socket.error:
        print("The DNS could not resolve and the test was " +
              colorize("FAILED", "red") + "!")
    print("")
    press_enter()
    return result


def colorize(text, color="green"):
    color = {'green': '\033[92m', 'red': '\033[91m',
             'yellow': '\033[93m'}[color]
    return color + text + '\033[0m'


def clear_screen():
    os.system("clear")


def press_enter():
    input("\nPress enter to continue...")


def main():
    choice = ""
    while choice != "q" or choice != "Q":
        clear_screen()
        print(f"""**************************************
****** {colorize("Ping Test Troubleshooter")} ******
**************************************

Enter Selection:

1 - Test connectivity to your gateway.
2 - Test for remote connectivity.
3 - Test for DNS resolution.
4 - Display gateway IP Address.
""")

        choice = input("Please enter a " + colorize("number (1-4)") +
                       " or " + colorize('"Q/q"') + " to quit the program: ")

        if choice == "1":
            test_gateway()
        elif choice == "2":
            test_remote()
        elif choice == "3":
            test_dns()
        elif choice == "4":
            gateway = get_gateway()
            clear_screen()
            print("Your gateway IP address is: " +
                  colorize(gateway, "yellow") + ".")
            press_enter()
        elif choice == "q" or choice == "Q":
            clear_screen()
            print("Quitting program: returning to shell.\n\n")
            print(colorize("Have a wonderful day!", "yellow"))
            sleep(1)
            clear_screen()
            break
        else:
            choice = input("""
You entered an """ + colorize("invalid option","red") + """!
Please select a number between 1 through 4.""")
            continue


if __name__ == "__main__":
    main()
