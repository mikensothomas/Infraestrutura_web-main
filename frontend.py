import grpc
import messenger_pb2
import messenger_pb2_grpc

def send_message(stub, sender, content):
    response = stub.SendMessage(messenger_pb2.Message(sender=sender, content=content))
    print("Mensagem enviada para o servidor.")

def main():
    channel = grpc.insecure_channel('100.0.0.10:50051')
    stub = messenger_pb2_grpc.MessengerStub(channel)
    
    sender = input("Digite seu nome: ")
    while True:
        message = input("Digite sua mensagem (ou 'sair' para sair): ")
        if message.lower() == 'sair':
            break
        send_message(stub, sender, message)
    
    channel.close()

if __name__ == '__main__':
    main()
