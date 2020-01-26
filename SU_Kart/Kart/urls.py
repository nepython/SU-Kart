from django.urls import path
from . import views
#from . import views as core_views
from django.conf.urls import url
from django.conf import settings
from django.contrib.staticfiles.urls import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.auth import views as auth_views

app_name = 'Kart'

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('product_list/', views.product_list, name='product_list'),
    path('<slug:title>/',
         views.product_detail,
         name='product_detail'),
    path('add/<slug:title>/',
         views.cart_order,
         name='cart_order'),
    path('remove/<slug:title>/',
         views.cart_remove,
         name='cart_remove'),
    url(r'^$', views.searchposts, name='searchposts'),
]

#urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)