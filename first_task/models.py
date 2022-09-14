from django.db import models

# Исходный вариант


class Delivery(models.Model):
    state = models.ForeignKey('DeliveryState', related_name='deliverys', on_delete=models.PROTECT)
    address = models.CharField(max_length=1000)

    class Meta:
        verbose_name = u"Доставка"
        verbose_name_plural = u"Доставки"


class DeliveryState(models.Model):
    class Meta:
        verbose_name = u"Состояние доставки"
        verbose_name_plural = u"Состояния доставок"

    STATE_NEW = 1  # Новая
    STATE_ISSUED = 2  # Выдана курьеру
    STATE_DELIVERED = 3  # Доставлена
    STATE_HANDED = 4  # Курьер сдал
    STATE_REFUSED = 5  # Отказ
    STATE_PAID_REFUSED = 6  # Отказ с оплатой курьеру
    STATE_COMPLETE = 7  # Завершена
    STATE_NONE = 8  # Не определено

    @classmethod
    def get_new(cls):
        return cls.objects.get(pk=cls.STATE_NEW)

    @classmethod
    def get_issued(cls):
        return cls.objects.get(pk=cls.STATE_ISSUED)

    @classmethod
    def get_delivered(cls):
        return cls.objects.get(pk=cls.STATE_DELIVERED)

    @classmethod
    def get_handed(cls):
        return cls.objects.get(pk=cls.STATE_HANDED)

    @classmethod
    def get_refused(cls):
        return cls.objects.get(pk=cls.STATE_REFUSED)

    @classmethod
    def get_paid_refused(cls):
        return cls.objects.get(pk=cls.STATE_PAID_REFUSED)

    @classmethod
    def get_complete(cls):
        return cls.objects.get(pk=cls.STATE_COMPLETE)

    @classmethod
    def get_none(cls):
        return cls.objects.get(pk=cls.STATE_NONE)


"""
 Вариант_1
 Возможно немного упросить код, с помощью вынесения фильтрации в отдельный метод _filering;
 От отдельных методов никуда не ушли, но стало красивее.
 """

# class DeliveryState(models.Model):
#     class Meta:
#         verbose_name = u"Состояние доставки"
#         verbose_name_plural = u"Состояния доставок"
#
#     STATE_NEW = 1  # Новая
#     STATE_ISSUED = 2  # Выдана курьеру
#     STATE_DELIVERED = 3  # Доставлена
#     STATE_HANDED = 4  # Курьер сдал
#     STATE_REFUSED = 5  # Отказ
#     STATE_PAID_REFUSED = 6  # Отказ с оплатой курьеру
#     STATE_COMPLETE = 7  # Завершена
#     STATE_NONE = 8  # Не определено
#
#     @classmethod
#     def _filering(cls, pk):
#         return cls.objects.get(pk=pk)
#
#     @classmethod
#     def get_new(cls):
#         return cls._filering(cls.STATE_NEW)
#
#     @classmethod
#     def get_issued(cls):
#         return cls._filering(cls.STATE_ISSUED)
#
#     @classmethod
#     def get_delivered(cls):
#         return cls._filering(cls.STATE_DELIVERED)
#
#     @classmethod
#     def get_handed(cls):
#         return cls._filering(cls.STATE_HANDED)
#
#     @classmethod
#     def get_refused(cls):
#         return cls._filering(cls.STATE_REFUSED)
#
#     @classmethod
#     def get_paid_refused(cls):
#         return cls._filering(cls.STATE_PAID_REFUSED)
#
#     @classmethod
#     def get_complete(cls):
#         return cls._filering(cls.STATE_COMPLETE)
#
#     @classmethod
#     def get_none(cls):
#         return cls._filering(cls.STATE_NONE)

"""
 Вариант_2
 Использование pk в качестве айди выглядит довольно странным (при удалении/добавлении новой записи, 
 pk может измениться). 
 Добавив поле ModelChoiceField можно избавиться от однообразных методов + в качестве айди статуса будет отдельный
 ключ, это упростит код, в тоже время поменяет интерфейс, который предоставляет класс.
"""

# class Delivery(models.Model):
#     state = models.ForeignKey('DeliveryState', related_name='deliverys', on_delete=models.PROTECT)
#     address = models.CharField(max_length=1000)
#
#     class Meta:
#         verbose_name = u"Доставка"
#         verbose_name_plural = u"Доставки"
#
# class DeliveryState(models.Model):
#     class Meta:
#         verbose_name = u"Состояние доставки"
#         verbose_name_plural = u"Состояния доставок"
#
#     CHOICES = (
#         ('STATE_NEW', 'New'),
#         ('STATE_ISSUED', 'Issued'),
#         ('STATE_DELIVERED', 'Delivered'),
#         ('STATE_HANDED', 'Handed'),
#         ('STATE_REFUSED', 'Refused'),
#         ('STATE_PAID_REFUSED', 'Paid Refuced'),
#         ('STATE_COMPLETE', 'Complete'),
#         ('STATE_NONE', 'None'),
#     )
#
#     status = models.CharField(max_length=50, choices=CHOICES)

#  Тогда фильтрация будет такого вида
#  Delivery.objects.filter(state__status='STATE_PAID_REFUSED')

"""
 Вариант_3
 Можно вынести методы в качестве методов QuerySet'a при редактировании менеджера модели, однако это так же поменять
 интерфейс,
 к стандартному менеджеру модели objects добавим все перечисленные методы,
 получить все отмененные заказы мы сможем например таким образом:
"""


# Delivery.objects.filter(state=State.objects.get_refused())
# А чтобы поддержать интерфейс, нужно получать так:
# Delivery.objects.filter(state=State.get_refused())

"""
Вариант_4
Можно вынести методы в ProxyModel и наследоваться от основной модели, это визуально разгрузит основную модель;
Но мы не избавимся от однообразных методов в прокси модели.
"""


#
# class DeliveryStateGeneral(models.Model):
#     class Meta:
#         verbose_name = u"Состояние доставки"
#         verbose_name_plural = u"Состояния доставок"
#
#     STATE_NEW = 1  # Новая
#     STATE_ISSUED = 2  # Выдана курьеру
#     STATE_DELIVERED = 3  # Доставлена
#     STATE_HANDED = 4  # Курьер сдал
#     STATE_REFUSED = 5  # Отказ
#     STATE_PAID_REFUSED = 6  # Отказ с оплатой курьеру
#     STATE_COMPLETE = 7  # Завершена
#     STATE_NONE = 8  # Не определено
#
#
# class DeliveryState(DeliveryStateGeneral):
#     class Meta:
#         proxy = True
#
#     @classmethod
#     def get_new(cls):
#         return cls.objects.get(pk=cls.STATE_NEW)
#
#     @classmethod
#     def get_issued(cls):
#         return cls.objects.get(pk=cls.STATE_ISSUED)
#
#     @classmethod
#     def get_delivered(cls):
#         return cls.objects.get(pk=cls.STATE_DELIVERED)

"""
Вариант_5
Так же можно принимать параметр соответствующий статусу и фильтровать все в одном методе,
если у нас python 3.10, то все это красиво упакуется в конструкцию match/case.
Однако это так же поменяет интерфейс.
"""

# class DeliveryState(models.Model):
#     class Meta:
#         verbose_name = u"Состояние доставки"
#         verbose_name_plural = u"Состояния доставок"
#
#     STATE_NEW = 1  # Новая
#     STATE_ISSUED = 2  # Выдана курьеру
#     STATE_DELIVERED = 3  # Доставлена
#     STATE_HANDED = 4  # Курьер сдал
#     STATE_REFUSED = 5  # Отказ
#     STATE_PAID_REFUSED = 6  # Отказ с оплатой курьеру
#     STATE_COMPLETE = 7  # Завершена
#     STATE_NONE = 8  # Не определено
#
#     @classmethod
#     def filtering(cls, status):
#         match status:
#             case 'STATE_NEW':
#                 return cls.objects.get(pk=cls.STATE_NEW)
#             case 'STATE_DELIVERED':
#                 return cls.objects.get(pk=cls.STATE_DELIVERED)
#             case 'STATE_ISSUED':
#                 return cls.objects.get(pk=cls.STATE_ISSUED)
#             case _:
#                 raise DeliveryState.DoesNotExist

# Тогда фильтровать мы сможем таким образом
# Delivery.objects.filter(state=State.objects.filtering('STATE_REFUSED'))
# А чтобы поддержать интерфейс, нужно получать так:
# Delivery.objects.filter(state=State.get_refused())
