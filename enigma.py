import re
from enigma_machine import enigma_machine
from rotor import rotor

# Set rotor options variable for global usage
rotor_options = {}


def import_rotors():
    """
    This method reads rotors file and initialises
    all rotors into program
    """

    # Get all lines of file
    file_lines = open('rotor_details.txt', 'r').read().splitlines()

    for i in range(0, len(file_lines)):
        # Check if meant to read line of file
        if file_lines[i][0] != ('#'):
            # If so, split via '|'
            data_line = file_lines[i].split('|')
            # Convert data to variables
            gear_name = data_line[0]
            gear_key = data_line[1]
            gear_notch = data_line[2]

            # Add to existing dictionary
            rotor_options[gear_name] = [gear_key, gear_notch]


def rotor_setup():
    """
    This method is used to ask the user what
    rotors they want to use and return the selected
    rotors and starting position of the rotors.
    """

    # Get all available rotors
    available_rotors = list(rotor_options.keys())

    # Preset  array for selected rotors
    selected_rotors = []

    # Allow maximum of three to be selected
    to_choose = 3
    while to_choose > 0:
        print("Select from the following options")
        print(str(available_rotors))
        option = input().upper()

        # If rotor available, add to selected and remove from available
        if option in available_rotors:
            selected_rotors.append(option)
            to_choose += -1
            available_rotors.remove(option)

        # Check if user wants to exit proram
        if option == "Q!":
                exit()

        else:
            print("Invalid rotor option. Please try again.\n")

    # Allow user to input starting position of rotors
    while True:
        print("Input start positions or leave blank for AAA e.g. ABC")
        option = input().upper()

        # Set default value
        if not option:
            selected_rotors.append("AAA")
            break

        elif option == "Q!":
                exit()

        # Check if input is valid via regex and add to array
        elif re.match('^[A-Z]{3}$', option):
            selected_rotors.append(option)
            break

        else:
            print("Invalid starting configuration.\n")

    # Return three selected rotors and starting position
    return selected_rotors


def main():
    """
    This method is used to get the settings for machine
    then to initiate it and allow user to input data
    """
    # Define and create rotors
    selected = rotor_setup()

    # Create three rotor objects
    rotor_1 = rotor(rotor_options[selected[0]], ord(selected[3][0]) - 65)
    rotor_2 = rotor(rotor_options[selected[1]], ord(selected[3][1]) - 65)
    rotor_3 = rotor(rotor_options[selected[2]], ord(selected[3][2]) - 65)

    # Define plugboard
    # Currently not implemented
    plugboard = ""

    # Create enigma_machine object
    myenigma = enigma_machine(rotor_1, rotor_2, rotor_3, plugboard)

    # Allow user to select from options
    option = input("Menu: 1. Sentence | 2. Character input | 3. Quit : ")

    while True:
        # Option 1 does an entire sentence at once
        # Avoids need to wait and ignores non-alphabetic characters
        if option == "1":
            ciphertext = ""
            sentence = input("#: ").upper()

            # Check if user wants to quit
            if sentence == "Q!":
                exit()

            # Check if each char is alphabetic and transmute if it is
            for i in range(0, len(sentence)):
                if sentence[i].isalpha():
                    ciphertext += myenigma.transmute(sentence[i])

                else:
                    ciphertext += sentence[i]

            # Print output and current enigma settings
            print(f"Current setting: {myenigma.current_index()}")
            print(f"Encrypted: {ciphertext}")

        # Option 2 is traditional
        # Input one char and get one char back
        elif option == "2":
            character = input("#: ").upper()
            while character != "Q!":
                # Check input is single character
                if re.match('^[A-Z]$', character):
                    # Transmute and return output with current rotor positions
                    cipher = myenigma.transmute(character)
                    print(f"{myenigma.current_index()} | ", end='')
                    print(f"{character} >> {cipher}")
                else:
                    print("Invalid input.")

                character = input("#: ").upper()

        # Option 3 quits program
        elif option == "3":
            exit()

        else:
            print("Invalid input.\n")

        # Infine loop to keep asking user
        option = input("Menu: 1. Sentence | 2. Character input | 3. Quit : ")


if __name__ == "__main__":
    # Import rotors and start program
    import_rotors()
    main()
