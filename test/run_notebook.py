import nbformat
from .wrap_cells import TestWrapperExecutePreprocessor

def execute_wrapped_notebook(input_path, output_path, execution_path='.'):
    with open(input_path) as f:
        nb = nbformat.read(f, as_version=4)

    ep = TestWrapperExecutePreprocessor(timeout=600, kernel_name='python3')
    ep.preprocess(nb, {'metadata': {'path': execution_path}})

    with open(output_path, 'w', encoding='utf-8') as f:
        nbformat.write(nb, f)