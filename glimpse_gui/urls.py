from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'glimpse_gui.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^dao/columnsByDs/(\d+)/$', 'configurator.views.columnsByDs'),
    url(r'^dao/columnsByDs//$', 'configurator.views.columnsByDs'),
    url(r'^dao/cleaningParameterByType/(\d+)/$', 'configurator.views.cleaningParameterByType'),
    url(r'^dao/cleaningParameterByType//$', 'configurator.views.cleaningParameterByType'),
    url(r'^dao/matchParameterByType/(\d+)/$', 'configurator.views.matchParameterByType'),
    url(r'^dao/matchParameterByType//$', 'configurator.views.matchParameterByType'),
)
