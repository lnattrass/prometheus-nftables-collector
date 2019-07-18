# prometheus-nftables-collector

This Textfile Collector for Prometheus Node Exporter exports named counters, meters, maps and sets from the Nftables ruleset to Prometheus.

## Requirements

You need `python3.7` or newer to run the collector script and obviously `nft` (tested with `v0.9.0`).

## Setup

``` sh
install -D -m 755 ./collector.py /usr/share/prometheus-node-exporter/nftables.py
install -D -t /etc/systemd/system ./prometheus-node-exporter-nftables.service ./prometheus-node-exporter-nftables.timer
systemctl enable --now prometheus-node-exporter-nftables.timer
```

## Example

Nftables ruleset

``` nft
table ip filter {
  counter http-allowed {
  }

  counter http-denied {
  }

  chain input {
    type filter hook input priority 0
    policy drop
    tcp dport { 80, 443 } meter http-limit { ip saddr limit rate over 16mbytes/second } counter name http-denied drop
    tcp dport { 80, 443 } counter name http-allowed accept
  }
}
```

Resulting metrics

``` prom
nftables_counter_bytes{family="ip", name="http-allowed", table="filter", handle="17"} 90576
nftables_counter_packets{family="ip", name="http-allowed", table="filter", handle="17"} 783
nftables_counter_bytes{family="ip", name="http-denied", table="filter", handle="20"} 936
nftables_counter_packets{family="ip", name="http-denied", table="filter", handle="20"} 13
nftables_meter_element_count{family="ip", name="http-limit", table="filter", type="ipv4_addr", handle="34"} 3
```
