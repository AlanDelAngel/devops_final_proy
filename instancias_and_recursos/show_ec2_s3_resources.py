import boto3
from datetime import datetime

REGION = 'us-east-1'
MAX_INSTANCIAS = 3

ec2 = boto3.resource('ec2', region_name=REGION)
s3 = boto3.client('s3', region_name=REGION)

def crear_instancias(cantidad):
    if cantidad > MAX_INSTANCIAS:
        print(f"No puedes crear más de {MAX_INSTANCIAS} instancias.")
        return
    
    print(f"Creando {cantidad} instancia(s)...")
    instances = ec2.create_instances(
        ImageId='ami-0fc5d935ebf8bc3bc',  # Ubuntu 22.04 LTS
        MinCount=1,
        MaxCount=cantidad,
        InstanceType='t2.micro',
        KeyName='clave',
        TagSpecifications=[
            {
                'ResourceType': 'instance',
                'Tags': [{'Key': 'Proyecto', 'Value': 'DevOps_Avance'}]
            }
        ]
    )
    for i, inst in enumerate(instances, start=1):
        print(f"Instancia {i}: {inst.id} creada")

def listar_buckets_y_objetos():
    print("\n=== Buckets en S3 ===")
    buckets = s3.list_buckets()
    for bucket in buckets['Buckets']:
        nombre = bucket['Name']
        print(f"\nBucket: {nombre}")
        try:
            objetos = s3.list_objects_v2(Bucket=nombre)
            if 'Contents' in objetos:
                for obj in objetos['Contents']:
                    print(f" - {obj['Key']} ({obj['Size']} bytes)")
            else:
                print(" (Vacío)")
        except Exception as e:
            print(f" Error al acceder a {nombre}: {e}")

def generar_reporte():
    instancias = ec2.instances.all()
    reporte = []
    for inst in instancias:
        reporte.append(f"{inst.id} | {inst.state['Name']} | {inst.instance_type}")
    
    nombre_archivo = f"reporte_aws_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    with open(nombre_archivo, 'w') as f:
        f.write("=== REPORTE DE INSTANCIAS EC2 ===\n")
        f.write('\n'.join(reporte))
    print(f"\nReporte generado: {nombre_archivo}")

# --- Interfaz simple ---
if __name__ == "__main__":
    print("\n--- Automatización AWS ---")
    print("1. Crear instancias EC2")
    print("2. Listar Buckets S3 y objetos")
    print("3. Generar reporte de EC2")
    opcion = input("Selecciona una opción: ")

    if opcion == "1":
        num = int(input(f"¿Cuántas instancias quieres crear? (máx {MAX_INSTANCIAS}): "))
        crear_instancias(num)
    elif opcion == "2":
        listar_buckets_y_objetos()
    elif opcion == "3":
        generar_reporte()
    else:
        print("Opción inválida.")

