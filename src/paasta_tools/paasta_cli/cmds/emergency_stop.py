#!/usr/bin/env python
from argcomplete.completers import ChoicesCompleter

from paasta_tools.paasta_cli.utils import execute_paasta_serviceinit_on_remote_master
from paasta_tools.paasta_cli.utils import list_services
from paasta_tools.paasta_cli.utils import list_instances
from paasta_tools.marathon_tools import list_clusters


def add_subparser(subparsers):
    status_parser = subparsers.add_parser(
        'emergency-stop',
        description="Stop a PaaSTA service",
        help="Stops a PaaSTA service by asking Marathon to have 0 instances.")
    status_parser.add_argument(
        '-s', '--service',
        help='Service that you want to stop. Like example_service.'
    ).completer = ChoicesCompleter(list_services())
    status_parser.add_argument(
        '-i', '--instance',
        help='Instance of the service that you want to stop. Like "main" or "canary".'
    ).completer = ChoicesCompleter(list_instances())
    status_parser.add_argument(
        '-c', '--cluster',
        help='The PaaSTA cluster that has the service you want to stop. Like norcal-prod'
    ).completer = ChoicesCompleter(list_clusters())
    status_parser.set_defaults(command=paasta_emergency_stop)


def paasta_emergency_stop(args):
    """Performs an emergency stop on a given service.instance on a given cluster"""
    print "Performing an emergency stop on %s.%s..." % (args.service, args.instance)
    execute_paasta_serviceinit_on_remote_master('stop', args.cluster, args.service, args.instance)
    print "Warning: This service will start back up again when the next"
    print "config change happens, or deploy, or bounce, etc"
    print ""
    print "If you want this stop to be permanant, adjust the %s/marathon-%s.yaml" % (args.service, args.cluster)
    print "file to reflect that. (set 'instances: 0', or perhaps rm the yaml entirely)"
    print ""
    print "To start this service again asap, run:"
    print "paasta emergency-start --service %s --instance %s --cluster %s" % (args.service, args.instance, args.cluster)