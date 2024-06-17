import grpc
from concurrent import futures
import messenger_pb2
import messenger_pb2_grpc
import psycopg2

# Configuração do banco de dados PostgreSQL
DB_HOST = 'banco'  # Nome do serviço do contêiner do banco de dados no Docker Compose
DB_PORT = '5432'    # Porta padrão do PostgreSQL
DB_NAME = 'db_name' # Nome do banco de dados
DB_USER = 'db_user' # Usuário do banco de dados
DB_PASSWORD = '12345' # Senha do banco de dados

# Classe que implementa o serviço gRPC Messenger
class MessengerServicer(messenger_pb2_grpc.MessengerServicer):
    def SendMessage(self, request, context):
        # Obtém os dados da mensagem do cliente
        sender = request.sender
        content = request.content
        
        # Conecta ao banco de dados PostgreSQL
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        
        try:
            # Cria um cursor para executar operações SQL
            with conn.cursor() as cursor:
                # Insere a mensagem na tabela messages
                sql = "INSERT INTO messages (client_name, message) VALUES (%s, %s)"
                cursor.execute(sql, (sender, content))
                conn.commit()
                print(f"Mensagem recebida do cliente {sender}: {content}.")
        except psycopg2.Error as e:
            print(f"Erro ao inserir mensagem no banco de dados: {e}")
        finally:
            conn.close()
        
        # Retorna uma resposta vazia para o cliente
        return messenger_pb2.Empty()

# Função para iniciar o servidor gRPC
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    messenger_pb2_grpc.add_MessengerServicer_to_server(MessengerServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Servidor conectado na porta 50051")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
