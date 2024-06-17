#!/bin/bash

# Nome das redes
REDE_WEB="rede_web"

# Criar redes Docker
docker network create --driver bridge $REDE_WEB

# Exibir redes criadas
echo "Redes Docker criadas:"
docker network ls

# Conectar os contêineres às redes (exemplo de comando)
# docker network connect $rede_web <nome_do_conteiner>

echo "Redes configuradas com sucesso."

# Manter o container em execução
exec "$@"
