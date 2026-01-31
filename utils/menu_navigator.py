from typing import Tuple

from aiogram.types import ReplyKeyboardMarkup

from app import keyboards
from config import (MenuStates as Ms,
                    State, DialogStates as Ds, SecondBlockStates as SBS,
                    FirstBlockStates as FBS, ThirdBlockStates as TBS,
                    FourthBlockStates as F4BS, FifthBlockStates as F5BS)
import app.keyboards

async def step_back_check(state: str, sub_status: str) -> (
        Tuple[State, ReplyKeyboardMarkup] | bool
):
    # Проверка основных вкладок
    if state == Ms.main_menu.state:
        return Ms.main_menu, keyboards.main_menu

    if state == Ms.my_rate.state:
        return Ms.main_menu, keyboards.main_menu

    if state == Ds.waiting_confirm_user_agreement.state:
        return Ds.waiting_confirm_user_agreement, keyboards.confirm_and_register1

    elif state == Ms.my_lessons.state:
        return Ms.main_menu, keyboards.main_menu

    elif state == Ms.profile.state:
        return Ms.main_menu, keyboards.main_menu

    elif state == Ms.pro_chapter.state:
        return Ms.main_menu, keyboards.main_menu

    elif state == Ms.support.state:
        return Ms.main_menu, keyboards.main_menu

    elif state == Ms.update_rate.state:
        if sub_status == 'PRO':
            return Ms.my_rate, keyboards.my_rate_1
        else:
            return Ms.my_rate, keyboards.my_rate_0

    elif state == SBS.wait_for_letsgo.state:
        return Ms.my_lessons, keyboards.my_lessons

    elif state == FBS.waiting_time_for_work.state:
        return Ms.my_lessons, keyboards.my_lessons

    elif state == TBS.state1.state:
        return Ms.my_lessons, keyboards.my_lessons

    elif state == F4BS.state1.state:
        return Ms.my_lessons, keyboards.my_lessons

    elif state == F5BS.state1.state:
        return Ms.my_lessons, keyboards.my_lessons
    else:
        return False


# async def get_keyboard_by_state(state: State):

