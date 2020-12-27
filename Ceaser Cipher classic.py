import string


class Message:
    def __init__(self, text, shift):
        """
        Initializing the message as an object, text and shift is being passed in
        """
        self.message = text
        self.shift = shift

    def get_text(self):
        """
        Will allow for safe access of the message that has been inputted
        """
        return self.message

    def build_shift_dict(self, shift):
        """
        Will create a dictionary that will be used to apply the cipher to a letter
        Will return a dictionary with a shifted letter being mapped to each letter based on desired shift
        """
        # Initialize all the possible letters
        letters = string.ascii_letters
        shift = shift % 26
        shift_dict = {}
        for i in range(26):
            # Will iterate over all possible letters both uppercase and lowercase and create the mapping in the dict
            shift_dict[letters[i].lower()] = letters[i+shift].lower()
            shift_dict[letters[i].upper()] = letters[i+shift].upper()
        return shift_dict

    def encrypt_message(self):
        """
        Will encrypt the message based on the desired shift
        """
        # Will list all the possible words
        letters = string.ascii_uppercase + string.ascii_lowercase
        output = ""
        shifted_letters = self.build_shift_dict(self.shift)
        # Will iterate over the words in the phrase
        for letter in self.message:

            if letter in letters:
                output += shifted_letters[letter]
            # If the character is not a letter, it will not be shifted just added
            else:
                output += letter
        return output

    def decrypt_message(self):
        """
        Will decrypt an encrypted message
        """
        # All possible letters:
        letters = string.ascii_uppercase + string.ascii_lowercase
        output = ""
        de_shift = 26 - self.shift
        shifted_letters = self.build_shift_dict(de_shift)
        # Will iterate over all letters in the shifted message and apply shift
        for letter in self.message:
            if letter in letters:
                output += shifted_letters[letter]
            # If character in message is not a letter
            else:
                output += letter
        return output

    def get_encrypted(self):
        """
        Will return the encrypted message
        """
        return self.encrypt_message()

    def get_decrypted(self):
        """
        Will return the decrypted message
        """
        return self.decrypt_message()


while True:
    # Runs while loop in order to gain correct user information on decrypt on encrypt
    try:
        choice = input("Do you want to encrypt or decrypt a message? Please enter 'encrypt' or 'decrypt'").lower()
        if choice.startswith('e'):
            choice = True
            break
        elif choice.startswith('d'):
            choice = False
            break
        else:
            continue
    except:
        print("Appears as if you made a mistake. Try again or solve your issue by hand")

if choice:
    # Encrypt has been chosen. Will ask for message and amount of shift
    message = str(input("Please enter your message"))
    shift = int(input("Please enter the amount of shift you would like:"))
    # Creates instance of Message with the text and amount of shift
    encrypted = Message(message,shift)
    # Prints the encrypted text
    print(encrypted.get_encrypted())

elif not choice:
    # Asks for encrypted message and amount of shift applied
    message = str(input("Pleas enter the encrypted message"))
    shift = int(input("Please enter the amount of shift applied on the text"))
    # Creates and instance of Message with the encrypted message and amount of shift
    decrypted = Message(message, shift)
    # Will print the decrypted message
    print(decrypted.get_decrypted())
else:
    print("Congratulations, you have broken my program")

