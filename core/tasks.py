from celery import shared_task
from celery.utils.log import get_task_logger
from . import models


logger = get_task_logger(__name__)


@shared_task(name='delete_file')
def delete_file(file_id):
    file: 'models.File' = models.File.objects.select_related('folder').prefetch_related(
        'children'
    ).get(pk=file_id)

    # Delete children first
    # (children do not have children of themselves so depth is 1)
    for child in file.children.all():
        child.delete()

    # delete file content
    file.content.delete(save=False)
    # remove from database
    file.delete(lazy=False)
    return
