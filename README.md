# prometheus-nftables-collector
Nftables Textfile Collector for Prometheus Node Exporter

## Requirements

You need `python3.7` or newer to run the collector script and obviously `nft` (tested with `v0.9.0`).

## Setup

``` sh
install -D -m 755 ./collector.py /usr/share/prometheus-node-exporter/nftables.py
install -D -t /etc/systemd/system ./prometheus-node-exporter-nftables.service ./prometheus-node-exporter-nftables.timer
systemctl enable --now prometheus-node-exporter-nftables.timer
```
