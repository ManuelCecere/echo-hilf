import os

def find_relative_path(target:str = 'algo-rag', home_path:str = os.path.expanduser('~')):
    for root, dirs, files in os.walk(home_path):
        if target in dirs:
            # Construct the relative path to the target
            absolute_path = os.path.join(root, target)
            real_path = os.path.relpath(absolute_path, start=os.getcwd()) 
            return real_path

    return None
