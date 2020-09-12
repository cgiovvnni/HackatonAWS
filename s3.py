import boto3,conect

def datosS3():
  '''Inicia los datos del comprehend, el objeto cliente para el
  AWS services comprehend'''
  AWS_ACCESS_KEY_ID,AWS_SECRET_KEY=conect.obtenerLlaves()

  #Se crea la instancia del cliente para generar el trabajo de comprehend
  s3 = boto3.client(
      's3',
      aws_access_key_id=AWS_ACCESS_KEY_ID,
      aws_secret_access_key=AWS_SECRET_KEY,
      region_name='us-east-1')

  return s3

def borrarObjeto(s3,bucket_name,file_name):
  respuesta = s3.delete_object(
      Bucket=bucket_name,
      Key=file_name,
  )

  return respuesta