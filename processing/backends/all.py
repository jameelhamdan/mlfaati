import hashlib
import zipfile
from io import BytesIO
from django.core.files.uploadedfile import SimpleUploadedFile
from . import utils


HASH_CHUNK_SIZE = 4096


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


def checksum(uploaded_file: 'SimpleUploadedFile', **options):
    """
    Function to calculate SHA256 checksum for file,
    can be used to verify downloaded file integrity
    """

    hash_type = options['type']

    if hash_type == 'MD5':
        hasher = hashlib.md5()
    elif hash_type == 'SHA256':
        hasher = hashlib.sha256()
    else:
        raise ValueError(f'Hash type "{hash_type}" in "checksum" function is not valid')

    if uploaded_file.multiple_chunks():
        for data in uploaded_file.chunks(HASH_CHUNK_SIZE):
            hasher.update(data)
    else:
        hasher.update(uploaded_file.read())

    return {
        'checksum': hasher.hexdigest()
    }
