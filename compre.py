import boto3
import json

'''Se lee el archivo de credenciales para encontrar
la llave de acceso y la llave secreta'''
with open('AbrahamLazaroKeys.csv', 'r') as f:
    content = f.readlines()

keys = {}
llaves = content[0].replace(" ","").split(",")
valores = content[1].replace(" ","").split(",")
for i in range(5):
    keys.update({llaves[i] : valores[i]})

AWS_ACCESS_KEY_ID = keys['AccesskeyID']
AWS_SECRET_KEY = keys['Secretaccesskey']

#Se crea la instancia del cliente para generar el trabajo de transcribe
comprehend = boto3.client(
    'comprehend',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_KEY,
    region_name='us-east-1')
                
#se lee el texto de un archivo
archivo = open("textoPreliminar.txt","r")
text=archivo.read()
archivo.close()

'''
Aquí se ocupa comprehend
Texto será la información que arroja, en formato de objetos lista/diccionarios
obtenemos las palabras clave con el ciclo
'''
#texto=json.dumps(comprehend.detect_key_phrases(Text=text[:len(text)//2], LanguageCode='es'), sort_keys=True, indent=4)
texto = comprehend.detect_key_phrases(Text=text[:len(text)//2], LanguageCode='es')
palabrasClave=list()
for item in texto["KeyPhrases"]:
  if item["Score"]>0.99:
    palabrasClave.append(item["Text"])
print(palabrasClave)