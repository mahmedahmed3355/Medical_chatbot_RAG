from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
K8S_DIR = PROJECT_ROOT / "k8s"


def read_manifest(name: str) -> str:
    return (K8S_DIR / name).read_text(encoding="utf-8")


def test_required_kubernetes_manifests_exist():
    required_manifests = {
        "namespace.yaml",
        "configmap.yaml",
        "deployment.yaml",
        "service.yaml",
        "limitrange.yaml",
        "resourcequota.yaml",
        "networkpolicy.yaml",
        "poddisruptionbudget.yaml",
        "kustomization.yaml",
    }

    existing_manifests = {path.name for path in K8S_DIR.glob("*.yaml")}

    assert required_manifests <= existing_manifests


def test_kustomization_includes_all_resource_manifests():
    kustomization = read_manifest("kustomization.yaml")

    required_resources = {
        "namespace.yaml",
        "configmap.yaml",
        "deployment.yaml",
        "service.yaml",
        "networkpolicy.yaml",
        "resourcequota.yaml",
        "limitrange.yaml",
        "poddisruptionbudget.yaml",
    }

    for resource in required_resources:
        assert f"  - {resource}" in kustomization


def test_deployment_matches_application_runtime_contract():
    deployment = read_manifest("deployment.yaml")
    dockerfile = (PROJECT_ROOT / "Dockerfile").read_text(encoding="utf-8")
    application = (PROJECT_ROOT / "app" / "application.py").read_text(encoding="utf-8")

    assert "kind: Deployment" in deployment
    assert "name: medical-rag-chatbot" in deployment
    assert "containerPort: 5000" in deployment
    assert "name: http" in deployment

    assert "EXPOSE 5000" in dockerfile
    assert "0.0.0.0:5000" in dockerfile

    assert '@app.get("/health")' in application


def test_deployment_health_probes_target_application_health_endpoint():
    deployment = read_manifest("deployment.yaml")

    assert "startupProbe:" in deployment
    assert "readinessProbe:" in deployment
    assert "livenessProbe:" in deployment

    assert deployment.count("path: /health") >= 3
    assert deployment.count("port: http") >= 3


def test_service_matches_deployment_selector_and_named_port():
    deployment = read_manifest("deployment.yaml")
    service = read_manifest("service.yaml")

    assert "app: medical-rag-chatbot" in deployment
    assert "app: medical-rag-chatbot" in service

    assert "port: 80" in service
    assert "targetPort: http" in service


def test_deployment_uses_configmap_port_contract():
    deployment = read_manifest("deployment.yaml")
    configmap = read_manifest("configmap.yaml")

    assert "name: PORT" in deployment
    assert "name: medical-rag-config" in deployment
    assert "key: PORT" in deployment

    assert "kind: ConfigMap" in configmap
    assert "name: medical-rag-config" in configmap
    assert 'PORT: "5000"' in configmap


def test_deployment_defines_resource_requests_and_limits():
    deployment = read_manifest("deployment.yaml")

    assert "resources:" in deployment
    assert "requests:" in deployment
    assert "limits:" in deployment

    assert 'cpu: "250m"' in deployment
    assert 'memory: "512Mi"' in deployment
    assert 'cpu: "1"' in deployment
    assert 'memory: "1Gi"' in deployment


def test_resource_governance_manifests_define_expected_contracts():
    limit_range = read_manifest("limitrange.yaml")
    resource_quota = read_manifest("resourcequota.yaml")

    assert "kind: LimitRange" in limit_range
    assert "type: Container" in limit_range
    assert "defaultRequest:" in limit_range
    assert "max:" in limit_range
    assert "min:" in limit_range

    assert "kind: ResourceQuota" in resource_quota
    assert "requests.cpu:" in resource_quota
    assert "requests.memory:" in resource_quota
    assert "limits.cpu:" in resource_quota
    assert "limits.memory:" in resource_quota
    assert 'pods: "10"' in resource_quota


def test_pod_disruption_budget_matches_application_selector():
    deployment = read_manifest("deployment.yaml")
    pdb = read_manifest("poddisruptionbudget.yaml")

    assert "kind: PodDisruptionBudget" in pdb
    assert "minAvailable: 1" in pdb

    assert "app: medical-rag-chatbot" in deployment
    assert "app: medical-rag-chatbot" in pdb


def test_network_policy_targets_application_and_required_ports():
    network_policy = read_manifest("networkpolicy.yaml")

    assert "kind: NetworkPolicy" in network_policy
    assert "app: medical-rag-chatbot" in network_policy

    assert "- Ingress" in network_policy
    assert "- Egress" in network_policy

    assert "port: 5000" in network_policy
    assert "port: 443" in network_policy
    assert network_policy.count("port: 53") >= 2


def test_namespace_contract_is_consistent():
    namespace = read_manifest("namespace.yaml")

    assert "kind: Namespace" in namespace
    assert "name: medical-rag" in namespace

    for manifest_name in {
        "configmap.yaml",
        "deployment.yaml",
        "service.yaml",
        "limitrange.yaml",
        "resourcequota.yaml",
        "networkpolicy.yaml",
        "poddisruptionbudget.yaml",
    }:
        manifest = read_manifest(manifest_name)
        assert "namespace: medical-rag" in manifest
