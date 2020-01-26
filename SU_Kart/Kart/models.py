from django.core.validators import MinValueValidator
from django.db import models
from django.urls import reverse


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
    name = models.TextField(max_length=200,
                            db_index=True)
    Email = models.EmailField(max_length=50,
                              db_index=True)
    DOB = models.DateField()
    City = models.TextField(max_length=20,
                            db_index=True)
    State = models.TextField(max_length=40,
                             db_index=True)
    currency = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    order = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True, null=True)
    correspondent = models.CharField(max_length=10,blank=True, null=True)
    complain = models.CharField(max_length=200, blank=True, null=True)

    """class Shopper(models.Model):
        complain = models.TextField(max_length=500,
                                    db_index=True)

        class Meta:
            ordering = ('order',)

    class Delivery():
        shopper = models.TextField(max_length=50,
                                   db_index=True)

        class Meta:
            ordering = ('name',)"""

    class Meta:
        ordering = ('name',)

    def get_absolute_url(self):
        return reverse('Kart:product_detail', args=self.UID)

    def __str__(self):
        return self.name