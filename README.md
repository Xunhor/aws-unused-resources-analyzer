# Script de Análise de Recursos AWS

Este script em Python utiliza a biblioteca `boto3` para listar recursos não utilizados em sua infraestrutura da AWS. O objetivo é ajudar na identificação de serviços que podem ser eliminados ou ajustados para redução de custos.

## Pré-requisitos

Antes de executar o script, você precisa ter:

- Uma conta na AWS.
- Credenciais da AWS configuradas no seu ambiente local. Isso pode ser feito através do arquivo `~/.aws/credentials` ou utilizando variáveis de ambiente.
- O pacote `boto3` instalado. Você pode instalá-lo usando o seguinte comando:

```bash
pip install boto3
