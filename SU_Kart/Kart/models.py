from django.core.validators import MinValueValidator
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Company(models.Model):
    company = models.CharField(max_length=200,
                               db_index=True)
    link = "Edit"  # Reason for using it is the requirement of a list_display link in case all fields are to be edited(kindof work around)

    class Meta:
        verbose_name_plural = 'Companies'  # Since it's showing Companys by default

    def __str__(self):
        return self.company


class Product(models.Model):
    objects = models.Manager
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products', blank=True)
    title = models.CharField(max_length=50,
                             db_index=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    link = "Edit"

    class Meta:
        ordering = ('title',)

    def get_absolute_url(self):
        return reverse('Kart:product_detail', args=[self.title])

    def __str__(self):
        return self.title


class WebsiteUser(models.Model):
    objects = models.Manager
    Task = models.TextField(max_length=10,
                           db_index=True)
    UID = models.CharField(max_length=50,
                           db_index=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE) #do it later using one-to-one-field
    DOB = models.DateField(null=True)
    City = models.TextField(max_length=20,
                            db_index=True)
    State = models.TextField(max_length=40,
                             db_index=True)
    currency = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)], null=True, blank=True)
    order = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True, null=True)
    correspondent = models.CharField(max_length=10,blank=True, null=True)
    complain = models.CharField(max_length=200, blank=True, null=True)

    # class Shopper(models.Model):
    #     complain = models.TextField(max_length=500,
    #                                 db_index=True)
    #
    #     class Meta:
    #         ordering = ('order',)
    #
    # class Delivery():
    #     shopper = models.TextField(max_length=50,
    #                                db_index=True)
    #
    #     class Meta:
    #         ordering = ('name',)

    class Meta:
        ordering = ('user',)

    def get_absolute_url(self):
        return reverse('Kart:product_detail', args=self.UID)

    def __str__(self):
        return self.user.name

    # @receiver(post_save, sender=User)
    # def create_user_profile(sender, instance, created, **kwargs):
    #     if created:
    #         WebsiteUser.objects.create(user=instance)
    #
    # @receiver(post_save, sender=User)
    # def save_user_profile(sender, instance, **kwargs):
    #     instance.websiteuser.save()