from . import views
from django.urls import path

urlpatterns=[
    path('',views.register_page,name='register'),
    path('login/',views.login_page,name='login'),
    path('pdf/',views.pdf,name='pdf'),
    path('receipt/',views.receipts,name='receipt'),
    path('logout/',views.custom_logout,name='logout'),
    path('delete_receipt/<id>',views.delete_receipt,name='deletereceipt'),
    path('update_receipt/<id>',views.update_receipt,name='updatereceipt')
]