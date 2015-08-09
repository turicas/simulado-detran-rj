#!/usr/bin/env python
# coding: utf-8

import json


url_imagem = 'http://simulado.detran.rj.gov.br/img/placas/{}.gif'
arquivo_entrada = 'detran-rj.json'
arquivo_saida = 'questoes.json'


def main():
    with open(arquivo_entrada) as fobj:
        entrada = json.load(fobj)
    questoes = list(entrada.values())
    questoes.sort(key=lambda questao: questao['repeticoes'], reverse=True)
    novas_questoes = []
    for questao in questoes:
        opcoes = [{'texto': opcao,
                   'correta': int(questao['resposta_correta']) == index + 1}
                  for index, opcao in enumerate(questao['opcoes'])]

        imagem = str(questao['imagem'])
        if not imagem.strip() or imagem.strip() == '[]':
            imagem = ''
        else:
            imagem = url_imagem.format(imagem)

        nova_questao = {'enunciado': questao['enunciado'],
                        'imagem': imagem,
                        'repeticoes': questao['repeticoes'],
                        'opcoes': opcoes, }
        novas_questoes.append(nova_questao)

    with open(arquivo_saida, 'w') as fobj:
        json.dump(novas_questoes, fobj)


if __name__ == '__main__':
    main()
