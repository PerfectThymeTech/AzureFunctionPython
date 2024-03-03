# General variables
location    = "northeurope"
environment = "dev"
prefix      = "myfunc"
tags        = {}

# Function variables
function_container_registry_url = "https://ghcr.io"
function_container_image        = "ghcr.io/perfectthymetech/azurefunctionpython:main"
function_sku                    = "EP1"
function_sku_cpus               = 1
function_health_path            = "/v1/health/heartbeat"

# Network variables
vnet_id        = "/subscriptions/8f171ff9-2b5b-4f0f-aed5-7fa360a1d094/resourceGroups/mycrp-prd-function-network-rg/providers/Microsoft.Network/virtualNetworks/mycrp-prd-function-vnet001"
nsg_id         = "/subscriptions/8f171ff9-2b5b-4f0f-aed5-7fa360a1d094/resourceGroups/mycrp-prd-function-network-rg/providers/Microsoft.Network/networkSecurityGroups/mycrp-prd-function-nsg001"
route_table_id = "/subscriptions/8f171ff9-2b5b-4f0f-aed5-7fa360a1d094/resourceGroups/mycrp-prd-function-network-rg/providers/Microsoft.Network/routeTables/mycrp-prd-function-rt001"

# Monitoring variables
alert_endpoints = {}

# DNS variables
private_dns_zone_id_blob              = "/subscriptions/8f171ff9-2b5b-4f0f-aed5-7fa360a1d094/resourceGroups/mycrp-prd-global-dns/providers/Microsoft.Network/privateDnsZones/privatelink.blob.core.windows.net"
private_dns_zone_id_queue             = "/subscriptions/8f171ff9-2b5b-4f0f-aed5-7fa360a1d094/resourceGroups/mycrp-prd-global-dns/providers/Microsoft.Network/privateDnsZones/privatelink.queue.core.windows.net"
private_dns_zone_id_table             = "/subscriptions/8f171ff9-2b5b-4f0f-aed5-7fa360a1d094/resourceGroups/mycrp-prd-global-dns/providers/Microsoft.Network/privateDnsZones/privatelink.table.core.windows.net"
private_dns_zone_id_file              = "/subscriptions/8f171ff9-2b5b-4f0f-aed5-7fa360a1d094/resourceGroups/mycrp-prd-global-dns/providers/Microsoft.Network/privateDnsZones/privatelink.file.core.windows.net"
private_dns_zone_id_key_vault         = "/subscriptions/8f171ff9-2b5b-4f0f-aed5-7fa360a1d094/resourceGroups/mycrp-prd-global-dns/providers/Microsoft.Network/privateDnsZones/privatelink.vaultcore.azure.net"
private_dns_zone_id_sites             = "/subscriptions/8f171ff9-2b5b-4f0f-aed5-7fa360a1d094/resourceGroups/mycrp-prd-global-dns/providers/Microsoft.Network/privateDnsZones/privatelink.azurewebsites.net"
private_dns_zone_id_monitor           = "/subscriptions/8f171ff9-2b5b-4f0f-aed5-7fa360a1d094/resourceGroups/mycrp-prd-global-dns/providers/Microsoft.Network/privateDnsZones/privatelink.monitor.azure.com"
private_dns_zone_id_oms_opinsights    = "/subscriptions/8f171ff9-2b5b-4f0f-aed5-7fa360a1d094/resourceGroups/mycrp-prd-global-dns/providers/Microsoft.Network/privateDnsZones/privatelink.oms.opinsights.azure.com"
private_dns_zone_id_ods_opinsights    = "/subscriptions/8f171ff9-2b5b-4f0f-aed5-7fa360a1d094/resourceGroups/mycrp-prd-global-dns/providers/Microsoft.Network/privateDnsZones/privatelink.ods.opinsights.azure.com"
private_dns_zone_id_automation_agents = "/subscriptions/8f171ff9-2b5b-4f0f-aed5-7fa360a1d094/resourceGroups/mycrp-prd-global-dns/providers/Microsoft.Network/privateDnsZones/privatelink.agentsvc.azure-automation.net"
