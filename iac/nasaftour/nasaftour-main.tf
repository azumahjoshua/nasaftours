provider "azurerm" {
  subscription_id = var.subscription
  tenant_id       = var.tenant
  use_cli         = true
  features {}
}

data "terraform_remote_state" "vnet-state" {
  backend = "local"
  config = {
    path = "../vnet/terraform.tfstate"
  }
}

locals {
  location            = data.terraform_remote_state.vnet-state.outputs.resource_group_location
  resource_group_name = "nasaftour_rg" # Explicitly set to match existing RG
}

resource "azurerm_public_ip" "main-ip" {
  count               = var.assign_public_ip ? 1 : 0
  name                = "${var.publicIP.name}-pubIP"
  location            = local.location
  resource_group_name = local.resource_group_name
  allocation_method   = var.publicIP.type
  sku                 = var.publicIP.sku
  tags                = var.tags
}

resource "azurerm_network_interface" "main" {
  name                = "${var.nsg_name}-nic"
  location            = local.location
  resource_group_name = local.resource_group_name
  tags                = var.tags

  ip_configuration {
    name                          = var.ip_config_name
    subnet_id                     = data.terraform_remote_state.vnet-state.outputs.subnet_id
    private_ip_address_allocation = var.private_ip.type
    private_ip_address            = var.private_ip.address
    public_ip_address_id          = var.assign_public_ip ? azurerm_public_ip.main-ip[0].id : null
  }
}

resource "azurerm_network_security_group" "main" {
  name                = "${var.nsg_name}-nsg"
  location            = local.location
  resource_group_name = local.resource_group_name
  tags                = var.tags

  security_rule {
    name                       = var.inbound_security_rule.name
    priority                   = var.inbound_security_rule.priority
    direction                  = "Inbound"
    access                     = "Allow"
    protocol                   = "Tcp"
    source_port_range          = "*"
    destination_port_ranges    = var.inbound_security_rule.dest_ports
    source_address_prefix      = "*"
    destination_address_prefix = "*"
  }
}

resource "azurerm_network_interface_security_group_association" "main" {
  network_interface_id      = azurerm_network_interface.main.id
  network_security_group_id = azurerm_network_security_group.main.id
}

resource "azurerm_linux_virtual_machine" "main" {
  name                = "${var.vm_spec.name}-VM"
  resource_group_name = local.resource_group_name
  location            = local.location
  size                = var.vm_spec.size
  admin_username      = var.vm_spec.admin-name
  tags                = var.tags

  network_interface_ids = [azurerm_network_interface.main.id]

  os_disk {
    name                 = "${var.vm_spec.name}-osdisk"
    caching              = var.disk_spec.caching-type
    storage_account_type = var.disk_spec.storage-type
    disk_size_gb         = var.disk_spec.size_gb
  }

  source_image_reference {
    publisher = var.OS_image.publisher
    offer     = var.OS_image.type
    sku       = var.OS_image.sku
    version   = var.OS_image.version
  }

  admin_ssh_key {
    username   = var.vm_spec.admin-name
    public_key = var.pub_key
  }
}

resource "null_resource" "install_docker" {
  depends_on = [azurerm_linux_virtual_machine.main]

  connection {
    type        = "ssh"
    user        = var.vm_spec.admin-name
    private_key = file(var.private_key_file)
    host        = azurerm_linux_virtual_machine.main.public_ip_address
  }

  provisioner "file" {
    source      = "${var.docker_install_dir}/${var.docker_install_script}"
    destination = "${var.dest_dir}/${var.docker_install_script}"
  }

  provisioner "remote-exec" {
    inline = [
      "chmod +x ${var.dest_dir}/${var.docker_install_script}",
      "sudo ${var.dest_dir}/${var.docker_install_script}"
    ]
  }
}

resource "azurerm_storage_account" "blob_storage" {
  name                     = "nasaftoursstoragedev"
  resource_group_name      = local.resource_group_name
  location                 = local.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
  tags                     = var.tags
}

resource "azurerm_storage_container" "media" {
  name                  = "media"
  storage_account_id  = azurerm_storage_account.blob_storage.id
  container_access_type = "blob"
}

resource "azurerm_storage_container" "static" {
  name                  = "static"
  storage_account_id    = azurerm_storage_account.blob_storage.id
  container_access_type = "blob"
}


output "vm-details" {
  value = {
    vm_name        = azurerm_linux_virtual_machine.main.name
    public_ip      = var.assign_public_ip ? azurerm_public_ip.main-ip[0].ip_address : null
    private_ip     = azurerm_network_interface.main.private_ip_address
    admin_username = var.vm_spec.admin-name
  }
}
output "resource_group_name" {
  value = local.resource_group_name
}

output "storage_account_id" {
  value = azurerm_storage_account.blob_storage.id
}

output "storage_account_key" {
  value     = azurerm_storage_account.blob_storage.primary_access_key
  sensitive = true
}

