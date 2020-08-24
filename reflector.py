"""
This class contains details for the reflectors.
Initialisation requires gear_substitution as a string.
"""

class reflector:
    """
    This method initialises the reflector

    Variables:
    name - name of reflector
    gear_substitution - string for substitution
    """

    def __init__(self, name, gear_substitution):
        # Pass pre-defined variables
        self.name = name
        self.substitute = gear_substitution
