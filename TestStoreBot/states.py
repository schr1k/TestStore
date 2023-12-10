from aiogram.fsm.state import State, StatesGroup


class AddToBasket(StatesGroup):
    amount = State()
    confirm = State()


class Buy(StatesGroup):
    address = State()
    money = State()
