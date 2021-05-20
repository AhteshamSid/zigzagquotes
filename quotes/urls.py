
from django.urls import path

from.import views
app_name = 'quotes'
urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('add_quotes/', views.add_quotes, name='add_quotes'),
    # path('add_quote1/', views.AddQuote.as_view(), name='add_quote1'),
    path('quote_detail/<int:pk>/<str:category>/', views.QuoteDetail.as_view(), name='quote_detail'),
    path('quote_update/<int:pk>/', views.QuoteUpdate.as_view(), name='quote_update'),
    path('quote_delete/<int:pk>/', views.QuoteDelete.as_view(), name='quote_delete'),
    path('add_category/', views.AddCategory.as_view(), name='add_category'),
    path('categories/<str:category>/', views.Categories, name='categories'),
    path('quote_like/<int:pk>/', views.QuoteLike, name='quote_like'),
    path('quote_like1', views.quoteLike, name='quote_like1'),
]