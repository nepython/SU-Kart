from django.contrib import admin
from .models import WebsiteUser, Company, Product
from import_export.admin import ImportExportModelAdmin

@admin.register(Product)
class ProductAdmin(ImportExportModelAdmin):
    list_display = ['image', 'title', 'description', 'price', 'company','link']
    list_display_links = ['link']
    list_editable = ['price', 'company', 'description', 'title', 'image']


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ['company','link']
    list_display_links = ['link']
    list_editable = ['company']


@admin.register(WebsiteUser)
class WebsiteUser(admin.ModelAdmin):
    list_display = ['Task','UID', 'name', 'Email', 'DOB', 'City', 'State', 'currency','order','complain','correspondent']
    list_editable = ['currency']
