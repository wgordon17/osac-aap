# Ansible Role Reference

This page documents the parameters for all roles in the OSAC Ansible collections.
Parameter information is sourced from each role's `meta/argument_specs.yaml`.

Collections covered:

- `osac.service` — Core fulfillment service roles (cluster and compute instance lifecycle)
- `osac.templates` — Template roles implementing specific infrastructure patterns
- `osac.config_as_code` — AAP configuration-as-code roles
- `osac.workflows` — Workflow orchestration helper roles
- `osac.test_overrides` — Test override roles for integration testing

## osac.service

<!-- roles:osac.service -->
#### `osac.service.cleanup_stale_network_resources`

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `cleanup_stale_network_resources_namespace` | str | yes |  | Namespace to filter network resources |

#### `osac.service.cluster_infra`

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `agent_resource_class_label` | str | yes |  |  |
| `cluster_infra_name` | str | yes |  |  |
| `cluster_infra_namespace` | str | yes |  |  |
| `cluster_infra_node_requests` | list | no | [] |  |
| `cluster_infra_state` | str | no |  |  |
| `cluster_order` | dict | yes |  |  |
| `cluster_order_label` | str | yes |  |  |
| `cluster_working_namespace` | str | yes |  |  |
| `default_agent_namespace` | str | yes |  |  |
| `network_steps_collection` | str | yes |  | Ansible collection providing network-class-specific steps (e.g. 'netris.steps', 'massopencloud.steps') |

#### `osac.service.cluster_settings`

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `cluster_order` | dict | yes |  | ClusterOrder resource dict. The role reads spec.templateParameters and spec.nodeRequests from this object and may update them with defaults. |
| `cluster_settings_default_credentials_secret_name` | str | no | default-cluster-credentials | Name of the Secret containing default pull-secret and ssh-key. |
| `cluster_settings_default_credentials_secret_namespace` | str | no | fulfillment-aap | Namespace of the default credentials Secret. |
| `cluster_settings_template_defaults` | dict | no | {} | Baseline template parameter defaults. Merged with user-provided templateParameters; user values take precedence. |

#### `osac.service.cluster_working_namespace`

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `cluster_order_label` | str | yes |  | Label key used to identify the cluster's working namespace. |
| `cluster_working_namespace` | str | no |  | Pre-resolved working namespace for the cluster. If already set the lookup step is skipped; the role sets this fact when not provided. |
| `cluster_working_namespace_cluster_order_name` | str | yes |  | Value of the cluster-order label to filter Namespaces against. Typically the ClusterOrder name. |

#### `osac.service.common`

**Entrypoint: `get_remote_cluster_kubeconfig`**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `remote_cluster_kubeconfig` | str | no |  | Path or content of the remote cluster kubeconfig. The role sets this fact from the OSAC_REMOTE_CLUSTER_KUBECONFIG environment variable when the variable is not already defined. |

#### `osac.service.compute_instance_working_namespace`

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `compute_instance` | dict | yes |  | ComputeInstance resource dict. The role reads status.tenantReference.name and status.tenantReference.namespace to locate the working namespace. |
| `compute_instance_working_namespace` | str | no |  | Pre-resolved working namespace for the compute instance. If already set the lookup step is skipped; the role sets this fact when not provided. |

#### `osac.service.enumerate_templates`

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `osac_template_collections` | list | yes |  |  |

#### `osac.service.external_access`

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `cluster_order` | dict | yes |  |  |
| `cluster_working_namespace` | str | yes |  |  |
| `external_access_base_domain` | str | yes |  |  |
| `external_access_name` | str | yes |  |  |
| `external_access_namespace` | str | yes |  |  |
| `external_access_state` | str | no |  |  |
| `network_steps_collection` | str | yes |  | Ansible collection providing network-class-specific steps (e.g. 'netris.steps', 'massopencloud.steps') |

#### `osac.service.extract_template_info`

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `cluster_order` | dict | yes |  | ClusterOrder resource dict. The role extracts spec.templateID, spec.templateParameters, and spec.nodeRequests from this object. |
| `node_requests` | list | no |  | Node requests list. If already set the extraction step is skipped; the role sets this fact when not provided. |
| `template_id` | str | no |  | Resolved template identifier (e.g. osac.templates.ocp_4_17_small). If already set the extraction step is skipped; the role sets this fact when not provided. |
| `template_parameters` | dict | no |  | Parsed template parameters dict. If already set the extraction step is skipped; the role sets this fact when not provided. |

#### `osac.service.finalizer`

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `finalizer_name` | str | yes |  |  |
| `finalizer_state` | str | yes |  |  |
| `finalizer_target` | dict | yes |  |  |
| &nbsp;&nbsp;`finalizer_target.api_version` | str | yes |  |  |
| &nbsp;&nbsp;`finalizer_target.kind` | str | yes |  |  |
| &nbsp;&nbsp;`finalizer_target.name` | str | yes |  |  |
| &nbsp;&nbsp;`finalizer_target.namespace` | str | no |  |  |

#### `osac.service.hosted_cluster`

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `hosted_cluster_controller_availability_policy` | str | no |  |  |
| `hosted_cluster_infrastructure_availability_policy` | str | no |  |  |
| `hosted_cluster_name` | str | yes |  |  |
| `hosted_cluster_namespace` | str | yes |  |  |
| `hosted_cluster_node_requests` | list | no |  |  |
| &nbsp;&nbsp;`hosted_cluster_node_requests.numberOfNodes` | int | yes |  |  |
| &nbsp;&nbsp;`hosted_cluster_node_requests.resourceClass` | str | yes |  |  |
| `hosted_cluster_settings` | dict | yes |  |  |
| &nbsp;&nbsp;`hosted_cluster_settings.ocp_release_image` | str | yes |  |  |
| &nbsp;&nbsp;`hosted_cluster_settings.pull_secret` | str | yes |  |  |
| &nbsp;&nbsp;`hosted_cluster_settings.ssh_public_key` | str | no |  |  |
| `hosted_cluster_state` | str | yes |  |  |

#### `osac.service.lease`

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `lease_delay` | int | no | 1 |  |
| `lease_holder` | str | yes |  |  |
| `lease_name` | str | yes |  |  |
| `lease_retries` | int | no | 0 |  |
| `lease_state` | str | yes |  |  |

#### `osac.service.manage_agents`

**Entrypoint: `attach_and_approve_all_new_agents`**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `manage_agents_cluster_network` | str | yes |  |  |
| `manage_agents_cluster_order_name` | str | yes |  |  |
| `manage_agents_skip_network_attach` | bool | no | False |  |

**Entrypoint: `detach_and_unlabel_all_removed_agents`**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `manage_agents_cluster_order_name` | str | yes |  |  |
| `manage_agents_idle_agents_network` | str | yes |  |  |
| `manage_agents_skip_network_detach` | bool | no | False |  |

**Entrypoint: `select_and_label_new_agents`**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `manage_agents_cluster_order_name` | str | yes |  |  |
| `manage_agents_desired_count` | int | yes |  |  |
| `manage_agents_resource_class` | str | yes |  |  |

**Entrypoint: `wait_for_agents_to_be_removed`**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `manage_agents_cluster_order_name` | str | yes |  |  |
| `manage_agents_desired_count` | int | yes |  |  |
| `manage_agents_resource_class` | str | yes |  |  |

**Entrypoint: `import_agents`**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `manage_agents_idle_agents_network` | str | yes |  |  |
| `manage_agents_node_names` | list | yes |  |  |

**Entrypoint: `remove_agents`**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `manage_agents_node_names` | list | yes |  |  |

#### `osac.service.metallb_ingress`

**Entrypoint: `configure_metallb_ingress`**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `metallb_ingress_admin_kubeconfig` | str | yes |  |  |
| `metallb_ingress_ip` | str | yes |  |  |

#### `osac.service.nmstate_config`

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `nmstate_config_apply_live` | bool | no | True | Whether to apply nmstate config on live agents via SSH. |
| `nmstate_config_state` | str | yes |  | Whether to create or delete NMStateConfig CRs. |

**Entrypoint: `create`**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `nmstate_config_agents` | list | yes |  | List of Agent resources to create NMStateConfig CRs for. |
| `nmstate_config_cluster_name` | str | yes |  | Name of the cluster (used for CR naming and label selectors). |
| `nmstate_config_gateway_cidr` | str | yes |  | VPC gateway in CIDR notation (e.g. 192.168.101.1/24). |
| `nmstate_config_interface_names` | list | no |  | Logical VPC interface names in Netris (used for MAC lookup from agent inventory). |
| `nmstate_config_ip_offset` | int | no | 1 | IP offset for first host (gateway + offset). |
| `nmstate_config_labels` | dict | no |  | Labels to apply to NMStateConfig CRs (must match InfraEnv nmStateConfigLabelSelector). |
| `nmstate_config_mgmt_interface` | str | no |  | Management interface name used to reach agents via SSH. |
| `nmstate_config_mgmt_route_destination` | str | no |  | Management network route destination CIDR. |
| `nmstate_config_mgmt_route_gateway` | str | no |  | Management network gateway (next-hop for the mgmt route). |
| `nmstate_config_mgmt_route_metric` | int | no | 100 | Route metric for the management interface. |
| `nmstate_config_namespace` | str | no |  | Namespace for NMStateConfig CRs. |
| `nmstate_config_server_interfaces` | list | no |  | Actual server interface names for nmstate config (what the OS sees). |
| `nmstate_config_template` | str | no | default_static.yaml.j2 | Jinja2 template file for nmstate YAML. |
| `nmstate_config_vpc_route_metric` | int | no | 50 | Route metric for the VPC default route. |

**Entrypoint: `apply`**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `nmstate_config_agents` | list | yes |  | List of Agent resources to apply nmstate config on. |
| `nmstate_config_cluster_name` | str | yes |  | Name of the cluster (used for looking up NMStateConfig CR annotations). |
| `nmstate_config_gateway_cidr` | str | yes |  | VPC gateway in CIDR notation (e.g. 192.168.101.1/24). |
| `nmstate_config_interface_names` | list | no |  | Logical VPC interface names in Netris (used for MAC lookup from agent inventory). |
| `nmstate_config_ip_offset` | int | no | 1 | IP offset for first host (gateway + offset). |
| `nmstate_config_mgmt_interface` | str | yes |  | Management interface name used to discover agent mgmt IPs. |
| `nmstate_config_mgmt_route_destination` | str | no |  | Management network route destination CIDR. |
| `nmstate_config_mgmt_route_gateway` | str | no |  | Management network gateway (next-hop for the mgmt route). |
| `nmstate_config_mgmt_route_metric` | int | no | 100 | Route metric for the management interface. |
| `nmstate_config_namespace` | str | no |  | Namespace for NMStateConfig CRs. |
| `nmstate_config_server_interfaces` | list | no |  | Actual server interface names for nmstate config (what the OS sees). |
| `nmstate_config_ssh_bastion_host` | str | yes |  | Bastion host to proxy SSH through to reach agent mgmt IPs. |
| `nmstate_config_ssh_bastion_key` | str | yes |  | SSH private key file for local -> bastion connection. |
| `nmstate_config_ssh_bastion_user` | str | yes |  | SSH user for the bastion host. |
| `nmstate_config_ssh_key` | str | yes |  | SSH private key file for bastion -> agent connection. |
| `nmstate_config_ssh_user` | str | no | core | SSH user for connecting to agents. |
| `nmstate_config_template` | str | no | default_static.yaml.j2 | Jinja2 template file for nmstate YAML. |
| `nmstate_config_vpc_route_metric` | int | no | 50 | Route metric for the VPC default route. |

**Entrypoint: `delete`**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `cluster_order_label` | str | yes |  | Label key used to identify NMStateConfig CRs belonging to this cluster. |
| `nmstate_config_cluster_name` | str | yes |  | Name of the cluster (used for label selector to find CRs to delete). |
| `nmstate_config_namespace` | str | yes |  | Namespace for NMStateConfig CRs. |

#### `osac.service.publish_templates`

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `osac_cluster_templates` | list | no |  | Cluster templates to publish to the cluster_templates endpoint |
| `osac_compute_instance_templates` | list | no |  | ComputeInstance templates |
| `osac_fulfillment_service_token` | str | yes |  |  |
| `osac_fulfillment_service_uri` | str | yes |  |  |
| `publish_templates_cluster_api_endpoint` | str | no | <osac_fulfillment_service_uri>/api/private/v1/cluster_templates | API endpoint for cluster templates |
| `publish_templates_compute_instance_api_endpoint` | str | no | <osac_fulfillment_service_uri>/api/private/v1/compute_instance_templates | API endpoint for ComputeInstance templates |

#### `osac.service.retrieve_kubeconfig`

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `retrieve_kubeconfig_cluster_name` | str | yes |  | Name of the HostedCluster to retrieve kubeconfig for |
| `retrieve_kubeconfig_namespace` | str | yes |  | Namespace where the HostedCluster and admin kubeconfig secret are located |
| `retrieve_kubeconfig_wait_delay` | int | no |  | Delay between retries in seconds |
| `retrieve_kubeconfig_wait_retries` | int | no |  | Maximum number of retries to wait for kubeconfig secret |

#### `osac.service.tenant_storage_class`

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `tenant_storage_class_tenant_name` | str | yes |  | Tenant name (e.g. from compute_instance.status.tenantReference.name) used to look up the Tenant CR. |
| `tenant_storage_class_tenant_namespace` | str | yes |  | Namespace of the Tenant CR on the management cluster (e.g. from compute_instance.status.tenantReference.namespace). |

#### `osac.service.wait_for`

**Entrypoint: `wait_for_dns`**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `wait_for_dns_delay` | int | no |  |  |
| `wait_for_dns_record` | str | yes |  |  |
| `wait_for_dns_retries` | int | no |  |  |

**Entrypoint: `wait_for_cluster`**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `wait_for_cluster_delay` | int | no |  |  |
| `wait_for_cluster_retries` | int | no |  |  |
| `wait_for_kubeconfig` | str | yes |  |  |

#### `osac.service.write_ssh_keys`

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `server_ssh_bastion_key` | str | yes |  | Destination path for the bastion SSH private key. Key content is read from the SERVER_SSH_BASTION_KEY environment variable (base64-encoded). |
| `server_ssh_key` | str | yes |  | Destination path for the server SSH private key. The parent directory is created automatically with mode 0700. Key content is read from the SERVER_SSH_KEY environment variable (base64-encoded). |

<!-- /roles:osac.service -->

## osac.templates

<!-- roles:osac.templates -->
#### `osac.templates.cudn_net`

**Entrypoint: `create_virtual_network`**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `default_ipam_lifecycle` | str | no | Persistent | IPAM lifecycle setting for ClusterUserDefinedNetwork. |
| `default_layer2_role` | str | no | Primary | Layer2 topology role for ClusterUserDefinedNetwork. |
| `default_subnet_labels` | dict | no | {'osac.io/managed-by': 'osac-fulfillment'} | Default labels applied to Subnet-created namespaces. |
| `virtual_network` | dict | yes |  | VirtualNetwork CR from the fulfillment operator. |
| `virtual_network_name` | str | yes |  | Name of the VirtualNetwork resource. |

**Entrypoint: `delete_virtual_network`**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `virtual_network` | dict | yes |  | VirtualNetwork CR from the fulfillment operator. |
| `virtual_network_name` | str | yes |  | Name of the VirtualNetwork resource. |

**Entrypoint: `create_subnet`**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `default_subnet_labels` | dict | no | {'osac.io/managed-by': 'osac-fulfillment'} | Default labels applied to the created namespace. |
| `subnet` | dict | yes |  | Subnet CR from the fulfillment operator. |
| `subnet_name` | str | yes |  | Name of the Subnet resource. |

**Entrypoint: `delete_subnet`**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `subnet` | dict | yes |  | Subnet CR from the fulfillment operator. |
| `subnet_name` | str | yes |  | Name of the Subnet resource. |

**Entrypoint: `create_security_group`**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `default_security_group_labels` | dict | no | {'osac.io/managed-by': 'osac-fulfillment'} | Default labels applied to created NetworkPolicy resources. |
| `security_group` | dict | yes |  | SecurityGroup CR from the fulfillment operator. |

**Entrypoint: `delete_security_group`**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `security_group` | dict | yes |  | SecurityGroup CR from the fulfillment operator. |

#### `osac.templates.metallb_l2`

**Entrypoint: `create_public_ip_pool`**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `public_ip_pool` | dict | yes |  | PublicIPPool CR from fulfillment-api via EDA payload |
| `public_ip_pool_name` | str | yes |  | Name of the PublicIPPool resource |
| `template_parameters` | dict | no | {} | Template-specific parameters (reserved for future use) |

**Entrypoint: `delete_public_ip_pool`**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `public_ip_pool` | dict | yes |  | PublicIPPool CR from fulfillment-api via EDA payload |
| `public_ip_pool_name` | str | yes |  | Name of the PublicIPPool resource |

#### `osac.templates.ocp_4_17_small`

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `cluster_order` | dict | yes |  |  |
| `cluster_working_namespace` | str | yes |  |  |
| `node_requests` | list | no |  |  |
| &nbsp;&nbsp;`node_requests.numberOfNodes` | int | yes |  |  |
| &nbsp;&nbsp;`node_requests.resourceClass` | str | yes |  |  |
| `template_parameters` | dict | no |  |  |
| &nbsp;&nbsp;`template_parameters.pull_secret` | str | yes |  | The pull secret contains credentials for authenticating to image repositories. |
| &nbsp;&nbsp;`template_parameters.ssh_public_key` | str | no |  | A public ssh key that will be installed into the `authorized_keys` file of the `core` user on cluster worker nodes. |

#### `osac.templates.ocp_4_17_small_github`

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `cluster_order` | dict | yes |  |  |
| `cluster_working_namespace` | str | yes |  |  |
| `node_requests` | list | no |  |  |
| &nbsp;&nbsp;`node_requests.numberOfNodes` | int | yes |  |  |
| &nbsp;&nbsp;`node_requests.resourceClass` | str | yes |  |  |
| `template_parameters` | dict | no |  |  |
| &nbsp;&nbsp;`template_parameters.github_client_id` | str | yes |  | GitHub Oauth client id |
| &nbsp;&nbsp;`template_parameters.github_client_secret` | str | yes |  | GitHub Oauth client secret |
| &nbsp;&nbsp;`template_parameters.github_mapping_method` | str | no | claim | Configure how OpenShift oauth will map GitHub identities to GitHub users. See [the OpenShift documentation][docs] for more information.  [docs]: https://docs.redhat.com/en/documentation/openshift_container_platform/4.18/html/authentication_and_authorization/understanding-identity-provider#removing-kubeadmin_understanding-identity-provider |
| &nbsp;&nbsp;`template_parameters.github_organizations` | list | no |  | A list of GitHub organizations that should be allowed to authenticate to the cluster. |
| &nbsp;&nbsp;`template_parameters.github_teams` | list | no |  | A list of GitHub teams that should be allowed to authenticate to the cluster. |
| &nbsp;&nbsp;`template_parameters.pull_secret` | str | yes |  | The pull secret contains credentials for authenticating to image repositories. |
| &nbsp;&nbsp;`template_parameters.ssh_public_key` | str | no |  | A public ssh key that will be installed into the `authorized_keys` file of the `core` user on cluster worker nodes. |

#### `osac.templates.ocp_virt_vm`

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `compute_instance` | dict | yes |  | ComputeInstance configuration |
| `gpu_device_name` | str | no |  | The resource name of the GPU device to pass through to the virtual machine. When set, the virtual machine will be configured with GPU passthrough support via the `hostDevices` field in the KubeVirt domain devices spec.  This must match a `resourceName` defined in the KubeVirt CR under `spec.configuration.permittedHostDevices.pciHostDevices`. For example, to pass through an NVIDIA A100 PCIe 80GB (PCI ID `10DE:20B5`), the KubeVirt CR should contain:      configuration:       permittedHostDevices:         pciHostDevices:           - pciVendorSelector: "10DE:20B5"             resourceName: "nvidia.com/GA100"             externalResourceProvider: false  And the value of this parameter would be `nvidia.com/GA100`.  The PCI vendor and product ID for a given GPU can be found by running `lspci -nn \| grep -i nvidia` on a node that has the device. |
| `template_parameters` | dict | no |  | VM configuration parameters |
| &nbsp;&nbsp;`template_parameters.exposed_ports` | str | no | 22/tcp | Ports to expose on the VM for ingress traffic. The syntax is a comma-separated list of `<port>/<protocol>` pairs, where `<protocol>` is either `tcp` or `udp`. For example, `22/tcp,80/tcp` will expose tcp ports 22 and 80 on the VM. |

<!-- /roles:osac.templates -->

## osac.config_as_code

<!-- roles:osac.config_as_code -->
#### `osac.config_as_code.aap`

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `aap_ee_image` | str | yes |  | Container image reference for the AAP execution environment. |
| `aap_organization_name` | str | yes |  | Name of the AAP organization to configure resources in. |
| `aap_prefix` | str | yes |  | Prefix applied to all AAP resource names (projects, templates, inventories, instance groups, schedules). Typically the deployment environment identifier. |
| `aap_project_name` | str | yes |  | Human-readable project name used in descriptions. |
| `osac_publish_templates_enabled` | bool | no |  | Whether the publish-templates periodic schedule is enabled. |

<!-- /roles:osac.config_as_code -->

## osac.workflows

<!-- roles:osac.workflows -->
#### `osac.workflows.workflow_helpers`

_No parameters._

<!-- /roles:osac.workflows -->

## osac.test_overrides

<!-- roles:osac.test_overrides -->
#### `osac.test_overrides.ocp_virt_vm_with_gpu`

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `compute_instance` | dict | yes |  | ComputeInstance configuration |
| `template_parameters` | dict | no |  | VM configuration parameters |
| &nbsp;&nbsp;`template_parameters.exposed_ports` | str | no | 22/tcp | Ports to expose on the VM for ingress traffic. The syntax is a comma-separated list of `<port>/<protocol>` pairs, where `<protocol>` is either `tcp` or `udp`. For example, `22/tcp,80/tcp` will expose tcp ports 22 and 80 on the VM. |

<!-- /roles:osac.test_overrides -->
