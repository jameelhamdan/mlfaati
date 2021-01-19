from io import BytesIO
from django.core.files.uploadedfile import SimpleUploadedFile
import zipfile
from . import utils


def compress(uploaded_file: 'SimpleUploadedFile', **options):
    # TODO: Optimize this to better handle large files
    compress_level = options['quality']

    buffer = BytesIO()

    zf = zipfile.ZipFile(buffer, 'w', compresslevel=compress_level)
    zf.writestr(uploaded_file.name, uploaded_file.file.read())
    zf.close()

    return SimpleUploadedFile(
        name=utils.replace_extension(uploaded_file.name, 'zip'),
        content=buffer.getvalue(),
        content_type='application/x-zip-compressed'
    )
