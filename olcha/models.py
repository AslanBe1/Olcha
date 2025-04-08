from multiprocessing.managers import Value

from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify


# Create your models here.

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Category(BaseModel):
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to='images/')
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.slug:
            self.slug = slugify(self.name)
            super(Category, self).save(*args, **kwargs)


class SubCategory(BaseModel):
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to='images/')
    slug = models.SlugField(max_length=50, unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='sub_categories')

    def __str__(self):
        return self.name

class Product(BaseModel):
    class RatingChoices(models.IntegerChoices):
        ONE = 1
        TWO = 2
        THREE = 3
        FOUR = 4
        FIVE = 5

    name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()
    discount = models.FloatField()
    description = models.TextField()
    rating = models.IntegerField(choices=RatingChoices.choices, default=RatingChoices.ONE)
    slug = models.SlugField(unique=True)
    sub_category = models.ForeignKey(SubCategory, on_delete=models.CASCADE, related_name='product')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.slug:
            self.slug = slugify(self.name)
            super(Product, self).save(*args, **kwargs)


class Image(BaseModel):
    image = models.ImageField(upload_to='media/')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='image')



class Comment(BaseModel):
    class RatingChoices(models.IntegerChoices):
        ONE = 1
        TWO = 2
        THREE = 3
        FOUR = 4
        FIVE = 5

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments')
    comment = models.TextField()
    rating = models.IntegerField(choices=RatingChoices.choices, default=RatingChoices.ONE)

    def __str__(self):
        return f"{self.user} => {self.product} => {self.comment}"


class Attribute(BaseModel):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class AttributeValue(BaseModel):
    value = models.CharField(max_length=50)

    def __str__(self):
        return self.value

class ProductAttribute(BaseModel):
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE, related_name='product_attribute')
    attribute_value = models.ForeignKey(AttributeValue, on_delete=models.CASCADE, related_name='product_attribute')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_attribute')

    def __str__(self):
        return f"{self.attribute} => {self.attribute_value} => {self.product}"



class Order(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    address = models.CharField(max_length=50)
    is_paid = models.BooleanField(default=False)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=50,choices=[('panding', 'Panding'), ('complected', 'complected')], default='pending')

    def __str__(self):
        return f"{self.user} => {self.is_paid} => {self.address} => {self.created_at}"


class OrderItem(BaseModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_items')
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        if self.product.quantity >= self.quantity:
            self.product.quantity -= self.quantity
            self.product.save()
        else:
            raise ValueError('Not enough stock for this product')

        super().save(*args, **kwargs)

    def get_total(self):
        return self.quantity * self.price

    def __str__(self):
        return f"{self.order} => {self.product}"