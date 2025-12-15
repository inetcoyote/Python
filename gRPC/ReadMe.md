## gRPC

Для формирования кода в файлах user_service_pb2.py и
user_service_pb2_grpc.py из файла user_service.proto файла
нужно выполнить команду команду:
```bash
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. user_service.proto
```

### Запуск сервера
```bash
python server.py
```
В терминале сервера будет выведено сообщение:
```
✅ Сервер запущен на порту 50051...
```

### Запуск клиента
```bash
python main.py
```

В результате запуска приложения main.py в терминале
будет выведено сообщение:
```
User: Alice, Email: alice@example.com
```

