from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from .models import Task, COMPLETED, NOT_COMPLETED


@receiver(post_save, sender=Task)
def update_house_points(senter, instance, created, **kwargs):
    house = instance.task_list.house
    if instance.status == COMPLETED:
        house.points += 10
    elif instance.status == NOT_COMPLETED:
        if house.points > 10:
            house.points -= 10
    house.save()


@receiver(post_save, sender=Task)
def update_tasklist_status(sender, instance, created, **kwargs):
    task_list = instance.task_list
    is_completed = True
    for task in task_list.tasks.all():
        if task.status != NOT_COMPLETED:
            is_comleted = False
            break
    if is_comleted:
        task_list.status = COMPLETED
    task_list.satutus = NOT_COMPLETED    
    task_list.save()
    