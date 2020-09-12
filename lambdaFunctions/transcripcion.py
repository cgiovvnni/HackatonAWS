import json,boto3

def lambda_handler(event, context):
    cliente=datosTranscribe()
    job_name=event["job_name"]
    bucket_name="businessoft"
    file_name=event["file_name"]
    resultado=start_transcribe_job(cliente,job_name,bucket_name,file_name)
    
    if resultado==True:
        return {
            'statusCode': 200,
            'body': {
                "job_name": job_name,
                "job_status": "True"
            }
        }
    else:
        return {
            'statusCode': 400,
            'body': {
                "job_name": job_name,
                "job_status": resultado
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
        return str(e)

