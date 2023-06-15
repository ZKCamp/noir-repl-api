import re


def clean_output(output):
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    cleaned_output = ansi_escape.sub('', output)

    cleaned_output = cleaned_output.strip()

    return cleaned_output
