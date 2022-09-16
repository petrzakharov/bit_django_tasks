from django.db import models
from django.db import transaction

# class Deal(models.Model):
#     # user = models.ForeignKey('User', on_delete=models.PROTECT, related_name='deals')
#     # product = models.ForeignKey('Product', on_delete=models.PROTECT, related_name='deals')
#     # publication = models.DateTimeField(auto_now_add=True)
#
#     # Исходный вариант
#     @classmethod
#     def buy(cls, user, item_id):
#         product_qs = Product.objects.filter(item_id=item_id)
#         if product_qs.exists():
#             product = product_qs[0]
#             if product.available:
#                 user.withdraw(product.price)
#                 send_email_to_user_of_buy_product(user)
#                 product.available = False
#                 product.buyer = user
#                 product.save()
#                 return True
#         else:
#             return False


"""

## Комментарий
1. Необходимо проверять if product.available and user.balance >= product.price. Либо мы должны быть 
уверены, что метод user.withdraw это проверит сам.
2. Избыточно создавать 2 кверисета и держать их в памяти, (product_qs, product_qs[0]). 
3. Для операций с покупкой и переводом денег желательно использовать транзакции, это позволит откатить состояние при 
возникновении непредвиденной ошибки в запросах и сохранить согласованность данных в бд;
4. Перед вторым return else излишне;
5. Отправка емейла может быть долгой операцией, ее нужно выполнять в самом конце (иначе товар могут 
купить 2 раза)

Ниже вариант, как может выглядеть исправленный код:

"""


class Deal2(models.Model):
    # user = models.ForeignKey('User', on_delete=models.PROTECT, related_name='deals')
    # product = models.ForeignKey('Product', on_delete=models.PROTECT, related_name='deals')
    # publication = models.DateTimeField(auto_now_add=True)

    # Исправленный вариант
    @classmethod
    def buy(cls, user, item_id):
        product = Product.objects.filter(item_id=item_id).first()
        if product and product.available:
            with transaction.atomic():
                user.withdraw(product.price)
                product.available = False
                product.buyer = user
                product.save()
                send_email_to_user_of_buy_product(user)
                return True
        return False