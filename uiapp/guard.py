import re

NAME_MIN_LENGTH = 2
NAME_MAX_LENGTH = 20

USERNAME_MIN_LENGTH = 5
USERNAME_MAX_LENGTH = 20

PASSWORD_MIN_LENGTH = 8
PASSWORD_MAX_LENGTH = 20


def input_test(input_map, case):
    def name_check(name):
        """
        In Name english letters are only allowed characters
        """

        name = name.strip()
        match = re.fullmatch("^[A-Za-z]*$", name)

        if len(name) < NAME_MIN_LENGTH or len(name) > NAME_MAX_LENGTH:
            return f"Name must be from {NAME_MIN_LENGTH} to {NAME_MAX_LENGTH} characters long each", 1
        elif not match:
            return "In name, only english letters are allowed", 1
        else:
            return name, 0

    def username_check(username):
        """
        Special characters are restricted
        """

        username = username.strip()
        restricted_chars = ['/', '\\', '\'', '"']

        for char in username:
            for i in restricted_chars:
                if char == i:
                    return "Special characters('/', '\\', '\'', '\"') are restricted", 1

        if len(username) < USERNAME_MIN_LENGTH or len(username) > USERNAME_MAX_LENGTH:
            return format(f"Username must be from {USERNAME_MIN_LENGTH} to {USERNAME_MAX_LENGTH} characters long"), 1

        return username, 0

    def psw_check(psw):
        """
        Check that passwords follow next rules:
            - Are PASSWORD_MIN_LENGTH to PASSWORD_MAX_LENGTH characters long
        Then the password is hashed and returned as a hex hash
        """

        if len(psw) < PASSWORD_MIN_LENGTH or len(psw) > PASSWORD_MAX_LENGTH:
            return f"Password must be from {PASSWORD_MIN_LENGTH} to {PASSWORD_MAX_LENGTH} characters", 1
        else:
            return psw, 0

    if case == 'LOGIN':
        input_map['username'], error = username_check(input_map['username'])
        if error:
            return [None, [error]]
        return [input_map, None]

    elif case == 'REGISTER':
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
                continue
            input_map[key] = function_output

        if input_map['psw'] != input_map['psw_rp']:
            error_list.append('Passwords do not match')

        if len(error_list) != 0:
            error_list = [*set(error_list)]
            return [None, error_list]

        else:
            return [input_map, None]

    else:
        return [None, None]
