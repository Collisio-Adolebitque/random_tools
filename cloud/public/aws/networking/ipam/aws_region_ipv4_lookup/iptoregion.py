# _*_ coding: utf-8 _*_
# !/usr/bin/env python3

"""
AWS Region Finder.

Created on: 06/03/2020

Requirements:

Python 3.5 or higher
ipaddress==1.0.23
requests==2.23.0

Run command:
    pip3 install ipaddress
to install the IP Address Library.

Run command:
    pip3 install requests
to install the Requests Library.

Command line usage example (on Mac):
    python3 iptoregion.py 54.153.41.72

NB: If valid AWS IP address is not entered the script will error
out as I haven't added validation yet.
"""

import requests
import json
import sys
from ipaddress import ip_network, ip_address


def get_aws_ip_ranges():
    """
    Pull the latest copy of the AWS IP Range JSON file from the web.
    :return: dict
    """
    try:
        aws_ranges = requests.get('https://ip-ranges.amazonaws.com/ip-ranges.json').text
        result = json.loads(aws_ranges)
        return result
    except requests.exceptions.HTTPError as err:
        return 'Error: {}'.format(err)


def find_aws_region(ip: str) -> list:
    """
    Get the list of prefixes from the aws_ip_dictionary and search for a match on the IP address.
    :param ip:
    :return: list
    """
    aws_ip_dictionary = get_aws_ip_ranges()
    prfx_lst = aws_ip_dictionary['prefixes']
    aws_ip = ip_address(ip)
    prefix_and_region = [prfx for prfx in prfx_lst if aws_ip in ip_network(prfx['ip_prefix'])]
    return prefix_and_region


def main():
    if len(sys.argv) == 2:
        supplied_ip_address = sys.argv[1]
        result = find_aws_region(supplied_ip_address)
        print('IP address: {}, Subnet: {}, Region: {}.'.format(supplied_ip_address,
                                                               result[0]['ip_prefix'],
                                                               result[0]['region']))
    else:
        print('Wrong number of arguments, please try again.')


if __name__ == '__main__':
    main()
