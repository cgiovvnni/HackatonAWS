import sys,boto3

sys.path.append("/home/lazaro/Pictures/awsHackaton/transcribe")

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

#Variables importantes para generar el trabajo
'''
Se define el nombre del bucket
Nombre del archivo en el bucket
Nombre del trabajo transcribe
'''
BUCKET_NAME = "businessoft" #***********************************************
FILE_NAME = "20_Curiosidades_que_te_pondran_incomodo_.mp4"
JOB_NAME = "trans1"

#Se crea la instancia del cliente para generar el trabajo de transcribe
transcribe = boto3.client(
    'transcribe',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_KEY,
    region_name='us-east-1')

def start_transcribe_job(transcribe, job_name, bucket, file):
    """Función para iniciar el trabajo de transcribe
    
    Parametros
    ----------
    transcribe : Cliente AWS para el transcribe
    job_name : str, Nombre del trabajo en el aws
    bucket : str, Nombre del bucket
    file : str, Nombre del archivo a transcribir
    
    Retorna
    -------
    True: Si el trabajo inició satisfactoriamente
    
    """
    #URL de donde se encuentra el archivo
    #Esta url depende el bucket, checar bien la forma en que se forma
    file_uri = f'https://{bucket}.s3.amazonaws.com/{file}'

    #Se intenta generar el trabajo en transcribe
    #Regresa el error en caso de generarse uno
    try:
        #Objeto para generar o empezar el trabajo de transcripción
        transcribe.start_transcription_job(
            TranscriptionJobName=job_name,
            Media={'MediaFileUri': file_uri},
            MediaFormat='mp4',
            LanguageCode='es-US'
        )
        return True
    except Exception as e:
        return e

def get_transcription_text(transcribe, job_name):
    """Regresa la transcripción del trabajo transcribe
    
    Parámetros
    ----------
    transcribe : Cliente AWS para el transcribe
    job_name : Nombre del trabajo transcribe
    
    Retorna
    -------
    Actual estatus del trabajo si sigue en progreso
    Ó la transcripción del trabajo si esta completo
    """
    '''Bibliotecas a usar para hacer las request a internet'''
    import urllib.request
    import json
    import time
    
    #Obtenemos la instancia del trabajo
    job = transcribe.get_transcription_job(TranscriptionJobName=job_name)
    
    #Con esa instancia obtenemos el estatus
    status = job['TranscriptionJob']['TranscriptionJobStatus']
    
    '''
    Se checa el estatus,
      * Si esta "COMPLETED", se arroja un mensaje de que esta completo,
      Mediante urllib se obtiene ese archivo de internet y se lee en forma de json,
      solo se regresa la parte de resultados, transcripts en la pos 0 y en 
      la parte transcript
      * Si esta en "FAILED", 
    '''
    while True:
        if status == 'COMPLETED':
            print(f"Trabajo {job_name} terminado")
            with urllib.request.urlopen(job['TranscriptionJob']['Transcript']['TranscriptFileUri']) as r:
                data = json.loads(r.read())
            return data['results']['transcripts'][0]['transcript'],data['results']['items']
        elif status == 'FAILED':
            print(f"Trabajo {job_name} fallido")
            return None
        else:
            print(f"Estado de {job_name}: {status}")
            time.sleep(5)
            job = transcribe.get_transcription_job(TranscriptionJobName=job_name)
            status = job['TranscriptionJob']['TranscriptionJobStatus']

#Se inicia el trabajo, y el True o la excepción se comparan
job_status = start_transcribe_job(transcribe, JOB_NAME, BUCKET_NAME, FILE_NAME)

job_status=True
#Si se genera el trabajo de manera correcta, "job_status" será True
if job_status: #Y empezaremos a hacer las request 
    texto,items = get_transcription_text(transcribe, JOB_NAME)
    print(f'The transcribed text for {FILE_NAME} file:')
    print(texto)
    '''
    textoConfiable=""
    for item in items:
      confianza=float(item["alternatives"][0]["confidence"])
      palabra=item["alternatives"][0]["content"]
      if confianza>0.75: textoConfiable+=" "+palabra
    print(textoConfiable)

    texto1=open("textoPreliminar.txt","w")
    texto1.write(texto)
    texto1.close()

    texto1=open("textoConfiable.txt","w")
    texto1.write(textoConfiable)
    texto1.close()
    '''
else: # O imprime el código de error
    print(f'Job {JOB_NAME} failed with the error: {job_status}')