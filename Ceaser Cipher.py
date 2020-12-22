import string


# Primary use of function is for MIT problem set in order to decrypt encrypted story.
def load_words(file):
    """
    Will return a list of words from a file.
    Note that the file must be in the same folder or directory on the computer,
    unless otherwise specified
    """
    print("Loading words list from file...")
    in_file = open(file, "r")
    line = in_file.readline()
    word_list = line.split()
    print("{} words loaded".format(len(word_list)))
    in_file.close()
    return word_list


def is_word(word_list, word):
    """
    Determines if a word is valid, ignores capitalization and punctuation
    Will return a boolean on whether or not the word passed in is valid (ie; in the word list)
    """
    word = word.strip(" !@#$%^&*()-_+={}[]|\:;'<>?,./\"").lower()
    return word in word_list


# Primary use of function is to decrypt a text from the MIT problem set
def get_story_string():
    """
    Will return a joke in encrypted text
    """
    file = open("story.txt", "r")
    story = str(file.read())
    file.close()
    return story


class Message:
    def __init__(self, text):
        """
        Initialized the object message
        """
        self.message_text = text
        self.valid_words = load_words("words.txt")

    def get_message_text(self):
        """
        Allows for safe acess of the message outside of the class
        """
        return self.message_text

    def get_valid_words(self):
        """
        Used for safe access to a copy of the words list
        """
        return self.valid_words[:]

    def build_shift_dict(self, shift):
        """
        Will create a dictionary that can be used to apply a cipher to a letter
        that will map for every uppercase and lowercase letter.
        Will return a dictionary mapping one letter to another based on the amount of shift
        """
        # initializes all possible letters
        letters = string.ascii_lowercase + string.ascii_lowercase
        # The shift must be a under 26 so in case a large integer is inputted, it will be divised
        shift = shift % 26
        shiftdict = {}
        for i in range(26):
            # Will iterate for every letter in the alphabet and add both uppercase and lowercase letters to the
            # dictionary along with the corresponding shifted letter
            shiftdict[letters[i]] = letters[i + shift]
            shiftdict[letters[i].upper()] = letters[i + shift].upper()
        return shiftdict

    def apply_shift(self, shift):
        """
        Applies caesar cipher to self.message_text with the input shift.
        Will create a new message that is self.message_text but encypted
        Will return the encrypted message
        """
        # All possible letters in the words that will be shifted
        alpha = string.ascii_lowercase + string.ascii_uppercase
        output = ""
        # Will iterate through the word or phrase
        for letter in self.message_text:
            # If the char is a letter, it will be shifted
            if letter in alpha:
                output += self.build_shift_dict(shift)[letter]
            # If char is not a letter, it will be added to the encrypted message as is with no shift
            else:
                output += letter
        return output


class PlaintextMessage(Message):
    def __init__(self, text, shift):
        """
        Will initialize the plain text object
        """
        Message.__init__(self, text)
        self.shift = shift
        self.encrypting_dict = self.build_shift_dict(shift)
        self.encrypted_message = self.apply_shift(shift)

    def get_shift(self):
        """
        Used for safe access to self.shift from outside of the class
        """
        return self.shift

    def get_encrypting_dict(self):
        """
        Used for safe access to the encrypting dictionary from outside the class
        Will return a copy
        """
        return self.encrypting_dict.copy()

    def get_message_text_encrypted(self):
        """
        Used for safe access to the encrypted message from outside of the class
        """
        return self.encrypted_message

    def change_shift(self, shift):
        """
        Will change the amount of shift within the encrypted message.
        In essence, update the encrypted message with a new shift
        """
        self.shift = shift
        self.encrypting_dict = self.build_shift_dict(shift)
        self.encrypted_message = self.apply_shift(shift)


class CiphertextMessage(Message):
    def __init__(self, text):
        """
        Initializes CiphertestMessage as an object
        """
        Message.__init__(self, text)

    def decrypt_message(self):
        """
        Decrypting the message text will try every possible shift value and in
        essence find the best shift.
        Will return a best shift value for the amount of shift as well as the output
        """
        best_result = 0
        best_shift = 0
        # Will iterate through all possible shifts to find the most correct one
        for s in range(26):
            words = 0
            # Applies shift to the text that is attributed to the CiphertextMessage object
            test = self.apply_shift(s).split(" ")
            # Will ensure the decoded words in the sequence are in fact words
            for word in test:
                if is_word(self.valid_words, word):
                    words += 1
            # Ensures the best result is kept updated in the memory
            if words > best_result:
                best_result = words
                best_shift = s
        # Essentially we are shifting the phrase the rest of the way so that it is once again in plain text
        return self.apply_shift(best_shift)


def decrypt_story():
    return CiphertextMessage(get_story_string()).decrypt_message()


while True:
    # Running a do while loop to ensure the user inputs the correct information
    try:
        choice = input("Do you want to encrypt or decrypt a message, please enter 'encrypt' or 'decrypt'").lower()
        if choice.startswith('e'):
            choice = True
            break
        elif choice.startswith('d'):
            choice = False
            break
        else:
            continue
    except TypeError:
        print("Appears as if you have made a mistake. Try again or do it by hand ")

if choice:
    # If user wants to encrypt will ask them for message and shift amount. Prints encrypted message
    message = str(input("Please enter your message"))
    shift = int(input("Please enter an integer value for the amount of shift you would like for your encrypted message"))
    encrypted = PlaintextMessage(message, shift)
    print(encrypted.get_message_text_encrypted())

elif not choice:
    message = str(input("Please enter the decrypted message. Note there is an algorithm that will find the best shift"))
    decrypted = CiphertextMessage(message)
    print(decrypted.decrypt_message())

else:
    print("Appears as if you have broken my program. Please shoot me a message")
