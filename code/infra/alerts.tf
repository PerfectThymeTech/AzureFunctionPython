resource "azurerm_monitor_activity_log_alert" "monitor_activity_log_alert_service_health" {
  name                = "${local.prefix}-alert-servicehealth"
  resource_group_name = azurerm_resource_group.logging_rg.name
  tags                = var.tags

  enabled     = true
  description = "Alerts about service health and maintenance events."
  scopes = [
    data.azurerm_subscription.current.id
  ]
  action {
    action_group_id = azurerm_monitor_action_group.monitor_action_group.id
    webhook_properties = {
      "alert-type"   = "service-health",
      "location"     = var.location
      "environment"  = var.environment
      "subscription" = data.azurerm_client_config.current.subscription_id
      "severity"     = "Info"
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
