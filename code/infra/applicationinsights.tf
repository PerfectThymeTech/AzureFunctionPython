module "application_insights" {
  source = "github.com/PerfectThymeTech/terraform-azurerm-modules//modules/applicationinsights?ref=main"
  providers = {
    azurerm = azurerm
  }

  location                                        = var.location
  resource_group_name                             = azurerm_resource_group.logging_rg.name
  tags                                            = var.tags
  application_insights_name                       = "${local.prefix}-appi001"
  application_insights_application_type           = "other"
  application_insights_log_analytics_workspace_id = var.log_analytics_workspace_id
  diagnostics_configurations                      = [] # local.diagnostics_configurations # Disabled to avoid duplicate logs in LAW and App Insights
}
