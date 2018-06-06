#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Escaneador de posicion de interior
"""

from argparse import ArgumentParser, RawDescriptionHelpFormatter
from commands import getoutput, getstatusoutput
import simplejson
import textwrap
import urllib2
import grp
import sys
import os
import re
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

__version__ = "0.1.23"


API_KEY = os.environ.get('AIzaSyBZiGlKKQgyjxUojJk8d9ZrNlRJ_Lt1lnk') or 'AIzaSyBZiGlKKQgyjxUojJk8d9ZrNlRJ_Lt1lnk'



def get_scriptpath():
    pathname = os.path.dirname(sys.argv[0])
    fullpath = os.path.abspath(pathname)

    if not fullpath.endswith('/'):
        fullpath += '/'

    return fullpath


def prettify_json(json_data):
    
    print str(json_data['location']['lat']) + " " + str(json_data['location']['lng'])
    return simplejson.dumps(json_data)

def get_signal_strengths(wifi_scan_method):
    wifi_data = []

    # GNU/Linux
    if wifi_scan_method is 'iw':
		iw_command = 'iw dev %s scan' % (args.wifi_interface)
		iw_scan_status, iw_scan_result = getstatusoutput(iw_command)

		if iw_scan_status != 0:
			print "[!] Unable to scan for Wi-Fi networks !"
			print "Used command: '%s'" % iw_command
			print "Result:\n" + '\n'.join(iw_scan_result.split('\n')[:10])
			if len(iw_scan_result.split('\n')) > 10:
				print "[...]"
			exit(1)
		else:
			parsing_result = re.compile("BSS ([\w\d\:]+).*\n.*\n.*\n.*\n.*\n\tsignal: ([-\d]+)", re.MULTILINE).findall(iw_scan_result)

			wifi_data = [(bss[0].replace(':', '-'), int(bss[1])) for bss in parsing_result]

    return wifi_data


def check_prerequisites():

    if sys.platform.startswith(('linux')) or sys.platform == 'darwin':
        wifi_scan_method = None
        perm_cmd = None

        if sys.platform.startswith('linux'):
            if os.geteuid() != 0:
                which_sudo_status, which_sudo_result = getstatusoutput('which sudo')
                if which_sudo_status is 0:
                    current_user_groups = [grp.getgrgid(g).gr_name for g in os.getgroups()]
                    if 'sudo' in current_user_groups or \
                       'admin' in current_user_groups:
                        perm_cmd = 'sudo --preserve-env'
            if perm_cmd:
                    os.execvp(perm_cmd.split()[0], perm_cmd.split() + [
                                  ' '.join(['./' + sys.argv[0].lstrip('./')])
                              ] + sys.argv[1:])

            which_iw_status, which_iw_result = getstatusoutput('which iw')
            if which_iw_status != 0:
                print "Missing dependency: 'iw' is needed\n" + \
                      "    iw - tool for configuring Linux wireless devices"
                if 'ubuntu' in getoutput('uname -a').lower():
                    print "    > sudo apt-get install iw"
                elif 'gentoo' in getoutput('cat /etc/*release').lower():
                    print "    > su -c 'emerge -av net-wireless/iw'"
                exit(1)
            else:
                wifi_scan_method = 'iw'


    return wifi_scan_method


class MyParser(ArgumentParser):
    def error(self, message):
        sys.stderr.write('erreur: %s\n\n' % message)
        #self.print_help()
        self.print_usage()
        sys.exit(2)


def get_arguments(argv=None):
    """Command line options."""

    if argv is not None:
        sys.argv.extend(argv)

    program_name = os.path.basename(sys.argv[0])
    program_version = 1
    program_version_message = '''Primera version'''
    program_shortdesc = '''PTIN'''
    program_copyright = '''PTIN 2018'''

    program_license = '''Ptin'''


    detailed_license = '''Higía'''

    parser = MyParser(description=program_license,
                      formatter_class=RawDescriptionHelpFormatter,
                      epilog=textwrap.dedent(''' '''))

   
    required_parser = parser.add_argument_group('required arguments')
    required_parser = required_parser.add_mutually_exclusive_group(required=True)
    required_parser.add_argument('-i', action="store", dest="wifi_interface", help='specify Wi-Fi scan interface')

    return parser.parse_args()


if __name__ == "__main__":
  

	args = get_arguments()

	wifi_scan_method = check_prerequisites()


	wifi_data = get_signal_strengths(wifi_scan_method)


	location_request = {
		'considerIp': False,
		'wifiAccessPoints':[
		    {
		        "macAddress": mac,
		        "signalStrength": signal
		    } for mac, signal in wifi_data]
	}


	json_data = simplejson.JSONEncoder().encode(location_request)
	http_request = urllib2.Request('https://www.googleapis.com/geolocation/v1/geolocate?key=' + API_KEY)
	http_request.add_header('Content-Type', 'application/json')

	api_result = simplejson.loads(urllib2.urlopen(http_request, json_data).read())

	b = prettify_json(api_result)
