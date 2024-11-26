import pymysql
import os
import json

RDS_HOST = os.environ['RDS_HOST']
USERNAME = os.environ['RDS_USERNAME']
PASSWORD = os.environ['RDS_PASSWORD']
DB_NAME = os.environ['RDS_DATABASE']

def lambda_handler(event, context):
  
    carro_id = event['carro_id']
    cliente_id = event['cliente_id']
    
    try:
        print("Conectando...")
        connection = pymysql.connect(host=RDS_HOST,
                                     user=USERNAME,
                                     password=PASSWORD,
                                     database=DB_NAME, 
                                     connect_timeout=20)
        
        print("Conectou!")
    
        # Consulta SQL para buscar o carro pelo modelo e ano
        cursor = connection.cursor()
        cursor.execute("SELECT estoque FROM mtcarsApp_carro WHERE id = %s", (carro_id,))
        result = cursor.fetchone()
            
        # Se encontrar o carro, retorna os detalhes
        if result is None:
            return {
                    'statusCode': 404,
                    'body': json.dumps('Carro não encontrado')
                }
        estoque = result[0]
        
        if estoque > 0:
            # Decrementar o estoque
                cursor.execute("UPDATE mtcarsApp_carro SET estoque = estoque - 1 WHERE id = %s", (carro_id,))
                
                # Adicionar cliente à lista de interessados
                cursor.execute("INSERT INTO mtcarsApp_carro_clientes_reservados (carro_id, cliente_id) VALUES (%s, %s)", (carro_id, cliente_id))

                connection.commit()

                if estoque - 1 == 0:
                    cursor.execute("UPDATE mtcarsApp_carro SET disponibilidade = %s WHERE id = %s", (False, carro_id))
                    connection.commit()
                    
                return {
                    'statusCode': 200,
                    'body': json.dumps('Carro reservado com sucesso!')
                }
        else:
            cursor.execute("UPDATE mtcarsApp_carro SET disponibilidade = FALSE WHERE id = %s", (carro_id,))
            return {
                'statusCode': 400,
                'body': json.dumps('Carro indisponível')
            }
            
    except Exception as e:
            return {
            'statusCode': 500,
            'body': json.dumps(f"Erro ao processar a reserva: {str(e)}")
        }
    finally:
        if connection:
            connection.close()
                
            
          