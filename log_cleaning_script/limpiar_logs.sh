#!/bin/bash

echo "=== Limpiando archivos de log ==="
sudo find /var/log -type f -name "*.log" -exec truncate -s 0 {} \;
echo "Limpieza realizada el: $(date)" >> ~/log_limpieza.log

