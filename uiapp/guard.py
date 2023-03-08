import hashlib
import re

error_keys = {
    1: "In name, only english letters are allowed",
    2: 'Special characters (/, \\, ", \', -) are not allowed name and username',
    3: "Passwords do not match",
    4: "Password must be from 8 to 20 characters long"
}


def hashing(psw, psw_rp=""):
    psw = psw.encode() + b"6b5450e51be27571c15011ea41c53c1f"  # salting
    hashed_psw = hashlib.sha512()
    hashed_psw.update(psw)

    return hashed_psw.hexdigest()


def input_test(input_map, if_signin):
    """
    if_signin variable tells the function if it is received SIGN IN or REGISTER input maps
    True -> SIGN IN
    False -> REGISTER
    """

    def name_check(name):
        """
        In First and Second names english letters are only allowed letters
        """
        return 1

    def username_check(username):
        """
        Special characters are restricted
        """
        return 1

    def psw_check(psw, psw_rp):
        """
        Check that passwords follow next rules:
            - Are 8-20 characters long
            - Match

        Then the password is hashed and returned as hex hash
        """
        return 2

    if if_signin:
        # input_map = {
        #             "first_name": "Hello1",
        #             "second_name": "Hello2",
        #             "username": "Hello3",
        #             "psw": "Hello4",
        #             "psw_rp": "Hello5"
        #         }
        input_map['first_name'] = name_check(input_map['first_name'])
        input_map['second_name'] = name_check(input_map['second_name'])
        input_map['username'] = username_check(input_map['username'])

        input_map['psw'] = psw_check(input_map['psw'], input_map['psw_rp'])
        input_map['psw_rp'] = ''

        error_list = []
        for key, value in input_map.items():
            for i in error_keys:
                if value == i:
                    error_list.append(i)

        if len(error_list) != 0:
            error_list = [*set(error_list)]  # Remove duplicate errors just in case

            for i in range(len(error_list)):
                error_list[i] = error_keys[error_list[i]]

            return error_list

        else:
            return input_map

    else:
        return {}
