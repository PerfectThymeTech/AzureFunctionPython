resource "azapi_resource" "subnet_function" {
  type      = "Microsoft.Network/virtualNetworks/subnets@2022-07-01"
  name      = "FunctionSubnet"
  parent_id = data.azurerm_virtual_network.virtual_network.id

  body = jsonencode({
    properties = {
      addressPrefix = tostring(cidrsubnet(data.azurerm_virtual_network.virtual_network.address_space[0], 27 - tonumber(reverse(split("/", data.azurerm_virtual_network.virtual_network.address_space[0]))[0]), 2))
      delegations = [
        {
          name = "FunctionDelegation"
          properties = {
            serviceName = "Microsoft.Web/serverFarms"
          }
        }
      ]
      ipAllocations = []
      networkSecurityGroup = {
        id = data.azurerm_network_security_group.network_security_group.id
      }
      privateEndpointNetworkPolicies    = "Enabled"
      privateLinkServiceNetworkPolicies = "Enabled"
      routeTable = {
        id = data.azurerm_route_table.route_table.id
      }
      serviceEndpointPolicies = []
      serviceEndpoints        = []
    }
  })
}

resource "azapi_resource" "subnet_services" {
  type      = "Microsoft.Network/virtualNetworks/subnets@2022-07-01"
  name      = "PeSubnet"
  parent_id = data.azurerm_virtual_network.virtual_network.id

  body = jsonencode({
    properties = {
      addressPrefix = tostring(cidrsubnet(data.azurerm_virtual_network.virtual_network.address_space[0], 27 - tonumber(reverse(split("/", data.azurerm_virtual_network.virtual_network.address_space[0]))[0]), 3))
      delegations   = []
      ipAllocations = []
      networkSecurityGroup = {
        id = data.azurerm_network_security_group.network_security_group.id
      }
      privateEndpointNetworkPolicies    = "Enabled"
      privateLinkServiceNetworkPolicies = "Enabled"
      routeTable = {
        id = data.azurerm_route_table.route_table.id
      }
      serviceEndpointPolicies = []
      serviceEndpoints        = []
    }
  })
}
