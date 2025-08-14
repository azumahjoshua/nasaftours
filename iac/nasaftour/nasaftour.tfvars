
subscription = "f9f5b83e-17f4-4d04-8c07-5c3ffd9500df"
tenant       = "4487b52f-f118-4830-b49d-3c298cb71075"

tags = {
  Environment = "Production"
  Project     = "NASAFTour"
}

assign_public_ip = true

publicIP = {
  name = "nasaftour-new" # Changed to avoid conflict
  type = "Static"
  sku  = "Standard"
}

nsg_name = "nasaftour-new" # Changed to avoid conflict

inbound_security_rule = {
  name       = "all-app-ports"
  priority   = 1000
  dest_ports = ["22", "443", "80", "8000", "8080"]
}

ip_config_name = "nasaftour"

private_ip = {
  type    = "Static"
  address = "10.0.1.23"
}

vm_spec = {
  name       = "nasaftour"
  size       = "Standard_B1s"
  admin-name = "azureuser"
}

disk_spec = {
  caching-type = "ReadWrite"
  storage-type = "Standard_LRS"
  size_gb      = "30"
}

OS_image = {
  publisher = "Canonical"
  type      = "0001-com-ubuntu-server-focal"
  sku       = "20_04-lts-gen2"
  version   = "latest"
}

pub_key = "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQC/M3ZfHrHla6NuNnSHiyZfHh2XJhqYAjv7HW686/DC33uqy/m4pIAeb5Uw5QOngoszMa/CkXZEa8gjcslrOHtPPKAE7FDRaRd383aEcKD0x7iq0ycJ/iZvc18EJwZIEngIcBH1qjg/4fwtlhE9ovPmGlFt9tPVnVooHVoIZlk7duDrNImi44PdOLHg8lcCbanf4ECk6jnLQCdVxM9Slja3DWsKHOBuZxMZSLqIigd2esMnjD9dYdb+4/dnf+U4h0nsY6OGaqaOtDVN87M4/pNvPSn2LFz90WyDyD8iEA2Y6JHQ0y3sCZy1j5Fmajv5eksSDXw1Q2fyyDbJvtcjtnq8uCBtyuHeuxJlteVpBhsnWvpL0wAgDdVu17MxV0onZblLWnNd8LEj/jSY/zbFp+afAu6A+yOGqTVRBbZyot1Fr3NkOVYMgyRUsA+iDFPRf6khBP/5t1slM9Dmxf+GsBXc7anpJHoZOe/J4P1Ir1QcCKWMEXjQUX2JE6qbgo8Bkb0="

# CI/CD variables
compose_source_dir    = "/home/engineer/Desktop/nasaftours"
docker_install_dir    = "/home/engineer/Desktop/nasaftours/all_scripts"
docker_install_script = "docker-az.sh"
dest_dir              = "/home/azureuser"
private_key_file      = "/home/engineer/Desktop/nasaftours/key/nasaftour.pem"
