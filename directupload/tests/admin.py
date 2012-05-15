from django.test import TestCase

class PatchAdminTestCase(TestCase):
    def test_patch(self):
        from directupload.admin import patch_admin
        patch_admin()

class DirectUploadAdminMixinTestCase(TestCase):
    def test_form_field_for_db_field(self):
        pass

