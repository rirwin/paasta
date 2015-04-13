#!/usr/bin/env python

from mock import patch
from paasta_tools import paasta_metastatus


@patch('paasta_tools.paasta_metastatus.fetch_mesos_stats')
def test_get_mesos_status(
    mock_fetch_mesos_stats,
):
    mock_fetch_mesos_stats.return_value = {
        'master/cpus_total': 3,
        'master/cpus_used': 2,
        'master/mem_total': 10240,
        'master/mem_used': 2048,
        'master/tasks_running': 3,
        'master/tasks_staging': 4,
        'master/tasks_starting': 0,
        'master/slaves_active': 4,
        'master/slaves_inactive': 0,
    }
    expected_cpus_output = "cpus: 3 total => 2 used, 1 available"
    expected_mem_output = \
        "memory: 10.00 GB total => 2.00 GB used, 8.00 GB available"
    expected_tasks_output = \
        "tasks: 3 running, 4 staging, 0 starting"
    expected_slaves_output = \
        "slaves: 4 active, 0 inactive"
    output = paasta_metastatus.get_mesos_status()

    assert mock_fetch_mesos_stats.called_once()
    assert expected_cpus_output in output
    assert expected_mem_output in output
    assert expected_tasks_output in output
    assert expected_slaves_output in output


@patch('paasta_tools.paasta_metastatus.get_marathon_client')
def test_get_marathon_status(
    mock_get_marathon_client,
):
    client = mock_get_marathon_client.return_value
    client.list_apps.return_value = [
        "MarathonApp::1",
        "MarathonApp::2"
    ]
    client.list_deployments.return_value = [
        "MarathonDeployment::1",
    ]
    client.list_tasks.return_value = [
        "MarathonTask::1",
        "MarathonTask::2",
        "MarathonTask::3"
    ]
    expected_apps_output = "2 apps"
    expected_deployment_output = "1 deployments"
    expected_tasks_output = "3 tasks"

    output = paasta_metastatus.get_marathon_status()

    assert expected_apps_output in output
    assert expected_deployment_output in output
    assert expected_tasks_output in output