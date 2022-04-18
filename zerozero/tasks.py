from celery import shared_task
from django.conf import settings
from zerozero_pilot.warehouse import (
    run_query_report_task,
    get_ready_query_reports,
)


@shared_task
def query_report_task(report_id):
    from zerozero import client

    run_query_report_task(report_id, settings.WAREHOUSE_DATABASE_URL, client)


@shared_task
def run_query_report_tasks():
    from zerozero import client

    report_ids = get_ready_query_reports(client)

    for report_id in report_ids:
        query_report_task.delay(report_id)
