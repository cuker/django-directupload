from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('directupload.views',
    url(r'^uploadify-options/$', 'uploadify_options_view', name='uploadify-options'),
    url(r'^upload/$', 'upload_file', name='uploadify-upload-file'),
    url(r'^exists/$', 'determine_name', name='uploadify-determine-name'),
)

