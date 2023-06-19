from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from djStore import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path("__reload__/", include("django_browser_reload.urls")),
    path('',include('app.urls'))
]


# Adding Media Root to browser.
urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

