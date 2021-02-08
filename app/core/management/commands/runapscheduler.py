import logging

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django.utils import timezone
from django.conf import settings

from core.models import Rule, User
from core.utils import RedisCache


# now = timezone.now()

logger = logging.getLogger(__name__)


def rule_checker():

    """
    Deactivates outdated rules
    """

    cache = RedisCache()
    time = settings.RULE_TIME

    for rule in Rule.objects.filter(active=True):
        if (timezone.now() - rule.created_at).seconds >= time:
            rule.active = False
            rule.save()

            cache.delete(rule.short_url)
            logger.error(f'rule deactivated: {rule.id}')

def delete_old_job_executions(max_age=604_800):
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            rule_checker,
            trigger=CronTrigger(second="*/10"),  # Every 10 seconds
            id="rule_checker",  # The `id` assigned to each job MUST be unique
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'rule_checker'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),  # Midnight on Monday, before start of the next work week.
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Added weekly job: 'delete_old_job_executions'."
        )

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")