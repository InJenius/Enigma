class enigma_machine:
    def __init__(self, slow_rotor, normal_rotor, fast_rotor, plugboard):
        self.slow_rotor = slow_rotor
        self.normal_rotor = normal_rotor
        self.fast_rotor = fast_rotor
        self.reflector = "YRUHQSLDPXNGOKMIEBFZCWVJAT"
        self.plugboard = plugboard

    def substitute(self, value, char):
        char_index = ord(char) - 65
        return value[char_index]

    def rotor_substitute(self, first_pass, rotor, char):
        if first_pass:
            conversion = []

            for alpha_index in range(0, 26):
                retrieve = (alpha_index + rotor.index) % 26
                current_wire = rotor.wiring[chr(retrieve + 65)]
                adjustment = current_wire + alpha_index

                if adjustment > 0:
                    adjustment = adjustment % 26

                if adjustment + 65 < 65:
                    adjustment += 26

                conversion.append(chr(65 + adjustment))

            rotor.extra = conversion

            return conversion[ord(char)-65]

        else:
            chr_location = rotor.extra.index(char)

            return chr(chr_location + 65)

    def rotor_update(self):
        self.fast_rotor.index += 1

        # Normal rotor
        if self.normal_rotor.index == ord(self.normal_rotor.notch) - 65:
            self.normal_rotor.index += 1
            self.slow_rotor.index += 1
        elif self.normal_rotor.index == 26:
            self.normal_rotor.index = 0

        # Fast rotor
        if self.fast_rotor.index == ord(self.fast_rotor.notch) - 64:
            self.normal_rotor.index += 1
        elif self.fast_rotor.index == 26:
            self.fast_rotor.index = 0

        # Slow rotor
        if self.slow_rotor.index == 26:
            self.slow_rotor.index = 0

    def rotor_adjust(self, rotor, rotor_to_accelerate):
        if rotor.notch == '-':
            print('ok')
            # Call double check
        else:
            if rotor.index == ord(rotor.notch) - 64:
                rotor_to_accelerate.index += 1
            elif rotor.index == 26:
                rotor.index = 0

    def transmute(self, character):
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
        index = chr(self.slow_rotor.index + 65)
        index += chr(self.normal_rotor.index + 65)
        index += chr(self.fast_rotor.index + 65)

        return index