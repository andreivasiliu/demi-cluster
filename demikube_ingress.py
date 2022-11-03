#!/var/demi/k8s/venv/bin/python3

from typing import (
    NamedTuple, Optional, List, Union, Literal, Iterator, NoReturn, Dict,
)
import logging
import subprocess
import itertools
import os
import re

import kubernetes


log = logging.getLogger('demikube-ingress')


class IngressRule(NamedTuple):
    host: Optional[str]
    prefix: bool
    path: str
    service_name: str
    service_port: Union[int, str]


class Ingress(NamedTuple):
    name: str
    namespace: str
    default_backend: Optional[str]
    rules: List[IngressRule]


def ingress_events() -> Iterator[Ingress]:
    watch = kubernetes.watch.Watch()
    net_v1 = kubernetes.client.NetworkingV1Api()

    for event in watch.stream(net_v1.list_ingress_for_all_namespaces):
        event_type = event['type']
        ingress = event['object']

        yield event_type, Ingress(
            name=ingress.metadata.name,
            namespace=ingress.metadata.namespace,
            default_backend=ingress.spec.default_backend,
            rules=[
                IngressRule(
                    host=rule.host,
                    prefix=path.path_type == "Prefix",
                    path=path.path,
                    service_name=path.backend.service.name,
                    service_port=path.backend.service.port.name or path.backend.service.port.number,
                )
                for rule in ingress.spec.rules
                for path in rule.http.paths
            ]
        )


def write_ingresses(ingresses: Dict[str, Ingress]) -> None:
    rules = sorted(
        (rule for ingress in ingresses.values() for rule in ingress.rules),
        key=lambda rule: -len(rule.path)
    )

    with open('/etc/nginx-ingresses.conf.tmp', 'w') as f:
        for host, host_rules in itertools.groupby(rules, lambda rule: rule.host):
            if not re.match("^[a-z_\\./-]+$", host):
                continue

            for rule in host_rules:
                # Proxy to just simple services in the cluster for now
                if not re.match("^[a-z_\\.-]+$", rule.service_name):
                    continue

                # Allow just simple paths
                if not re.match("^[a-z_/-]+$", rule.path):
                    continue

                if rule.prefix:
                    path_prefix = rule.path.rstrip('/')
                    matcher = f'~^{host}/{path_prefix}(?<path_suffix>.*)$'
                else:
                    matcher = f'{host}/{rule.path}'

                service_name = rule.service_name + ".svc.cluster.local"
                target = f"{service_name}:{rule.service_port}"

                f.write(f'"{matcher}"\t"{target}";\n')
        
    os.rename('/etc/nginx-ingresses.conf.tmp', '/etc/nginx-ingresses.conf')


def reload_nginx() -> None:
    subprocess.check_call([
        '/usr/bin/systemctl', 'reload', 'nginx'
    ])


def main_loop() -> NoReturn:
    kubernetes.config.load_kube_config("/var/demi/k8s/demikube-ingress.kubeconfig")

    ingresses = {}

    for event_type, ingress in ingress_events():
        log.info(f"Ingress {ingress.namespace}/{ingress.name} {event_type}")

        if event_type in ('ADDED', 'MODIFIED'):
            ingresses[f"{ingress.namespace}/{ingress.name}"] = ingress
        elif event_type == 'DELETED':
            del ingresses[f"{ingress.namespace}/{ingress.name}"]
        else:
            log.warning("Ignored unknown event type %s", event_type)
            continue

        write_ingresses(ingresses)
        reload_nginx()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    main_loop()
