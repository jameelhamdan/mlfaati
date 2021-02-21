from celery import shared_task
from celery.utils.log import get_task_logger
from django.core.files.uploadedfile import SimpleUploadedFile
import core.models
import copy
from .definitions import TransformationType


logger = get_task_logger(__name__)


class ProcessingException(Exception):
    pass


@shared_task(name='process_file')
def process_file(file_id):
    file = core.models.File.objects.select_related('folder').prefetch_related(
        'folder__pipelines', 'folder__pipelines__transformations'
    ).get(pk=file_id)

    child_list = []
    file_metadata = {}

    for pipeline in file.folder.pipelines.all():
        if not pipeline.is_enabled:
            continue

        # skip pipeline if file type not supported by it
        if pipeline.target_type != file.get_file_type() and pipeline.target_type != pipeline.TYPES.ALL:
            continue

        # Create Temporary file
        # TODO: copy file into memory in a more efficient way
        pipeline_metadata = {}
        temp_file = SimpleUploadedFile(
            name=copy.deepcopy(file.name),
            content=copy.deepcopy(file.content).read(),
            content_type=copy.deepcopy(file.content_type),
        )

        # Starting Processing of file
        file_transformation_count = 0
        for transformation in pipeline.transformations.filter(type__in=TransformationType.file_types()):
            transform_type = transformation._type

            # Skip transformation if it cannot be applied to file of this type
            if transform_type not in pipeline._target_type.get_file_type(temp_file.content_type).mapping and pipeline.target_type != pipeline.TYPES.ALL:
                continue

            temp_file = transformation.process_file(temp_file)
            file_transformation_count += 1

        metadata_transformation_count = 0
        for transformation in pipeline.transformations.filter(type__in=TransformationType.metadata_types()):
            transform_type = transformation._type

            # Skip transformation if it cannot be applied to file of this type
            if transform_type not in pipeline._target_type.get_file_type(temp_file.content_type).mapping and pipeline.target_type != pipeline.TYPES.ALL:
                continue

            pipeline_metadata.update(transformation.process_metadata(temp_file))
            metadata_transformation_count += 1

        if metadata_transformation_count > 0:
            # Append new pipeline metadata to main file
            file_metadata.update({pipeline.name: pipeline_metadata})

        if file_transformation_count > 0:
            # Add prefix to file name
            temp_file.name = '%s__%s' % (pipeline.name, temp_file.name)

            new_file = core.models.File(
                content=temp_file,
                parent=file,
                folder_id=file.folder_id,
                space_id=file.space_id,
                pipeline_id=pipeline.id,
                metadata=pipeline_metadata,
            )

            new_file.save()
            child_list.append({
                'id': new_file.pk,
                'file_name': new_file.name,
                'pipeline_id': pipeline.id,
                'pipeline_name': pipeline.name,
            })

    # Update main file metadata after finishing processing pipelines
    if file_metadata != {}:
        file.metadata = file_metadata
        file.save(update_fields=['metadata'])

    return child_list
