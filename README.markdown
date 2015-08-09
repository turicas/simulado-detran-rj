# `simulado-detran-rj`

Esse repositório tem como objetivo:

- Hospedar o código de um crawler que baixa e armazena questões do simulado
  para a prova de habilitação do DETRAN-RJ -- branch `develop`;
- Hospedar o código do site que exibe os resultados (todas as questões
  disponíveis, questões que mais aparecem, respostas corretas etc.) -- branch
  `gh-pages`.


## Funcionamento do Crawler

- O arquivo `detran_rj.py` é o crawler em si e gera o arquivo `detran-rj.json`
  com os resultados obtidos. Você pode parar a execução do mesmo e voltar a
  qualquer momento que ele não perderá os dados: a cada vez que ele roda, ele
  carrega o arquivo `detran-rj.json` em memória - caso exista - e continua o
  trabalho, até que então salva o arquivo quando recebe um signal `SIGINT`
  (ctrl+c).
- O arquivo `converte.py` lê o arquivo `detran-rj.json` e converte seu formato
  (para facilitar a leitura pelo JavaScript do site), salvando então o arquivo
  `questoes.json`, que será servido para o site.

## Funcionamento do Site

- O arquivo `render.py` lê os HTMLs em `templates` e o arquivo `questoes.json`
  e gera os arquivos finais em `build/`.
