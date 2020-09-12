import boto3,conect,transcribe

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

def procesarTranscripcion(job_status,transcribe,bucket_name,file_name,job_name):
    '''Función que permite ejecutar las funciones necesarias para 
    generar la transcripción'''
    
    #Si se genera el trabajo de manera correcta, "job_status" será True
    if job_status: #Y empezaremos a hacer las request 
        texto,items = get_transcription_text(transcribe, job_name)
        return texto
    else: # O imprime el código de error
        print(f'El trabajo {job_name} falló con el error: {job_status}')
        return None
