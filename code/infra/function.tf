resource "azurerm_service_plan" "service_plan" {
  name                = "${local.prefix}-asp001"
  location            = var.location
  resource_group_name = azurerm_resource_group.app_rg.name
  tags                = var.tags

  # maximum_elastic_worker_count = 20
  os_type                  = "Linux"
  per_site_scaling_enabled = false
  sku_name                 = "P1v3"
  worker_count             = 3
  zone_balancing_enabled   = true
}

resource "azapi_resource" "function" {
  type      = "Microsoft.Web/sites@2022-09-01"
  parent_id = azurerm_resource_group.app_rg.id
  name      = "${local.prefix}-fctn001"
  location  = var.location
  tags      = var.tags
  identity {
    type = "SystemAssigned"
  }

  body = jsonencode({
    kind = "functionapp,linux"
    properties = {
      clientAffinityEnabled     = false
      clientCertEnabled         = false
      clientCertMode            = "Required"
      enabled                   = true
      hostNamesDisabled         = false
      httpsOnly                 = true
      hyperV                    = false
      isXenon                   = false
      keyVaultReferenceIdentity = "SystemAssigned"
      publicNetworkAccess       = "Disabled"
      redundancyMode            = "None"
      reserved                  = true
      scmSiteAlsoStopped        = false
      serverFarmId              = azurerm_service_plan.service_plan.id
      storageAccountRequired    = false
      vnetContentShareEnabled   = true
      virtualNetworkSubnetId    = azapi_resource.subnet_function.id
      vnetRouteAllEnabled       = true
      siteConfig = {
        autoHealEnabled            = false
        acrUseManagedIdentityCreds = false
        alwaysOn                   = true
        appSettings = [
          {
            name  = "APPLICATIONINSIGHTS_CONNECTION_STRING"
            value = azurerm_application_insights.application_insights.connection_string
          },
          {
            name  = "APPINSIGHTS_INSTRUMENTATIONKEY"
            value = azurerm_application_insights.application_insights.instrumentation_key
          },
          {
            name  = "FUNCTIONS_EXTENSION_VERSION"
            value = "~4"
          },
          {
            name  = "FUNCTIONS_WORKER_RUNTIME"
            value = "python"
          },
          {
            name  = "WEBSITE_CONTENTOVERVNET"
            value = "1"
          },
          {
            name  = "WEBSITE_RUN_FROM_PACKAGE"
            value = "0"
          },
          {
            name  = "PYTHON_ENABLE_WORKER_EXTENSIONS"
            value = "1"
          },
          {
            name  = "ENABLE_ORYX_BUILD"
            value = "1"
          },
          {
            name  = "SCM_DO_BUILD_DURING_DEPLOYMENT"
            value = "1"
          },
          {
            name  = "AzureWebJobsStorage__accountName"
            value = azurerm_storage_account.storage.name
          }
        ]
        azureStorageAccounts                   = {}
        detailedErrorLoggingEnabled            = true
        functionAppScaleLimit                  = 0
        functionsRuntimeScaleMonitoringEnabled = false
        ftpsState                              = "Disabled"
        healthCheckPath                        = var.function_health_path
        http20Enabled                          = false
        ipSecurityRestrictionsDefaultAction    = "Deny"
        linuxFxVersion                         = "Python|${var.function_python_version}"
        localMySqlEnabled                      = false
        loadBalancing                          = "LeastRequests"
        minTlsVersion                          = "1.2"
        minimumElasticInstanceCount            = 0
        numberOfWorkers                        = 1
        preWarmedInstanceCount                 = 0
        scmMinTlsVersion                       = "1.2"
        scmIpSecurityRestrictionsUseMain       = false
        scmIpSecurityRestrictionsDefaultAction = "Deny"
        use32BitWorkerProcess                  = true
        vnetPrivatePortsCount                  = 0
        webSocketsEnabled                      = false
      }
    }
  })
}

data "azurerm_monitor_diagnostic_categories" "diagnostic_categories_function" {
  resource_id = azapi_resource.function.id
}

resource "azurerm_monitor_diagnostic_setting" "diagnostic_setting_function" {
  name                       = "logAnalytics"
  target_resource_id         = azapi_resource.function.id
  log_analytics_workspace_id = azurerm_log_analytics_workspace.log_analytics_workspace.id

  dynamic "enabled_log" {
    iterator = entry
    for_each = data.azurerm_monitor_diagnostic_categories.diagnostic_categories_function.log_category_groups
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
    for_each = data.azurerm_monitor_diagnostic_categories.diagnostic_categories_function.metrics
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

resource "azurerm_private_endpoint" "function_private_endpoint" {
  name                = "${azapi_resource.function.name}-pe"
  location            = var.location
  resource_group_name = azurerm_resource_group.app_rg.name
  tags                = var.tags

  custom_network_interface_name = "${azapi_resource.function.name}-nic"
  private_service_connection {
    name                           = "${azapi_resource.function.name}-pe"
    is_manual_connection           = false
    private_connection_resource_id = azapi_resource.function.id
    subresource_names              = ["sites"]
  }
  subnet_id = azapi_resource.subnet_services.id
  private_dns_zone_group {
    name = "${azapi_resource.function.name}-arecord"
    private_dns_zone_ids = [
      var.private_dns_zone_id_sites
    ]
  }
}
