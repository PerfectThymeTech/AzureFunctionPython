resource "azurerm_role_assignment" "function_role_assignment_storage_blob_data_owner" {
  scope                = module.storage_account.storage_account_id
  role_definition_name = "Storage Blob Data Owner"
  principal_id         = azapi_resource.function.identity[0].principal_id
}

# resource "azurerm_role_assignment" "function_role_assignment_storage_account_contributor" { # Enable when using blob triggers
#   scope                = module.storage_account.storage_account_id
#   role_definition_name = "Storage Account Contributor"
#   principal_id         = azapi_resource.function.identity[0].principal_id
# }

# resource "azurerm_role_assignment" "function_role_assignment_storage_queue_data_contributor" { # Enable when using blob triggers
#   scope                = module.storage_account.storage_account_id
#   role_definition_name = "Storage Queue Data Contributor"
#   principal_id         = azapi_resource.function.identity[0].principal_id
# }

# Additional permissions may be required based on the trigger that is being used.
# For more details, refer to: https://learn.microsoft.com/en-us/azure/azure-functions/functions-reference?tabs=blob&pivots=programming-language-python#grant-permission-to-the-identity

resource "azurerm_role_assignment" "function_role_assignment_key_vault" {
  scope                = module.key_vault.key_vault_id
  role_definition_name = "Key Vault Secrets Officer"
  principal_id         = azapi_resource.function.identity[0].principal_id
}

# resource "azurerm_role_assignment" "function_role_assignment_application_insights" { # Enable to rely on Entra ID-based authentication to Application Insights
#   scope                = module.application_insights.application_insights_id
#   role_definition_name = "Monitoring Metrics Publisher"
#   principal_id         = azapi_resource.function.identity[0].principal_id
# }
