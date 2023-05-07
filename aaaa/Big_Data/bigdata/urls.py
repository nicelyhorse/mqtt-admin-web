from django.conf.urls import url, include
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^$', views.Log_in, name="mian"),
    url(r'^Home$', views.Home, name="Home"),
    url(r'^Log_in$', views.Log_in, name="Log_in"),
    url(r'^Log_out$', views.Log_in, name="Log_out"),
    url(r'^Regist$', views.Register, name="Register"),

    # 上传函数
    url(r'^changeAccount$', views.changeAccount, name="changeAccount"),
    url(r'^writeEmail$', views.writeEmail, name="writeEmail"),
    url(r'^emailList$', views.emailList, name="emailList"),
    url(r'^sendEmailList$', views.sendEmialList, name="sendEmialList"),
    url(r'^cgEmailList$', views.cgEmialList, name="cgEmialList"),
    url(r'^ljEmailList$', views.ljEmialList, name="ljEmialList"),
    url(r'^connect$', views.connect, name="connect"),
    url(r'^reWriteEmai/', views.reWriteEmai, name="reWriteEmai"),

]
