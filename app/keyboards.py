from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from config import BASE_CALL_BACK_DATA, PRO_CALL_BACK_DATA



# Клавиатура с подпиской
sub_button_inline_keyboard_free = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='BASE - 5000 рублей', callback_data=BASE_CALL_BACK_DATA)
        ],
        [
            InlineKeyboardButton(text='PRO - 8000 рублей', callback_data=PRO_CALL_BACK_DATA)
        ]
    ]
)
# Клавиатура с подпиской
sub_button_inline_keyboard_base = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='PRO - 3000 рублей', callback_data=PRO_CALL_BACK_DATA)
        ]
    ]
)

menu_button = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='/menu')]
    ],
    resize_keyboard=True
)



bl3_start_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Ну… я просто ставлю текст куда влезет 😅'), KeyboardButton(text='Понимаю, что важно, но не знаю как правильно :(')],
        [KeyboardButton(text='Конечно, я же эстет ✨'), KeyboardButton(text='Назад')]
    ],
    resize_keyboard=True
)

bl3_2_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Ничего, все отлично')],
        [KeyboardButton(text='Что-то не так, но не понимаю что')],
        [KeyboardButton(text='Возможно сильно пусто?')]
    ],
    resize_keyboard=True
)
bl3_3_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Да!')]
    ],
    resize_keyboard=True
)
bl3_4_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Супер, погнали!')],
        [KeyboardButton(text='Летс гооооооооу')]
    ],
    resize_keyboard=True
)
bl3_5_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Посмотрел/а ✅')]
    ],
    resize_keyboard=True
)
bl3_6_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Дз уже в чате :)')]
    ],
    resize_keyboard=True
)
bl3_7_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Спасибо, Маша, реально узнал/а что-то новое 🔥')],
        [KeyboardButton(text='Информация годная, но я уже все знаю 😅')]
    ],
    resize_keyboard=True
)
bl3_8_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Я, пожалуй, пойду отдыхать 😴')],
        [KeyboardButton(text='Хочу дальше, но надо работать 🫠')],
        [KeyboardButton(text='Погнали дальше 🚀')]
    ],
    resize_keyboard=True
)

bl3_9_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Главное меню'), KeyboardButton(text='Блок 4')]
    ],
    resize_keyboard=True
)

bl4_1_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Быстрые склейки'), KeyboardButton(text='Движение камеры')],
        [KeyboardButton(text='Текст в разных частях экрана'),KeyboardButton(text='Назад')],
    ],
    resize_keyboard=True
)

bl4_2_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Я в предвкушении!')],
        [KeyboardButton(text='Настрой лучше всех!')],
        [KeyboardButton(text='Чуть-чуть волнуюсь')]
    ],
    resize_keyboard=True
)

bl4_3_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Маша, я посмотрел/а!')]
    ],
    resize_keyboard=True
)

bl4_4_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Это круто, спасибо, все буду использовать 🔥')],
        [KeyboardButton(text='Взглянул/а на все по-новому')],
        [KeyboardButton(text='Соу-соу')]
    ],
    resize_keyboard=True
)

bl4_5_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Дз уже готово 🫡')]
    ],
    resize_keyboard=True
)

bl4_6_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Главное меню'), KeyboardButton(text='Блок 5')]
    ],
    resize_keyboard=True
)

bl5_1_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Рваная склейка ✂️'), KeyboardButton(text='Плоское видео 🙊')],
        [KeyboardButton(text='Резкие переходы и анимации 😶‍🌫'), KeyboardButton(text='Назад')],
    ],
    resize_keyboard=True
)

bl5_2_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='ДАДАДАДА')],
        [KeyboardButton(text='Что там? 👀')]
    ],
    resize_keyboard=True
)

bl5_3_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Да, пожалуйста 🙏')],
        [KeyboardButton(text='Нет, погнали скорее к уроку 🔥')]
    ],
    resize_keyboard=True
)

bl5_4_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Посмотрел/а ✅')]
    ],
    resize_keyboard=True
)
bl5_tutorial_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Можем переходить к уроку!')]
    ],
    resize_keyboard=True
)
bl5_5_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Значит, это все?🥲')]
    ],
    resize_keyboard=True
)
bl5_6_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Главное меню')]
    ],
    resize_keyboard=True
)




cringe_send_or_not_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Отправляй, отправляй 🤪'), KeyboardButton(text='Я спасу тебя от стыда, не отправляй 😇')]
    ],
    resize_keyboard=True
)

after_cringe_what_start = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Склейка ✂️')],
        [KeyboardButton(text='Цветокор 🎨')],
        [KeyboardButton(text='Масштабы 📏')],
    ],
    resize_keyboard=True
)

block1_letsgo_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Погнали!')],
        [KeyboardButton(text='Нет, мне страшно, у меня не получится…')]
    ],
    resize_keyboard=True
)

block1_okay_understand = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Окей, все понятно')]
    ],
    resize_keyboard=True
)

block1_i_looked = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Я посмотрел/а, спасибо за инфу!🤍')]
    ],
    resize_keyboard=True
)

block1_first_video_in_chat = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Мое первое видео в чате! ✅')]
    ],
    resize_keyboard=True
)

block1_review_about = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='👍')],
        [KeyboardButton(text='👍👍👍👍👍')]
    ],
    resize_keyboard=True
)

last_in_block_1 = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Конечно! У меня еще полно сил!')],
        [KeyboardButton(text='Не, пока отдохну')]
    ],
    resize_keyboard=True
)

go_next_1block = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Блок 2')],
        [KeyboardButton(text='Главное меню')]
    ],
    resize_keyboard=True
)

after_payment = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Главное меню'), KeyboardButton(text='Блок 1')]
    ],
    resize_keyboard=True
)

block2_so_letsgo = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Тогда давай начнем 🚀')],
        [KeyboardButton(text='Назад')]
    ],
    resize_keyboard=True
)

what_is_that_sound = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Понятия не имею :)')],
        [KeyboardButton(text='Для удержания внимания?')],
        [KeyboardButton(text='Подчеркнуть важность момента?')]
    ],
    resize_keyboard=True
)

is_it_interesting = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Конечно интересно!')]
    ],
    resize_keyboard=True
)

where_is_raiser = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Конечно, трудно было не заметить!')],
        [KeyboardButton(text='Не понимаю где он((')]
    ],
    resize_keyboard=True
)

answer_to_small_request = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Конечно, что такое?')],
        [KeyboardButton(text='Давай помогу!')]
    ],
    resize_keyboard=True
)

complete_request = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Готово ✅')]
    ],
    resize_keyboard=True
)

after_watch_lesson_block2=ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Маша, я досмотрел/а, спасибо, что все объяснила!')]
    ],
    resize_keyboard=True
)

i_send_dz_in_chat = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Отправил/а 🤩')]
    ],
    resize_keyboard=True
)

last_in_block_2 = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='👀')],
        [KeyboardButton(text='👀👀👀👀👀')]
    ],
    resize_keyboard=True
)

block3_or_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Блок 3')],
        [KeyboardButton(text='Главное меню')]
    ],
    resize_keyboard=True
)



# Начальная клавиатура, когда бот предлагает перейти к регистрации
register1 = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Зарегистрироваться'), KeyboardButton(text='Продолжить позже')],
        [KeyboardButton(text='Поддержка')]],
        resize_keyboard=True, input_field_placeholder='Зарегистрируйтесь или продолжите позже...')
# Клавиатура для ознакомления с пользовательским соглашением
confirm_and_register1 = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Продолжить позже'), KeyboardButton(text='Ознакомился/-ась✅')],
        [KeyboardButton(text='Поддержка')]],
        resize_keyboard=True, input_field_placeholder='Ознакомьтесь с пользовательским соглашением')
# Клавиатура, которая выдается после сообщения с информацией о службе поддержки
confirm_support_info = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text='Хорошо, буду иметь ввиду')]],
                                          resize_keyboard=True,)
# Клавиатура главного меню
main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Мой тариф'), KeyboardButton(text='Мои уроки')],
        [KeyboardButton(text='Профиль'), KeyboardButton(text='PRO')],
        [KeyboardButton(text='Поддержка')]
    ],
    resize_keyboard=True, input_field_placeholder='Главное меню...'

)
main_menu_pro = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Мой тариф'), KeyboardButton(text='Мои уроки')],
        [KeyboardButton(text='Профиль'), KeyboardButton(text='PRO')],
        [KeyboardButton(text='Поддержка'), KeyboardButton(text='Финальное дз')]
    ],
    resize_keyboard=True, input_field_placeholder='Главное меню...'

)



# Клавиатура при переходе во вкладку ПРОФИЛЬ
profile = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Изменить имя'), KeyboardButton(text='Мой тариф')],
        [KeyboardButton(text='Назад')]
    ],
    resize_keyboard=True, input_field_placeholder='Ваш профиль...'
)
# Клавиатура при переходе во вкладку PRO, если у пользователя есть тариф PRO
pro_chapter_1 = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Бонусный пак'), KeyboardButton(text='Чек лист с идеями')],
        [KeyboardButton(text='Назад'), KeyboardButton(text='Отправить финальное дз')]
    ],
    resize_keyboard=True, input_field_placeholder='Вам доступные бонусы...'
)
# Клавиатура при переходе во вкладу PRO, если у пользователя НЕ PRO
pro_chapter_0 = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='🔒Доступно в PRO')],
        [KeyboardButton(text='Назад'), KeyboardButton(text='Мой тариф')]
    ],
    resize_keyboard=True, input_field_placeholder='Доступно с тарифом PRO...'
)
# Клавиатура при переходе во вкладу ПОДДЕРЖКИ
support_from_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Назад')]
    ],
    resize_keyboard=True, input_field_placeholder='Поддержка работает 24/7'
)
# Клавиатура при переходе во вкладку ТАРИФА, если у пользователя НЕ куплен тариф PRO
my_rate_0 = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Обновить тариф')],
        [KeyboardButton(text='Назад')]
    ],
    resize_keyboard=True, input_field_placeholder='Вы можете обновиться до PRO...'
)
# Клавиатура при переходе во вкладку ТАРИФА, если у пользователя куплен тариф PRO
my_rate_1 = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Назад')]
    ],
    resize_keyboard=True, input_field_placeholder='Загляните в раздел PRO...'
)
# Клавиатура при переходе во вкладку мои уроки
my_lessons = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Блок 1'),KeyboardButton(text='Блок 2')],
        [KeyboardButton(text='Блок 3'),KeyboardButton(text='Блок 4')],
        [KeyboardButton(text='Блок 5'),KeyboardButton(text='Назад')],
    ],
    resize_keyboard=True, input_field_placeholder='Выберите блок обучения...'
)

time_for_work = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Я новичок, пока не знаю'), KeyboardButton(text='1-2 часа')],
        [KeyboardButton(text='3-4 часа'), KeyboardButton(text='5+ часов')],
        [KeyboardButton(text='Назад')]
    ],
    resize_keyboard=True, input_field_placeholder='Сколько ты готов тратить времени?'
)

fb_first_hello_answer = ReplyKeyboardMarkup(
    keyboard=[
         [KeyboardButton(text='Я новичок, пока не знаю'), KeyboardButton(text='1-2 часа')],
         [KeyboardButton(text='3-4 часа'), KeyboardButton(text='5+ часов')]
    ],
    resize_keyboard=True, input_field_placeholder='Сколько времени ты готов тратить?'
)

fb_how_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Каааак?')]
    ],
    resize_keyboard=True
)

fb_thanks_cap = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Ура, спасибо, кэп 😎')]
    ],
    resize_keyboard=True
)

