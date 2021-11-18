from django.urls import path
from news_app import views

urlpatterns = [
    path("",views.index,name="index"),

    path("addnews/",views.add_news,name="add_news"),
    path("updatenews/<int:id>/",views.update_news,name="update_news"),
    path("deletenews/<int:id>/",views.delete_news,name="delete_news"),

    path("signin/",views.signin,name="signin"),
    path("signout/",views.signout,name="signout"),
    path("signup/",views.signup,name="signup"),

    path('contact/', views.contact, name='contact'),
    path('profile/', views.profile, name='profile'),
    
    path('reset_password/', views.reset_password, name='reset_password'),

]
