class rotor:
    def __init__(self, gear_details, starting_index):
        self.notch = gear_details[1]
        self.index = starting_index
        cipher_key = gear_details[0]

        wiring_dict = {}

        for i in range(0, 26):
            char_key = chr(i + 65)

            # Creates fist_pass key
            comp_value = ord(cipher_key[i]) - 65
            wiring_dict[char_key] = comp_value - i

        self.wiring = wiring_dict
        self.extra = []