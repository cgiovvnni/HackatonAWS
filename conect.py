AWS_ACCESS_KEY_ID=""
AWS_SECRET_KEY=""

def crearLlaves():
  '''Genera las llaves para el acceso'''
  global AWS_ACCESS_KEY_ID,AWS_SECRET_KEY
  
  '''Se lee el archivo de credenciales para encontrar
  la llave de acceso y la llave secreta'''
  with open('Rodrigo.csv', 'r') as f:
      content = f.readlines()

  keys = {}
  llaves = content[0].replace(" ","").split(",")
  valores = content[1].replace(" ","").split(",")
  for i in range(5):
      keys.update({llaves[i] : valores[i]})

  AWS_ACCESS_KEY_ID = keys['AccesskeyID']
  AWS_SECRET_KEY = keys['Secretaccesskey']

def obtenerLlaves():
  '''Genera las llaves y las regresa en el modo
  AWS_ACCESS_KEY_ID, AWS_SECRET_KEY'''
  crearLlaves()
  return AWS_ACCESS_KEY_ID,AWS_SECRET_KEY

if __name__ == '__main__':
  crearLlaves()
  print(AWS_ACCESS_KEY_ID)
  print(AWS_SECRET_KEY)
