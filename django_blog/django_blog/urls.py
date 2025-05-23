"""
URL configuration for django_blog project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.contrib import admin
from django.conf import settings
from django.urls import include, path
from django.conf.urls.static import static
from django.views.generic import RedirectView

# URLs de base
urlpatterns = [
    path('admin/', admin.site.urls),
    path('blog/', include('blog.urls', namespace='blog')), 
    path('portfolio/', include('portfolio.urls', namespace='portfolio')),
    path('', RedirectView.as_view(url='portfolio/projects/', permanent=True)),
    path('openaichat/', include('openaichat.urls', namespace='openaichat')),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('ckeditor5/', include('django_ckeditor_5.urls')),
]
   
# Ajouter la gestion des médias en mode développement
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


