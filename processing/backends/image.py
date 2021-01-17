from io import BytesIO
from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile


__all__ = ['compress']


def compress(uploaded_file: 'SimpleUploadedFile', **options):
    assert 'quality' in options.keys(), 'Quality attribute must be in options'
    quality = options['quality']
    assert isinstance(quality, int), 'Quality must be an integer'

    buffer = BytesIO()
    img = Image.open(uploaded_file)
    img.save(buffer, format=img.format, quality=quality)
    return SimpleUploadedFile(
        name=uploaded_file.name,
        content=buffer.getvalue(),
        content_type=uploaded_file.content_type
    )
