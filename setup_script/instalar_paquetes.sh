#!/bin/bash

echo "=== Actualizando sistema ==="
sudo yum update -y

echo "=== Instalando paquetes esenciales ==="
sudo yum install -y git vim python3 docker

echo "=== Instalando pip3 si no está presente ==="
sudo python3 -m ensurepip --upgrade

echo "=== Habilitando Docker ==="
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -aG docker $USER

echo "=== Instalación completada ==="