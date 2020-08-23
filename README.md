Autotest - Instant Programming contest framework
===============================

This project is used for creating fully automated programming contests

It has 5 roles
1. Superuser: it is like a root user, super user can do following actions.
    1. Create contest
    2. Delete contest
    3. create test admins
    4. create test creators
2. Test Creator: this role can select questions for context from existing questions.
3. Test Admins: This role can do following actions
    1. start contest
    2. stop contest
    3. see leader board
4. Students: This role can do following actions
    1. view questions
    2. submit answers
    3. see result of submissions

### System Requirements:
  1. python 2.7.16 :If you don't have python 2.7 as default, install pyenv and then install pyton 2.7
https://realpython.com/intro-to-pyenv/#installing-pyenv
  2. Mongodb
  3. AWS

### Local setup:
1. Create virtual environment
    ```shell script
    virutalenv venv -p `which python`
    source venv/bin/activate
    ```
2. Install Requirements
    ```shell script
    pip install -r requirements.txt
    ```
3. Run django server
    ```shell script
   cd webui
   python manage.py runserver
    ```

### Limitations
In local you can test the following roles
1. Super user
2. Test Creator

Test Admin:To Start the contest you need AWS setup.