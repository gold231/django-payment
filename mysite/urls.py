from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="home"),
    path('register', views.register, name="register"),
    path('activate/<slug:uidb64>/<slug:token>/', views.activate_account, name='activate'),
    path('signin', views.signin, name="signin"),
    path('logout', views.signout, name="logout"),
    path('plan-pricing', views.plan_pricing, name="plan_pricing"),
    path('order-now/<int:price_id>', views.order_now, name='order'),

    path('features', views.features, name='features'),
    path('contact', views.contact, name='contact'),
    path('about', views.about, name='about'),
]
