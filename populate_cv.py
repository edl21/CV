import os
import json
import re

from jinja2 import Environment, FileSystemLoader

json_filepath = r"data.json"
template_path = r"template.tex"
output_path = r"CV.tex"


def build_latex(json_filepath, template_path, output_path):
    # Load JSON data and extract the name
    with open(json_filepath, 'r', encoding='utf-8') as jf:
        data = json.load(jf)

    # Load template
    env = Environment(loader=FileSystemLoader('.'))
    template = env.get_template('template.tex')

    # Render template
    rendered_tex = template.render(data=data)

    # Write to a .tex file
    with open('CV.tex', 'w') as f:
        f.write(rendered_tex)

def build_pdf(output_path):
    # Run pdflatex to generate PDF from the .tex file
    cwd = os.getcwd().replace('\\', '/')
    # Create the Docker run command using the absolute path
    command = f'docker run --rm -v "{cwd}:/data" blang/latex:ctanfull pdflatex {output_path}'
    os.system(command)
    if os.name == 'nt':
        pass
        os.system("del CV.aux CV.out CV.log")
    else:
        os.system("rm CV.aux CV.out CV.log")


def main():
    while (inp := input("\n\n\nEnter a command: \nb: build\nq: quit\n\n-->:").strip().lower()) != "q":
        if inp == "b":
            print("Building... ")
            build_latex(json_filepath, template_path, output_path)
            build_pdf(output_path)
            print("Finished")

main()