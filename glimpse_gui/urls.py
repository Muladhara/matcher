from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'glimpse_gui.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^plotSeries?.*$','glimpse_ts.views.plot_series'),
    url(r'^getAvailableTransformationsByTsAndVintage?.*$','glimpse_ts.views.get_available_transformations_by_ts_and_vintage'),
    url(r'^getAllTimeseries?.*$','glimpse_ts.views.get_all_timeseries'),
    url(r'^getTsMetadata?.*$','glimpse_ts.views.get_ts_metadata'),
    url(r'^loadDataset?.*$','glimpse_ts.views.load_dataset'),
    url(r'^saveDataset?.*$','glimpse_ts.views.save_dataset'),
	url(r'^deleteDataset?.*$','glimpse_ts.views.delete_dataset'),
    url(r'^timeSeriesTransform?.*$','glimpse_ts.views.transform_time_series'),
    url(r'^timeSeriesExport?.*$','glimpse_ts.views.share_time_series'),
	url(r'^timeSeries?.*$','glimpse_ts.views.collect_time_series'),
	url(r'^index.html$', 'glimpse_ts.views.welcome'),
	url(r'^$', 'glimpse_ts.views.welcome'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^dao/columnsByDs/(\d+)/$', 'configurator.views.columnsByDs'),
    url(r'^dao/columnsByDs//$', 'configurator.views.columnsByDs'),
    url(r'^dao/cleaningParameterByType/(\d+)/$', 'configurator.views.cleaningParameterByType'),
    url(r'^dao/cleaningParameterByType//$', 'configurator.views.cleaningParameterByType'),
    url(r'^dao/matchParameterByType/(\d+)/$', 'configurator.views.matchParameterByType'),
    url(r'^dao/matchParameterByType//$', 'configurator.views.matchParameterByType'),
)