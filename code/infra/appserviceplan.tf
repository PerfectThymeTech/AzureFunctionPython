module "app_service_plan" {
  source = "github.com/PerfectThymeTech/terraform-azurerm-modules//modules/appserviceplan?ref=main"
  providers = {
    azurerm = azurerm
  }

  location                                  = var.location
  resource_group_name                       = azurerm_resource_group.app_rg.name
  tags                                      = var.tags
  service_plan_name                         = "${local.prefix}-asp001"
  service_plan_maximum_elastic_worker_count = null
  service_plan_os_type                      = "Linux"
  service_plan_per_site_scaling_enabled     = false
  service_plan_sku_name                     = var.function_sku
  service_plan_worker_count                 = 1     # Update to '3' for production
  service_plan_zone_balancing_enabled       = false # Update to 'true' for production
  diagnostics_configurations                = local.diagnostics_configurations
}
