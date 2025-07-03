import os
import json
import re
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


from jinja2 import Environment, FileSystemLoader

json_filepath = r"data.json"
template_path = r"template.tex"
output_path = r"CV.tex"

class JsonChangeHandler(FileSystemEventHandler):
    def __init__(self, json_filepath, template_path, output_path):
        self.json_filepath = json_filepath
        self.template_path = template_path
        self.output_path = output_path

    def on_modified(self, event):
        if event.src_path.endswith(self.json_filepath):
            print(f"{self.json_filepath} changed, rebuilding...")
            try:
                change(self.json_filepath, self.template_path, self.output_path)
                print("\n\nRebuild complete!\nWatching...\n\n")

            except Exception as e:
                print(f"Error during rebuild: {e}")


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

def change(json_filepath, template_path, output_path):
    build_latex(json_filepath, template_path, output_path)
    build_pdf(output_path)

def watch_json(json_filepath, template_path, output_path):
    event_handler = JsonChangeHandler(json_filepath, template_path, output_path)
    observer = Observer()
    observer.schedule(event_handler, path='.', recursive=False)
    observer.start()
    print(f"Watching {json_filepath} for changes. Press Ctrl+C to stop.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

def main():
    while (inp := input("\n\n\nEnter a command: \nb: build\nq: quit\nw: watch\n\n-->:").strip().lower()) != "q":
        if inp == "b":
            print("Building... ")
            build_latex(json_filepath, template_path, output_path)
            build_pdf(output_path)
            print("Finished")
        
        elif inp == "w":
            print("Watching for changes...")
            watch_json(json_filepath, template_path, output_path)


main()