import hashlib
import re


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
        In Name english letters are only allowed letters
        """

        min_length = 2
        max_length = 20
        name = name.strip()
        match = re.fullmatch("^[A-Za-z]*$", name)

        if len(name) > max_length:
            return "Name is too long", 1
        elif len(name) < min_length:
            return "Name is too short", 1
        elif not match:
            return "In name, only english letters are allowed", 1
        else:
            return name, 0

    def username_check(username):
        """
        Special characters are restricted
        """
        min_length = 5
        max_length = 20
        username = username.strip()
        restricted_chars = ['/', '\\', '\'', '"']

        for char in username:
            for i in restricted_chars:
                if char == i:
                    return "Special characters('/', '\\', '\'', '\"') are restricted", 1

        if len(username) > max_length or len(username) < min_length:
            return format(f"Username must be from {min_length} to {max_length} characters long"), 1

        return username, 0

    def psw_check(psw):
        """
        Check that passwords follow next rules:
            - Are 8-20 characters long
        Then the password is hashed and returned as hex hash
        """
        return "psw: debug error", 1

    if if_signin:
        """
        Explanation of next For loop:
        
        
        """
        error_list = []
        for key, value in input_map.items():
            if key == 'first_name' or key == 'second_name':
                function_output, error = name_check(input_map[key])
            elif key == 'username':
                function_output, error = username_check(input_map[key])
            elif key == 'psw' or key == 'psw_rp':
                function_output, error = psw_check(input_map[key])
            else:
                return [None, None]

            if error:
                error_list.append(function_output)
                input_map[key] = ''
                continue
            input_map[key] = function_output

        if len(error_list) != 0:
            error_list = [*set(error_list)]
            return [input_map, error_list]

        else:
            return [input_map, None]

    else:
        return {}
