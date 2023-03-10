from django.test import TestCase

from uiapp.guard import NAME_MIN_LENGTH, NAME_MAX_LENGTH
from uiapp.guard import USERNAME_MIN_LENGTH, USERNAME_MAX_LENGTH
from uiapp.guard import PASSWORD_MIN_LENGTH, PASSWORD_MAX_LENGTH


def create_register_input_map(first_name="", second_name="", username="", psw="", psw_rp=""):
    input_map = {
        "first_name": first_name,
        "second_name": second_name,
        "username": username,
        "psw": psw,
        "psw_rp": psw_rp  # psw_rp means password repeat
    }
    return input_map


class GuardTest(TestCase):
    def test_register_special_characters_name(self):
        input_map = create_register_input_map("Andrei", "Lopatov\\", "andlop", "andrei_1234", "andrei_1234")

        response = self.client.post('/register/', input_map)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "In name, only english letters are allowed")
        self.assertQuerysetEqual(response.context['error_list'], ["In name, only english letters are allowed"])

    def test_register_special_characters_username(self):
        input_map1 = create_register_input_map("Andrei", "Lopatov", "andlop\\", "andrei_1234", "andrei_1234")
        input_map2 = create_register_input_map("Andrei", "Lopatov", "andlop\"", "andrei_1234", "andrei_1234")
        input_map3 = create_register_input_map("Andrei", "Lopatov", "andlop/", "andrei_1234", "andrei_1234")
        input_map4 = create_register_input_map("Andrei", "Lopatov", "andlop\'", "andrei_1234", "andrei_1234")

        response1 = self.client.post('/register/', input_map1)
        response2 = self.client.post('/register/', input_map2)
        response3 = self.client.post('/register/', input_map3)
        response4 = self.client.post('/register/', input_map4)

        self.assertEqual(response1.status_code, 200)
        self.assertEqual(response2.status_code, 200)
        self.assertEqual(response3.status_code, 200)
        self.assertEqual(response4.status_code, 200)

        self.assertQuerysetEqual(response1.context['error_list'],
                                 ["Special characters('/', '\\', '\'', '\"') are restricted"])
        self.assertQuerysetEqual(response2.context['error_list'],
                                 ["Special characters('/', '\\', '\'', '\"') are restricted"])
        self.assertQuerysetEqual(response3.context['error_list'],
                                 ["Special characters('/', '\\', '\'', '\"') are restricted"])
        self.assertQuerysetEqual(response4.context['error_list'],
                                 ["Special characters('/', '\\', '\'', '\"') are restricted"])

    def test_register_passwords_match(self):
        input_map = create_register_input_map("Andrei", "Lopatov", "andlop", "andrei_123", "andrei_1234")
        response = self.client.post('/register/', input_map)
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['error_list'], ["Passwords do not match"])

    def test_length_name(self):
        # Short
        test_string = ""
        for i in range(NAME_MIN_LENGTH - 1):
            test_string += "a"

        input_map_short = create_register_input_map(test_string, "Lopatov", "andlop", "andrei_1234", "andrei_1234")
        response_short = self.client.post('/register/', input_map_short)

        self.assertEqual(response_short.status_code, 200)
        self.assertQuerysetEqual(response_short.context['error_list'],
                                 [f"Name must be from {NAME_MIN_LENGTH} to {NAME_MAX_LENGTH} characters long each"])

        # Long
        test_string = ""
        for i in range(NAME_MAX_LENGTH + 1):
            test_string += "a"

        input_map_long = create_register_input_map("Andrei", test_string, "andlop",
                                                   "andrei_1234", "andrei_1234")
        response_long = self.client.post('/register/', input_map_long)

        self.assertEqual(response_long.status_code, 200)
        self.assertQuerysetEqual(response_long.context['error_list'],
                                 [f"Name must be from {NAME_MIN_LENGTH} to {NAME_MAX_LENGTH} characters long each"])

    def test_length_username(self):
        # Short
        test_string = ""
        for i in range(USERNAME_MIN_LENGTH - 1):
            test_string += "a"

        input_map_short = create_register_input_map("Andrei", "Lopatov", test_string, "andrei_1234", "andrei_1234")
        response_short = self.client.post('/register/', input_map_short)

        self.assertEqual(response_short.status_code, 200)
        self.assertQuerysetEqual(response_short.context['error_list'],
                                 [
                                     f"Username must be from {USERNAME_MIN_LENGTH} to {USERNAME_MAX_LENGTH} characters long"])

        # Long
        test_string = ""
        for i in range(USERNAME_MAX_LENGTH + 1):
            test_string += "a"

        input_map_long = create_register_input_map("Andrei", "Lopatov",
                                                   test_string, "andrei_1234", "andrei_1234")
        response_long = self.client.post('/register/', input_map_long)

        self.assertEqual(response_long.status_code, 200)
        self.assertQuerysetEqual(response_long.context['error_list'],
                                 [
                                     f"Username must be from {USERNAME_MIN_LENGTH} to {USERNAME_MAX_LENGTH} characters long"])

    def test_length_password(self):
        # Short
        test_string = ""
        for i in range(PASSWORD_MIN_LENGTH - 1):
            test_string += "a"

        input_map_short = create_register_input_map("Andrei", "Lopatov", "andlop", test_string, test_string)
        response_short = self.client.post('/register/', input_map_short)

        self.assertEqual(response_short.status_code, 200)
        self.assertQuerysetEqual(response_short.context['error_list'],
                                 [
                                     f"Password must be from {PASSWORD_MIN_LENGTH} to {PASSWORD_MAX_LENGTH} characters"])

        # Long
        test_string = ""
        for i in range(PASSWORD_MAX_LENGTH + 1):
            test_string += "a"

        input_map_long = create_register_input_map("Andrei", "Lopatov",
                                                   "andlop", test_string, test_string)
        response_long = self.client.post('/register/', input_map_long)

        self.assertEqual(response_long.status_code, 200)
        self.assertQuerysetEqual(response_long.context['error_list'],
                                 [
                                     f"Password must be from {PASSWORD_MIN_LENGTH} to {PASSWORD_MAX_LENGTH} characters"])
