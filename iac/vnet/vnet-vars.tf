variable "subscription" {
  type        = string
  description = "User subscrition ID"
}

variable "tenant" {
  type        = string
  description = "User tenant ID"
}

variable "resource_group_name" {
  type = string
}

variable "region" {
  type = string
}

variable "vnet" {
  description = "Names the VNet and sets the CIDR block range"
  type = object({
    name = string
    cidr = list(string)
  })
}


variable "subnet" {
  description = "Names the first subnet and sets the CIDR block range"
  type = object({
    name = string
    cidr = list(string)
  })
}



