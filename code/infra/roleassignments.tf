resource "azurerm_role_assignment" "role_assignment_storage_function" {
  scope                = azurerm_storage_account.storage.id
  role_definition_name = "Storage Blob Data Owner"
  principal_id         = azapi_resource.function.identity[0].principal_id
}
