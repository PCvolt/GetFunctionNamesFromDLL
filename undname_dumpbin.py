import subprocess
import re

def run_dumpbin(dll_path):
    try:
        result = subprocess.run(['dumpbin', '/EXPORTS', dll_path], capture_output=True, text=True, check=True, shell=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error running dumpbin: {e}")
        return None

def extract_function_names(dumpbin_output):
    lines = dumpbin_output.splitlines()
    function_names = []
    export_section = False

    for line in lines:
        if 'ordinal' in line.lower() and 'name' in line.lower():
            export_section = True
            continue
        
        if export_section:
            match = re.search(r'[\dA-F]+\s+[\dA-F]+\s+[\dA-F]+\s+(\S+)', line)
            if match:
                function_names.append(match.group(1))

    return function_names

def run_undname(function_name):
    try:
        result = subprocess.run(['undname', function_name], capture_output=True, text=True, check=True, shell=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error running undname: {e}")
        return None

def main(dll_path):
    dumpbin_output = run_dumpbin(dll_path)
    if not dumpbin_output:
        return

    function_names = extract_function_names(dumpbin_output)
    for name in function_names:
        undname_output = run_undname(name)
        if undname_output:
            print(f"{name} -> {undname_output}")
        else:
            print(f"Failed to demangle {name}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python script.py <path_to_dll>")
        sys.exit(1)

    dll_path = sys.argv[1]
    main(dll_path)
    input()
