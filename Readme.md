# Genome Search
- Instituição: Universidade Estadual de Santa Cruz
- Curso: Ciência da Computação
- Disciplina: CET098 - Rede de Computadores I
- Docente: Jorge Lima de Oliveira Filho
- Discentes: Luca Sacramento, Matheus Brandão.

Este projeto tem como objetivo a conclusão da avaliação prática para a disciplina. Ela consiste em uma aplicação cliente-servidor simulando o funcionamento de um buscador para genomas que a partir de seu nome científico ou popular retorna sua informação hereditária codificada em seu DNA no formato ".fasta", além da possibilidade de cadastro de novas espécies, armazenando-as em nosso sistema.

Conteúdo:
- Requisitos
- Recomendações
- Integrantes
- Instalação
- Organização do projeto
- Protocolo
- Diagrama
- Motivações
- Contribuições

## Requisitos:
- [x] Comunicação via TCP ou UDP;
- [x] Documentação do protocolo da camada de aplicação;
- [x] Documentação do funcionamento do software.

## Recomendações
- Cada desenvolvedor terá sua branch para ficar a vontade para inserir novas funcionalidades ao projeto.
- Ao desenvolver uma nova funcionalidade o dev deverá solicitar o Pull Request comentando o que foi feito.
- Em relação aos commits será utilizado um padrão
    - Commits de novas features. Ex: git commit -m "New: Readme"
    - Commits de updates. Ex: git commit -m "Update: Readme"
    - Commits de remoção. Ex: git commit -m "Removed: Readme"

## Integrantes
Projeto desenvolvido pelos Devs:

- [Luca Sacramento](https://github.com/lucasao98)
- [Matheus Brandão](https://github.com/MatBrands)

## Instalação

### Conda
No desenvolvimento foi utilizado o gerenciador de pacotes e ambientes [Conda](https://conda.io/). Portanto para prosseguir necessita-se de sua [instalação](https://conda.io/projects/conda/en/latest/user-guide/install/index.html).

- Instalar dependências
```sh
conda env create enviroment.yml
```

- Ativar
```sh
conda activate genome_search-venv
```

- Desativar
```sh
conda deactivate
```

### Requirements
Pode-se utilizar o arquivo requiremets.txt para criar o ambiente virtual.

- Criar ambiente virtual
```sh
python -m venv genome_search-venv
```

- Ativar
```sh
source ./genome_search-venv/bin/activate
```

- Instalar dependências
```sh
pip install -r requirements.txt
```

- Desativar
```sh
deactivate
```

## Organização do projeto

### O funcionamento detalhado encontra-se dentro de cada pasta no arquivo Readme.md

#### Cliente

```sh
├── client
│   ├── interface
│   │   ├── menuClass.py
│   │   └── socketClient.py
│   └── storage
│       ├── abelha.fasta
│       ├── cachorro.fasta
│       ├── morcego.fasta
│       └── panda.fasta
│   ├── __init__.py
│   ├── Readme.md
```

#### Server

```sh
├── server
│   ├── interface
│   │   └── socketServer.py
│   └── database
│       ├── abelha.fasta
│       ├── cachorro.fasta
│       ├── morcego.fasta
│       └── panda.fasta
│   ├── __init__.py
│   ├── Readme.md
```


## Protocolo
Para execução e testes foi feita configuração para rede local, com nome 'localhost' e porta padrão 55552
<div style="line-height: 2;">
    <ol>
        <li>Servidor é preparado e aguarda solicitações - O servidor aguarda novas solicitações;</li>
        <li>Cliente ao ser inicializado solicita conexão - O cliente envia ao servidor uma solicitação de conexão do socket para iniciar as interações;</li>
        <li>Servidor aceita a conexão - O servidor aceita a conexão solicitada pelo cliente e então aguarda informações para prosseguir;</li>
        <li>Cliente solicita um conteúdo do servidor - O cliente envia uma solicitação para o servidor para começar a receber uma determinada informação;</li>
        <ul>
            <li>Cliente solicita genomas disponíveis - O cliente envia um 'get_items';</li>
            <ul>
                <li>Servidor calcula a quantidade de genomas existentes e envia seu tamanho para o Cliente;</li>
                <li>Servidor envia cada nome de arquivo para o Cliente;</li>
                <li>Cliente armazena cada nome de arquivo em uma lista.</li>
            </ul>
            <li>Cliente solicita download de um genomas catalogado - O cliente envia um 'get_files';</li>
            <ul>
                <li>Cliente envia o nome do arquivo para o Servidor;</li>
                <li>Cliente verifica se o arquivo ja está baixado;</li>
                <ul>
                    <li>Caso exista envia uma mensagem para não prosseguir;</li>
                    <li>Caso não exista envia uma mensagem para prosseguir.</li>
                </ul>
                <li>Servidor abre o arquivo .fasta para leitura binária;</li>
                <li>Cliente abre o arquivo .fasta para escrita binária;</li>
                <li>Servidor envia linha por linha suas informações;</li>
                <li>Cliente escreve linha por linha suas informações;</li>
                <li>Servidor envia uma mensagem 'stop' para finalização.</li>
            </ul>
            <li>Cliente solicita cadastrar um genoma - O cliente envia um 'set_files';</li>
            <ul>
                <li>Cliente envia o nome do arquivo para o Servidor;</li>
                <li>Servidor verifica se o arquivo ja está catalogado;</li>
                <ul>
                    <li>Caso exista envia uma mensagem para não prosseguir;</li>
                    <li>Caso não exista envia uma mensagem para prosseguir.</li>
                </ul>
                <li>Cliente abre o arquivo .fasta para leitura binária;</li>
                <li>Servidor abre o arquivo .fasta para escrita binária;</li>
                <li>Cliente envia linha por linha suas informações;</li>
                <li>Servidor escreve linha por linha suas informações;</li>
                <li>Cliente envia uma mensagem 'stop' para finalização.</li>
            </ul>
        </ul>
        <li>Cliente pode repetir o passo 4 repetidamente;</li>
        <li>Cliente encerra a conexão - O cliente envia um 'close'.</li>
    </ol>
</div>

## Diagrama
![Fluxograma](https://raw.githubusercontent.com/MatBrands/Genome_search/2f0c21104e7f6e8ad06d914e132b29d8891e40cb/utils/Fluxograma_redes_I.jpg)

## Motivações
O protocolo escolhido foi o TCP por conta de garantir maior integradade na tranferência de dados, evitando perdas. A implementação dos recursos de Multi-Thread foram feitos para tentar simular um uso real da aplicação, onde diversos clientes se comunicariam com esse serviço.

## Contribuições
Ao longo do desenvolvimento do projeto pode-se pontuar a leitura constante da documentação das bibliotecas Sockets e Thread_, e por fim pesquisar em fóruns e sites por aplicações que utilizavam essas ferramentas para melhor entendimento e exemplificação.