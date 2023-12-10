import asyncio
import logging
from datetime import datetime

from aiogram import Bot, Dispatcher, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.types import FSInputFile, Message, CallbackQuery
from aiogram.filters.command import Command
from redis.asyncio import Redis

from config import *
import kb
from states import *
from db import DB

from payments import *

db = DB()

redis = Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    db=REDIS_DB
)
storage = RedisStorage(redis)

bot = Bot(token=TOKEN)
dp = Dispatcher(storage=storage)

logging.basicConfig(filename="all.log", level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(filename)s function: %(funcName)s line: %(lineno)d - %(message)s')
errors = logging.getLogger("errors")
errors.setLevel(logging.ERROR)
fh = logging.FileHandler("errors.log")
formatter = logging.Formatter(
    '%(asctime)s - %(levelname)s - %(filename)s function: %(funcName)s line: %(lineno)d - %(message)s')
fh.setFormatter(formatter)
errors.addHandler(fh)


@dp.message(Command('start'))
async def start(message: Message):
    try:
        status = await bot.get_chat_member(chat_id=CHANNEL_ID, user_id=message.from_user.id)
        if status.model_dump()['status'] != 'left':
            if not await db.user_exists(str(message.from_user.id)):
                await db.insert_in_users(str(message.from_user.id))
            await message.answer(f'Привет, {message.from_user.first_name}.', reply_markup=kb.main_kb)
        else:
            await message.answer('Сначала нужно подписаться на наш [канал](https://t.me/test_store_blablabla)\.',
                                 parse_mode='MarkdownV2')
    except Exception as e:
        errors.error(e, exc_info=True)


@dp.callback_query(F.data.split('-')[0] == 'categories')
async def catalog(call: CallbackQuery):
    try:
        await call.answer()
        await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id,
                                    text='Выберите категорию.',
                                    reply_markup=kb.categories_kb(await db.get_categories(),
                                                                  int(call.data.split('-')[1])))
    except Exception as e:
        errors.error(e, exc_info=True)


@dp.callback_query(F.data.split('-')[0] == 'subcategories')
async def subcategories(call: CallbackQuery):
    try:
        await call.answer()
        await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id,
                                    text='Выберите подкатегорию.',
                                    reply_markup=kb.subcategories_kb(
                                        await db.get_subcategories(int(call.data.split('-')[2])),
                                        int(call.data.split('-')[1]),
                                        int(call.data.split('-')[2])))
    except Exception as e:
        errors.error(e, exc_info=True)


@dp.callback_query(F.data.split('-')[0] == 'products')
async def products(call: CallbackQuery):
    try:
        await call.answer()
        await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id,
                                    text='Выберите товар.',
                                    reply_markup=kb.products_kb(
                                        await db.get_products(int(call.data.split('-')[2])),
                                        int(call.data.split('-')[1]),
                                        int(call.data.split('-')[2])))
    except Exception as e:
        errors.error(e, exc_info=True)


@dp.callback_query(F.data.split('-')[0] == 'product')
async def product(call: CallbackQuery):
    try:
        await call.answer()
        product_info = await db.get_product_info(int(call.data.split('-')[1]))
        await call.message.answer_photo(photo=FSInputFile(f'./photos/{call.data.split("-")[1]}.png'),
                                        caption=f'Название: {product_info["name"]}.\n'
                                                f'Описание: {product_info["description"]}.\n',
                                        reply_markup=kb.product_kb(int(call.data.split("-")[1])))
    except Exception as e:
        errors.error(e, exc_info=True)


@dp.callback_query(F.data.split('-')[0] == 'add_to_basket')
async def add_to_basket(call: CallbackQuery, state: FSMContext):
    try:
        await call.answer()
        await call.message.answer('Укажите кол-во товара.')
        await state.set_state(AddToBasket.amount)
        await state.update_data(product_id=int(call.data.split('-')[-1]))
    except Exception as e:
        errors.error(e, exc_info=True)


@dp.message(AddToBasket.amount)
async def add_to_basket_amount(message: Message, state: FSMContext):
    try:
        if message.text.isnumeric():
            await state.update_data(amount=message.text)
            data = await state.get_data()
            product_info = await db.get_product_info(int(data['product_id']))
            await message.answer_photo(photo=FSInputFile(f'./photos/{data["product_id"]}.png'),
                                       caption=f'Название: {product_info["name"]}.\n'
                                               f'Описание: {product_info["description"]}.\n'
                                               f'Количество: {message.text}.\n',
                                       reply_markup=kb.confirm_kb(int(await db.get_user_id(str(message.from_user.id))),
                                                                  int(data['product_id']),
                                                                  int(message.text)))
            await state.set_state(AddToBasket.confirm)
        else:
            await message.answer('Кол-во должно быть указанно числом.')
    except Exception as e:
        errors.error(e, exc_info=True)


@dp.callback_query(AddToBasket.confirm, F.data.split('-')[0] == 'confirm')
async def add_to_basket_confirm(call: CallbackQuery, state: FSMContext):
    try:
        await call.answer()
        data = await state.get_data()
        product_info = await db.get_product_info(int(data['product_id']))
        await db.insert_in_basket(int(call.data.split('-')[1]),
                                  int(call.data.split('-')[2]),
                                  product_info['name'],
                                  product_info['description'],
                                  int(call.data.split('-')[3]))
        await call.message.answer('Товар добавлен в корзину.')
        await state.clear()
    except Exception as e:
        errors.error(e, exc_info=True)


@dp.callback_query(F.data.split('-')[0] == 'basket')
async def basket(call: CallbackQuery):
    try:
        await call.answer()
        await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id,
                                    text='Ваша корзина:',
                                    reply_markup=kb.basket_kb(await db.get_basket(
                                        int(await db.get_user_id(str(call.from_user.id)))),
                                                              int(call.data.split('-')[1])))
    except Exception as e:
        errors.error(e, exc_info=True)


@dp.callback_query(F.data.split('-')[0] == 'inspect')
async def inspect(call: CallbackQuery):
    try:
        await call.answer()
        product_info = await db.get_basket_product_info(int(call.data.split('-')[1]))
        await call.message.answer_photo(photo=FSInputFile(f'photos/{product_info["product_id"]}.png'),
                                        caption=f'Название: {product_info["name"]}.\n'
                                                f'Описание: {product_info["description"]}.\n'
                                                f'Количество: {product_info["amount"]}.\n',
                                        reply_markup=kb.inspect_kb(int(product_info["id"])))
    except Exception as e:
        errors.error(e, exc_info=True)


@dp.callback_query(F.data.split('-')[0] == 'delete')
async def delete(call: CallbackQuery):
    try:
        await call.answer()
        await db.delete_from_basket(int(call.data.split('-')[1]))
        await call.message.answer('Товар удален из корзины.')
    except Exception as e:
        errors.error(e, exc_info=True)


@dp.callback_query(F.data.split('-')[0] == 'buy')
async def buy(call: CallbackQuery, state: FSMContext):
    try:
        await call.answer()
        await call.message.answer('Введите адрес для доставки.')
        await state.set_state(Buy.address)
        await state.update_data(product_id=call.data.split('-')[1])
    except Exception as e:
        errors.error(e, exc_info=True)


@dp.message(Buy.address)
async def address(message: Message, state: FSMContext):
    try:
        await state.update_data(address=message.text)
        data = await state.get_data()
        product_info = await db.get_basket_product_info(int(data['product_id']))
        url, payment_id = create_payment(100, f'Название: {product_info["name"]}.\n'
                                              f'Описание: {product_info["description"]}.\n'
                                              f'Количество: {product_info["amount"]}.\n'
                                              f'Адрес доставки: {message.text}.\n')
        await message.answer_photo(photo=FSInputFile(f'photos/{product_info["product_id"]}.png'),
                                   caption=f'Название: {product_info["name"]}.\n'
                                           f'Описание: {product_info["description"]}.\n'
                                           f'Количество: {product_info["amount"]}.\n'
                                           f'Адрес доставки: {message.text}.\n',
                                   reply_markup=kb.buy_kb(url))
        c = 0
        paid = False
        while True:
            if get_payment_status(payment_id) == 'waiting_for_capture':
                paid = True
                break
            elif c == 600:
                await message.answer('Платеж отменен.\n'
                                     'Причина: прошло 10 минут с момента создания платежа.')
                break
            else:
                await asyncio.sleep(1)
                c += 1
        if paid:
            response = json.loads(confirm_payment(payment_id))
            if response['status'] == 'succeeded':
                await db.delete_from_basket(product_info['id'])
                await message.answer('Успешно оплачено.')
            else:
                await message.answer('Произошла ошибка.\n'
                                     'Деньги будут возвращены вам в течение 24 часов.')
        await state.clear()
    except Exception as e:
        errors.error(e, exc_info=True)


@dp.callback_query(F.data == 'faq')
async def faq(call: CallbackQuery):
    try:
        await call.answer()
        await call.message.answer('Ответы на частозадаваемые вопросы.')
    except Exception as e:
        errors.error(e, exc_info=True)


@dp.message(Command('id'))
async def ids(message: Message):
    try:
        await message.answer(str(message.from_user.id))
    except Exception as e:
        errors.error(e, exc_info=True)


@dp.message(Command('gid'))
async def gids(message: Message):
    try:
        await message.answer(str(message.chat.id))
    except Exception as e:
        errors.error(e, exc_info=True)


async def main():
    await db.connect()
    await dp.start_polling(bot)


if __name__ == '__main__':
    print(f'Бот запущен ({datetime.now().strftime("%H:%M:%S %d.%m.%Y")}).')
    asyncio.run(main())
