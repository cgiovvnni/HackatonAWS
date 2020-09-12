import json,boto3

def lambda_handler(event, context):
    
    cliente = datosTranscribe()
    status,texto = procesarTranscripcion(event["job_status"],cliente,event["job_name"])
    
    if status=="COMPLETED":
        return {
            'statusCode': 200,
            'body': {
                "job_name":event["job_name"],
                "job_status":"COMPLETED",
                "texto": texto
            }
        }
    elif status=="FAILED":
        return {
            'statusCode': 400,
            'body': {
                "job_name":event["job_name"],
                "job_status":"FAILED",
                "texto": "Transcripción fallida"
            }
        }
    else:
        return {
            'statusCode': 200,
            'body': {
                "job_name":event["job_name"],
                "job_status": status,
                "texto":""
            }
        }
    
def datosTranscribe():
    '''Inicia los datos del transcribe, el objeto cliente para el
    AWS services transcribe'''
    #AWS_ACCESS_KEY_ID,AWS_SECRET_KEY=conect.obtenerLlaves()

    #Se crea la instancia del cliente para generar el trabajo de transcribe
    transcribe = boto3.client(
        'transcribe',
        region_name='us-east-1')

    return transcribe
    
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
    if status == 'COMPLETED':
        print(f"Trabajo {job_name} terminado")
        with urllib.request.urlopen(job['TranscriptionJob']['Transcript']['TranscriptFileUri']) as r:
            data = json.loads(r.read())
        return "COMPLETED",data['results']['transcripts'][0]['transcript']#,data['results']['items']
    elif status == 'FAILED':
        print(f"Trabajo {job_name} fallido")
        return "FAILED",""
    else:
        print(f"Estado de {job_name}: {status}")
        return status,""

def procesarTranscripcion(job_status,transcribe,job_name):
    '''Función que permite ejecutar las funciones necesarias para 
    generar la transcripción'''
    
    #Si se genera el trabajo de manera correcta, "job_status" será True
    if job_status=="True": #Y empezaremos a hacer las request 
        status,texto= get_transcription_text(transcribe, job_name)
        return status,texto
    else: # O imprime el código de error
        print(f'El trabajo {job_name} falló con el error: {job_status}')
        return "FAILED",""
