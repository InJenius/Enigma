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
        print("\nSelect from the following options")
        print(str(available_rotors))
        option = input().upper()

        # If rotor available, add to selected and remove from available
        if option in available_rotors:
            selected_rotors.append(option)
            to_choose += -1
            available_rotors.remove(option)

        # Check if user wants to exit proram
        elif option == "Q!":
                exit()

        else:
            print("Invalid rotor option. Please try again.")

    # Allow user to input starting position of rotors
    while True:
        print("\nInput start positions or leave blank for AAA e.g. ABC")
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
            print("Invalid starting configuration.")

    # Return three selected rotors and starting position
    return selected_rotors


def plugboard_setup():
    """
    This method is used to ask the user what
    plugboard settings they want to use and
    create and then return a substitution
    alphabet corresponding to the input
    """
    # Set variable outside of loop scope
    plug_settings = {}

    print("\nInput settings for plugboard\nLeave empty for no connection.\nFormat AB-CD-EF")

    while True:
        # Reset values for loop
        errors = False
        plug_settings = generate_alphabet_dic()

        wiring = input('#: ').upper() + '-'

        if wiring == "-":
            print("No connections made.")
            return "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        
        elif wiring == "Q!-":
            exit()

        elif re.match('^([A-Z]{2}-){1,13}$', wiring):
                # Split input into pares
                pairs = wiring.split('-')
                for plugs in pairs:
                    if plugs:
                        plug_one = plugs[0]
                        plug_two = plugs[1]
                        if plug_one == plug_two:
                            print('Invalid config. Plugboard can not connect to itself.\n')
                            errors = True
                            break

                        # Used to check if duplicate pairs
                        if plug_settings[plug_one] == plug_one:
                            plug_settings[plug_one] = plug_two
                        else:
                            print('Invalid config. Plugboard can only have one connection.\n')
                            errors = True
                            break

                        # Used to check if duplicate pairs
                        if plug_settings[plug_two] == plug_two:
                            plug_settings[plug_two] = plug_one
                        else:
                            print('Invalid config. Plugboard can only have one connection.\n')
                            errors = True
                            break

                # If successful, break from loop
                if errors:
                    continue
                else:
                    break
        else:
           print('Invalid config. Format: AB-CD-EF.\n')
    
    plugboard = list(plug_settings.values())
    return ('').join(plugboard)


def generate_alphabet_dic():
    """
    Generate new dictionary with keys
    and values equal to the alphabet 
    in upper case.
    """
    alpha = {}
    for i in range(0, 26):
        char = chr(i + 65)
        alpha[char] = char

    return alpha


def main():
    """
    This method is used to get the settings for machine
    then to initiate it and allow user to input data
    """

    print('To quit at anytime, input Q! (Case-insensitive)')

    # Define and create rotors
    selected = rotor_setup()

    # Create three rotor objects
    rotor_1 = rotor(rotor_options[selected[0]], ord(selected[3][0]) - 65)
    rotor_2 = rotor(rotor_options[selected[1]], ord(selected[3][1]) - 65)
    rotor_3 = rotor(rotor_options[selected[2]], ord(selected[3][2]) - 65)

    # Define plugboard
    plugboard = plugboard_setup()

    # Create enigma_machine object
    myenigma = enigma_machine(rotor_1, rotor_2, rotor_3, plugboard)

    while True:
        # Infine loop to keep asking user
        option = input("Menu: 1. Sentence | 2. Character input | 3. Quit : ")

        # Option 1 does an entire sentence at once
        # Avoids need to wait and ignores non-alphabetic characters
        if option == "1":
            ciphertext = ""
            sentence = input("#: ").upper()

            # Check if user wants to quit
            if sentence == "Q!":
                continue

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


if __name__ == "__main__":
    # Import rotors and start program
    import_rotors()
    main()
