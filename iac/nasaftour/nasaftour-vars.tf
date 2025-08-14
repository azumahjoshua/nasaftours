variable "subscription" {
  type        = string
  description = "Azure subscription ID"
}

variable "tenant" {
  type        = string
  description = "Azure tenant ID"
}

variable "tags" {
  type        = map(string)
  description = "Resource tags"
  default     = {}
}

variable "vm_spec" {
  type = object({
    name       = string
    size       = string
    admin-name = string
  })
  description = "VM configuration"
}

variable "pub_key" {
  type        = string
  description = "SSH public key (key body only, without type)"
}

variable "disk_spec" {
  type = object({
    caching-type = string
    storage-type = string
    size_gb      = string
  })
  description = "Disk configuration"
}

variable "assign_public_ip" {
  type        = bool
  description = "Whether to assign public IP"
  default     = false
}

variable "publicIP" {
  type = object({
    name = string
    type = string
    sku  = string
  })
  description = "Public IP configuration"
}

variable "inbound_security_rule" {
  type = object({
    name       = string
    priority   = number
    dest_ports = list(string)
  })
  description = "NSG inbound rules"
}

variable "nsg_name" {
  type        = string
  description = "Network Security Group name"
}

variable "ip_config_name" {
  type        = string
  default     = "main"
  description = "IP configuration name"
}

variable "private_ip" {
  type = object({
    type    = string
    address = string
  })
  default = {
    type    = "Dynamic"
    address = null
  }
  description = "Private IP configuration"
}

variable "OS_image" {
  type = object({
    publisher = string
    type      = string
    sku       = string
    version   = string
  })
  description = "OS image configuration"
}

# CI/CD variables
variable "compose_source_dir" { type = string }
variable "dest_dir" { type = string }
variable "private_key_file" { type = string }
variable "docker_install_dir" { type = string }
variable "docker_install_script" { type = string }
