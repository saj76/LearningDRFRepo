from celery.schedules import crontab
from celery.task import Task, PeriodicTask, periodic_task
from .models import Shop
from datetime import datetime, timedelta
from django.utils import timezone
from .utils.mail_util import send_email
from celery.utils.log import get_task_logger
from logging import getLogger


logger = getLogger(__name__)


class ReportRegistersByEmail(Task):
    name = 'ReportRegistersByEmail'
    soft_time_limit = 1 * 60

    def run(self, date_interval_start, date_interval_finish):
        new_registers = Shop.objects.filter(created_at__range=[date_interval_start, date_interval_finish]).count()
        send_email("Daily Report", f"Registered shop since yesterday {0}".format(new_registers),
                   ['sajjad.vahedi@ronash.co'])


class ReportDailyRegisters(PeriodicTask):
    name = 'ReportDailyRegisters'
    run_every = (crontab(hour=18, minute=22))

    def run(self, *args, **kwargs):
        current_time = timezone.now()
        last_day = timezone.now() - timedelta(1)
        ReportRegistersByEmail().delay(last_day, current_time)


class R:
    name = "ali"