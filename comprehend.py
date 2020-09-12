import boto3,conect

def datosComprehend():
  '''Inicia los datos del comprehend, el objeto cliente para el
  AWS services comprehend'''
  AWS_ACCESS_KEY_ID,AWS_SECRET_KEY=conect.obtenerLlaves()

  #Se crea la instancia del cliente para generar el trabajo de comprehend
  comprehend = boto3.client(
    'comprehend',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_KEY,
    region_name='us-east-1')

  return comprehend
   
def iniciarComprehend(comprehend,texto):            
  '''
  Aquí se ocupa comprehend
  Texto será la información que arroja, en formato de objetos lista/diccionarios
  obtenemos las palabras clave con el ciclo
  '''
  #texto=json.dumps(comprehend.detect_key_phrases(Text=text[:len(text)//2], LanguageCode='es'), sort_keys=True, indent=4)
  resultados = comprehend.detect_key_phrases(Text=texto, LanguageCode='es')
  palabrasClave=list()
  for item in resultados["KeyPhrases"]:
    if item["Score"]>0.99:
      palabrasClave.append(item["Text"])
  return palabrasClave
