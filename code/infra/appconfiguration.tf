resource "azurerm_app_configuration" "app_configuration" {
  name                = "${local.prefix}-appcs001"
  location            = var.location
  resource_group_name = azurerm_resource_group.app_rg.name
  tags                = var.tags
  identity {
    type = "SystemAssigned"
  }

  local_auth_enabled       = false
  public_network_access    = "Enabled"
  purge_protection_enabled = true
  sku                      = "standard"
}
