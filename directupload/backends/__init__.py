try:
    import importlib
except ImportError:
    from django.utils import importlib

def get_uploadify_backend():
    from directupload.app_settings import UPLOADIFY_BACKEND
    module_name, class_name = UPLOADIFY_BACKEND.rsplit('.', 1)
    module = importlib.import_module(module_name)
    return getattr(module, class_name)

