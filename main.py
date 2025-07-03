from populate import build

json_filepath = r"data.json"
template_path = r"template.tex"
output_path = r"CV.tex"

build(json_filepath, template_path, output_path)