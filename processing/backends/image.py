from io import BytesIO
from PIL import Image
from pilkit.processors import SmartResize, Adjust
from django.core.files.uploadedfile import SimpleUploadedFile


__all__ = ['compress', 'resize', 'adjust']


def compress(uploaded_file: 'SimpleUploadedFile', **options):
    buffer = BytesIO()
    img = Image.open(uploaded_file)
    img.save(buffer, format=img.format, **options)
    return SimpleUploadedFile(
        name=uploaded_file.name,
        content=buffer.getvalue(),
        content_type=uploaded_file.content_type
    )


def resize(uploaded_file: 'SimpleUploadedFile', **options):
    buffer = BytesIO()
    img = Image.open(uploaded_file)
    processor = SmartResize(**options)
    new_img = processor.process(img)
    new_img.save(buffer, format=img.format)
    return SimpleUploadedFile(
        name=uploaded_file.name,
        content=buffer.getvalue(),
        content_type=uploaded_file.content_type
    )


def adjust(uploaded_file: 'SimpleUploadedFile', **options):
    buffer = BytesIO()
    img = Image.open(uploaded_file)
    processor = Adjust(**options)
    new_img = processor.process(img)
    new_img.save(buffer, format=img.format)
    return SimpleUploadedFile(
        name=uploaded_file.name,
        content=buffer.getvalue(),
        content_type=uploaded_file.content_type
    )


