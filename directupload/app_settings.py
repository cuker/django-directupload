from django.conf import settings

UPLOADIFY_BACKEND = getattr(settings, 'UPLOADIFY_BACKEND', 'directupload.backends.djangoview.DjangoViewBackend')
#UPLOADIFY_BACKEND = getattr(settings, 'UPLOADIFY_BACKEND', 'directupload.backends.s3.S3UploadifyBackend')

