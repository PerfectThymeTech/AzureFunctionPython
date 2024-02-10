resource "azurerm_monitor_activity_log_alert" "monitor_activity_log_alert_service_health" {
  name                = "${local.prefix}-alert-servicehealth"
  resource_group_name = azurerm_resource_group.logging_rg.name
  tags                = var.tags

  enabled     = true
  description = "Alerts for service health and maintenance events."
  scopes = [
    data.azurerm_subscription.current.id
  ]
  action {
    action_group_id = azurerm_monitor_action_group.monitor_action_group.id
    webhook_properties = {
      "alert_custom_type"              = "service-health",
      "alert_custom_location"          = var.location
      "alert_custom_env"               = var.environment
      "alert_custom_sub"               = data.azurerm_client_config.current.subscription_id
      "alert_custom_resource_group"    = azurerm_resource_group.extension_rg.name
      "alert_custom_instance"          = var.prefix
      "alert_custom_layer"             = "core"
      "alert_custom_layer_name"        = "core"
      "alert_custom_snowseverity"      = "Info"
      "alert_custom_snowfgroup"        = "A.TEC.GLOB.ADP.DL.3RD"
      "alert_custom_snowincidentlevel" = "P3"
    }
  }
  criteria {
    category = "ServiceHealth"
    service_health {
      events = [
        "Incident",
        "Maintenance"
      ]
      locations = [
        "Global",
        data.azurerm_location.current.display_name
      ]
    }
  }
}
