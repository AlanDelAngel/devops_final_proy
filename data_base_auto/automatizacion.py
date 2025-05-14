import boto3
import time
from botocore.exceptions import ClientError

# =====================
# CONFIGURACIÓN GENERAL
# =====================
BUCKET_NAME = 'mi-bucket-proyecto-prueba-2'
REGION = 'us-east-1'
ARCHIVO_LOCAL = '/home/eee_W_4302958/devops_final_proy/data_base_auto/datos/ejemplo.csv'
OBJETO_S3 = 'uploads/ejemplo.csv'
NOMBRE_TABLA = 'RegistrosPrueba'
ID_REGISTRO = '001'

# =====================
# CLIENTES DE AWS
# =====================
s3 = boto3.client('s3', region_name=REGION)
dynamodb = boto3.client('dynamodb', region_name=REGION)
dynamo_resource = boto3.resource('dynamodb', region_name=REGION)


def cargar_archivo_a_s3():
    print("🔼 Cargando archivo a S3...")
    s3.upload_file(ARCHIVO_LOCAL, BUCKET_NAME, OBJETO_S3)
    print(f"✅ Archivo '{OBJETO_S3}' cargado en el bucket '{BUCKET_NAME}'")


def habilitar_cifrado_s3():
    print("🔐 Habilitando cifrado SSE-S3 en el bucket...")
    s3.put_bucket_encryption(
        Bucket=BUCKET_NAME,
        ServerSideEncryptionConfiguration={
            'Rules': [
                {
                    'ApplyServerSideEncryptionByDefault': {
                        'SSEAlgorithm': 'AES256'
                    }
                }
            ]
        }
    )
    print("✅ Cifrado habilitado")


def aplicar_ciclo_vida():
    print("🗑️ Aplicando regla de ciclo de vida para eliminar archivos tras 7 días...")
    s3.put_bucket_lifecycle_configuration(
        Bucket=BUCKET_NAME,
        LifecycleConfiguration={
            'Rules': [
                {
                    'ID': 'EliminarObjetosViejos',
                    'Prefix': '',
                    'Status': 'Enabled',
                    'Expiration': {'Days': 7}
                }
            ]
        }
    )
    print("✅ Regla aplicada")


def crear_tabla_dynamodb():
    print(f"🗃️ Creando tabla DynamoDB: {NOMBRE_TABLA}...")
    try:
        dynamodb.create_table(
            TableName=NOMBRE_TABLA,
            KeySchema=[{'AttributeName': 'id', 'KeyType': 'HASH'}],
            AttributeDefinitions=[{'AttributeName': 'id', 'AttributeType': 'S'}],
            BillingMode='PAY_PER_REQUEST'
        )
        print("⏳ Esperando a que la tabla esté disponible...")
        waiter = dynamodb.get_waiter('table_exists')
        waiter.wait(TableName=NOMBRE_TABLA)
        print("✅ Tabla creada y disponible")
    except ClientError as e:
        if e.response['Error']['Code'] == 'ResourceInUseException':
            print("⚠️ La tabla ya existe, continuando...")
        else:
            raise


def insertar_registro():
    print("➕ Insertando registro...")
    table = dynamo_resource.Table(NOMBRE_TABLA)
    table.put_item(Item={'id': ID_REGISTRO, 'nombre': 'Alan', 'rol': 'Admin'})
    print("✅ Registro insertado")


def actualizar_registro():
    print("✏️ Actualizando registro...")
    table = dynamo_resource.Table(NOMBRE_TABLA)
    table.update_item(
        Key={'id': ID_REGISTRO},
        UpdateExpression='SET rol = :nuevoRol',
        ExpressionAttributeValues={':nuevoRol': 'Usuario'}
    )
    print("✅ Registro actualizado")


def eliminar_registro():
    print("❌ Eliminando registro...")
    table = dynamo_resource.Table(NOMBRE_TABLA)
    table.delete_item(Key={'id': ID_REGISTRO})
    print("✅ Registro eliminado")


# ===============
# EJECUCIÓN TOTAL
# ===============
if __name__ == "__main__":
    cargar_archivo_a_s3()
    habilitar_cifrado_s3()
    aplicar_ciclo_vida()
    crear_tabla_dynamodb()
    insertar_registro()
    actualizar_registro()
    eliminar_registro()
    print("\n🚀 Todo completado con éxito.")
