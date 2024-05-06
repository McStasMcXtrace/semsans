import os
import nbformat
from nbconvert.preprocessors import ClearOutputPreprocessor
from nbconvert import HTMLExporter

def clear_notebook_outputs(notebook_path):
    with open(notebook_path, 'r', encoding='utf-8') as f:
        nb = nbformat.read(f, as_version=4)
    
    # Create a preprocessor to clear outputs
    preprocessor = ClearOutputPreprocessor()
    
    # Process the notebook
    cleared_nb, _ = preprocessor.preprocess(nb, {})

    # Write the cleared notebook back to file
    with open(notebook_path, 'w', encoding='utf-8') as f:
        nbformat.write(cleared_nb, f)

def clear_all_notebooks_in_directory(directory):
    for filename in os.listdir(directory):
        if filename.endswith('.ipynb'):
            notebook_path = os.path.join(directory, filename)
            clear_notebook_outputs(notebook_path)
            print(f"Cleared outputs for {notebook_path}")

if __name__ == "__main__":
    directory_path = "./"
    clear_all_notebooks_in_directory(directory_path)