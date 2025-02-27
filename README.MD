# Apresentação de Case Técnico para Quero Bolsa

## Situação Problema do Projeto

Obter preços de ações via API do site https://www.stockdata.org/pricing. O problema consiste em escolher 10 ações para monitorar seus valores, tendo uma margem de 10 dias de histórico para cada ação, prezando um full load inicial.

Será necessário organizar os dados em camadas, Bronze, Silver e Gold, onde na Gold o preço da ação no dia deve ser a média entre o preço de abertura e o de fechamento da ação.

No final, será necessário o geramento de um gráfico que exiba o preço de cada ação por dia, levando em conta os dados em parquet da camada Gold.



## O que será necessário

Para o funcionamento do projeto, você precisara das seguintes tecnologias:

1. [Git](https://git-scm.com/downloads): Utilizaremos o Git para clonar o nosso repositório.

2. [Python](https://www.python.org/downloads/): Precisaremos do python para podermos utilizar de maneira adequada o ambiente virtual.

## 1º Passo: Clonando o repositório

<details>
  <summary><b>Clique aqui</b></summary>

  Para clonar o projeto e utilizá-lo em seu computador, siga os seguintes passos:
  
  1. Crie uma pasta onde deseja armazenar o projeto, e então abra-a e clique na url da pasta, ou então utilize o atalho `Ctrl+L` para selecionar a url, e escreva 'cmd' para abrir o prompt de comando.
  
  > _Obs.: Caso você esteja no LINUX, a parte de escrever "cmd" não irá funcionar, então clique com o botão direito na pasta que você criou e selecione a opção "Abrir no terminal"_

  Um prompt de comando irá se abrir, e então execute o comando abaixo:
  
  ```
  git clone https://github.com/DuuhZero/Case-Tecnico-Quero.git
  ``` 
  E depois
  ```
  cd Case-Tecnico-Quero
  ```
  
</details>
<br>

## 2º Passo: Iniciando o ambiente virtual

<details>
  <summary><b>Clique aqui</b></summary>

  1. Após a clonagem e avançar o diretŕio, ainda no terminal, execute o seguinte comando:

  ```
  python -m venv venv
  venv\Scripts\activate
  ```


  > _Caso você esteja em LINUX, digite os comandos desta maneira:_<br>
  `python3 -m venv venv`<br>
  `source venv/bin/activate`<br>

  2. Para a intalação dos requirements, após ativar o ambiente virtual, execute os seguintes comandos:
  ```
  cd src/
  pip install -r requirements.txt
  ```

</details>
<br>

## 3º Passo: Executando o Projeto
<details>
  <summary><b>Clique aqui</b></summary>
  Por fim, para poder executar o arquivo <b>tdd_api.py</b> basta escrever no terminar o seguinte comando:

  ```
  python tdd_api.py
  ```
> _Caso você esteja em LINUX, digite os comandos desta maneira:_<br>
  `python3 tdd_api.py`

E veja a mágica acontecer!
</details>
<br>

## Finalização

Gostaria de agradecer profundamente a oportunidade por ter avançado mais uma etapa, é de extrema importância para mim poder ter a chance de mostrar meu potencial para trabalhar com vocês <3

### Feito por Eduardo da Silva Fontes



