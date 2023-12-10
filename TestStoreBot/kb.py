from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

catalog = InlineKeyboardButton(text='🔍 Каталог', callback_data='categories-1')
basket = InlineKeyboardButton(text='🛒 Корзина', callback_data='basket-1')
faq = InlineKeyboardButton(text='❔ FAQ', callback_data='faq')
main_kb = InlineKeyboardBuilder().row(catalog).row(basket).row(faq).as_markup()


def categories_kb(categories: list[dict], page: int):
    kb = InlineKeyboardBuilder()
    pages_amount = len(categories) // 5 + 1
    for categories in categories[5 * (page - 1):page * 5]:
        kb.row(InlineKeyboardButton(text=categories["name"], callback_data=f'subcategories-1-{categories["id"]}'))
    left = InlineKeyboardButton(text='⬅️', callback_data=f'categories-{page - 1 if page != 1 else pages_amount}')
    count = InlineKeyboardButton(text=f'{page}/{pages_amount}', callback_data=f'categories-{page}')
    right = InlineKeyboardButton(text='➡️', callback_data=f'categories-{page + 1 if page != pages_amount else 1}')
    kb.row(left, count, right)
    return kb.as_markup()


def subcategories_kb(subcategories: list[dict], page: int, category: int):
    kb = InlineKeyboardBuilder()
    pages_amount = len(subcategories) // 5 + 1
    for subcategories in subcategories[5 * (page - 1):page * 5]:
        kb.row(InlineKeyboardButton(text=subcategories["name"], callback_data=f'products-1-{subcategories["id"]}'))
    left = InlineKeyboardButton(text='⬅️',
                                callback_data=f'subcategories-{page - 1 if page != 1 else pages_amount}-{category}')
    count = InlineKeyboardButton(text=f'{page}/{pages_amount}', callback_data=f'subcategories-{page}-{category}')
    right = InlineKeyboardButton(text='➡️',
                                 callback_data=f'subcategories-{page + 1 if page != pages_amount else 1}-{category}')
    kb.row(left, count, right)
    return kb.as_markup()


def products_kb(products: list[dict], page: int, subcategory: int):
    kb = InlineKeyboardBuilder()
    pages_amount = len(products) // 5 + 1
    for product in products[5 * (page - 1):page * 5]:
        kb.row(InlineKeyboardButton(text=product["name"], callback_data=f'product-{product["id"]}'))
    left = InlineKeyboardButton(text='⬅️',
                                callback_data=f'products-{page - 1 if page != 1 else pages_amount}-{subcategory}')
    count = InlineKeyboardButton(text=f'{page}/{pages_amount}', callback_data=f'products-{page}-{subcategory}')
    right = InlineKeyboardButton(text='➡️',
                                 callback_data=f'products-{page + 1 if page != pages_amount else 1}-{subcategory}')
    kb.row(left, count, right)
    return kb.as_markup()


def product_kb(product_id: int):
    add_to_basket = InlineKeyboardButton(text='Добавить в корзину', callback_data=f'add_to_basket-{product_id}')
    kb = InlineKeyboardBuilder().row(add_to_basket).as_markup()
    return kb


def confirm_kb(user_id: int, product_id: int, amount: int):
    confirm = InlineKeyboardButton(text='✅ Подтвердить', callback_data=f'confirm-{user_id}-{product_id}-{amount}')
    kb = InlineKeyboardBuilder().row(confirm).as_markup()
    return kb


def basket_kb(basket: list[dict], page: int):
    kb = InlineKeyboardBuilder()
    pages_amount = len(basket) // 5 + 1
    for product in basket[5 * (page - 1):page * 5]:
        kb.row(InlineKeyboardButton(text=product["name"], callback_data=f'inspect-{product["id"]}-{product["product_id"]}'))
    left = InlineKeyboardButton(text='⬅️', callback_data=f'basket-{page - 1 if page != 1 else pages_amount}')
    count = InlineKeyboardButton(text=f'{page}/{pages_amount}', callback_data=f'basket-{page}')
    right = InlineKeyboardButton(text='➡️', callback_data=f'basket-{page + 1 if page != pages_amount else 1}')
    kb.row(left, count, right)
    return kb.as_markup()


def inspect_kb(product_id: int):
    buy = InlineKeyboardButton(text='Оформить заказ', callback_data=f'buy-{product_id}')
    delete = InlineKeyboardButton(text='Удалить из корзины', callback_data=f'delete-{product_id}')
    kb = InlineKeyboardBuilder().row(buy).row(delete).as_markup()
    return kb


def buy_kb(link: str):
    buy = InlineKeyboardButton(text='Оплатить', url=link)
    kb = InlineKeyboardBuilder().row(buy).as_markup()
    return kb
