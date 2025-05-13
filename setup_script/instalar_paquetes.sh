#!/bin/bash

echo "=== Actualizando sistema ==="
sudo apt update -y && sudo apt upgrade -y

echo "=== Instalando paquetes esenciales ==="
sudo apt install -y git vim python3 python3-pip docker.io

echo "=== Habilitando Docker ==="
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -aG docker $USER

echo "=== Instalación completada ==="
