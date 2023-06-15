"""annual_report_sum URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from django.conf.urls import url
from annual_report_sum import views

#from .views import (
#    FormReportView,
#)

urlpatterns = [
    path("", views.annual_report_select, name='form_10kselectreport'),
    #path("form_10kreport", FormReportView.as_view(), name="form_10kreport"),
    url(r'^form_10kreport$', views.annual_report_select, name='form_10kselectreport'),
    #url(r'^get_10kreport$', views.get_report_doc, name='form_10k_getreport'),
    url(r'^about$', views.system_about_page, name='system_about'),
    url(r'^features$', views.system_features_page, name='system_features'),
]
