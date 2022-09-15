from django.core.exceptions import ValidationError
from django.db import models


class LeadState(models.Model):
    # pk экземпляров модели
    STATE_NEW = 1  # Новый
    STATE_IN_PROGRESS = 2  # В работе
    STATE_POSTPONED = 3  # Приостановлен
    STATE_DONE = 4  # Завершен
    name = models.CharField(
        u"Название",
        max_length=50,
        unique=True,
    )

#
# class Lead(models.Model):
#     STATUS_FLOW = (
#         (LeadState.STATE_NEW, LeadState.STATE_IN_PROGRESS),
#         (LeadState.STATE_IN_PROGRESS, LeadState.STATE_POSTPONED),
#         (LeadState.STATE_IN_PROGRESS, LeadState.STATE_DONE),
#         (LeadState.STATE_POSTPONED, LeadState.STATE_IN_PROGRESS),
#         (LeadState.STATE_POSTPONED, LeadState.STATE_DONE),
#     )
#
#     name = models.CharField(
#         max_length=255,
#         db_index=True,
#         verbose_name=u"Имя",
#     )
#     state = models.ForeignKey(
#         LeadState,
#         on_delete=models.PROTECT,
#         default=LeadState.STATE_NEW,
#         verbose_name=u"Состояние",
#     )
#
#     @staticmethod
#     def make_some_business_logic_1():
#         print('Метод выполняющий какую-то бизнес логику 1')
#
#     @staticmethod
#     def make_some_business_logic_2():
#         print('Метод выполняющий какую-то бизнес логику 2')
#
#     def make_state_in_progress(self):
#         if (self.state_id, LeadState.STATE_IN_PROGRESS) in self.STATUS_FLOW:
#             # Если переход статуса из текущего в статус state_in_progress разрешен
#             self.state_id = LeadState.STATE_IN_PROGRESS
#             # Меняем и сохраняем статус
#             self.save()
#             # Выполняем какую-то бизнес логику для такого типа перехода (из текущего статуса в state_in_progress)
#             self.make_some_business_logic_1()
#             # При успешной/неуспешной установке статуса возвращаем флаг, чтобы корректно обработать во вьюхе
#             return True
#         return False
#
#     def make_state_postponed(self):
#         if (self.state_id, LeadState.STATE_POSTPONED) in self.STATUS_FLOW:
#             self.state_id = LeadState.STATE_IN_PROGRESS
#             self.save()
#             self.make_some_business_logic_2()
#             return True
#         return False
#
#     def make_state_done(self):
#         if (self.state_id, LeadState.STATE_DONE) in self.STATUS_FLOW:
#             self.save()
#             self.make_some_business_logic_2()
#             self.make_some_business_logic_1()
#             self.make_some_business_logic_2()
#             return True
#         return False
#
#     def __str__(self):
#         return self.name + '__' + str(self.state_id)
#

"""

## Комментарий
Предполагается, что управление сменой статусов будет производится через методы, в которых реализована валидация:
    1. make_state_in_progress()
    2. make_state_postponed()
    3. make_state_done()
При необходимости в модель можно добавить валидацию, (ниже пример модели с общей валидацией).
Это полезно, если предполагается, к примеру, что статусы заказов могут менять в админке и есть вероятность ошибки.

"""


class Lead(models.Model):
    STATUS_FLOW = (
        (LeadState.STATE_NEW, LeadState.STATE_IN_PROGRESS),
        (LeadState.STATE_IN_PROGRESS, LeadState.STATE_POSTPONED),
        (LeadState.STATE_IN_PROGRESS, LeadState.STATE_DONE),
        (LeadState.STATE_POSTPONED, LeadState.STATE_IN_PROGRESS),
        (LeadState.STATE_POSTPONED, LeadState.STATE_DONE),
    )

    name = models.CharField(
        max_length=255,
        db_index=True,
        verbose_name=u"Имя",
    )
    state = models.ForeignKey(
        LeadState,
        on_delete=models.PROTECT,
        default=LeadState.STATE_NEW,
        verbose_name=u"Состояние",
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._prev_state = self.state_id

    @staticmethod
    def make_some_business_logic_1():
        print('Метод выполняющий какую-то бизнес логику 1')

    @staticmethod
    def make_some_business_logic_2():
        print('Метод выполняющий какую-то бизнес логику 2')

    def make_state_in_progress(self):
        if (self.state_id, LeadState.STATE_IN_PROGRESS) in self.STATUS_FLOW:
            # Если переход статуса из текущего в статус state_in_progress разрешен
            self.state_id = LeadState.STATE_IN_PROGRESS
            # Меняем и сохраняем статус
            self.save()
            # Выполняем какую-то бизнес логику для такого типа перехода (из текущего статуса в state_in_progress)
            self.make_some_business_logic_1()
            # При успешной/неуспешной установке статуса возвращаем флаг, чтобы корректно обработать во вьюхе
            return True
        return False

    def make_state_postponed(self):
        if (self.state_id, LeadState.STATE_POSTPONED) in self.STATUS_FLOW:
            self.state_id = LeadState.STATE_IN_PROGRESS
            self.save()
            self.make_some_business_logic_2()
            return True
        return False

    def make_state_done(self):
        if (self.state_id, LeadState.STATE_DONE) in self.STATUS_FLOW:
            self.save()
            self.make_some_business_logic_2()
            self.make_some_business_logic_1()
            self.make_some_business_logic_2()
            return True
        return False

    def clean(self):
        if (
                self._prev_state != self.state_id and
                (self._prev_state, self.state_id) not in Lead.STATUS_FLOW
        ):
            raise ValidationError('This is wrong status flow!')

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
        self._prev_state = self.state_id

    def __str__(self):
        return self.name + '__' + str(self.state_id)
