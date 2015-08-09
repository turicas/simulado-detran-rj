#!/usr/bin/env python3
# coding: utf-8

import codecs
import json
import math
import os

from jinja2 import Environment, FileSystemLoader


QUESTOES = 'questoes.json'


def histogram(data, bin_size):
    sorted_data = sorted(data)
    minimum, maximum = sorted_data[0], sorted_data[-1]
    total_bins = int(math.ceil((maximum - minimum) / float(bin_size)))
    answer = []
    for current_bin in range(total_bins):
        value = minimum + current_bin * bin_size
        count = 0
        for x in sorted_data:
            if x < value + bin_size:
                count += 1
            else:
                break
        sorted_data = sorted_data[count:]
        answer.append((value, count))
    return answer


class Renderer:
    def __init__(self, template_path, build_path):
        self.template_path = template_path
        self.build_path = build_path
        self.env = Environment(loader=FileSystemLoader(template_path))

    def render(self, template_filename, context):
        template = self.env.get_template(template_filename)

        output = template.render(**context)

        output_filename = os.path.join(self.build_path, template_filename)
        if not os.path.exists(self.build_path):
            os.mkdir(self.build_path)

        with codecs.open(output_filename, 'w', encoding='utf-8') as fobj:
            fobj.write(output)

    def render_index(self, perguntas):
        template = 'index.html'
        repeticoes = [pergunta['repeticoes'] for pergunta in perguntas]
        simulados = int(sum(repeticoes) / 30)
        perguntas_com_imagem = sum([1 for perg in perguntas if perg['imagem']])
        perguntas_sem_imagem = len(perguntas) - perguntas_com_imagem
        freqdist = json.dumps(histogram(data=repeticoes, bin_size=50))
        context = {'total_perguntas': len(perguntas),
                   'total_simulados': simulados,
                   'perguntas_com_imagem': perguntas_com_imagem,
                   'freqdist': freqdist,
                   'perguntas_sem_imagem': perguntas_sem_imagem, }
        self.render(template, context)

    def render_perguntas(self, perguntas):
        template = 'perguntas.html'
        context = {'perguntas': perguntas,}
        self.render(template, context)


def main():
    with open(QUESTOES) as fobj:
        questoes = json.load(fobj)
    questoes.sort(key=lambda pergunta: pergunta['repeticoes'], reverse=True)

    renderer = Renderer(template_path='templates', build_path='build')
    renderer.render_index(questoes)
    renderer.render_perguntas(questoes)


if __name__ == '__main__':
    main()
