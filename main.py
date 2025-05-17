import inspect

def organize_class_methods(cls) -> str:
    members = inspect.getmembers(cls)
    methods = []
    other_attributes = []
    
    for name, obj in members:
        if name.startswith('__') and name.endswith('__'):
            methods.append((name, obj))
        elif inspect.isfunction(obj) or inspect.ismethod(obj):
            methods.append((name, obj))
        else:
            other_attributes.append((name, obj))
    
    dunder_methods = []
    regular_methods = []
    
    for name, obj in methods:
        if name.startswith('__') and name.endswith('__'):
            dunder_methods.append((name, obj))
        else:
            regular_methods.append((name, obj))
    
    dunder_methods.sort(key=lambda x: (x[0] != '__init__', x[0]))
    regular_methods.sort(key=lambda x: x[0])
    organized_methods = dunder_methods + regular_methods
    source = inspect.getsource(cls)
    lines = source.splitlines()
    class_def_index = 0
    for i, line in enumerate(lines):
        if line.strip().startswith('class '):
            class_def_index = i
            break
    
    indent = ''
    for line in lines[class_def_index + 1:]:
        if line.strip():
            indent = line[:len(line) - len(line.lstrip())]
            break
    
    new_source_lines = [lines[class_def_index]]
    
    for name, obj in other_attributes:
        if inspect.isdatadescriptor(obj):
            attr_source = inspect.getsource(obj)
            new_source_lines.extend([indent + line for line in attr_source.splitlines()])
    
    for i, (name, obj) in enumerate(organized_methods):
        if inspect.isfunction(obj) or inspect.ismethod(obj):
            method_source = inspect.getsource(obj)
            method_lines = [indent + line for line in method_source.splitlines()]
            
            # I dont know
            if i > 0:
                new_source_lines.append("")
            new_source_lines.extend(method_lines)
    
    return '\n'.join(new_source_lines)


# Example usage:
if __name__ == "__main__":
    from yourmodule import yourclass
    organized = organize_class_methods(yourclass)
