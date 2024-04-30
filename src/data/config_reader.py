from dotenv import load_dotenv 
import os
from os. path import join, dirname

def get_from_env (key):
    dotenv_path = join(dirname(__file__), 'token.env')
    load_dotenv(dotenv_path)
    return os.environ. get(key)

# Необходимые двнные
bot_token = get_from_env('BOT_TOKEN')
drivername = get_from_env('DRIVENAME')
username = get_from_env('DB_USERNAME')
password = get_from_env('DB_PASSWRD')
database = get_from_env('DB')
host = get_from_env('HOST')
port = get_from_env('PORT')

# Тут могут быть ваши данные
admin_id = int(get_from_env('ADMINS_ID'))
code_word_601_21 = get_from_env('CODE_WORD_60121')
code_word_601_31 = get_from_env('CODE_WORD_60131')
code_word_603_31 = get_from_env('CODE_WORD_60331')

list_code_word = (code_word_601_21, code_word_601_31, code_word_603_31)
code_words = {
    '1': code_word_601_21,
    '2': code_word_601_31,
    '3': code_word_603_31
}

