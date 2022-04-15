"""A Kubernetes Python Pulumi program"""

import pulumi
from pulumi_kubernetes.apps.v1 import Deployment, DeploymentSpecArgs
from pulumi_kubernetes.meta.v1 import LabelSelectorArgs, ObjectMetaArgs
from pulumi_kubernetes.core.v1 import ContainerArgs, PodSpecArgs, PodTemplateSpecArgs, Namespace

config = pulumi.Config()
ns_name = config.get('namespace')
replicas = config.get_int('replicas') or 1

app_labels = { "app": "nginx" }
namespace = Namespace("web", metadata = ObjectMetaArgs(name=ns_name))
deployment = Deployment(
    "nginx",
    metadata = ObjectMetaArgs(name="nginx", namespace=namespace.metadata["name"]),
    spec=DeploymentSpecArgs(
        selector=LabelSelectorArgs(match_labels=app_labels),
        replicas=replicas,
        template=PodTemplateSpecArgs(
            metadata=ObjectMetaArgs(labels=app_labels),
            spec=PodSpecArgs(containers=[ContainerArgs(name="nginx", image="nginx")])
        ),
    ))

pulumi.export("namespace_name", namespace.metadata["name"])
pulumi.export("deployment_name", deployment.metadata["name"])
