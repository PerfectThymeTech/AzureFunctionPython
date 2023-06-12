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
