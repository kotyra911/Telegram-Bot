import os
import uuid
from uuid import UUID
from aiogram.fsm.state import StatesGroup, State
from dotenv import load_dotenv
import logging


lg = logging.getLogger()  # Создание логгера
logging.basicConfig(level=logging.INFO)  # Установка уровня логов

load_dotenv()  # Выгрузка переменных окружения
STICKERS_PATH=os.getenv("STICKERPATH")
PAYLOAD_PATH=os.getenv("PAYLOADPATH")
cringe_video_file_id=os.getenv("BLOCK1CRINGEVIDEO_ID")
jax = os.getenv("JAX")
BLOCK1MATERIALS = os.getenv("BLOCK1MATERIALS")


TOKEN = os.getenv('TOKEN')  # Извлечение токена для ТГ

# Переменные для подключения к бд
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")

BASE_CALL_BACK_DATA = os.getenv("BASECALLBACKDATA")
PRO_CALL_BACK_DATA = os.getenv("PROCALLBACKDATA")


YOOTOKEN = os.getenv("YOOTOKEN")

# Ссылка на базу данных для создания подключения к бд
SQLALCHEMY_DATA_BASE_URL: str = f'postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

stickers = [
    os.getenv("STICKER0"),
    os.getenv("STICKER1"),
    os.getenv("STICKER2"),
    os.getenv("STICKER3"),
    os.getenv("STICKER4"),
    os.getenv("STICKER5"),
]

media = {
    "program":os.getenv("PROGRAM"),
    "hello_vm":os.getenv("HELLO_VC"),
}

block1_media = {
    "lesson1":os.getenv("LESSON"),
    "materials":os.getenv("MATERIAL1BL1"),
    "materials2":os.getenv("MATERIAL2BL1"),
    "chat_link_vm":os.getenv("CHAT_LINK_VM"),
}

block2_media = {
    "sound":os.getenv("SOUND1"),
    "piece1":os.getenv("PIECE1"),
    "piece2":os.getenv("PIECE2"),
    "material":os.getenv("MATERIALBL2"),
    "lesson2":os.getenv("LESSON2"),
}

block3_media = {
    "image1":os.getenv("IMAGE1"),
    "image2":os.getenv("IMAGE2"),
    "lesson3":os.getenv("LESSON3"),
    "materials":[os.getenv("WHITE_BG"),os.getenv("DISK"),
                 os.getenv("FOR_TEXT"),os.getenv("SQUARE"),
                 os.getenv("LIST_BG"),os.getenv("TESLA"),
                 os.getenv("COLOR_CIRCLE"),os.getenv("COLOR_CIRCLE2")]
}


block4_media = {
    "lesson4":os.getenv("LESSON4"),
    "materials":[os.getenv("WHITE4"),os.getenv("ACTOR"),
                 os.getenv("COPY"),os.getenv("CUT"),
                 os.getenv("SOUND"),os.getenv("PINK_DR"),
                 os.getenv("BLUE_DR"), os.getenv("VM_BEFORE5")]
}

block5_media = {
    "shortv":os.getenv("SHORTVID"),
    "lesson5":os.getenv("LESSON5"),
    "materials":[os.getenv("EYES1"),os.getenv("EYES2"),
                 os.getenv("GIRL"),os.getenv("SCARED_MAN"),
                 os.getenv("CAMERA"),os.getenv("LIST_BG4"),
                 os.getenv("CAT"),os.getenv("GLASSES"),
                 os.getenv("MESSAGE"),os.getenv("HEART")]
}



# Состояния для связанного диалога
class DialogStates(StatesGroup):
    waiting_name = State()  # Бот спросил имя и ожидает ответ
    waiting_click = State()
    waiting_confirm_user_agreement = State()  # Бот прислал пользовательское соглашение и ожидает ответ Соглашаюсь
    waiting_confirm_support_info = State()  # Бот ожидает, когда пользователь скажет, "Хорошо, буду иметь в виду"

class MenuStates(StatesGroup):
    main_menu = State()
    my_rate = State()
    my_lessons = State()
    profile = State()
    pro_chapter = State()
    support = State()
    update_rate = State()

class TabsStates(StatesGroup):
    change_name = State()
    after_payment = State()

class FirstBlockStates(StatesGroup):
    waiting_time_for_work = State()
    how_waiting_for_bot = State()
    said_thanks_cap = State()
    cringe_send_or_not = State()
    wait_for_letsgo = State()
    wait_for_understand = State()
    wait_for_looking = State()
    wait_first_chat_video = State()
    wait_review = State()
    last1 = State()

class SecondBlockStates(StatesGroup):
    wait_for_letsgo = State()
    wait_what_sound_answer = State()
    is_it_interesting = State()
    where_is_raiser = State()
    wait_answer_on_small_request = State()
    wait_for_complete_request = State()
    wait_for_watch = State()
    wait_sending_message = State()
    last_block2 = State()

class ThirdBlockStates(StatesGroup):
    state1 = State()
    state2 = State()
    state3 = State()
    state4 = State()
    state5 = State()
    state6 = State()
    state7 = State()
    state8 = State()
    final = State()

class FourthBlockStates(StatesGroup):
    state1 = State()
    state2 = State()
    state3 = State()
    state4 = State()
    final = State()

class FifthBlockStates(StatesGroup):
    state1 = State()
    state2 = State()
    state3 = State()
    state4 = State()
    state5 = State()
    final = State()
    spc_double = State()

# Класс, который является по сути конфигом invoice. Я создал его из удобства и чтобы не нарушать правило DRY
class BaseInvoiceConfig:
    def __init__(self, chat_id: int, payload: str,
                 start_parameter: str, title: str='Курс BASE',
                 description: str='Базовый курс по монтажу в программе CapCut',
                 currency: str='RUB',
                 provider_token: str=YOOTOKEN):

        self.chat_id = chat_id
        self.title = title
        self.description = description
        self.currency = currency
        self.provider_token = provider_token
        self.payload = payload
        self.start_parameter = start_parameter
        self.prices = [{
                "label":"Руб",
                "amount":500000
            }]

# Еще один класс для invoice, только для тарифа PRO
class ProInvoiceConfig:
    def __init__(self, chat_id: int, payload: str, amount: int,
                 start_parameter: str, title: str = 'Курс PRO',
                 description: str = 'PRO Курс по монтажу в программе CapCut',
                 currency: str = 'RUB',
                 provider_token: str = YOOTOKEN):
        self.chat_id = chat_id
        self.title = title
        self.description = description
        self.currency = currency
        self.provider_token = provider_token
        self.payload = payload
        self.start_parameter = start_parameter
        self.prices = [{
            "label": "Руб",
            "amount": amount
        }]

