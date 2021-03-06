from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.views import defaults as default_views
from rental.rents.v0.urls import router as rent
from rental.common.utils import DefaultRouter

router = DefaultRouter()
router.extend(rent)

urlpatterns = [
    url(r'^api/v0/', include(router.urls, namespace='api')),
    url(r'^', include(router.urls, namespace='api1'), name='home'),

    # Django Admin, use {% url 'admin:index' %}
    url(settings.ADMIN_URL, admin.site.urls),

    # Your stuff: custom urls includes go here

]

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        url(r'^400/$', default_views.bad_request, kwargs={'exception': Exception('Bad Request!')}),
        url(r'^403/$', default_views.permission_denied, kwargs={'exception': Exception('Permission Denied')}),
        url(r'^404/$', default_views.page_not_found, kwargs={'exception': Exception('Page not Found')}),
        url(r'^500/$', default_views.server_error),
    ]
    if 'debug_toolbar' in settings.INSTALLED_APPS:
        import debug_toolbar
        urlpatterns = [
            url(r'^__debug__/', include(debug_toolbar.urls)),
        ] + urlpatterns
