from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # path('advanced_filters/', include('advanced_filters.urls')),
    # path('_nested_admin', include('nested_admin.urls')),
    # path('docs/', include('app_docs.urls')),
    # path('silk/', include('silk.urls', namespace='silk')),
    # path('anymail/', include('anymail.urls')),
    # path('', include(default_urls)),
    path('', admin.site.urls),
]

admin.site.site_header = "AnyChat Administration"
admin.site.site_title = "AnyChat Admin Portal"
admin.site.index_title = "Welcome to Admin Portal"
