"""
This class contains details for the rotors.
Initialisation requires gear_details, an array.
Array structure:
0: substitution cipher for gear to resemble default wiring
1: notch location on gear
Initialisation also requires starting index as character
"""

class rotor:
    """
    This method initialises the rotor and all its variables for
    functionality

    Variables:
    gear_details - array of 2 items
        0 - Substitution cipher alphabet for gear for default wiring
        1 - Location of notch on gear
    starting_index - Integer that represents char of rotor's
                     current position
    """
    def __init__(self, gear_details, starting_index):
        # Pass pre-defined variables
        self.notch = gear_details[1]
        self.index = starting_index

        # Declare tempororary variables
        cipher_key = gear_details[0]
        wiring_dict = {}

        for i in range(0, 26):
            char_key = chr(i + 65)

            # Creates wiring for rotor
            comp_value = ord(cipher_key[i]) - 65
            wiring_dict[char_key] = comp_value - i

        # Declares wiring property of gear and presets extra variable
        # Extra contains gear's current reverse alphabet for substitution
        self.wiring = wiring_dict
        self.extra = []
