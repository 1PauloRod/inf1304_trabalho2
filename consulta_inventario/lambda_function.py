import pymysql
import os
import logging

# Configurações do banco de dados (coloque esses valores como variáveis de ambiente na Lambda)
RDS_HOST = os.environ['RDS_HOST']
USERNAME = os.environ['RDS_USERNAME']
PASSWORD = os.environ['RDS_PASSWORD']
DB_NAME = os.environ['RDS_DATABASE']

def lambda_handler(event, context):
    # Obtém os parâmetros modelo e ano do evento (por exemplo, via API Gateway)
    modelo = event['modelo']
    ano = event['ano']
    connection = None
    # Conectando-se ao banco de dados RDS
    try:
        logging.info("Conectando...")
        connection = pymysql.connect(host=RDS_HOST,
                                     user=USERNAME,
                                     password=PASSWORD,
                                     database=DB_NAME, 
                                     connect_timeout=20)
        
        logging.info("Conectou!")
    
        
        cursor = connection.cursor()
        sql = "SELECT * FROM mtcarsApp_carro WHERE modelo = %s AND ano = %s"
        cursor.execute(sql, (modelo, ano))
        result = cursor.fetchall()
       
        if result:
            carro = {
                "id": result[0][0], 
                "modelo": result[0][1], 
                "ano": result[0][2],
                "disponibilidade": result[0][3], 
                "estoque": result[0][4], 
                "preco": result[0][5], 
                "clientes_reservados": [], 
                "clientes_interessados": []
            }

            sql_clientes_reservados = """
                SELECT c.id, c.nome, c.sobrenome, c.email
                FROM mtcarsApp_cliente c 
                JOIN mtcarsApp_carro_clientes_reservados ci ON ci.cliente_id = c.id
                WHERE ci.carro_id = %s
            """
            cursor.execute(sql_clientes_reservados, (carro["id"],))
            result_clientes = cursor.fetchall()

            for cliente in result_clientes:
                cliente = {
                    "id": cliente[0], 
                    "nome": cliente[1], 
                    "sobrenome": cliente[2], 
                    "email": cliente[3]
                }
                carro["clientes_reservados"].append(cliente)

            sql_clientes_interessados = """
                SELECT c.id, c.nome, c.sobrenome, c.email
                FROM mtcarsApp_cliente c 
                JOIN mtcarsApp_carro_clientes_interessados ci ON ci.cliente_id = c.id
                WHERE ci.carro_id = %s
            """
            cursor.execute(sql_clientes_interessados, (carro["id"],))
            result_clientes_interessados = cursor.fetchall()

            for cliente in result_clientes_interessados:
                cliente = {
                    "id": cliente[0], 
                    "nome": cliente[1], 
                    "sobrenome": cliente[2], 
                    "email": cliente[3]
                }
                carro["clientes_interessados"].append(cliente)

            return {
                    'statusCode': 200,
                    'body': {
                        'message': 'Carro encontrado',
                        'carro': carro
                    }
                }
        else:
            return {
                    'statusCode': 404,
                    'body': {
                        'message': 'Carro não encontrado'
                    }
                }
    
    except Exception as e:
        return {
            'statusCode': 500,
            'body': {
                'message': f'Erro ao conectar no banco de dados: {str(e)}'
            }
        }
    finally:
        if connection:
            connection.close()
            
          