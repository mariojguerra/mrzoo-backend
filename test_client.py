import socketio

sio = socketio.Client()

@sio.event
def connect():
    print("Conectado ao servidor!")

@sio.event
def disconnect():
    print("Desconectado do servidor!")

@sio.event
def nova_mensagem(data):
    print(f"Nova mensagem recebida: {data}")

# Conectar ao servidor (altere o IP se necessário)
sio.connect("http://10.0.2.2:5000")

# Enviar mensagem de teste
sio.emit("enviar_mensagem", {"remetente_id": 1, "destinatario_id": 2, "mensagem": "Olá, tudo bem?"})

# Aguarde para receber resposta
sio.wait()
