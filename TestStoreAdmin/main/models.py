from django.db import models


class Categories(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class SubCategories(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Подкатегория'
        verbose_name_plural = 'Подкатегории'

    def __str__(self):
        return self.name


class Products(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=100, default='Описание не указано.')
    subcategory = models.ForeignKey(SubCategories, to_field='id', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return self.name


class Users(models.Model):
    id = models.AutoField(primary_key=True)
    telegram_id = models.CharField(max_length=50)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.telegram_id


class Basket(models.Model):
    id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    amount = models.IntegerField(default=1)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, default='Не указано')
    description = models.CharField(max_length=100, default='Не указано')

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Корзина'

    def __str__(self):
        return self.id
