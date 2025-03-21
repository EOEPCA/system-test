import re
from nbconvert.preprocessors import ExecutePreprocessor
from nbformat.notebooknode import NotebookNode

TEST_CELL_PATTERN = re.compile(r'^\s*#\s*(\w+)')

class TestWrapperExecutePreprocessor(ExecutePreprocessor):
    def preprocess_cell(self, cell: NotebookNode, resources, cell_index):
        if cell.cell_type == 'code':
            first_line = cell.source.strip().split('\n')[0]
            match = TEST_CELL_PATTERN.match(first_line)
            if match:
                test_name = match.group(1)
                original_source = cell.source
                indented_source = '\n'.join('    ' + line for line in original_source.split('\n'))
                wrapped_source = f"with test_cell('{test_name}'):\n{indented_source}"
                cell.source = wrapped_source
        return super().preprocess_cell(cell, resources, cell_index)