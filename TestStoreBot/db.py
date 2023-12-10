import asyncpg

from config import *


class DB:
    def __init__(self):
        self.pool = None

    async def connect(self):
        self.pool = await asyncpg.create_pool(
            user=POSTGRES_USER,
            password=POSTGRES_PASSWORD,
            host=POSTGRES_HOST,
            port=POSTGRES_PORT,
            database=POSTGRES_DB
        )

    async def user_exists(self, telegram_id: str) -> bool:
        async with self.pool.acquire() as connection:
            async with connection.transaction():
                result = await connection.fetchrow(
                    'SELECT telegram_id FROM main_users WHERE telegram_id = $1', telegram_id
                )
                return False if result is None else True

    async def get_categories(self) -> list[dict]:
        async with self.pool.acquire() as connection:
            async with connection.transaction():
                result = await connection.fetch(
                    'SELECT id, name FROM main_categories',
                )
                return [dict(i) for i in result]

    async def get_subcategories(self, category: int) -> list[dict]:
        async with self.pool.acquire() as connection:
            async with connection.transaction():
                result = await connection.fetch(
                    'SELECT id, name FROM main_subcategories WHERE category_id = $1', category
                )
                return [dict(i) for i in result]

    async def get_products(self, subcategory: int) -> list[dict]:
        async with self.pool.acquire() as connection:
            async with connection.transaction():
                result = await connection.fetch(
                    'SELECT id, name FROM main_products WHERE subcategory_id = $1', subcategory
                )
                return [dict(i) for i in result]

    async def get_basket(self, user_id: int) -> list[dict]:
        async with self.pool.acquire() as connection:
            async with connection.transaction():
                result = await connection.fetch(
                    'SELECT id, product_id, name, description FROM main_basket WHERE user_id = $1', user_id
                )
                return [dict(i) for i in result]

    async def get_product_info(self, product_id: int) -> dict:
        async with self.pool.acquire() as connection:
            async with connection.transaction():
                result = await connection.fetchrow(
                    'SELECT name, description FROM main_products WHERE id = $1', product_id
                )
                return dict(result)

    async def get_basket_product_info(self, product_id: int) -> dict:
        async with self.pool.acquire() as connection:
            async with connection.transaction():
                result = await connection.fetchrow(
                    'SELECT id, product_id, name, description, amount FROM main_basket WHERE id = $1', product_id
                )
                return dict(result)

    async def get_user_id(self, telegram_id: str) -> str:
        async with self.pool.acquire() as connection:
            async with connection.transaction():
                result = await connection.fetchrow(
                    'SELECT id FROM main_users WHERE telegram_id = $1', telegram_id
                )
                return dict(result)['id']

    async def insert_in_users(self, telegram_id: str):
        async with self.pool.acquire() as connection:
            async with connection.transaction():
                await connection.execute(
                    'INSERT INTO main_users (telegram_id) VALUES($1)', telegram_id
                )

    async def insert_in_basket(self, user_id: int, product_id: int, name: str, description: str, amount: int):
        async with self.pool.acquire() as connection:
            async with connection.transaction():
                await connection.execute(
                    'INSERT INTO main_basket (user_id, product_id, name, description, amount) '
                    'VALUES($1, $2, $3, $4, $5)',
                    user_id, product_id, name, description, amount
                )

    async def delete_from_basket(self, product_id: int):
        async with self.pool.acquire() as connection:
            async with connection.transaction():
                await connection.execute(
                    'DELETE FROM main_basket WHERE id = $1', product_id
                )
