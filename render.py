#!/usr/bin/env python3
# coding: utf-8

import json
import os

from jinja2 import Environment, FileSystemLoader


QUESTOES = 'detran-rj.json'

def ordena_questoes(questoes):
    perguntas = list(questoes.values())
    perguntas.sort(key=lambda a: a['repeticoes'], reverse=True)
    return perguntas

class Render:
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

        with open(output_filename, 'w', encoding='utf-8') as fobj:
            fobj.write(output)

    def make_index(self, perguntas):
        template = 'index.html'
        simulados = sum([perg['repeticoes'] for perg in perguntas]) / 30
        context = {'total_perguntas': len(perguntas),
                   'total_simulados': int(simulados),}
        self.render(template, context)

    def make_perguntas(self, perguntas):
        template = 'perguntas.html'
        simulados = sum([perg['repeticoes'] for perg in perguntas]) / 30
        context = {'perguntas': perguntas,}
        self.render(template, context)

def main():
    with open(QUESTOES) as fobj:
        questoes = json.load(fobj)
    perguntas = ordena_questoes(questoes)

    renderer = Render(template_path='templates', build_path='build')
    renderer.make_index(perguntas)
    renderer.make_perguntas(perguntas)


if __name__ == '__main__':
    main()
