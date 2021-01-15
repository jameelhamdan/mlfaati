from celery import shared_task
from celery.utils.log import get_task_logger
from django.core.files.uploadedfile import SimpleUploadedFile
import core.models


logger = get_task_logger(__name__)


@shared_task(name='process_file')
def process_file(file_id):
    file = core.models.File.objects.get(pk=file_id)

    child_list = []

    for pipeline in file.folder.pipelines.prefetch_related('transformations'):

        # Create Temporary file
        # TODO: copy file into memory in a more efficient way
        temp_file = SimpleUploadedFile(
            name='%s__%s' % (pipeline.name, file.name),
            content=file.content.read(),
            content_type=file.content_type,
        )

        # Starting Processing of file
        for transformation in pipeline.transformations.all():
            # TODO: actually process the temp_file using transformation
            pass

        child_file = core.models.File(
            content=temp_file,
            parent=file,
            folder_id=file.folder_id,
            space_id=file.space_id,
        )

        child_file.save()
        child_list.append({
            'id': child_file,
            'pipeline_id': pipeline.id,
            'pipeline_name': pipeline.name,
        })

    return child_list
