#!/usr/bin/env python3
import pynetbox
import argparse
from rich.console import Console
from rich.table import Table
import requests
from requests.packages import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def print_prefixes(nb, site):
    """
    print prefixes per site
    """
    table_prefixes = Table(title="PREFIXES")
    table_prefixes.add_column("PREFIX", justify="center", style="cyan", no_wrap=True)
    table_prefixes.add_column("DESCRIPTION", style="magenta")
    table_prefixes.add_column("VLAN ID", justify="center", style="green", no_wrap=True)
    table_prefixes.add_column(
        "VLAN NAME", justify="center", style="yellow", no_wrap=True
    )
    for p in nb.ipam.prefixes.filter(site=site):
        if p.vlan:
            table_prefixes.add_row(
                p.prefix,
                p.description,
                str(nb.ipam.vlans.filter(site=site, name=p.vlan)[0].vid),
                str(p.vlan),
            )
        else:
            table_prefixes.add_row(p.prefix, p.description, str(p.vlan), "")
    console = Console()
    console.print(table_prefixes)


def print_vlans(nb, site):
    """
    print vlans per site
    """
    table_vlans = Table(title="VLANS")
    table_vlans.add_column("VLAN ID", justify="center", style="cyan", no_wrap=True)
    table_vlans.add_column("NAME", style="magenta")
    table_vlans.add_column("DESCRIPTION", style="green")
    for v in nb.ipam.vlans.filter(site=site):
        table_vlans.add_row(str(v.vid), v.name, v.description)
    console = Console()
    console.print(table_vlans)


def print_ip(nb, site):
    """
    print ip addresses per site
    """
    table_ip = Table(title="IP ADDRESSES")
    table_ip.add_column("PREFIX", justify="center", style="cyan", no_wrap=True)
    table_ip.add_column("VLAN", style="yellow")
    table_ip.add_column("IP", style="magenta")
    table_ip.add_column("NAME", style="green")
    for p in nb.ipam.prefixes.filter(site=site):
        ipList = nb.ipam.ip_addresses.filter(parent=p.prefix)
        for ip in ipList:
            if p.vlan:
                table_ip.add_row(
                    p.prefix,
                    str(nb.ipam.vlans.filter(site=site, name=p.vlan)[0].vid),
                    ip.address,
                    ip.description,
                )

    console = Console()
    console.print(table_ip)


def main():

    my_parser = argparse.ArgumentParser(description="Netbox site report")
    my_parser.add_argument("site", help="site", action="store", type=str)
    my_parser.add_argument("url", help="netbox url", action="store", type=str)
    my_parser.add_argument("token", help="netbox token", action="store", type=str)
    args = my_parser.parse_args()
    site = args.site
    netboxurl = args.url
    token = args.token
    nb = pynetbox.api(url=netboxurl, token=token, ssl_verify=False)
    print_prefixes(nb, site)
    print_vlans(nb, site)
    print_ip(nb, site)
    return True


main()
