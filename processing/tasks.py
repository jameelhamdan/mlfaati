from celery import shared_task
from celery.utils.log import get_task_logger
from django.core.files.uploadedfile import SimpleUploadedFile
import core.models


logger = get_task_logger(__name__)


class ProcessingException(Exception):
    pass


@shared_task(name='process_file')
def process_file(file_id):
    file = core.models.File.objects.select_related('folder').prefetch_related(
        'folder__pipelines', 'folder__pipelines__transformations'
    ).get(pk=file_id)

    child_list = []

    for pipeline in file.folder.pipelines.all():
        # skip pipeline if file type not supported by it
        if pipeline.target_type != file.get_file_type():
            continue

        # Create Temporary file
        # TODO: copy file into memory in a more efficient way
        metadata = {}
        temp_file = SimpleUploadedFile(
            name='%s__%s' % (pipeline.name, file.name),
            content=file.content.read(),
            content_type=file.content_type,
        )

        # Starting Processing of file
        for transformation in pipeline.transformations.all():
            _types = transformation.TYPES
            transform_type = _types(transformation.type)

            if transform_type not in pipeline._target_type.get_allowed_operations(file.content_type):
                # Skip transformation if it cannot be applied to file of this type
                continue

            # Choose either Processing functions or metadeta functions
            if transform_type in _types.file_types():
                temp_file = transformation.process_file(temp_file)
            elif transform_type in _types.metadata_types():
                metadata.update(transformation.process_metadata(temp_file))
            else:
                raise ProcessingException('Transformation %s type is not mapped correctly in file types' % transform_type)

        new_file = core.models.File(
            content=temp_file,
            parent=file,
            folder_id=file.folder_id,
            space_id=file.space_id,
            pipeline_id=pipeline.id,
            metadata=metadata,
        )

        new_file.save()
        child_list.append({
            'id': new_file.pk,
            'file_name': new_file.name,
            'pipeline_id': pipeline.id,
            'pipeline_name': pipeline.name,
        })

    return child_list
