import re
from enigma_machine import enigma_machine
from rotor import rotor

rotor_options = {}


def import_rotors():
    file_lines = open('rotor_details.txt', 'r').read().splitlines()

    for i in range(0, len(file_lines)):
        if file_lines[i][0] != ('#'):
            data_line = file_lines[i].split('|')
            gear_name = data_line[0]
            gear_key = data_line[1]
            gear_notch = data_line[2]
            rotor_options[gear_name] = [gear_key, gear_notch]


def rotor_setup():
    available_rotors = list(rotor_options.keys())

    selected_rotors = []

    to_choose = 3
    while to_choose > 0:
        print("Select from the following options")
        print(str(available_rotors))
        option = input().upper()

        if option in available_rotors:
            selected_rotors.append(option)
            to_choose += -1
            available_rotors.remove(option)
        else:
            print("Invalid rotor option. Please try again.\n")

    while True:
        print("Input start positions or leave blank for AAA e.g. ABC")
        option = input().upper()
        if not option:
            selected_rotors.append("AAA")
            break

        elif re.match('^[A-Z]{3}$', option):
            selected_rotors.append(option)
            break

        else:
            print("Invalid starting configuration.\n")

    return selected_rotors


def main():
    # Define and create rotors
    selected = rotor_setup()

    rotor_1 = rotor(rotor_options[selected[0]], ord(selected[3][0]) - 65)
    rotor_2 = rotor(rotor_options[selected[1]], ord(selected[3][1]) - 65)
    rotor_3 = rotor(rotor_options[selected[2]], ord(selected[3][2]) - 65)

    plugboard = ""

    myenigma = enigma_machine(rotor_1, rotor_2, rotor_3, plugboard)

    option = input("Menu: 1. Sentence | 2. Character input | 3. Quit : ")

    while True:
        if option == "1":
            ciphertext = ""
            sentence = input("#: ").upper()
            for i in range(0, len(sentence)):
                if sentence[i].isalpha():
                    ciphertext += myenigma.transmute(sentence[i])
                else:
                    ciphertext += sentence[i]

            print(f"Current setting: {myenigma.current_index()}")
            print(f"Encrypted: {ciphertext}")

        elif option == "2":
            character = input("#: ").upper()
            while character != "Q!":
                if re.match('^[A-Z]$', character):
                    cipher = myenigma.transmute(character)
                    print(f"{myenigma.current_index()} | ", end='')
                    print(f"{character} >> {cipher}")
                else:
                    print("Invalid input.")

                character = input("#: ").upper()

        elif option == "3":
            exit()

        else:
            print("Invalid input.\n")

        option = input("Menu: 1. Sentence | 2. Character input | 3. Quit : ")


if __name__ == "__main__":
    import_rotors()
    main()
