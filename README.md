# Redis-MongoAtlas
Nome: Guilherme Zanoni Guidetti

Descrição do código:
Primeiro é feito a importação das biliotecas que serão utilizadas e estabelecida a conexão com o MongoDB. Em seguida, é utilizada a biblioteca Faker para gerar dados aleatórios para cada aluno, incluindo nome, CPF, curso aprovado e ano de aprovação, que são armazenados em uma lista e posteriormente inseridos dentro da coleção "APROVADOS" no MongoDB.
Após popular a coleção, é estabelecido a conexão com o Redis para sincronizar os dados dos alunos em tempo real. Para isso, ele percorre a coleção de alunos aprovados no MongoDB e armazena cada documento no Redis com a chave sendo o "_id" do aluno gerado pelo MongoAtlas e o valor sendo um objeto JSON representando o documento completo.
Para monitorar a coleção, é utilizado um change stream do MongoDB na coleção de "APROVADOS", quando uma operação de update ou inserção é detectada, o código atualiza o documento correspondente no Redis com a nova versão do documento. Quando uma operação de exclusão é detectada, o código remove o documento correspondente do Redis.

Resultados:
O código gerou 5000 alunos fictícios e os sincronizou em tempo real com o Redis. Quando uma operação de inserção ou atualização foi detectada no MongoDB, o documento correspondente foi atualizado com sucesso no Redis. Quando uma operação de exclusão foi detectada no MongoDB, o documento correspondente foi excluído com sucesso do Redis.
 
Metodologia:
O código foi desenvolvido em Python 3.5 utilizando o ambiente de desenvolvimento Visual Studio Code. O código foi testado em um ambiente local com o Redis instalado e Mongo Atlas.

Referências:
Documentação MongoDB: https://docs.mongodb.com/
Documentação Redis: https://redis.io/
Documentação Faker: https://faker.readthedocs.io/en/master/
