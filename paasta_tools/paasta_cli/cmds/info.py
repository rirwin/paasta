#!/usr/bin/env python
from paasta_tools.monitoring_tools import get_runbook
from paasta_tools.monitoring_tools import get_team
from paasta_tools.paasta_cli.cmds.status import get_actual_deployments
from paasta_tools.paasta_cli.utils import figure_out_service_name
from paasta_tools.paasta_cli.utils import get_pipeline_url
from paasta_tools.paasta_cli.utils import lazy_choices_completer
from paasta_tools.paasta_cli.utils import list_services
from paasta_tools.paasta_cli.utils import PaastaColors
from paasta_tools.utils import get_git_url
from service_configuration_lib import read_service_configuration


NO_DESCRIPTION_MESSAGE = (
    "No 'description' entry in service.yaml. Please a one line sentance that describes this service"
)
NO_EXTERNAL_LINK_MESSAGE = "No 'external_link' entry in service.yaml. Please add on that points to your CEP/SCF"


def add_subparser(subparsers):
    list_parser = subparsers.add_parser(
        'info',
        description="Prints the general information about a service.",
        help="Prints general service information")
    list_parser.add_argument(
        '-s', '--service',
        help='The name of the service you wish to inspect'
    ).completer = lazy_choices_completer(list_services)
    list_parser.set_defaults(command=paasta_info)


def deployments_to_clusters(deployments):
    clusters = []
    for deployment in deployments:
        cluster, _ = deployment.split('.')
        clusters.append(cluster)
    return set(clusters)


def get_service_info(service):
    service_configuration = read_service_configuration(service)
    description = service_configuration.get('description', NO_DESCRIPTION_MESSAGE)
    external_link = service_configuration.get('external_link', NO_EXTERNAL_LINK_MESSAGE)
    pipeline_url = get_pipeline_url(service)
    deployments = get_actual_deployments(service)
    git_url = get_git_url(service)

    output = []
    output.append('Service Name: %s' % service)
    output.append('Description: %s' % description)
    output.append('External Link (CEP/SCF): %s' % PaastaColors.cyan(external_link))
    output.append('Monitored By: team %s' % get_team(None, service))
    output.append('Runbook: %s' % PaastaColors.cyan(get_runbook(None, service)))
    output.append('Git Repo: %s' % git_url)
    output.append('Jenkins Pipeline: %s' % pipeline_url)
    output.append('Deployed to the following clusters:')
    for cluster in deployments_to_clusters(deployments):
        output.append(' - %s' % cluster)
    return '\n'.join(output)


def paasta_info(args):
    """Prints general information about a service"""
    service_name = figure_out_service_name(args)
    print get_service_info(service_name)