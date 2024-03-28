import os
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import uuid


def upload_user_file(instance, filename):
    ext = os.path.splitext(filename)[1]
    return 'user/{id_user}/nutritional_table{u_id}{ext}'.format(id_user=instance.user.id, u_id=uuid.uuid4(), ext=ext)

def validate_file(fieldfile_obj, megabyte_limit=5.0):
    filesize = fieldfile_obj.file.size
    if filesize > megabyte_limit * 1024 * 1024:
        raise ValidationError(_("Max file size is %sMB") % str(megabyte_limit))