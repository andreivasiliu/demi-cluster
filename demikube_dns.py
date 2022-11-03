#!/usr/bin/python3

import os
import subprocess
import re
import logging
from typing import Dict, Iterator, NamedTuple, Tuple, Optional

import kubernetes


log = logging.getLogger('demikube-dns')


class ServiceEvent(NamedTuple):
    event: str
    service: str
    namespace: str
    ip: Optional[str]


def service_events() -> Iterator[ServiceEvent]:
    v1 = kubernetes.client.CoreV1Api()
    watch = kubernetes.watch.Watch()

    for event in watch.stream(v1.list_service_for_all_namespaces):
        event_type = event['type']
        obj = event['object']

        yield ServiceEvent(
            event=event_type,
            service=obj.metadata.name,
            namespace=obj.metadata.namespace,
            ip=obj.spec.cluster_ip
        )


def write_hosts(hosts: Dict[Tuple[str, str], Optional[str]]) -> None:
    with open('/etc/hosts.kubernetes.tmp', 'w') as f:
        for (name, namespace), ip in hosts.items():
            if not ip or ip == "None":
                continue

            if not re.match("^[a-z_-]+$", name) or not re.match("^[a-z_-]+$", namespace):
                continue

            names = ' '.join([
                f"{name}",
                f"{name}.{namespace}",
                f"{name}.{namespace}.svc.cluster.local",
                f"{name}.svc.cluster.local",
                f"{name}.cluster.local",
                f"{name}.k",
                f"{name}.k.demi.lan",
            ])

            f.write(f"{ip}\t{names}\n")
        
    os.rename('/etc/hosts.kubernetes.tmp', '/etc/hosts.kubernetes')


def reload_dnsmasq() -> None:
    subprocess.check_call([
        '/usr/bin/systemctl', 'reload', 'dnsmasq'
    ])


def main_loop() -> None:
    kubernetes.config.load_kube_config("/var/demi/k8s/demikube.kubeconfig")

    hosts = {}

    for event, service, namespace, ip in service_events():
        if event == 'ADDED':
            hosts[(service, namespace)] = ip
        elif event == 'DELETED':
            del hosts[(service, namespace)]
        else:
            log.info("%s", f"Ignoring {event} event for {service} ({namespace})")
            continue

        log.info("%s", f"{event} service {service} ({namespace})")
        write_hosts(hosts)
        reload_dnsmasq()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    main_loop()
