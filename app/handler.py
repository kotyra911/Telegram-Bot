import os
import uuid

from aiogram.filters import CommandStart, Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.utils.chat_action import ChatActionSender
from dotenv import load_dotenv
from pygments.lexer import default

from utils.messages import BotMessages as m
from utils.menu_navigator import step_back_check
from aiogram.utils import markdown
from aiogram.enums import ParseMode, ContentType, ChatAction
from aiogram import types, Router, F
from aiogram import Bot
import app.keyboards as kb
from config import (DialogStates as DS, MenuStates as MS, TabsStates as TB, FirstBlockStates as FBS,
                    SecondBlockStates as SBS,BaseInvoiceConfig, ThirdBlockStates as TBS, FourthBlockStates as F4BS,
                    FifthBlockStates as F5BS, YOOTOKEN, PRO_CALL_BACK_DATA, ProInvoiceConfig)

from aiogram.types import FSInputFile, CallbackQuery, PreCheckoutQuery
from db.interaction import DataBaseInteraction as Db_functions
from config import (STICKERS_PATH as S_PATH,
                    PAYLOAD_PATH as P_PATH,
                    BASE_CALL_BACK_DATA, cringe_video_file_id as b1v1, jax as b1v2, BLOCK1MATERIALS as b1m1,
                    stickers, block1_media, block2_media, block5_media, block3_media, block4_media, media)



load_dotenv()
router = Router()

# /start
@router.message(CommandStart())  # Обработка /start. Сообщение создается в отдельной функции
async def start_handler(message: types.Message, bot: Bot, state: FSMContext, db):
    tg_id = message.from_user.id
    if await Db_functions.check_user(db, tg_id):
        # Кружочек от Маши
        await bot.send_video_note(tg_id, video_note=media.get("hello_vm"), protect_content=True)
        # Приветственное слово текстом
        await bot.send_message(tg_id, await m.get_first_hello(), parse_mode=ParseMode.MARKDOWN_V2,protect_content=True)  # Отправляем сообщение в MarkDown моде
        # Сообщение о программе курса(Смотри, какую программу я для тебя составила)
        await bot.send_message(tg_id, await m.get_course_programm_text(),protect_content=True)
        # Карточка с программой курса
        await bot.send_photo(tg_id, photo=media.get("program") ,protect_content=True)
        # Просьба ознакомится с пользовательским соглашением
        await bot.send_message(tg_id, await m.get_confirm_license(), reply_markup=kb.confirm_and_register1,protect_content=True)
        # Назначения состояния, для последующего ответа на сообщение
        await state.set_state(DS.waiting_confirm_user_agreement)

    # Если пользователь зарегистрирован в базе и ознакомился с пользовательским соглашением
    elif await Db_functions.check_user_agreement_status_id(db, tg_id):
        await bot.send_message(tg_id, await m.get_user_already_exist_message(),protect_content=True)

    # Если пользователь зарегистрирован, но НЕ ознакомился с пользовательским соглашением
    else:
        await bot.send_message(tg_id,
                               await m.get_user_a_exist_no_agreement_message(),
                               reply_markup=kb.confirm_and_register1,protect_content=True)
        await state.set_state(DS.waiting_confirm_user_agreement)

# Обработчик ответ из команды /start
@router.message(StateFilter(DS.waiting_name))
async def handler_name_answer(message: types.Message, bot: Bot, state: FSMContext, db):

    user_name = message.text  # Получаем имя из ответа пользователя
    tg_id = message.from_user.id  # Получаем tg id

    action_sender = ChatActionSender(
        bot=message.bot,
        chat_id=tg_id,
        action=ChatAction.UPLOAD_PHOTO
    )


    if len(message.text) > 30:  # Проверка длинны имени
        await bot.send_message(tg_id, text='Имя не должно превышать 30 символов!',protect_content=True)

    elif '-' in message.text or '@' in message.text:  # Проверка на запрещенные символы
        await bot.send_message(tg_id, text='Вы ввели запрещенный символ!',protect_content=True)

    else: # Если все проверки пройдены, происходит регистрация пользователя и отправка ответа
        await Db_functions.add_user(db, tg_id, user_name)
        await Db_functions.switch_user_agreement(db, tg_id)  # Изменение статуса о пользовательском соглашении
        # Ответ на получение имени
        await bot.send_message(tg_id, await m.get_message_after_confirm_agreement(user_name),
                               parse_mode=ParseMode.MARKDOWN_V2, reply_markup=kb.confirm_support_info,protect_content=True)

        await bot.send_message(tg_id, await m.get_info_about_kit(user_name), protect_content=True)

        async with action_sender:
            await bot.send_photo(tg_id, photo=stickers[0], protect_content=True)
        # Объяснение со статистическим котиком

        await bot.send_message(tg_id, await m.get_start_message_support_info(), reply_markup=kb.confirm_support_info,protect_content=True)

        await state.set_state(DS.waiting_confirm_support_info)


# Обработчик для команды /menu
@router.message(Command('menu'))
async def main_menu_handler(message: types.Message, bot: Bot, state: FSMContext, db):
    tg_id = message.from_user.id  # Получение телеграм id
    if await Db_functions.check_user_agreement_status_id(db, tg_id):  # Проверка, что пользователь ознакомился с пс
        await bot.send_message(tg_id, text='Вы перешли в главное меню', reply_markup=kb.main_menu,protect_content=True)
        await state.set_state(MS.main_menu)
    else:
        await bot.send_message(tg_id, text='Похоже некоторые формальности еще не пройдены\\.\\.\\. Напиши мне */start*',
                               parse_mode=ParseMode.MARKDOWN_V2,protect_content=True)

# Обработчик для главного меню в текстовом виде
@router.message(StateFilter(TB.after_payment, FBS.last1, SBS.last_block2, TBS.final, F4BS.final, F5BS.final), F.text == 'Главное меню')
async def main_menu_text_handler(message: types.Message, bot: Bot, state: FSMContext, db):
    tg_id = message.from_user.id  # Получение телеграм id
    if await Db_functions.check_user_agreement_status_id(db, tg_id):  # Проверка, что пользователь ознакомился с пс
        await bot.send_message(tg_id, text='Вы перешли в главное меню', reply_markup=kb.main_menu,protect_content=True)
        await state.set_state(MS.main_menu)
    else:
        await bot.send_message(tg_id, text='Похоже некоторые формальности еще не пройдены\\.\\.\\. Напиши мне */start*',
                               parse_mode=ParseMode.MARKDOWN_V2,protect_content=True)

# Обработчик для команды /help
@router.message(Command('help'))  # Обработка /help
async def help_handler(message: types.Message, bot: Bot):
    tg_id = message.from_user.id
    await bot.send_message(tg_id, await m.get_support_info(),protect_content=True)

# Обработчик для вкладки PRO
@router.message(StateFilter(MS.main_menu), F.text =='PRO')
async def pro_chapter_handler(message: types.Message, bot: Bot, state: FSMContext, db):
    tg_id = message.from_user.id
    user_rate = await Db_functions.get_user_sub_status(db, message.from_user.id)

    if user_rate.upper() == 'PRO':  # Если у пользователя тариф PRO, ему передается клавиатура с еще одними вкладками
        await bot.send_message(tg_id, text='Вы перешли во вкладку PRO',
                                   parse_mode=ParseMode.MARKDOWN_V2, reply_markup=kb.pro_chapter_1,protect_content=True)
        await state.set_state(MS.pro_chapter)

        await Db_functions.update_last_active(db, tg_id)  # Обновление статуса last_active

    else:  # Если у пользователя любой другой тариф, ему выдается следующая клавиатура
        await bot.send_message(tg_id, await m.get_pro_table_message_0(), parse_mode=ParseMode.MARKDOWN_V2,
                                   reply_markup=kb.pro_chapter_0,protect_content=True)
        await state.set_state(MS.pro_chapter)


@router.message(StateFilter(MS.main_menu), F.text=='Мои уроки')
async def my_lessons_menu_handler(message: types.Message, bot: Bot, state: FSMContext, db):
    tg_id = message.from_user.id
    await bot.send_message(tg_id, text='Вы перешли во вкладку уроков', reply_markup=kb.my_lessons,protect_content=True)
    await state.set_state(MS.my_lessons)



# Обработчик для вкладки мой тариф
@router.message(StateFilter(MS.main_menu, MS.profile, MS.pro_chapter), F.text == 'Мой тариф')
async def my_rate_handler(message: types.Message, bot: Bot, state: FSMContext, db):
    # Получение информации о тарифе из бд
    user_rate = await Db_functions.get_user_sub_status(db, message.from_user.id)
    tg_id = message.from_user.id  # Получение тг id
    # Ниже вилки по тарифам
    if user_rate.upper() == 'PRO':
         await bot.send_message(tg_id, await m.get_my_rate_pro_message(),
                                   reply_markup=kb.my_rate_1,parse_mode=ParseMode.MARKDOWN_V2,protect_content=True)

    elif user_rate.upper() == 'BASE':
          await bot.send_message(tg_id, await m.get_my_rate_base_message(),
                                   reply_markup=kb.my_rate_0,parse_mode=ParseMode.MARKDOWN_V2,protect_content=True)

    elif user_rate.upper() == 'FREE':
        await bot.send_message(tg_id, await m.get_my_rate_free_message(),
                                   reply_markup=kb.my_rate_0,parse_mode=ParseMode.MARKDOWN_V2,protect_content=True)

    else:  # В случае какой-то ошибки
        await bot.send_message(tg_id,text='Произошла непредвиденна ошибка, пожалуйста обратитесь в поддержку',protect_content=True)

    await state.set_state(MS.my_rate)


# Обработчик для вкладки профиль
@router.message(StateFilter(MS.main_menu), F.text=='Профиль')
async def my_profile_handler(message: types.Message, bot: Bot, state: FSMContext, db):
    tg_id = message.from_user.id  # Получение тг id

    user_name = await Db_functions.get_username_by_id(tg_id, db)  # Получение имени пользователя по tg id

    user_sub_status = await Db_functions.get_user_sub_status(db, tg_id)  # Получение информации о тарифе

    await bot.send_message(tg_id, await m.get_profile_message(user_name, user_sub_status),
                               reply_markup=kb.profile,protect_content=True)
    await state.set_state(MS.profile)

# Обработчик на "Изменить имя" из вкладки профиля
@router.message(StateFilter(MS.profile), F.text=='Изменить имя')
async def change_name_request(message: types.Message, bot: Bot, state: FSMContext, db):

    tg_id = message.from_user.id

    await bot.send_message(tg_id, text='Напиши мне пожалуйста свое новое имя ↓',protect_content=True)
    await state.set_state(TB.change_name)
    await Db_functions.update_last_active(db, tg_id)  # Обновление статуса last_active


# Обработчик, который ловит новое имя из "Изменить имя"
@router.message(StateFilter(TB.change_name))
async def change_name_handler(message: types.Message, bot: Bot, state: FSMContext, db):
    new_user_name = message.text  # Получение нового имени

    tg_id = message.from_user.id

    await Db_functions.update_user_name(db, tg_id, new_user_name)  # Изменение имени
    await state.set_state(MS.profile)

    await bot.send_message(tg_id, await m.get_success_change_name_message(new_user_name),
                           reply_markup=kb.profile,protect_content=True)
    await Db_functions.update_last_active(db, tg_id)  # Обновление статуса last_active

# Обработчик "Назад"
@router.message(F.text == 'Назад')
async def step_back(message: types.Message, bot: Bot, state: FSMContext, db):
    sub_status = await Db_functions.get_user_sub_status(db, message.from_user.id)

    current_state = await state.get_state()  # Получение текущего состояния
    new_state, new_keyboard = await step_back_check(current_state, sub_status)  # Получение клавиатуры и нового состояния

    await bot.send_message(message.from_user.id, text='Вы вернулись назад', reply_markup=new_keyboard,protect_content=True)

    await state.set_state(new_state)

# Обработчик на согласие пользователя на обработку персональных данных и т.д.
@router.message(F.text == 'Ознакомился/-ась✅', StateFilter(DS.waiting_confirm_user_agreement))
async def confirm_agreement_handler(message: types.Message, bot: Bot, state: FSMContext, db):
    tg_id = message.from_user.id


    await bot.send_message(tg_id, await m.get_name_message(), parse_mode=ParseMode.MARKDOWN_V2,protect_content=True)

    await state.set_state(DS.waiting_name)

# Обработчик ответа на сообщение с информацией о службе поддержки
@router.message(F.text == 'Хорошо, буду иметь ввиду', StateFilter(DS.waiting_confirm_support_info))
async def last_in_start_handler(message: types.Message, bot: Bot, state: FSMContext, db):

    await bot.send_message(message.from_user.id, await m.get_last_message_in_start(),
                           protect_content=True, reply_markup=kb.menu_button)

# Обработчик кнопки продолжить позже
@router.message(StateFilter(DS.waiting_confirm_user_agreement), F.text=='Продолжить позже')
async def cont_later_handler(message: types.Message, bot: Bot, state: FSMContext, db):

    await bot.send_message(message.from_user.id, await m.get_continue_later_message(),protect_content=True)

# Обработчик вкладки "Поддержка"
@router.message(StateFilter(MS.main_menu, DS.waiting_confirm_user_agreement), F.text == 'Поддержка')
async def support_from_main_menu_handler(message: types.Message, bot: Bot, state: FSMContext):
    await bot.send_message(message.from_user.id, await m.get_support_info(), reply_markup=kb.support_from_menu,protect_content=True)


# БЛОК 1 СТАРТ
@router.message(StateFilter(MS.my_lessons, TB.after_payment), F.text == 'Блок 1')
async def fb_start_handler(message: types.Message, bot: Bot, state: FSMContext, db):

    tg_id = message.from_user.id

    if await Db_functions.check_block_access(db, tg_id, 1):  # Проверка, открыт ли блок у пользователя

        await state.set_state(FBS.waiting_time_for_work)
        # Приветственное сообщение первого блока
        await bot.send_message(tg_id, await m.get_fb_hello_1_message(), reply_markup=kb.time_for_work,protect_content=True)

    else:

        await bot.send_message(tg_id, text='Тебе недоступен этот блок :(',protect_content=True)

# БЛОК 1
@router.message(StateFilter(FBS.waiting_time_for_work),
                F.text.in_(['Я новичок, пока не знаю','1-2 часа','3-4 часа','5+ часов']))
async def answer_time_for_work_handler(message: types.Message, bot: Bot, state: FSMContext):
    answer = message.text  # Получение ответа пользователя
    tg_id = message.from_user.id  # Получение тг id

    message_to_send = await m.get_time__answer_message(answer)  # Получение сообщения, которое зависит от ответа

    # Отправка следующего сообщения
    await bot.send_message(tg_id, message_to_send, reply_markup=kb.fb_how_keyboard,protect_content=True)
    # Обновление состояния
    await state.set_state(FBS.how_waiting_for_bot)


# БЛОК 1
@router.message(StateFilter(FBS.how_waiting_for_bot), F.text =='Каааак?')
async def how_answer_handler(message: types.Message, bot: Bot, state: FSMContext):
    tg_id = message.from_user.id  # Получение тг id
    # Следующее диалоговое сообщение
    await bot.send_message(tg_id, await m.get_how_answer_message(), reply_markup=kb.fb_thanks_cap,protect_content=True)
    # Назначение состояния
    await state.set_state(FBS.said_thanks_cap)


# БЛОК 1
@router.message(StateFilter(FBS.said_thanks_cap), F.text == 'Ура, спасибо, кэп 😎')
async def thanks_cap_answer_handler(message: types.Message, bot: Bot, state: FSMContext):
    tg_id = message.from_user.id

    # Просто отправляем следующее диалоговое сообщение
    await bot.send_message(tg_id, await m.get_answer_thanks_cap_message(), reply_markup=kb.cringe_send_or_not_keyboard,protect_content=True)
    # Задаем состояние, чтобы отловить ответ
    await state.set_state(FBS.cringe_send_or_not)


# БЛОК 1
@router.message(StateFilter(FBS.cringe_send_or_not), F.text.in_(['Отправляй, отправляй 🤪', 'Я спасу тебя от стыда, не отправляй 😇']))
async def cringe_send_handler(message: types.Message, bot: Bot, state: FSMContext):
    answer = message.text  # Получаем ответ пользователя
    tg_id = message.from_user.id  # Получаем тг ic
    file_id = b1v1  # Берем нужный file_id из env

    # Создание отправителя действий. -> "Загружает видео..."
    action_sender = ChatActionSender(
        bot=message.bot,
        chat_id=tg_id,
        action=ChatAction.UPLOAD_VIDEO
    )
    # Сообщение формируется в зависимости от ответа пользователя
    message_to_send = await m.get_cringe_video_answer_message(answer)

    await bot.send_message(tg_id, message_to_send,protect_content=True)  # Отправляем ответ на ответ

    # Отправка видео через action_sender, для отображения действия бота
    async with action_sender:
        await bot.send_video(tg_id, video=file_id, caption='ЗАГЛУШКА НА 30 МБ')  # Отправляем видео

    await bot.send_message(tg_id, await m.get_why_i_show_message1(),protect_content=True)  # Продолжение диалога

    await bot.send_message(tg_id, await m.get_why_i_show_message2_question(), reply_markup=kb.after_cringe_what_start,protect_content=True)  # Вопрос "с чего начнем?"


# БЛОК 1
@router.message(StateFilter(FBS.cringe_send_or_not), F.text.in_(['Склейка ✂️', 'Цветокор 🎨', 'Масштабы 📏']))
async def before_start_handler(message: types.Message, bot: Bot, state: FSMContext, db):

    user_message_text = message.text
    tg_id = message.from_user.id

    name = await Db_functions.get_username_by_id(tg_id, db)

    await bot.send_message(tg_id, await m.get_before_start_message(user_message_text), protect_content=True)

    await bot.send_message(tg_id, text=f'Ну что, {name}, погнали?', reply_markup=kb.block1_letsgo_keyboard, protect_content=True)

    await state.set_state(FBS.wait_for_letsgo)


# БЛОК 1
@router.message(StateFilter(FBS.wait_for_letsgo), F.text.in_(['Нет, мне страшно, у меня не получится…','Погнали!']))
async def letsgo_handler(message: types.Message, bot: Bot, state: FSMContext):
    answer = message.text
    tg_id = message.from_user.id

    await bot.send_message(tg_id, await m.get_answer_letsgo_message(answer), reply_markup=kb.block1_okay_understand, protect_content=True)

    await state.set_state(FBS.wait_for_understand)


# БЛОК 1
@router.message(StateFilter(FBS.wait_for_understand), F.text == 'Окей, все понятно')
async def understand_handler(message: types.Message, bot: Bot, state: FSMContext):

    tg_id = message.from_user.id

    docs = FSInputFile(b1m1)

    video = FSInputFile(b1v2)

    # Создание отправителя действий. -> "Загружает документ..."
    action_sender_docs = ChatActionSender(
        bot=message.bot,
        chat_id=tg_id,
        action=ChatAction.UPLOAD_DOCUMENT
    )

    # Создание отправителя действий. -> "Загружает видео..."
    action_sender_video = ChatActionSender(
        bot=message.bot,
        chat_id=tg_id,
        action=ChatAction.UPLOAD_VIDEO
    )

    await bot.send_message(tg_id, text='Лови материалы для первого блока 👇', protect_content=True)
    # Материалы
    async with action_sender_docs:
        await bot.send_document(tg_id, document=block1_media.get("materials"))
        await bot.send_document(tg_id, document=block1_media.get("materials2"))

    await bot.send_message(tg_id, text='И сам видеоурок:', protect_content=True)
    # Видео
    async with action_sender_docs:
        await bot.send_document(tg_id, document=block1_media.get("lesson1"), protect_content=True)

    await bot.send_message(tg_id, text='Дай знать, когда досмотришь 😉', protect_content=True, reply_markup=kb.block1_i_looked)

    await state.set_state(FBS.wait_for_looking)


# БЛОК 1
@router.message(StateFilter(FBS.wait_for_looking), F.text == 'Я посмотрел/а, спасибо за инфу!🤍')
async def i_looked_handler(message: types.Message, bot: Bot, state: FSMContext, db):
    tg_id = message.from_user.id
    name = await Db_functions.get_username_by_id(tg_id, db)

    message_1, message_2 = await m.get_after_looked_message(name)

    await bot.send_message(tg_id, text=message_1, protect_content=True )

    await bot.send_message(tg_id, text=message_2, protect_content=True, reply_markup=kb.block1_first_video_in_chat)

    await bot.send_video_note(tg_id, video_note=block1_media.get("chat_link_vm"), protect_content=True)

    await state.set_state(FBS.wait_first_chat_video)


# БЛОК 1
@router.message(StateFilter(FBS.wait_first_chat_video), F.text == 'Мое первое видео в чате! ✅')
async def first_video_chat_handler(message: types.Message, bot: Bot, state: FSMContext, db):
    tg_id = message.from_user.id
    name = await Db_functions.get_username_by_id(tg_id, db)

    # Создание менеджера действий. -> "Загружает фото..."
    action_sender = ChatActionSender(
        bot=message.bot,
        chat_id=tg_id,
        action=ChatAction.UPLOAD_PHOTO
    )

    await bot.send_message(tg_id, await m.get_first_video_chat_message(name), protect_content=True)
    await bot.send_message(tg_id, await m.get_new1(), protect_content=True)

    async with action_sender:
        await bot.send_photo(tg_id, photo=stickers[1], protect_content=True)

    await bot.send_message(tg_id, text='Как тебе первый блок? Много нового удалось узнать?', reply_markup=kb.block1_review_about, protect_content=True)

    await state.set_state(FBS.wait_review)


# БЛОК 1
@router.message(StateFilter(FBS.wait_review), F.text.in_(['👍','👍👍👍👍👍']))
async def review_handler(message: types.Message, bot: Bot, state: FSMContext):
    tg_id = message.from_user.id

    answer = message.text

    await bot.send_message(tg_id, await m.get_last_block1_message(answer), protect_content=True, reply_markup=kb.last_in_block_1)

    await state.set_state(FBS.last1)


# БЛОК 1
@router.message(StateFilter(FBS.last1), F.text.in_(['Конечно! У меня еще полно сил!', 'Не, пока отдохну']))
async def last_1block_handler(message: types.Message, bot: Bot, state: FSMContext, db):

    answer = message.text

    tg_id = message.from_user.id
    # Открытие доступа ко второму блоку обучения
    await Db_functions.update_user_course_status(db=db,user_telegram_id=tg_id, course_id=2)

    await bot.send_message(tg_id, await m.get_last_last_block1(answer), protect_content=True,
                           reply_markup=kb.go_next_1block, parse_mode=ParseMode.HTML)


# БЛОК 2 СТАРТ
@router.message(StateFilter(MS.my_lessons, FBS.last1), F.text == 'Блок 2')
async def block2_start_handler(message: types.Message, bot: Bot, state: FSMContext, db):

    tg_id = message.from_user.id

    name = await Db_functions.get_username_by_id(tg_id, db)

    if await Db_functions.check_block_access(db, tg_id, 2):  # Проверка, открыт ли блок у пользователя

        await state.set_state(SBS.wait_for_letsgo)

        # Приветственное сообщение первого блока
        await bot.send_message(tg_id, await m.get_second_block_1_message(name), reply_markup=kb.block2_so_letsgo,protect_content=True)

    else:

        await bot.send_message(tg_id, text='Тебе недоступен этот блок :(',protect_content=True)
# БЛОК 2
@router.message(StateFilter(SBS.wait_for_letsgo), F.text == 'Тогда давай начнем 🚀')
async def letsgo_block2_handler(message: types.Message, bot: Bot, state: FSMContext, db):
    tg_id = message.from_user.id

    await bot.send_message(tg_id, text='Блок 2: Саунд дизайн\n\nКак ты думаешь, для чего используется вот этот звук?', protect_content=True)

    # Отправка звука
    await bot.send_voice(tg_id, voice=block2_media.get("sound"),
                         protect_content=True, reply_markup=kb.what_is_that_sound)

    await state.set_state(SBS.wait_what_sound_answer)


# БЛОК 2
@router.message(StateFilter(SBS.wait_what_sound_answer), F.text.in_(['Понятия не имею :)','Для удержания внимания?','Подчеркнуть важность момента?' ]))
async def what_sound_answer_handler(message: types.Message, bot: Bot, state: FSMContext, db):
    answer = message.text
    tg_id = message.from_user.id

    await bot.send_message(tg_id, await m.get_after_what_sound_message(answer), protect_content=True,
                           parse_mode=ParseMode.HTML)

    await bot.send_message(tg_id, await m.get_new2(), protect_content=True,
                           parse_mode=ParseMode.HTML, reply_markup=kb.is_it_interesting)

    await state.set_state(SBS.is_it_interesting)


# БЛОК 2
@router.message(StateFilter(SBS.is_it_interesting), F.text =='Конечно интересно!')
async def course_interesting_handler(message: types.Message, bot: Bot, state: FSMContext, db):

    tg_id = message.from_user.id
    name = await Db_functions.get_username_by_id(tg_id, db)

    # Создание менеджера действий. -> "Загружает видео..."
    action_sender = ChatActionSender(
        bot=message.bot,
        chat_id=tg_id,
        action=ChatAction.UPLOAD_VIDEO
    )
    # Объяснение про райзер
    await bot.send_message(tg_id, await m.get_after_intr_message(), protect_content=True)

    # Отправка кусочка из видео Маши с райзером
    async with action_sender:
        await bot.send_video(tg_id, video=block2_media.get("piece1"), protect_content=True)

    # Отправка кусочка из видео Маши с райзером 2
    async with action_sender:
        await bot.send_video(tg_id, video=block2_media.get("piece2"), protect_content=True)

    await bot.send_message(tg_id, await m.get_where_is_raiser_message(name), protect_content=True,
                           reply_markup=kb.where_is_raiser)

    await state.set_state(SBS.where_is_raiser)


# БЛОК 2
@router.message(StateFilter(SBS.where_is_raiser), F.text.in_(['Конечно, трудно было не заметить!', 'Не понимаю где он((']))
async def after_where_raiser_handler(message: types.Message, bot: Bot, state: FSMContext, db):

    answer = message.text
    tg_id = message.from_user.id

    await bot.send_message(tg_id, await m.get_after_where_raise_message(answer), protect_content=True,)

    await bot.send_message(tg_id, await m.get_small_request_message(), protect_content=True,
                           reply_markup=kb.answer_to_small_request)

    await state.set_state(SBS.wait_answer_on_small_request)

# БЛОК 2
@router.message(StateFilter(SBS.wait_answer_on_small_request), F.text.in_(['Конечно, что такое?','Давай помогу!']))
async def answer_to_request_handler(message: types.Message, bot: Bot, state: FSMContext, db):

    await bot.send_message(message.from_user.id, await m.get_answer_to_answer_rq_message(),
                           protect_content=True, reply_markup=kb.complete_request)

    await state.set_state(SBS.wait_for_complete_request)

# БЛОК 2
@router.message(StateFilter(SBS.wait_for_complete_request), F.text =='Готово ✅')
async def complete_req_handler(message: types.Message, bot: Bot, state: FSMContext, db):

    tg_id = message.from_user.id

    docs = FSInputFile(b1m1)

    video = FSInputFile(b1v2)
    docs = FSInputFile(b1m1)

    # Создание менеджера действий. -> "Загружает документ..."
    action_sender_docs = ChatActionSender(
        bot=message.bot,
        chat_id=tg_id,
        action=ChatAction.UPLOAD_DOCUMENT
    )

    await bot.send_message(tg_id, await m.get_lesson_block2_message(), protect_content=True)
    # Отправка материалов для видео
    async with action_sender_docs:
        await bot.send_document(tg_id, document=block2_media.get("material"))

    await bot.send_message(tg_id, text='И лови наш второй урок:', protect_content=True)

    async with action_sender_docs:
        await bot.send_document(tg_id, document=block2_media.get("lesson2"))

    await bot.send_message(tg_id, text='Сообщи мне, как посмотришь видео🤍', protect_content=True,reply_markup=kb.after_watch_lesson_block2)

    await state.set_state(SBS.wait_for_watch)

# БЛОК 2
@router.message(StateFilter(SBS.wait_for_watch), F.text == 'Маша, я досмотрел/а, спасибо, что все объяснила!')
async def after_watch_handler(message: types.Message, bot: Bot, state: FSMContext, db):

    tg_id = message.from_user.id

    name = await Db_functions.get_username_by_id(tg_id,db)

    await bot.send_message(tg_id, await m.get_send_dz_in_chat_message(name), protect_content=True, reply_markup=kb.i_send_dz_in_chat)

    await state.set_state(SBS.wait_sending_message)

# БЛОК 2
@router.message(StateFilter(SBS.wait_sending_message), F.text=='Отправил/а 🤩')
async def i_send_message_handler(message: types.Message, bot: Bot, state: FSMContext):

    tg_id = message.from_user.id

    # Создание менеджера действий. -> "Загружает фото..."
    action_sender = ChatActionSender(
        bot=message.bot,
        chat_id=tg_id,
        action=ChatAction.UPLOAD_PHOTO
    )

    await bot.send_message(tg_id, await m.get_block2_pre_last_message(), protect_content=True)
    async with action_sender:
        await bot.send_photo(tg_id, photo=stickers[2], protect_content=True)

    await bot.send_message(tg_id, text='Поделись своими впечатлениями, как тебе второй блок?', protect_content=True, reply_markup=kb.last_in_block_2)

    await state.set_state(SBS.last_block2)

# БЛОК 2
@router.message(StateFilter(SBS.last_block2), F.text.in_(['👀','👀👀👀👀👀']))
async def last_handler_block2_handler(message: types.Message, bot: Bot, state: FSMContext, db):
    answer = message.text
    tg_id = message.from_user.id
    name = await Db_functions.get_username_by_id(tg_id,db)

    await bot.send_message(tg_id, await m.get_last_message_block2(name, answer), protect_content=True, reply_markup=kb.block3_or_menu)

    await Db_functions.update_user_course_status(db=db, user_telegram_id=tg_id, course_id=3)


# БЛОК 3 СТАРТ
@router.message(StateFilter(MS.my_lessons, SBS.last_block2), F.text == 'Блок 3')
async def block3_start_handler(message: types.Message, bot: Bot, state: FSMContext, db):

            tg_id = message.from_user.id

            if await Db_functions.check_block_access(db, tg_id, 3):  # Проверка, открыт ли блок у пользователя

                await state.set_state(TBS.state1)

                await bot.send_message(tg_id, await m.bl3_1_message(), protect_content=True, reply_markup=kb.bl3_start_kb)

            else:

                await bot.send_message(tg_id, text='Тебе недоступен этот блок :(', protect_content=True)


# БЛОК 3
@router.message(StateFilter(TBS.state1), F.text.in_(["Ну… я просто ставлю текст куда влезет 😅","Понимаю, что важно, но не знаю как правильно :(",
                                                     "Конечно, я же эстет ✨"]))
async def block3_2_handler(message: types.Message, bot: Bot, state: FSMContext, db):
    tg_id = message.from_user.id
    name = await Db_functions.get_username_by_id(tg_id, db)
    answer = message.text

    message_to_user = await m.bl3_1kb_message(answer)

    await bot.send_message(tg_id, message_to_user, reply_markup=kb.bl3_2_kb, protect_content=True, parse_mode=ParseMode.HTML)

    await bot.send_photo(tg_id, photo=block3_media.get("image1"), protect_content=True)

    await state.set_state(TBS.state2)


# БЛОК 3
@router.message(StateFilter(TBS.state2), F.text.in_(["Ничего, все отлично", "Что-то не так, но не понимаю что", "Возможно сильно пусто?"]))
async def block3_3_handler(message: types.Message, bot: Bot, state: FSMContext, db):
    tg_id = message.from_user.id
    name = await Db_functions.get_username_by_id(tg_id, db)

    await bot.send_photo(tg_id, photo=block3_media.get("image2"), protect_content=True)

    message_to_user = await m.bl3_2_message(name)

    await bot.send_message(tg_id, message_to_user, reply_markup=kb.bl3_3_kb,protect_content=True)

    await state.set_state(TBS.state3)


# БЛОК 3
@router.message(StateFilter(TBS.state3), F.text == "Да!")
async def block3_4_handler(message: types.Message, bot: Bot, state: FSMContext, db):
    tg_id = message.from_user.id
    name = await Db_functions.get_username_by_id(tg_id, db)

    message_to_user = await m.bl3_3_message(name)

    await bot.send_message(tg_id, message_to_user, reply_markup=kb.bl3_4_kb,protect_content=True)

    await state.set_state(TBS.state4)


# БЛОК 3
@router.message(StateFilter(TBS.state4), F.text.in_(["Супер, погнали!", "Летс гооооооооу"]))
async def block3_5_handler(message: types.Message, bot: Bot, state: FSMContext):

    tg_id = message.from_user.id

    await bot.send_message(tg_id, text='Держи материалы для урока 👇',protect_content=True)

    action_sender = ChatActionSender(
        bot=message.bot,
        chat_id=tg_id,
        action=ChatAction.UPLOAD_DOCUMENT
    )

    for i in block3_media.get("materials"):
        async with action_sender:
            await bot.send_document(tg_id, document=i, protect_content=True)

    await bot.send_message(tg_id, text='И, естественно, сам видеоурок:', protect_content=True)

    async with action_sender:
        await bot.send_document(tg_id, document=block3_media.get("lesson3"), protect_content=True)

    await bot.send_message(tg_id, text='Как досмотришь, возвращайся, обсудим!', reply_markup=kb.bl3_5_kb, protect_content=True)

    await state.set_state(TBS.state5)


# БЛОК 3
@router.message(StateFilter(TBS.state5), F.text =='Посмотрел/а ✅')
async def block3_6_handler(message: types.Message, bot: Bot, state: FSMContext, db):

    tg_id = message.from_user.id
    name = await Db_functions.get_username_by_id(tg_id, db)

    await bot.send_message(tg_id, await m.bl3_4_message(name), protect_content=True, reply_markup=kb.bl3_6_kb)

    await state.set_state(TBS.state6)


# БЛОК 3
@router.message(StateFilter(TBS.state6), F.text=='Дз уже в чате :)')
async def block3_7_handler(message: types.Message, bot: Bot, state: FSMContext, db):

    tg_id = message.from_user.id

    # Создание менеджера действий. -> "Загружает фото..."
    action_sender = ChatActionSender(
        bot=message.bot,
        chat_id=tg_id,
        action=ChatAction.UPLOAD_PHOTO
    )

    name = await Db_functions.get_username_by_id(tg_id, db)

    await bot.send_message(tg_id, await m.bl3_5_message(), protect_content=True)
    async with action_sender:
        await bot.send_photo(tg_id, photo=stickers[3], protect_content=True)

    await bot.send_message(tg_id, await m.bl3_6_message(name), protect_content=True, reply_markup=kb.bl3_7_kb)

    await state.set_state(TBS.state7)


# БЛОК 3
@router.message(StateFilter(TBS.state7), F.text.in_(['Спасибо, Маша, реально узнал/а что-то новое 🔥', 'Информация годная, но я уже все знаю 😅']))
async def block3_8_handler(message: types.Message, bot: Bot, state: FSMContext):
    tg_id = message.from_user.id

    answer = message.text

    await bot.send_message(tg_id, await m.bl3_3kb_message(answer), protect_content=True, reply_markup=kb.bl3_8_kb)

    await state.set_state(TBS.state8)


# БЛОК 3
@router.message(StateFilter(TBS.state8), F.text.in_(['Я, пожалуй, пойду отдыхать 😴',
                                                     'Хочу дальше, но надо работать 🫠', 'Погнали дальше 🚀']))
async def block3_9_handler(message: types.Message, bot: Bot, state: FSMContext, db):

    tg_id = message.from_user.id
    await Db_functions.update_user_course_status(db=db, user_telegram_id=tg_id, course_id=4)
    answer = message.text

    await bot.send_message(tg_id, await m.bl3_4kb_message(answer), protect_content=True, reply_markup=kb.bl3_9_kb)

    await state.set_state(TBS.final)


# БЛОК 4
# Обработчик вкладки с первым блоком обучения
@router.message(StateFilter(MS.my_lessons, TBS.final), F.text == 'Блок 4')
async def block4_start_handler(message: types.Message, bot: Bot, state: FSMContext, db):

            tg_id = message.from_user.id

            if await Db_functions.check_block_access(db, tg_id, 4):  # Проверка, открыт ли блок у пользователя

                await state.set_state(F4BS.state1)

                await bot.send_message(tg_id, await m.bl4_1_message(), protect_content=True, reply_markup=kb.bl4_1_kb)

            else:

                await bot.send_message(tg_id, text='Тебе недоступен этот блок :(', protect_content=True)


# БЛОК 4
@router.message(StateFilter(F4BS.state1), F.text.in_(['Быстрые склейки','Движение камеры','Текст в разных частях экрана']))
async def block4_2_handler(message: types.Message, bot: Bot, state: FSMContext, db):

    tg_id = message.from_user.id
    name = await Db_functions.get_username_by_id(tg_id, db)
    answer = message.text

    await bot.send_message(tg_id, await m.bl4_2_message(answer), protect_content=True)

    await bot.send_message(tg_id, await m.bl4_3_message(name), protect_content=True, reply_markup=kb.bl4_2_kb)

    await state.set_state(F4BS.state2)


# БЛОК 4
@router.message(StateFilter(F4BS.state2), F.text.in_(['Я в предвкушении!','Настрой лучше всех!','Чуть-чуть волнуюсь']))
async def block4_3_handler(message: types.Message, bot: Bot, state: FSMContext, db):

    tg_id = message.from_user.id

    answer = message.text

    action_sender = ChatActionSender(
        bot=message.bot,
        chat_id=tg_id,
        action=ChatAction.UPLOAD_DOCUMENT,
    )

    async with action_sender:
        for i in block4_media.get("materials"):
            await bot.send_document(tg_id, document=i, protect_content=True)

    async with action_sender:
        await bot.send_document(tg_id, document=block4_media.get("lesson4"), protect_content=True)

    await bot.send_message(tg_id, text='Пожалуйста, как досмотришь, сообщи мне 😉', protect_content=True,
                           reply_markup=kb.bl4_3_kb)

    await state.set_state(F4BS.state3)


# БЛОК 4
@router.message(StateFilter(F4BS.state3), F.text == 'Маша, я посмотрел/а!')
async def block4_4_handler(message: types.Message, bot: Bot, state: FSMContext, db):

    await bot.send_message(message.from_user.id, text=await m.bl4_5_message(), protect_content=True, reply_markup=kb.bl4_4_kb)

    await state.set_state(F4BS.state4)


# БЛОК 4
@router.message(StateFilter(F4BS.state4), F.text.in_(['Это круто, спасибо, все буду использовать 🔥',
                                                      'Взглянул/а на все по-новому','Соу-соу']))
async def block4_5_handler(message: types.Message, bot: Bot, state: FSMContext, db):
    tg_id = message.from_user.id

    answer = message.text

    name = await Db_functions.get_username_by_id(tg_id, db)

    await bot.send_message(tg_id, await m.bl4_6_message(answer, name), protect_content=True, reply_markup=kb.bl4_5_kb)

    await state.set_state(F4BS.final)


# БЛОК 4
@router.message(StateFilter(F4BS.final), F.text == 'Дз уже готово 🫡')
async def block4_6_handler(message: types.Message, bot: Bot, state: FSMContext, db):

    tg_id = message.from_user.id

    # Создание менеджера действий. -> "Загружает фото..."
    action_sender = ChatActionSender(
        bot=message.bot,
        chat_id=tg_id,
        action=ChatAction.UPLOAD_PHOTO
    )

    await bot.send_message(tg_id, text='Сууупер! Держи новый стикер со счастливым котиком 🐈', protect_content=True)
    async with action_sender:
        await bot.send_photo(tg_id, photo=stickers[4], protect_content=True)

    await bot.send_video_note(tg_id, video_note=block4_media.get("materials")[-1], protect_content=True,
                              reply_markup=kb.bl4_6_kb)

    await Db_functions.update_user_course_status(db=db, user_telegram_id=tg_id, course_id=5)


# БЛОК 5 СТАРТ
@router.message(StateFilter(MS.my_lessons, F4BS.final), F.text == 'Блок 5')
async def block5_start_handler(message: types.Message, bot: Bot, state: FSMContext, db):

            tg_id = message.from_user.id

            name = await Db_functions.get_username_by_id(tg_id, db)

            if await Db_functions.check_block_access(db, tg_id, 5):  # Проверка, открыт ли блок у пользователя

                await state.set_state(F5BS.state1)

                await bot.send_message(tg_id, await m.bl5_1_message(name), protect_content=True, reply_markup=kb.bl5_1_kb)

            else:

                await bot.send_message(tg_id, text='Тебе недоступен этот блок :(', protect_content=True)


# БЛОК 5
@router.message(StateFilter(F5BS.state1), F.text.in_(['Рваная склейка ✂️','Плоское видео 🙊','Резкие переходы и анимации 😶‍🌫']))
async def block5_2_handler(message: types.Message, bot: Bot, state: FSMContext, db):
    answer = message.text
    tg_id = message.from_user.id

    await bot.send_message(tg_id, await m.bl5_2_message(answer), protect_content=True, reply_markup=kb.bl5_2_kb)

    await state.set_state(F5BS.state2)


# БЛОК 5
@router.message(StateFilter(F5BS.state2), F.text.in_(['ДАДАДАДА','Что там? 👀']))
async def block5_3_handler(message: types.Message, bot: Bot, state: FSMContext, db):
    tg_id = message.from_user.id
    name = await Db_functions.get_username_by_id(tg_id, db)

    await bot.send_message(tg_id, await m.bl5_3_message(), protect_content=True)

    action_sender = ChatActionSender(
        bot=message.bot,
        chat_id=tg_id,
        action=ChatAction.UPLOAD_VIDEO
    )

    async with action_sender:
        await bot.send_document(tg_id, block5_media.get("shortv"), protect_content=True)


    await bot.send_message(tg_id, await m.bl5_4_message(name), protect_content=True)

    await bot.send_message(tg_id, await m.bl5_5_message(), protect_content=True, reply_markup=kb.bl5_tutorial_kb)

    await state.set_state(F5BS.spc_double)


# БЛОК 5
@router.message(StateFilter(F5BS.spc_double), F.text=='Можем переходить к уроку!')
async def block5_to_lesson_handler(message: types.Message, bot: Bot, state: FSMContext, db):

    tg_id = message.from_user.id

    action_sender = ChatActionSender(
        bot=message.bot,
        chat_id=tg_id,
        action=ChatAction.UPLOAD_DOCUMENT
    )

    await bot.send_message(tg_id, await m.bl5_6_message(), protect_content=True)

    async with action_sender:
        for i in block5_media.get("materials"):
            await bot.send_document(tg_id, i, protect_content=True)

    async with action_sender:
        await bot.send_document(tg_id, document=block5_media.get("lesson5"), protect_content=True)

    await bot.send_message(tg_id, text=await m.bl5_7_message(), protect_content=True, reply_markup=kb.bl5_4_kb)

    await state.set_state(F5BS.state4)


# БЛОК 5
@router.message(StateFilter(F5BS.state4), F.text=='Посмотрел/а ✅')
async def block_5_5_handler(message: types.Message, bot: Bot, state: FSMContext, db):
    tg_id = message.from_user.id
    name = await Db_functions.get_username_by_id(tg_id, db)

    # Создание менеджера действий. -> "Загружает фото..."
    action_sender = ChatActionSender(
        bot=message.bot,
        chat_id=tg_id,
        action=ChatAction.UPLOAD_PHOTO
    )
    async with action_sender:
        await bot.send_photo(tg_id, photo=stickers[5], protect_content=True)

    await bot.send_message(tg_id, await m.bl5_8_message(name), protect_content=True)

    await bot.send_message(tg_id, text='МАТВЕЙ!!! НЕ ЗАБУДЬ!!! ЗДЕСЬ ДОЛЖНА БЫТЬ ИНФА О ТОМ, КАК ОТПРАВИТЬ ФИНАЛЬНОЕ ДОМАШНЕЕ ЗАДАНИЕ!!!', protect_content=True)

    await bot.send_message(tg_id, await m.bl5_9_message(), protect_content=True, reply_markup=kb.bl5_5_kb)

    await state.set_state(F5BS.state5)


# БЛОК 5
@router.message(StateFilter(F5BS.state5), F.text =='Значит, это все?🥲')
async def block_5_6_handler(message: types.Message, bot: Bot, state: FSMContext, db):

    await bot.send_message(message.from_user.id, await m.bl5_10_message(), protect_content=True, reply_markup=kb.bl5_6_kb)

    await state.set_state(F5BS.final)



@router.message(StateFilter(MS.my_rate), F.text == 'Обновить тариф')
async def update_rate(message: types.Message, bot: Bot, state: FSMContext, db):
    tg_id = message.from_user.id

    sub_status_name = await Db_functions.get_user_sub_status(db, tg_id)
    sub_status_name = sub_status_name.upper()

    message_to_user, keyboard = await m.get_rates_message(sub_status_name)

    await bot.send_message(tg_id, message_to_user, reply_markup=keyboard, parse_mode=ParseMode.HTML,protect_content=True)

    await state.set_state(MS.update_rate)

# Колл бэк, который срабатывает на нажатие на клавиатуру с покупкой
@router.callback_query(F.data==PRO_CALL_BACK_DATA)
async def subscription(call: CallbackQuery, bot: Bot, db):

    tg_id = call.from_user.id
    user_id = await Db_functions.get_user_id_by_tg(db, tg_id)

    current_user_sub_status = await Db_functions.get_user_sub_status(db, tg_id)
    # Цена формируется в зависимости от того, приобретал ли пользователь какой-то курс до этого
    if current_user_sub_status.lower() == 'base':
        # Подготовка данных для Invoice(счета)
        order_id = str(uuid.uuid4())

        amount_in_bd = 3000

        np = ProInvoiceConfig(chat_id=tg_id, payload=order_id, start_parameter=order_id, amount=300000)


    else:

        order_id = str(uuid.uuid4())

        amount_in_bd = 8000

        np = ProInvoiceConfig(chat_id=tg_id, payload=order_id, start_parameter=order_id, amount=800000)


    # Отправка счета
    await bot.send_invoice(chat_id=np.chat_id, title=np.title, description=np.description, payload=np.payload,
                               provider_token=np.provider_token, currency=np.currency,
                               start_parameter=np.start_parameter, prices=np.prices)

    # Удаление предыдущего сообщения, чтобы красиво смотрелось
    await bot.delete_message(call.from_user.id, call.message.message_id)

    # Создание нового заказа в таблице, со статусом "0" -> "pending" -> "в ожидании"
    await Db_functions.create_new_order(db=db, order_id=order_id, user_id=user_id, sub_status_id=2, amount=amount_in_bd,
                                        currency=np.currency, order_status_id=0)



# Колл бэк, который срабатывает на нажатие на клавиатуру с покупкой
@router.callback_query(F.data==BASE_CALL_BACK_DATA)
async def subscription(call: CallbackQuery, bot: Bot, db):

    tg_id = call.from_user.id
    user_id = await Db_functions.get_user_id_by_tg(db, tg_id)
    # Формирование данных платежа
    order_id = str(uuid.uuid4())
    np = BaseInvoiceConfig(chat_id=tg_id, payload=order_id, start_parameter=order_id)
    # Отправка счета
    await bot.send_invoice(chat_id=np.chat_id, title=np.title, description=np.description, payload=np.payload,
                           provider_token=np.provider_token, currency=np.currency,
                           start_parameter=np.start_parameter, prices=np.prices)

    await bot.delete_message(call.from_user.id, call.message.message_id)

    await Db_functions.create_new_order(db=db, order_id=order_id, user_id=user_id, sub_status_id=1, amount=5000,
                                        currency=np.currency, order_status_id=0)

# Обязательный ответ в течение 10 секунд на webhook от Telegram
@router.pre_checkout_query()
async def process_pre_check_out_query(query: PreCheckoutQuery, bot: Bot):

    await bot.answer_pre_checkout_query(query.id, ok=True)

# Обработка успешного платежа
@router.message(F.content_type==ContentType.SUCCESSFUL_PAYMENT)
async def process_pay(message: types.Message, bot: Bot, state: FSMContext, db):
    tg_id = message.from_user.id  # Получение тг id

    name = await Db_functions.get_username_by_id(tg_id, db)
    """Получение order_id из объекта SuccessfulPayment, а после попытка получить 
    заказ из базы по этому order_id. Если такой заказ есть, происходит добавление добавление новых данных
    в базу(см. ниже). Если заказа такого нет, выдать сообщение об ошибке пользователю"""
    order_id = message.successful_payment.invoice_payload

    order_from_db = await Db_functions.get_order_by_payment_id(db, order_id)  # Получение order_id

    if order_from_db:

        user_order_sub_status_id = await Db_functions.get_user_sub_status_id_from_order(db,order_id)  # Получение купленного статуса

        provider_payment_id = message.successful_payment.provider_payment_charge_id
        # Записываем номер транзакции от ЮKassa
        await Db_functions.update_provider_payment_id(db,tg_id,provider_payment_id)

        # Обновляем статус подписки и статус заказа
        await Db_functions.update_user_sub_status(db, tg_id, user_order_sub_status_id)
        await Db_functions.update_order_status_id(db, order_id, 1)
        await Db_functions.update_user_course_status(db, tg_id, 1)

        # Сообщаем пользователю, что он успешно приобрел подписку и добавляем статус "оплачено в базу"
        await bot.send_message(tg_id, await m.get_after_payment_message(name), protect_content=True,
                               reply_markup=kb.after_payment, parse_mode=ParseMode.HTML)

        await state.set_state(TB.after_payment)

    else:
        await bot.send_message(tg_id, text='Произошла ошибка при обработке платежа. Пожалуйста, обратитесь в поддержку', reply_markup=kb.main_menu, protect_content=True)
        await state.set_state(MS.main_menu)



#@router.message()
#async def error_message(message: types.Message, bot: Bot):
  #  await bot.send_message(message.from_user.id, text='Я не знаю такую команду. Воспользуйтесь /menu, чтобы перейти в главное меню.\n\n'
                     #                                'Используйте /commands, чтобы увидеть все команды, которые вы можете использовать\n\n'
                      #                               'Если ошибка повторится, пожалуйста, обратитесь в нашу поддержку:\n'
                          #                           '👉 @Here_will_be_support_username',protect_content=True)

@router.message()
async def error_message(message: types.Message, bot: Bot):
    file_id = message.video_note.file_id
    print(file_id)

#@router.message()
#async def error_message(message: types.Message, bot: Bot):
  #  photo_id = message.video.file_id
   # print(photo_id)