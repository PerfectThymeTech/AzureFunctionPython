resource "azurerm_service_plan" "service_plan" {
  name                = "${local.prefix}-asp001"
  location            = var.location
  resource_group_name = azurerm_resource_group.app_rg.name
  tags                = var.tags

  # maximum_elastic_worker_count = 20
  os_type                  = "Linux"
  per_site_scaling_enabled = false
  sku_name                 = var.function_sku
  worker_count             = 1     # Update to '3' for production
  zone_balancing_enabled   = false # Update to 'true' for production
}

data "azurerm_monitor_diagnostic_categories" "diagnostic_categories_service_plan" {
  resource_id = azurerm_service_plan.service_plan.id
}

resource "azurerm_monitor_diagnostic_setting" "diagnostic_setting_service_plan" {
  name                       = "logAnalytics"
  target_resource_id         = azurerm_service_plan.service_plan.id
  log_analytics_workspace_id = azurerm_log_analytics_workspace.log_analytics_workspace.id

  dynamic "enabled_log" {
    iterator = entry
    for_each = data.azurerm_monitor_diagnostic_categories.diagnostic_categories_service_plan.log_category_groups
    content {
      category_group = entry.value
    }
  }

  dynamic "metric" {
    iterator = entry
    for_each = data.azurerm_monitor_diagnostic_categories.diagnostic_categories_service_plan.metrics
    content {
      category = entry.value
      enabled  = true
    }
  }
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
    kind = "functionapp,linux,container"
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
      scmSiteAlsoStopped        = true
      serverFarmId              = azurerm_service_plan.service_plan.id
      storageAccountRequired    = false
      vnetContentShareEnabled   = true
      vnetImagePullEnabled      = false # Set to 'true' when pulling image from private Azure Container Registry
      vnetRouteAllEnabled       = true
      virtualNetworkSubnetId    = azapi_resource.subnet_function.id
      siteConfig = {
        # autoHealEnabled = true # Enable to auto heal app based on configs
        # autoHealRules = {
        #   actions = {
        #     actionType = "LogEvent"
        #   }
        #   triggers = {
        #     statusCodes = [
        #       "429",
        #       "504",
        #       "507",
        #       "508"
        #     ]
        #   }
        # }
        acrUseManagedIdentityCreds = false
        alwaysOn                   = true
        appSettings = [
          {
            name  = "APPLICATIONINSIGHTS_CONNECTION_STRING"
            value = azurerm_application_insights.application_insights.connection_string
          },
          {
            name  = "AZURE_SDK_TRACING_IMPLEMENTATION"
            value = "opentelemetry"
          },
          {
            name  = "AZURE_TRACING_ENABLED"
            value = "true"
          },
          {
            name  = "AZURE_FUNCTIONS_ENVIRONMENT"
            value = "Production"
          },
          {
            name  = "FUNCTIONS_WORKER_PROCESS_COUNT"
            value = "${var.function_sku_cpus}"
          },
          {
            name  = "FUNCTIONS_EXTENSION_VERSION"
            value = "~4"
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
            name  = "AzureWebJobsStorage__accountName"
            value = azurerm_storage_account.storage.name
          },
          {
            name  = "AzureWebJobsSecretStorageType"
            value = "keyvault"
          },
          {
            name  = "AzureWebJobsSecretStorageKeyVaultUri"
            value = azurerm_key_vault.key_vault.vault_uri
          },
          {
            name  = "WEBSITES_ENABLE_APP_SERVICE_STORAGE" # Disable when not running a container
            value = "false"
          },
          {
            name  = "DOCKER_REGISTRY_SERVER_URL" # Disable when not running a container
            value = var.function_container_registry_url
          },
          # {
          #   name  = "FUNCTIONS_WORKER_RUNTIME" # Enable when running Python directly on the Function host
          #   value = "python"
          # },
          # {
          #   name  = "FUNCTIONS_WORKER_SHARED_MEMORY_DATA_TRANSFER_ENABLED" # Enable when running Python directly on the Function host
          #   value = "1"
          # },
          # {
          #   name  = "DOCKER_SHM_SIZE" # Enable when running Python directly on the Function host
          #   value = "268435456"
          # },
          # {
          #   name  = "PYTHON_THREADPOOL_THREAD_COUNT" # Enable when running Python directly on the Function host
          #   value = "None"
          # },
          # {
          #   name  = "PYTHON_ENABLE_DEBUG_LOGGING" # Enable when running Python directly on the Function host
          #   value = "0"
          # },
          # {
          #   name  = "PYTHON_ENABLE_WORKER_EXTENSIONS" # Enable when running Python directly on the Function host
          #   value = "1"
          # },
          # {
          #   name  = "ENABLE_ORYX_BUILD" # Enable when running Python directly on the Function host
          #   value = "1"
          # },
          # {
          #   name  = "SCM_DO_BUILD_DURING_DEPLOYMENT" # Enable when running Python directly on the Function host
          #   value = "1"
          # },
          {
            name  = "MY_SECRET_CONFIG"
            value = "@Microsoft.KeyVault(SecretUri=${azurerm_key_vault_secret.key_vault_secret_sample.id})"
          }
        ]
        azureStorageAccounts                   = {}
        detailedErrorLoggingEnabled            = true
        functionAppScaleLimit                  = 0
        functionsRuntimeScaleMonitoringEnabled = false
        ftpsState                              = "Disabled"
        healthCheckPath                        = var.function_health_path
        http20Enabled                          = true
        ipSecurityRestrictionsDefaultAction    = "Deny"
        linuxFxVersion                         = "DOCKER|${var.function_container_image}"
        localMySqlEnabled                      = false
        loadBalancing                          = "LeastRequests"
        minTlsVersion                          = "1.2"
        minTlsCipherSuite                      = "TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256"
        minimumElasticInstanceCount            = 0
        numberOfWorkers                        = 1
        preWarmedInstanceCount                 = 0
        remoteDebuggingEnabled                 = false
        requestTracingEnabled                  = true
        scmMinTlsVersion                       = "1.2"
        scmIpSecurityRestrictionsUseMain       = false
        scmIpSecurityRestrictionsDefaultAction = "Deny"
        use32BitWorkerProcess                  = true
        vnetPrivatePortsCount                  = 0
        webSocketsEnabled                      = false
      }
    }
  })

  schema_validation_enabled = false
  # ignore_body_changes = [ # Required when app settings are managed in a separate process
  #   "properties.siteConfig.appSettings"
  # ]
  depends_on = [
    azurerm_private_endpoint.key_vault_private_endpoint,
    azurerm_private_endpoint.storage_private_endpoint_blob,
    azurerm_private_endpoint.storage_private_endpoint_file,
    azurerm_private_endpoint.storage_private_endpoint_queue,
    azurerm_private_endpoint.storage_private_endpoint_table,
  ]
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
    }
  }

  dynamic "metric" {
    iterator = entry
    for_each = data.azurerm_monitor_diagnostic_categories.diagnostic_categories_function.metrics
    content {
      category = entry.value
      enabled  = true
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
