import os
from io import BytesIO
from django.core.files.uploadedfile import SimpleUploadedFile
import zipfile


def replace_extension(name, ext):
    dir_name, file_name = os.path.split(name)
    file_root, file_ext = os.path.splitext(file_name)
    return '%s.%s' % (file_root, 'zip')


def compress(uploaded_file: 'SimpleUploadedFile', **options):
    # TODO: Optimize this to better handle large files
    compress_level = options['quality']

    buffer = BytesIO()

    zf = zipfile.ZipFile(buffer, 'w', compresslevel=compress_level)
    zf.writestr(uploaded_file.name, uploaded_file.file.read())
    zf.close()

    return SimpleUploadedFile(
        name=replace_extension(uploaded_file.name, 'zip'),
        content=buffer.getvalue(),
        content_type='application/x-zip-compressed'
    )
