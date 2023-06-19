from django.urls import path, include
from app import views
from django.contrib.auth import views as auth_views

urlpatterns = [

    # Managing HomeView
    path('', views.IndexView.as_view(), name='index'),

    # Managing Authetication
    path('accounts/signup/', views.RegistrationUser.as_view(), name='signup'),
    path('accounts/profile/', views.ProfileView.as_view(), name='profile'),
    path('accounts/profile/update',
         views.ProfileUpdateView.as_view(), name='profile_update'),
    path('accounts/login/', views.MyLoginView.as_view(), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),

    # Managing Product
    path('product-list/<int:pk>/<slug:slug>/',
         views.ProductListView.as_view(), name='product_list'),
    path('product-detail/<int:id>/<slug:slug>/',
         views.ProductDetailView, name='product_detail'),
    path('ajaxcolor/',  views.AjaxColor, name='ajaxcolor'),

    # Search
    path('search/', views.SearchView, name='search'),
    path('main-category/<int:pk>/', views.MainCategory, name='main-category'),

    # Cart Management
    path('minus-quantity/', views.DecreaseQuantity, name='minus-quantity'),
    path('plus-quantity/', views.IncreaseQuantity, name='plus-quantity'),

    # Checkout
    path('checkout/', views.Checkout, name='checkout'),

    # Validating Payment
    path('validate-payment/<int:pk>/',
         views.ValidatePayment, name='validate_payment'),

    # Myorders
    path('myorders/', views.Myorders, name='myorders'),

    # Favicon
    path('favicon.ico/', views.Favicon)

    # Managing Password Reset (Authentication)
    # path('accounts/password_reset/' , auth_views.PasswordResetView.as_view(template_name='registration/password_reset.html'),name='password_reset'),
    # path('accounts/password_reset/done/' , auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'),name='password_reset_done'),
    # path('accounts/reset/<uidb64>/<token>/' , auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'),name='password_reset_confirm'),
    # path('accounts/reset/done/' , auth_views.PasswordResetCompleteView.as_view(template_name='registration/reset_done.html'),name='password_reset_complete')
]
