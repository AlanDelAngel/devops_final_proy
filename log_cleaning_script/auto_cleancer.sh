#!/bin/bash

IP1="44.220.159.90"
IP2="54.226.44.126"
CLAVE_PEM="~/.ssh/clave.pem"

# Ejecutar el script de limpieza en ambas instancias en paralelo
ssh -i $CLAVE_PEM ec2-user@$IP1 'bash -s' < limpiar_logs.sh &
ssh -i $CLAVE_PEM ec2-user@$IP2 'bash -s' < limpiar_logs.sh &
wait

echo "Limpieza de logs realizada en ambas instancias."
