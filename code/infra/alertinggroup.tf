resource "azurerm_monitor_action_group" "monitor_action_group" {
  name                = "${local.prefix}-ag001"
  resource_group_name = azurerm_resource_group.logging_rg.name
  tags                = var.tags

  enabled    = true
  short_name = substr(local.prefix, 0, 11)
  dynamic "email_receiver" {
    for_each = var.alert_endpoints.email == null ? [] : [1]
    content {
      name                    = local.prefix
      email_address           = email_receiver.value.email_address
      use_common_alert_schema = true
    }
  }
}
