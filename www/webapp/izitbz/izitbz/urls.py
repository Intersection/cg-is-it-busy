from django.conf.urls import patterns, include, url

from izitbz.views import latest_chart, simple_izitbz
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
        url(r'^$', simple_izitbz),
        url(r'^chart/', latest_chart)
    # Examples:
    # url(r'^$', 'izitbz.views.home', name='home'),
    # url(r'^izitbz/', include('izitbz.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
