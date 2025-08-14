subscription        = "f9f5b83e-17f4-4d04-8c07-5c3ffd9500df"
tenant              = "4487b52f-f118-4830-b49d-3c298cb71075"
resource_group_name = "nasaftour_rg"
region              = "UK South"

vnet = {
  name = "nasaftour-vnet"
  cidr = ["10.0.0.0/16"]
}

subnet = {
  name = "nasaftour"
  cidr = ["10.0.1.0/24"]
}
