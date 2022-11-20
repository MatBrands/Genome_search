# Genome Search

Este projeto tem como objetivo a conclusão da avaliação prática para a disciplina CET098 - Rede de Computadores I. 

Ela consiste em uma aplicação cliente-servidor simulando o funcionamento de um buscador para genomas que a partir de seu nome científico ou popular retorna sua informação hereditária codificada em seu DNA em formato ".fasta", além da possibilidade de cadastrar novas espécies, armazenando-as em nosso banco de dados.

Conteúdo:
- Requisitos
- Recomendações
- Integrantes
- Instalação
- Organização do projeto
- Contribuições

## Requisitos:
- [ ] Comunicação via TCP ou UDP;
- [ ] Documentação do protocolo da camada de aplicação;
- [ ] Documentação do funcionamento do software.

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

No desenvolvimento foi utilizado o gerenciador de pacotes e ambientes [Conda](https://conda.io/). Portanto para prosseguir necessita-se de sua [instalação](https://conda.io/projects/conda/en/latest/user-guide/install/index.html).

- Instalar dependências
```sh
conda env create enviroment.yml
```

- Ativação
```sh
conda activate genome_search-venv
```

- Desativação
```sh
conda deactivate
```

## Organização do projeto



Cliente ...

```sh
├── client
│   ├── ...
│   │   └── ...
```

Server ...

```sh
├── server
│   ├── ...
│   │   └── ...
```


## Contribuições

Ressaltar contribuições que julgar relevantes.