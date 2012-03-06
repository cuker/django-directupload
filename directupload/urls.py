from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('directupload.views',
    url(r'^upload-options/$', 'upload_options_view', name='directupload-options'),
    url(r'^upload/$', 'upload_file', name='directupload-file'),
    url(r'^exists/$', 'determine_name', name='directupload-determine-name'),
)

