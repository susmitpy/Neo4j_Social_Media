import os
import re

from jinja2 import Environment, FileSystemLoader

template = Environment(loader=FileSystemLoader(".")).get_template(
    "lambda_template.jinja"
)

funcs_pattern = re.compile(r"def.+\n(.+\n)+")
func_name_pattern = re.compile(r"def (\w+)")
func_signature_pattern = re.compile(r"def \w+.+")
args_pattern = re.compile(r"(\w+):")

folders = ["users"]
file_paths = []

# Get all files in the folders
for folder in folders:
    for file in os.listdir(folder):
        if file.endswith(".py"):
            file_paths.append(os.path.join(folder, file))

for fp in file_paths:
    with open(fp, "r") as f:
        txt = f.read()

    funcs = re.finditer(funcs_pattern, txt)
    for func in funcs:
        func_text = func.group(0)
        func_name = re.match(func_name_pattern, func_text).group(1)

        non_self_text = func_text.replace("self, ", "")  # Remove self argument
        non_self_text = non_self_text.replace("self.", "")  # self.driver to driver

        func_signature = re.match(func_signature_pattern, non_self_text).group(0)
        args = re.findall(args_pattern, func_signature)

        print(func_name)
        print(args)
        print(non_self_text)

        op_txt = template.render(
            func_name=func_name,
            args=args,
            func=non_self_text,
        )

        with open(f"src/{func_name}.py", "w") as f:
            f.write(op_txt)
