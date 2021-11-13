from django.conf.urls.static import static
from django.conf import settings
from django.urls import path
from django.views.generic.detail import DetailView
from .views import *
from .models import Product

app_name = 'product'

urlpatterns = [
    path('', product_list, name='product_list'),
    path('detail/<int:pk>/', DetailView.as_view(model=Product, template_name='product/detail.html'), name='product_detail'),
    path('detail/<int:pk>/try_on/',virtual_try_on, name='virtual_try_on'),
]

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
