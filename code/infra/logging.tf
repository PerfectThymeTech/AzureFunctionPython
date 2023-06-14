resource "azurerm_application_insights" "application_insights" {
  name                = "${local.prefix}-appi001"
  location            = var.location
  resource_group_name = azurerm_resource_group.logging_rg.name
  tags                = var.tags

  application_type                      = "other"
  daily_data_cap_notifications_disabled = false
  disable_ip_masking                    = false
  force_customer_storage_for_profiler   = false
  internet_ingestion_enabled            = true
  internet_query_enabled                = true
  local_authentication_disabled         = false
  retention_in_days                     = 90
  sampling_percentage                   = 100
  workspace_id                          = azurerm_log_analytics_workspace.log_analytics_workspace.id
}

data "azurerm_monitor_diagnostic_categories" "diagnostic_categories_application_insights" {
  resource_id = azurerm_application_insights.application_insights.id
}

resource "azurerm_monitor_diagnostic_setting" "diagnostic_setting_application_insights" {
  name                       = "logAnalytics"
  target_resource_id         = azurerm_application_insights.application_insights.id
  log_analytics_workspace_id = azurerm_log_analytics_workspace.log_analytics_workspace.id

  dynamic "enabled_log" {
    iterator = entry
    for_each = data.azurerm_monitor_diagnostic_categories.diagnostic_categories_application_insights.log_category_groups
    content {
      category_group = entry.value
      retention_policy {
        enabled = true
        days    = 30
      }
    }
  }

  dynamic "metric" {
    iterator = entry
    for_each = data.azurerm_monitor_diagnostic_categories.diagnostic_categories_application_insights.metrics
    content {
      category = entry.value
      enabled  = true
      retention_policy {
        enabled = true
        days    = 30
      }
    }
  }
}

resource "azurerm_log_analytics_workspace" "log_analytics_workspace" {
  name                = "${local.prefix}-log001"
  location            = var.location
  resource_group_name = azurerm_resource_group.logging_rg.name
  tags                = var.tags

  allow_resource_only_permissions = true
  cmk_for_query_forced            = false
  daily_quota_gb                  = -1
  internet_ingestion_enabled      = true
  internet_query_enabled          = true
  local_authentication_disabled   = true
  retention_in_days               = 30
  sku                             = "PerGB2018"
}

data "azurerm_monitor_diagnostic_categories" "diagnostic_categories_log_analytics_workspace" {
  resource_id = azurerm_log_analytics_workspace.log_analytics_workspace.id
}

resource "azurerm_monitor_diagnostic_setting" "diagnostic_setting_log_analytics_workspace" {
  name                       = "logAnalytics"
  target_resource_id         = azurerm_log_analytics_workspace.log_analytics_workspace.id
  log_analytics_workspace_id = azurerm_log_analytics_workspace.log_analytics_workspace.id

  dynamic "enabled_log" {
    iterator = entry
    for_each = data.azurerm_monitor_diagnostic_categories.diagnostic_categories_log_analytics_workspace.log_category_groups
    content {
      category_group = entry.value
      retention_policy {
        enabled = true
        days    = 30
      }
    }
  }

  dynamic "metric" {
    iterator = entry
    for_each = data.azurerm_monitor_diagnostic_categories.diagnostic_categories_log_analytics_workspace.metrics
    content {
      category = entry.value
      enabled  = true
      retention_policy {
        enabled = true
        days    = 30
      }
    }
  }
}

resource "azurerm_monitor_private_link_scope" "mpls" {
  name                = "${local.prefix}-ampls001"
  resource_group_name = azurerm_resource_group.logging_rg.name
  tags                = var.tags
}

resource "azurerm_monitor_private_link_scoped_service" "mpls_application_insights" {
  name                = "ampls-${azurerm_application_insights.application_insights.name}"
  resource_group_name = azurerm_monitor_private_link_scope.mpls.resource_group_name
  scope_name          = azurerm_monitor_private_link_scope.mpls.name
  linked_resource_id  = azurerm_application_insights.application_insights.id
}

resource "azurerm_monitor_private_link_scoped_service" "mpls_log_analytics_workspace" {
  name                = "ampls-${azurerm_log_analytics_workspace.log_analytics_workspace.name}"
  resource_group_name = azurerm_monitor_private_link_scope.mpls.resource_group_name
  scope_name          = azurerm_monitor_private_link_scope.mpls.name
  linked_resource_id  = azurerm_log_analytics_workspace.log_analytics_workspace.id
}

resource "azurerm_private_endpoint" "mpls_private_endpoint" {
  name                = "${azurerm_monitor_private_link_scope.mpls.name}-pe"
  location            = var.location
  resource_group_name = azurerm_monitor_private_link_scope.mpls.resource_group_name
  tags                = var.tags

  custom_network_interface_name = "${azurerm_monitor_private_link_scope.mpls.name}-nic"
  private_service_connection {
    name                           = "${azurerm_monitor_private_link_scope.mpls.name}-pe"
    is_manual_connection           = false
    private_connection_resource_id = azurerm_monitor_private_link_scope.mpls.id
    subresource_names              = ["azuremonitor"]
  }
  subnet_id = azapi_resource.subnet_services.id
  private_dns_zone_group {
    name = "${azurerm_monitor_private_link_scope.mpls.name}-arecord"
    private_dns_zone_ids = [
      var.private_dns_zone_id_monitor,
      var.private_dns_zone_id_oms_opinsights,
      var.private_dns_zone_id_ods_opinsights,
      var.private_dns_zone_id_automation_agents,
      var.private_dns_zone_id_blob
    ]
  }
}
