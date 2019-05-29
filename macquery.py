#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ============================================================================
# Title: mac_company
# Description:
# Tool to determine company from a mac address
# ============================================================================


import argparse
import requests
import logging as log
import os
import sys
import pprint

# see: https://macaddress.io/api/documentation/making-requests
BASEURL = 'https://api.macaddress.io/v1'

# name of environment variable
ENV_VAR = 'MACADDR_API_KEY'


'''
perform search if mac against api
'''


def search_macaddrs(api_key, macaddrs):
    r = {}
    for m in macaddrs:
        search_params = {
            'apiKey': api_key,
            'search': m,
            'output': 'vendor'
        }
        log.info('searching for %s at %s' %( m, BASEURL))
        if debug:
            pprint.pprint(search_params)

        reply = requests.get(
            url=BASEURL,
            params = search_params
        )

        if reply.status_code == requests.codes.ok: 
            r[m] = reply.text
        else: 
            print "error on query to %s, status:  " % (BASEURL, 
                                                       reply.status_code)
            sys.exit(1)

    return r


# Get API key from environment
def get_api_key(args):
    if 'api_key' in args:
        return args.api_key
    else:
        print "api_key not defined or in environment as %s" % (ENV_VAR)
        sys.exit(1)

# get the mac list


def get_macaddrs(args):
    macaddrs = args.macaddrs
    for m in macaddrs:
        validate_mac(m)
    return macaddrs

# Test mac address for required format


def validate_mac(macaddr):
    if ':' in macaddr:
        octets = macaddr.split(':')
        if len(octets) < 3:
            print '%s needs to have at least 3 octets.' % (macaddr)
            sys.exit(1)
    elif '.' in macaddr:
        octets = macaddr.split('.')
        if len(octets) < 3:
            print '%s needs to have at least 3 octets.' % (macaddr)
            sys.exit(1)
    elif '-' in macaddr:
        octets = macaddr.split('-')
        if len(octets) < 3:
            print '%s needs to have at least 3 octets.' % (macaddr)
            sys.exit(1)
    else:
        if len(macaddr) < 6:
            print '%s needs to have at least 3 octets.' % (macaddr)
            sys.exit(1)
    return macaddr


''' 
get arguments from C/L 
'''


def get_args():
    parser = argparse.ArgumentParser(
        description="search for mac address OUI and return company name.")
    # defaults
    parser.set_defaults(verbose=False)
    parser.set_defaults(debug=False)
    parser.add_argument("-v", "--verbose",
                        action="store_true",
                        help="Set verbose output.")
    parser.add_argument("-d", "--debug",
                        action="store_true",
                        help="Show debugging output.")
    parser.add_argument("-A", "--api-key",
                        default=os.environ[ENV_VAR],
                        help="use a speicifc API KEY")
    parser.add_argument("macaddrs",
                        nargs="*",
                        default=[],
                        help="MAC Address, must be at least 3 octets.")
    args = parser.parse_args()
    if len(args.macaddrs) == 0:
        parser.print_help()
        exit(0)
    return args


# setup logging
def setup_logging(args):
    if args.debug:
        log.basicConfig(format="%(levelname)s: %(message)s", level=log.DEBUG)
        log.debug("Debugging enabled.")
        debug = True
    elif args.verbose:
        log.basicConfig(format="%(levelname)s: %(message)s", level=log.INFO)
        log.info("Verbose output.")
        verbose = True
    else:
        log.basicConfig(format="%(levelname)s: %(message)s")


def main():
    # used as flags
    global debug, verbose
    debug = False
    verbose = False

    args = get_args()
    setup_logging(args)
    api_key = get_api_key(args)
    log.debug('api_key: %s' % (api_key))
 
    macaddrs=get_macaddrs(args)
    mac_map = search_macaddrs(api_key, macaddrs)

    for m in mac_map:
        print "%s %s" % (m, mac_map[m])

    sys.exit(0)


if __name__ == '__main__':
    main()
