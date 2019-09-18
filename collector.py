#!/usr/bin/env python3
import json
import subprocess
import sys

"""
Collect metrics from Nftables for Prometheus Node Exporter

Powered by the undocumented option '--json' of the nft command line tool.
"""

def fetch_json(*args: str):
    process = subprocess.run(
        args,
        capture_output=True,
        check=True,
        text=True,
    )
    return json.loads(process.stdout)


def list_counters() -> list:
    obj = fetch_json('nft', '--json', 'list', 'counters')
    return [item['counter'] for item in obj.get('nftables', []) if 'counter' in item]


def list_maps() -> list:
    obj = fetch_json('nft', '--json', 'list', 'maps')
    return [item['map'] for item in obj.get('nftables', []) if 'map' in item]


def list_meters() -> list:
    obj = fetch_json('nft', '--json', 'list', 'meters')
    return [item['meter'] for item in obj.get('nftables', []) if 'meter' in item]


def list_sets() -> list:
    obj = fetch_json('nft', '--json', 'list', 'sets')
    return [item['set'] for item in obj.get('nftables', []) if 'set' in item]


def format_labels(obj: dict) -> str:
    return ''.join((
        '{',
        ', '.join(f'{key}="{value}"' for key, value in obj.items()),
        '}',
    ))


def format_metric(name: str, labels: dict, value) -> str:
    return ''.join((name, format_labels(labels), ' ', str(value)))


def without(obj: dict, *keys: str) -> dict:
    return {key: value for key, value in obj.items() if key not in set(keys)}


def main() -> None:
    print('Collecting counters ...', file=sys.stderr)
    print('# HELP nftables_counter_bytes Mamed counters in bytes')
    print('# TYPE nftables_counter_bytes counter')
    print('# HELP nftables_counter_packets Named counters in packets')
    print('# TYPE nftables_counter_packets counter')
    for item in list_counters():
        print(format_metric(
            'nftables_counter_bytes',
            without(item, 'bytes', 'packets'),
            item['bytes'],
        ))
        print(format_metric(
            'nftables_counter_packets',
            without(item, 'bytes', 'packets'),
            item['packets'],
        ))
    print('Collecting maps ...', file=sys.stderr)
    print('# HELP nftables_map_element_count Element count of named maps')
    print('# TYPE nftables_map_element_count gauge')
    for item in list_maps():
        print(format_metric(
            'nftables_map_element_count',
            without(item, 'elem', 'flags'),
            len(item.get('elem', [])),
        ))
    print('Collecting meters ...', file=sys.stderr)
    print('# HELP nftables_meter_element_count Element count of named meters')
    print('# TYPE nftables_meter_element_count gauge')
    for item in list_meters():
        print(format_metric(
            'nftables_meter_element_count',
            without(item, 'elem', 'flags', 'size'),
            len(item.get('elem', [])),
        ))
    print('Collecting sets ...', file=sys.stderr)
    print('# HELP nftables_set_element_count Element count of named sets')
    print('# TYPE nftables_set_element_count gauge')
    for item in list_sets():
        print(format_metric(
            'nftables_set_element_count',
            without(item, 'elem', 'flags', 'size'),
            len(item.get('elem', [])),
        ))
    print('Done', file=sys.stderr)


if __name__ == '__main__':
    main()

