"""cafodca URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from notas import views as notas

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),
    url(r'^accounts/login/$', auth_views.login, name='login'),
    url(r'^accounts/logout/$', notas.logout_page, name='logout'),
    url(r'^password_change/$',auth_views.password_change,
                            {'template_name': 'registration/password_change_form.html',
                            'post_change_redirect': '/foros/perfil/'},
                            name='password-change'),
    url(r'^$', notas.index),
    url(r'^notas/', include('notas.urls')),
    # url(r'^contrapartes/', include('contrapartes.urls')),
    url(r'^agendas/', include('agendas.urls')),
    # url(r'^tagging_autocomplete/', include('tagging_autocomplete.urls')),
    url(r'^foros/', include('foros.urls')),
    # url(r'^busqueda/$', include('django_google_cse.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

