resource "azurerm_role_assignment" "current_role_assignment_key_vault" {
  scope                = azurerm_key_vault.key_vault.id
  role_definition_name = "Key Vault Administrator"
  principal_id         = data.azurerm_client_config.current.object_id
}

resource "azurerm_role_assignment" "function_role_assignment_storage" {
  scope                = azurerm_storage_account.storage.id
  role_definition_name = "Storage Blob Data Owner"
  principal_id         = azapi_resource.function.identity[0].principal_id
}

resource "azurerm_role_assignment" "function_role_assignment_key_vault" {
  scope                = azurerm_key_vault.key_vault.id
  role_definition_name = "Key Vault Secrets User"
  principal_id         = azapi_resource.function.identity[0].principal_id
}

# resource "azurerm_role_assignment" "function_role_assignment_application_insights" {
#   scope                = azurerm_application_insights.application_insights.id
#   role_definition_name = "Monitoring Metrics Publisher"
#   principal_id         = azapi_resource.function.identity[0].principal_id
# }
