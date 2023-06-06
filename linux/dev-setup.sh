#!/bin/bash

curl -fsSL https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor | sudo tee /usr/share/keyrings/packages.microsoft.gpg > /dev/null
curl -fsSL https://apt.releases.hashicorp.com/gpg | gpg --dearmor | sudo tee /usr/share/keyrings/hashicorp.gpg > /dev/null
curl -fsSL https://pkgs.tailscale.com/stable/ubuntu/$(lsb_release -cs).noarmor.gpg | sudo tee /usr/share/keyrings/tailscale-archive-keyring.gpg > /dev/null

arch=$(dpkg --print-architecture)

# azure-cli
echo "deb [arch=${arch} signed-by=/usr/share/keyrings/packages.microsoft.gpg] https://packages.microsoft.com/repos/azure-cli/ $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/azure-cli.list >/dev/null

# azure-functions-core-tools-4
echo "deb [arch=${arch} signed-by=/usr/share/keyrings/packages.microsoft.gpg] https://packages.microsoft.com/ubuntu/$(lsb_release -rs)/prod $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/microsoft-prod.list >/dev/null

# mdatp, msodbcsql17, mssql-tools
echo "deb [arch=${arch} signed-by=/usr/share/keyrings/packages.microsoft.gpg] https://packages.microsoft.com/repos/microsoft-ubuntu-$(lsb_release -cs)-prod $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/dotnetdev.list >/dev/null

# terraform
echo "deb [arch=${arch} signed-by=/usr/share/keyrings/hashicorp.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/hashicorp.list >/dev/null

# tailscale
echo "deb [arch=${arch} signed-by=/usr/share/keyrings/tailscale-archive-keyring.gpg] https://pkgs.tailscale.com/stable/ubuntu $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/tailscale.list >/dev/null

sudo apt update && sudo apt upgrade -y

sudo apt install azure-cli \
azure-functions-core-tools-4 \
build-essential \
jq \
msodbcsql17 \
mssql-tools \
net-tools \
python3-dev \
python3-venv \
terraform \
unixodbc-dev \
whois \
xml-twig-tools
