# server.py
from concurrent import futures
import grpc
import user_service_pb2
import user_service_pb2_grpc
import time

class UserService(user_service_pb2_grpc.UserServiceServicer):
    def GetUser(self, request, context):
        # Возвращаем тестовые данные
        return user_service_pb2.UserResponse(
            user_id=request.user_id,
            name="Alice",
            email="alice@example.com"
        )

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    user_service_pb2_grpc.add_UserServiceServicer_to_server(UserService(), server)
    server.add_insecure_port('[::]:50051')  # слушаем порт 50051
    print("✅ Сервер запущен на порту 50051...")
    server.start()
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        print("🛑 Остановка сервера...")
        server.stop(0)

if __name__ == '__main__':
    serve()