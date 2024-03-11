import ast

def load_dictionary_at_index(file_path, index):
    try:
        with open(file_path, 'r') as file:
            for i, line in enumerate(file):
                if i == index:
                    return ast.literal_eval(line.strip())
        print("Index out of range.")
        return None
    except FileNotFoundError:
        print("File not found.")
        return None
    except ValueError as e:
        print(f"Error in parsing the file: {e}")
        return None