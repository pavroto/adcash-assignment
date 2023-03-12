import re
import datetime
from .models import Loan, BlackList

NAME_MIN_LENGTH = 2
NAME_MAX_LENGTH = 20

USERNAME_MIN_LENGTH = 5
USERNAME_MAX_LENGTH = 20

PASSWORD_MIN_LENGTH = 8
PASSWORD_MAX_LENGTH = 20

APPLY_MIN_AMOUNT = 1000
APPLY_MAX_AMOUNT = 100000

APPLY_MIN_MONTHS = 6
APPLY_MAX_MONTHS = 120

APPLY_DAILY_LIMIT = 2

MONTHLY_INTEREST = 5  # in percent


def monthly_interest_calculation(amount, months):
    debt = amount * ((1 + MONTHLY_INTEREST / 100) ** months)
    return round(debt, 2)


def input_test(input_map, case, request=None):
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

    def amount_check(amount):

        if type(amount) != float:
            return "Invalid amount input", 1

        if amount < APPLY_MIN_AMOUNT or amount > APPLY_MAX_AMOUNT:
            return f"Amount can  be from {APPLY_MIN_AMOUNT} to {APPLY_MAX_AMOUNT} euro", 1

        return round(amount, 2), 0

    def term_check(term):
        if type(term) != int:
            return "Invalid term input", 1

        if term < APPLY_MIN_MONTHS or term > APPLY_MAX_MONTHS:
            return f"Term can be from {APPLY_MIN_MONTHS} to {APPLY_MAX_MONTHS} months", 1

        return term, 0

    ################################################################################################

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

    elif case == 'APPLY':
        error_list = []

        input_map['first_name'], error = name_check(input_map['first_name'])
        if error:
            error_list.append(input_map['first_name'])

        input_map['second_name'], error = name_check(input_map['second_name'])
        if error:
            error_list.append(input_map['second_name'])

        input_map['amount'], error = amount_check(input_map['amount'])
        if error:
            error_list.append(input_map['amount'])

        input_map['term'], error = term_check(input_map['term'])
        if error:
            error_list.append(input_map['term'])

        if input_map['first_name'] + " " + input_map['second_name'] != request.user.get_full_name():
            error_list.append("This name does not correspond this user")

        today_user_loans = Loan.objects.filter(user=request.user).all()
        i = 0
        for loan in today_user_loans:
            if loan.get_timestamp().date() == datetime.date.today():
                i += 1
            if i >= APPLY_DAILY_LIMIT:
                error_list.append("You reached the limit for today.")
                break

        blocked_user = BlackList.objects.filter(user=request.user).get()
        if blocked_user:
            error_list.append(f"You are black listed. Comment: {blocked_user.comment}")

        if len(error_list) != 0:
            error_list = [*set(error_list)]
            return [None, error_list]
        else:
            return [input_map, None]

    else:
        return [None, None]
