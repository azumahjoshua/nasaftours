# Main file to create a project wide virtul network and resource group
# Children of this will tap into its state file to get appropriate details
# to enable them to deploy into this vnet

provider "azurerm" {
  subscription_id = var.subscription
  tenant_id       = var.tenant
  use_cli         = true
  features {}
}

resource "azurerm_resource_group" "main" {
  name     = var.resource_group_name # RG name seen in the portal
  location = var.region
}


resource "azurerm_virtual_network" "main" {
  name                = var.vnet.name # Value seen in portal
  address_space       = var.vnet.cidr
  location            = azurerm_resource_group.main.location # Don't know why it can't work out the location from the RG name
  resource_group_name = azurerm_resource_group.main.name     # Specify resource group. Important it's same for vms to communicate
}

resource "azurerm_subnet" "subnet" {
  name                 = var.subnet.name                  # Subnet within the Vnet. 
  resource_group_name  = var.resource_group_name           # Which resurce group. AWS doesn't use RGs
  virtual_network_name = azurerm_virtual_network.main.name # Provide a vnet name that this subnet will belong to
  address_prefixes     = var.subnet.cidr                  # Set cidr block range of subnet
}



# Output values added to state to be used by other modules
output "resource_group_name" {
  value = azurerm_resource_group.main.name
}

output "resource_group_location" {
  value = azurerm_resource_group.main.location
}

output "vnet_name" {
  value = azurerm_virtual_network.main.name
}

output "subnet_id" {
  value     = azurerm_subnet.subnet.id
  sensitive = true # No need to output this big number to clutter the terminal just add it to state
}



# Output subnet details to user. Add _ if you want these are output first as it seems to be alphabetical
# I added z here to ensure it's output last
# and I can't stop the output of the others but need them for the state file. I main ly want to see these
# EOT or heredoc enables multiline output eexctly as specifies and without ""
output "z_subnet_allocation" {
  value = <<EOT



  ***********************************
  Subnet:${azurerm_subnet.subnet.name} CIDR:${join(", ", azurerm_subnet.subnet.address_prefixes)}
  
  ***********************************

  EOT
}
