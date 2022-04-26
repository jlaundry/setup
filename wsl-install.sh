#!/bin/bash

apt update && apt upgrade -y
apt install ca-certificates curl apt-transport-https lsb-release gnupg -y

curl -fsSL https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > /etc/apt/trusted.gpg.d/packages.microsoft.gpg
curl -fsSL https://apt.releases.hashicorp.com/gpg | gpg --dearmor > /etc/apt/trusted.gpg.d/hashicorp.gpg

arch=$(dpkg --print-architecture)

# azure-cli
echo "deb [arch=${arch} signed-by=/etc/apt/trusted.gpg.d/packages.microsoft.gpg] https://packages.microsoft.com/repos/azure-cli/ $(lsb_release -cs) main" > /etc/apt/sources.list.d/azure-cli.list

# azure-functions-core-tools-4
echo "deb [arch=${arch} signed-by=/etc/apt/trusted.gpg.d/packages.microsoft.gpg] https://packages.microsoft.com/ubuntu/$(lsb_release -rs)/prod $(lsb_release -cs) main" > /etc/apt/sources.list.d/microsoft-prod.list

# mdatp, msodbcsql17, mssql-tools
echo "deb [arch=${arch} signed-by=/etc/apt/trusted.gpg.d/packages.microsoft.gpg] https://packages.microsoft.com/repos/microsoft-ubuntu-$(lsb_release -cs)-prod $(lsb_release -cs) main" > /etc/apt/sources.list.d/dotnetdev.list

# terraform
echo "deb [arch=${arch} signed-by=/etc/apt/trusted.gpg.d/hashicorp.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" > /etc/apt/sources.list.d/hashicorp.list

apt update

apt install azure-cli \
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
