import reserve as reserve
from django.db import models
from django.contrib.auth.models import User
from django.db.models import ImageField


# class Category(models.Model):
#     sort = models.CharField(max_length=255)
#
#     def __str__(self):
#         return '{}'.format(self.sort)


class Product(models.Model):
    name = models.CharField(max_length=255)
    # category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='product_category')
    image = ImageField(upload_to='cloth')
    price = models.IntegerField()
    quantity = models.IntegerField(default=0)
    description = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)
    hit = models.IntegerField(default=0)

    def get_absolute_url(self):
        return reserve('photo:photo_detail', args=[str(self.id)])

    def __str__(self):
        return '{} {}'.format(self.name, self.pub_date)
