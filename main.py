import boto3,conect,transcribe,obtenerTexto,comprehend,s3

bucket_name="businessoft"
file_name="audiobject.mp4"
job_name="transcripcion3"


clienteTranscribe = transcribe.datosTranscribe()
inicioTrabajo = transcribe.start_transcribe_job(clienteTranscribe, job_name, bucket_name, file_name)
textoTranscrito = obtenerTexto.procesarTranscripcion(inicioTrabajo,clienteTranscribe,bucket_name,file_name,job_name)

clienteComprehend = comprehend.datosComprehend()
resultados = comprehend.iniciarComprehend(clienteComprehend,textoTranscrito)
print(resultados)

clienteS3 = s3.datosS3()
respuesta = s3.borrarObjeto(clienteS3,bucket_name,file_name)
print(respuesta)