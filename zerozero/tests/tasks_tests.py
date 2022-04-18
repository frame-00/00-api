import pytest

from unittest import mock
from zerozero.tasks import query_report_task, run_query_report_tasks


def test_query_report_task(mock_zerozero_client):

    with mock.patch("zerozero.tasks.run_query_report_task") as task_mock:
        query_report_task(23)

        task_mock.assert_called_with(
            23, "postgres:///some_db", mock_zerozero_client
        )


def test_run_query_report_tasks(mock_zerozero_client):

    with mock.patch("zerozero.tasks.query_report_task.delay") as task_mock:
        with mock.patch("zerozero.tasks.get_ready_query_reports") as ready_mock:
            ready_mock.return_value = [2, 7]
            run_query_report_tasks()

            task_mock.assert_any_call(2)
            task_mock.assert_any_call(7)
