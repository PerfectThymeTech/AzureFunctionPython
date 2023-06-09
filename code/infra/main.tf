resource "azurerm_resource_group" "app_rg" {
  name     = "${local.prefix}-app-rg"
  location = var.location
  tags     = var.tags
}

resource "azurerm_resource_group" "logging_rg" {
  name     = "${local.prefix}-logging-rg"
  location = var.location
  tags     = var.tags
}
