try:
    import importlib
except ImportError:
    from django.utils import importlib

def get_directupload_backend():
    from directupload.app_settings import DIRECT_UPLOAD_BACKEND
    module_name, class_name = DIRECT_UPLOAD_BACKEND.rsplit('.', 1)
    module = importlib.import_module(module_name)
    return getattr(module, class_name)

