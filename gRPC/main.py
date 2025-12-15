import grpc
import user_service_pb2
import user_service_pb2_grpc

def get_user(stub, user_id):
    request = user_service_pb2.UserRequest(user_id=user_id)
    response = stub.GetUser(request)
    return response

def main():
    # Установка соединения с gRPC-сервером
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = user_service_pb2_grpc.UserServiceStub(channel)
        response = get_user(stub, "123")
        print(f"User: {response.name}, Email: {response.email}")

if __name__ == '__main__':
    main()