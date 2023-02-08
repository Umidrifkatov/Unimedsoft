from django.db import models
from django.contrib.auth.models import User as Us
import random





roles = [
        ('reg', 'Регистратор'),
        ('admin', 'Админ'),
        ('cash', 'Кассир'),
        ('nurse', 'Медсестра'),
        ('manager', 'Менеджер'),
        ('doc', 'Медсестра'),
        ('prom', 'Промоутер'),
        ('no', 'Никто'),

    ]










class Specialization(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название специальности')
    cabinet = models.IntegerField(default=0, null=True, verbose_name='Кабинет (можно оставить пустым)')

    def __str__(self):
        return f'{self.name}'
    
    class Meta:
        verbose_name = "Специальность"
        verbose_name_plural = "Специальности"

















class User(models.Model): # Пользователи
    user          = models.OneToOneField(Us, on_delete=models.CASCADE, null=True, blank=True)
    phone         = models.CharField(max_length=13, default="Нет",  verbose_name='Телефон')
    role          = models.CharField(max_length=50, choices=roles, default='no', verbose_name='Роль') # Роль (доктор, направитель, медсестра, регистратор, промоутер, кассир)
    promoteid     = models.IntegerField(default=0) # бонусный айди id должен иметь две составляющих врач-промоутер

    telegram_id   = models.CharField(max_length=25, null=True, blank=True, verbose_name='ID телеграм для оповещений', help_text = 'можно оставить пустым если еще не был получен')
    card          = models.CharField(max_length=16, blank=True, null=True, verbose_name='Номер банковской карты')
    addinfo       = models.CharField(max_length=250, null=True, default='Нет', verbose_name='Дополнительная информация', help_text = 'место работы, учебы, заметки и тд ' )
       
    specialization= models.ForeignKey(Specialization, on_delete=models.SET_NULL, null=True, verbose_name='Специальность если врач', blank=True)
    queue         = models.IntegerField(default=0, verbose_name='Очередь')


    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'
    
    
    class Meta:
         verbose_name = "Сотрудник"
         verbose_name_plural = "Сотрудники"





















class Patient(models.Model): # Пациенты
    sexes = [
        ('male', 'Мужчина'),
        ('female', 'Женщина'),
        
    ]

    def passgenerate():
        keys = '123456789qwertyuipasdfghjklzxcvbnmQWERTYUIPASDFGHJKLZXCVBNM'
        bit = 8
        bit2 = 0
        result = ''
        while bit > bit2:
            bit2 += 1
            result += random.choice(keys)
        return result

    # Необходимые персональные данные
    firstname  = models.CharField(max_length=50, verbose_name='Имя')
    lastname   = models.CharField(max_length=50, verbose_name='Фамилия')
    midname   = models.CharField(max_length=50, verbose_name='Отчество', null=True, blank=True)
    birthdate  = models.DateField(verbose_name='Дата рождения дд.мм.гггг', default='01.01.1999')
    sex        = models.CharField(max_length=10, choices=sexes, default='male', verbose_name='Пол')
    phone      = models.CharField(max_length=12, verbose_name='Телефон', default='')
    password   = models.CharField(max_length=16, verbose_name='Пароль', default=passgenerate)
    
    # Второстепенные данные
    country    = models.CharField(max_length=50, default='Узбекистан', null=True, blank=True, verbose_name='Страна')
    city       = models.CharField(max_length=50, null=True, blank=True, verbose_name='Город')
    adress     = models.CharField(max_length=100, default='Адрес', null=True, blank=True, verbose_name='Адрес')
    passport   = models.CharField(max_length=100, default='AA0000000 IIB 31.12.2099', null=True, blank=True, verbose_name='Паспортные данные')

    # Автоматические данные
    registeredby = models.ForeignKey(User, on_delete=models.PROTECT, null=True)
    regtime      = models.DateTimeField(auto_now_add=True)
    lastvisit    = models.DateTimeField()

    # Платежные данные
    balance = models.IntegerField(default=0)


    def __str__(self):
            return f'{self.firstname} {self.lastname} {self.birthdate.year}'
        
    class Meta:
        ordering = ['-regtime']
        verbose_name = "Пациент"
        verbose_name_plural = "Пациенты"










# результаты и товары  Оплата 
  
class Result(models.Model):
    result_text = models.TextField(10000, verbose_name='Текст ответа')
    addedby = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='Кем добавлен') # Кем добавлен
    time_added = models.DateTimeField(auto_now_add=True, null=True, verbose_name='Время загрузки')

    def __str__(self):
        return f' {self.addedby}'

    class Meta:
        ordering = ['-time_added']
        verbose_name = "Результат"
        verbose_name_plural = "Результаты"

class Item(models.Model):
    name = models.CharField(max_length=34, null=True, verbose_name="Название")
    qty = models.IntegerField(default=0, null=True, verbose_name="Количество")
    oncesubtrackt = models.IntegerField(default=0, verbose_name="Отнимать при использовании")
    dangerqty = models.IntegerField(default=0, null=True, verbose_name="Критическое количество")
    
    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"


    def __str__(self):
        return f'{self.name}'

class Payment(models.Model): 
    paymethod = models.CharField(max_length=50, null=False, verbose_name='Метод оплаты')
    summ      = models.IntegerField(default=0, verbose_name='Сумма')
    account   = models.ForeignKey(Patient, on_delete=models.SET_NULL, null=True, verbose_name='Пациент')
    casher    = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='Кассир' )
    comment   = models.CharField(max_length=100, null=True, default='нет', verbose_name='Комментарий' )
    time      = models.DateTimeField(auto_now_add=True, verbose_name='Время оплаты' )
    

    class Meta:
        verbose_name = "Транзакция оплаты"
        verbose_name_plural = "Транзакции оплаты"
    






#услуги
class ServiceCategory(models.Model): 
    name   = models.CharField(max_length=100, null=False, verbose_name='Название услуги')
    
    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = "Категория услуг"
        verbose_name_plural = "Категории услуг"


class ServiceSubcategory(models.Model):
    name      = models.CharField(max_length=100, null=False, verbose_name='Название')
    categeory = models.ForeignKey(ServiceCategory, on_delete=models.CASCADE, null=True, verbose_name='Категория', related_name='sub')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = "Подкатегория услуг"
        verbose_name_plural = "Подкатеории услуг"
