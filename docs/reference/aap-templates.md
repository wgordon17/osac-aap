# AAP Job Template Reference

This page documents the Ansible Automation Platform (AAP) job templates and
workflows defined in the OSAC deployment. Templates are configured by the
`osac.config_as_code.aap` role via `collections/ansible_collections/osac/config_as_code/roles/aap/vars/controller.yml`.

Template names use a configurable prefix (`aap_prefix`) that is substituted at
deploy time. The tables below show the prefix as `<aap_prefix>`.

## Cluster Fulfillment Templates

<!-- aap:cluster-templates -->
| Name | Playbook | Inventory | Instance Group |
|------|----------|-----------|----------------|
| <aap_prefix>-create-hosted-cluster | playbook_osac_create_hosted_cluster.yml | <aap_prefix>-cluster-fulfillment | <aap_prefix>-cluster-fulfillment-ig |
| <aap_prefix>-delete-hosted-cluster | playbook_osac_delete_hosted_cluster.yml | <aap_prefix>-cluster-fulfillment | <aap_prefix>-cluster-fulfillment-ig |
| <aap_prefix>-config-as-code | playbook_osac_config_as_code.yml | <aap_prefix>-config-as-code | <aap_prefix>-config-as-code-ig |
| <aap_prefix>-publish-templates | collections/ansible_collections/osac/service/playbooks/publish_templates.yaml | <aap_prefix>-publish-templates | <aap_prefix>-publish-templates-ig |
| <aap_prefix>-create-hosted-cluster-post-install | playbook_osac_create_hosted_cluster_post_install.yml | <aap_prefix>-cluster-fulfillment | <aap_prefix>-create-hosted-cluster-post-install-ig |
| <aap_prefix>-report-hosted-cluster-status-success | playbook_osac_report_hosted_cluster_status.yml | <aap_prefix>-cluster-fulfillment | <aap_prefix>-cluster-fulfillment-ig |
| <aap_prefix>-report-hosted-cluster-status-failure | playbook_osac_report_hosted_cluster_status.yml | <aap_prefix>-cluster-fulfillment | <aap_prefix>-cluster-fulfillment-ig |

<!-- /aap:cluster-templates -->

## Compute Instance Templates

<!-- aap:compute-templates -->
| Name | Playbook | Inventory | Instance Group |
|------|----------|-----------|----------------|
| <aap_prefix>-create-compute-instance | playbook_osac_create_compute_instance.yml | <aap_prefix>-compute-instance-operations | <aap_prefix>-compute-instance-operations-ig |
| <aap_prefix>-delete-compute-instance | playbook_osac_delete_compute_instance.yml | <aap_prefix>-compute-instance-operations | <aap_prefix>-compute-instance-operations-ig |

<!-- /aap:compute-templates -->

## Networking Templates

<!-- aap:networking-templates -->
| Name | Playbook | Inventory | Instance Group |
|------|----------|-----------|----------------|
| <aap_prefix>-create-virtual-network | playbook_osac_create_virtual_network.yml | <aap_prefix>-networking-operations | <aap_prefix>-networking-operations-ig |
| <aap_prefix>-delete-virtual-network | playbook_osac_delete_virtual_network.yml | <aap_prefix>-networking-operations | <aap_prefix>-networking-operations-ig |
| <aap_prefix>-create-subnet | playbook_osac_create_subnet.yml | <aap_prefix>-networking-operations | <aap_prefix>-networking-operations-ig |
| <aap_prefix>-delete-subnet | playbook_osac_delete_subnet.yml | <aap_prefix>-networking-operations | <aap_prefix>-networking-operations-ig |
| <aap_prefix>-create-public-ip-pool | playbook_osac_create_public_ip_pool.yml | <aap_prefix>-networking-operations | <aap_prefix>-networking-operations-ig |
| <aap_prefix>-delete-public-ip-pool | playbook_osac_delete_public_ip_pool.yml | <aap_prefix>-networking-operations | <aap_prefix>-networking-operations-ig |

<!-- /aap:networking-templates -->

## Other Templates

<!-- aap:other-templates -->
_None._

<!-- /aap:other-templates -->

## Workflows

Workflows chain job templates together for multi-step operations with
success/failure branching.

<!-- aap:workflows -->
| Name | Description | Nodes |
|------|-------------|-------|
| <aap_prefix>-create-hosted-cluster-workflow | Workflow for creating hosted cluster | create-cluster, post-install, report-hosted-cluster-status-success, report-hosted-cluster-status-failure |
| <aap_prefix>-delete-hosted-cluster-workflow | Workflow for deleting hosted cluster | delete-cluster, report-hosted-cluster-status-success, report-hosted-cluster-status-failure |

<!-- /aap:workflows -->
