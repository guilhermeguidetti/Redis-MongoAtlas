#!/opt/homebrew/bin/python3
import pymongo
import redis
import json
from faker import Faker
import random

# --------------------- GERAR 5000 ALUNOS -------------------
fake = Faker('pt_BR')

mongoClient = pymongo.MongoClient("mongodb+srv://gzguidetti:<password>@cluster0.v4yzyhv.mongodb.net/test")
db = mongoClient.VESTIBULAR
col = db.APROVADOS
col.drop()

cursos = ['Medicina', 'Direito', 'Engenharia de Software', 'Administração', 'Arquitetura', 'Jogos Digitais', 'Educação Física']
anos = [2023, 2024]
lista_aprovados = []
for i in range(5000):
    nome = fake.name()
    cpf = fake.cpf()
    ano = random.choice(anos)
    curso_aprovado = random.choice(cursos)
    
    candidato = {
        'nome': nome,
        'cpf': cpf,
        'curso_aprovado': curso_aprovado,
        'ano': ano
    }
    
    lista_aprovados.append(candidato)
    
col.insert_many(lista_aprovados)

# --------------------- FIM DA GERAÇÃO DE ALUNOS ------------------------

# --------------------- REDIS -------------------------------------------
aprovados = col.find()
redis_client = redis.Redis(host="localhost", port=6379)
for i in aprovados:
    key = str(i["_id"])
    redis_client.set(key, json.dumps(i, default=str))
    value = redis_client.get(key)
    
change_stream = col.watch(full_document="updateLookup")

for change in change_stream:
    operation_type = change["operationType"]
    print(f"\n\n"+"=-"*75+f"\nTipo de operação executada: {operation_type}")
    
    if operation_type in ["insert", "update"]:
        full_document = change["fullDocument"]
        print(f"Documento completo no MongoDB: {full_document}")
        
        document_json = json.dumps(full_document, default=str)

        key = str(full_document["_id"])
        redis_client.set(key, document_json)
        doc = redis_client.get(key)
        print(f"Documento no redis: {doc}\n"+"=-"*75)
        print(f"Documento {key} inserido ou atualizado no Redis com sucesso!")
        
    elif operation_type == "delete":
        key = str(change['documentKey']['_id'])
        for i in redis_client.scan_iter(key): # adicionado aqui para depurar
            result = redis_client.delete(key)
            if result == 0:
                print("Documento não encontrado para remoção")
            else:
                print(f"\nDocumento {key} deletado do Redis\n"+"=-"*75)
