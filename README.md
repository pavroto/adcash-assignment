# Adcash assignment

### General information:

---
Author: Pavel Rotov

IDE: PyCharm

Language: Python

Framework: Django

### Launching

---
```shell
git clone git@github.com:BambuChan/adcash-assignment.git

cd adcash-assignment 

python manage.py runserver --insecure
```

NB! --insecure parameter is not necessary if you do not care about static CSS file

### External

---
This project uses rest framework, so if needed, use next  command:
```shell
pip install djangorestframework
```

### Default users:

---
| Login        | Password     | if_superuser |
|--------------|--------------|--------------|
| admin        | Admin1234    | True         |
| blocked_user | Blocked_1234 | False        |

### Blocking users:

---
To add users to the black list go to ***127.0.0.1:8000/admin*** page, login as admin and open "BlackLists" 

###  Ui app

---

***127.0.0.1:8000/*** leads to the menu with registration or sign in options.

For new users it is needed to registrate to access their api token on ***Profile*** page.

It is also available to list all the loans and apply for new ones through the ***Profile*** page

### Api  app

---

Api is available through the ***127.0.0.1:8000/api/*** and  ***127.0.0.1:8000/api/apply*** links

***127.0.0.1:8000/api/*** lists all loans of AUTHENTICATED user. It accepts only GET request with authorization and/or session
token

***127.0.0.1:8000/api/apply*** accepts only POST request with authorization token in header and next form-data:

    - first_name    must be a string
    - second_name   must be a string
    - amount        must be a float. Server rounds it using round(amount, 2) function
    - term          must be an int. Term is calculated in FULL MONTHS using 30*term formula

Due to the fact, that user already uses authorization token, personal_id is not used.


After submitting, debt is calculated using next function:
```python
MONTHLY_INTEREST = 5

def monthly_interest_calculation(amount, months):
    debt = amount * ((1 + MONTHLY_INTEREST / 100) ** months)
    return round(debt, 2)
```

For additional information about data validation and processing, go to ***uiapp/guard.py***


README v2.0