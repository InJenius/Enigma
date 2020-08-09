"""
This class contains details for the enigma machine.
Initialisation requires three rotors & substitution for the plugboard.
"""


class enigma_machine:
    def __init__(self, slow_rotor, normal_rotor, fast_rotor, plugboard):
        """
        This method initialises the machine and all its variables for
        functionality
        Variables:
        slow/normal/fast rotor - Three individual rotor objects
        reflector - Substitution alphabet for reflector, currently locked
        plugboard - Substitution alphabet for plugboard
        """
        self.slow_rotor = slow_rotor
        self.normal_rotor = normal_rotor
        self.fast_rotor = fast_rotor
        self.reflector = "YRUHQSLDPXNGOKMIEBFZCWVJAT"
        self.plugboard = plugboard

        # Generate initial conversion tables
        self.generate_conversion_map(self.fast_rotor)
        self.generate_conversion_map(self.normal_rotor)
        self.generate_conversion_map(self.slow_rotor)

    def substitute(self, value, char):
        """
        Substitute a single character from a passed alphabet.
        value - 26 character alphabet
        char - Character to substitute
        """
        char_index = ord(char) - 65
        return value[char_index]

    def rotor_substitute(self, first_pass, rotor, char):
        """
        Substitute for input of rotor that looks at both directions
        first_pass - Boolean variable
        rotor - Rotor object to look at
        char - Character to change
        """

        if first_pass:
            # Return character passed through rotor wiring
            return rotor.extra[ord(char)-65]

        else:
            # Get index of character in list
            chr_location = rotor.extra.index(char)

            # Return new character
            return chr(chr_location + 65)

    def rotor_update(self):
        """
        Moves rotor positions along as more keys are pressed
        """

        # Moves after every key press
        self.fast_rotor.index += 1
        self.generate_conversion_map(self.fast_rotor)

        # Normal rotor
        # Moves slow rotor after hitting notch
        # Contains double step to move an extra element
        if self.normal_rotor.index == ord(self.normal_rotor.notch) - 65:
            self.normal_rotor.index += 1
            self.slow_rotor.index += 1
            self.generate_conversion_map(self.normal_rotor)
        elif self.normal_rotor.index == 26:
            self.normal_rotor.index = 0
            self.generate_conversion_map(self.slow_rotor)

        # Fast rotor
        # Moves normal rotor after hitting notch
        if self.fast_rotor.index == ord(self.fast_rotor.notch) - 64:
            self.normal_rotor.index += 1
        elif self.fast_rotor.index == 26:
            self.fast_rotor.index = 0

        # Slow rotor
        # Does not move rotors, simply resets
        if self.slow_rotor.index == 26:
            self.slow_rotor.index = 0

    def transmute(self, character):
        """
        Function to run through all steps of enigma and return new character
        character - Plaintext character to convert
        """

        # Increment and update rotor configurations
        self.rotor_update()

        # Plugboard transmition
        if self.plugboard:
            character = self.substitute(self.plugboard, character)

        # Gear transmition | < | < |
        character = self.rotor_substitute(True, self.fast_rotor, character)
        character = self.rotor_substitute(True, self.normal_rotor, character)
        character = self.rotor_substitute(True, self.slow_rotor, character)

        # Reflector transmition
        character = self.substitute(self.reflector, character)

        # Gear transmition | > | > |
        character = self.rotor_substitute(False, self.slow_rotor, character)
        character = self.rotor_substitute(False, self.normal_rotor, character)
        character = self.rotor_substitute(False, self.fast_rotor, character)

        # Reverse plugboard transmition
        if self.plugboard:
            character = self.substitute(self.plugboard, character)

        return character

    def current_index(self):
        """
        Gets current index of all rotors in alphabetical form
        """

        index = chr(self.slow_rotor.index + 65)
        index += chr(self.normal_rotor.index + 65)
        index += chr(self.fast_rotor.index + 65)

        return index

    def generate_conversion_map(self, rotor):
        """
        Used to generate mapping for rotor's current wiring
        Allows for mapping to be done from either direction.
        Function is only called when a rotor updates to increase
        efficiency.
        """
        conversion = []

        # Loops through all letters of alphabet
        for alpha_index in range(0, 26):
            # Get position of key relative to rotor's position
            retrieve = (alpha_index + rotor.index) % 26
            # Get wiring (shift) of rotor at that position
            current_wire = rotor.wiring[chr(retrieve + 65)]

            # Calculate what character is created
            adjustment = current_wire + alpha_index

            # Checks to make sure character is within limits of 0-26
            if adjustment > 0:
                adjustment = adjustment % 26

            # Second error check if previous character was negative
            if adjustment + 65 < 65:
                adjustment += 26

            # Add to array
            conversion.append(chr(65 + adjustment))

        rotor.extra = conversion
