import os
import tempfile
from io import BytesIO
from PIL import Image
from pilkit.processors import SmartResize, Adjust
from django.core.files.uploadedfile import SimpleUploadedFile
from . import utils
from django.conf import settings
from logging import getLogger

logger = getLogger(__name__)


__all__ = ['compress', 'resize', 'adjust']


def compress(uploaded_file: 'SimpleUploadedFile', **options):
    buffer = BytesIO()
    img = Image.open(uploaded_file)
    img.save(buffer, format='png', **options)
    return SimpleUploadedFile(
        name=utils.replace_extension(uploaded_file.name, 'png'),
        content=buffer.getvalue(),
        content_type=uploaded_file.content_type
    )


def resize(uploaded_file: 'SimpleUploadedFile', **options):
    buffer = BytesIO()
    img = Image.open(uploaded_file)
    processor = SmartResize(**options)
    new_img = processor.process(img)
    new_img.save(buffer, format='png')
    return SimpleUploadedFile(
        name=utils.replace_extension(uploaded_file.name, 'png'),
        content=buffer.getvalue(),
        content_type=uploaded_file.content_type
    )


def adjust(uploaded_file: 'SimpleUploadedFile', **options):
    buffer = BytesIO()
    img = Image.open(uploaded_file)
    processor = Adjust(**options)
    new_img = processor.process(img)
    new_img.save(buffer, format='png')
    return SimpleUploadedFile(
        name=utils.replace_extension(uploaded_file.name, 'png'),
        content=buffer.getvalue(),
        content_type=uploaded_file.content_type
    )


def classify(uploaded_file: 'SimpleUploadedFile', **options):
    """
    Function to classify images based on selected algorithm in settings,
    only works in *unix systems*
    """
    try:
        from imageai.Classification import ImageClassification
    except ImportError as e:
        logger.warning('"ImageClassification" Import not found, please import to use classify functions')
        raise e

    model_options = settings.MODEL_OPTIONS[settings.IMAGE_CLASSIFY_MODEL]
    prediction = ImageClassification()
    prediction.setModelTypeAsInceptionV3()
    prediction.setModelPath(model_options['path'])
    prediction.loadModel()

    result = {}
    new_uploaded_file = compress(uploaded_file, quality=100)
    # Write file to tmp to get path
    temp = tempfile.NamedTemporaryFile(suffix='.png')
    temp.write(new_uploaded_file.read())
    temp.seek(0)

    predictions, probabilities = prediction.classifyImage(temp.name, result_count=5)
    for eachPrediction, eachProbability in zip(predictions, probabilities):
        result[eachPrediction] = eachProbability

    return {
        'classification': result
    }
