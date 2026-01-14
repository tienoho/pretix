import re
import sys
import os

def parse_and_fix_po(filename, autofix=False):
    print(f"Scanning {filename}...")
    with open(filename, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    new_lines = []
    errors = []
    
    # regex for placeholders
    def extract_placeholders(text):
        return sorted(re.findall(r'(?<!\{)\{([a-zA-Z0-9_]+)\}(?!\})', text))
    
    def extract_py_format(text):
        return sorted(re.findall(r'%\([a-zA-Z0-9_]+\)[sdi]|%[sdi]', text))

    i = 0
    while i < len(lines):
        line = lines[i]
        
        if line.strip().startswith('msgid "'):
            # Start of a block
            block_msgid = []
            block_msgstr = []
            block_lines_msgid = []
            block_lines_msgstr = []
            
            # Read msgid
            while i < len(lines):
                line = lines[i]
                stripped = line.strip()
                if stripped.startswith('msgid "') or (stripped.startswith('"') and not block_msgstr):
                    if stripped.startswith('msgid "'):
                        content = stripped[7:-1]
                    else:
                        content = stripped[1:-1]
                    block_msgid.append(content)
                    block_lines_msgid.append(line)
                    i += 1
                else:
                    break
            
            # Read msgstr
            while i < len(lines):
                line = lines[i]
                stripped = line.strip()
                if stripped.startswith('msgstr "') or (stripped.startswith('"') and block_msgstr is not None):
                    if stripped.startswith('msgstr "'):
                         content = stripped[8:-1]
                         block_msgstr = [content] # Initialize
                    elif block_msgstr is not None:
                         content = stripped[1:-1]
                         block_msgstr.append(content)
                    
                    block_lines_msgstr.append(line)
                    i += 1
                else:
                    break
            
            # Validate block
            full_msgid = "".join(block_msgid)
            full_msgstr = "".join(block_msgstr) if block_msgstr else ""
            
            p_id = extract_placeholders(full_msgid)
            p_str = extract_placeholders(full_msgstr)
            f_id = extract_py_format(full_msgid)
            f_str = extract_py_format(full_msgstr)
            
            if p_id != p_str or f_id != f_str:
                err_msg = f"Mismatch: ID {p_id}/{f_id} vs STR {p_str}/{f_str} in '{full_msgid[:20]}...'"
                errors.append(err_msg)
                
                if autofix:
                    # Append msgid lines as is
                    new_lines.extend(block_lines_msgid)
                    # Append empty msgstr
                    new_lines.append('msgstr ""\n')
                else:
                    # Append original
                    new_lines.extend(block_lines_msgid)
                    new_lines.extend(block_lines_msgstr)
            else:
                new_lines.extend(block_lines_msgid)
                new_lines.extend(block_lines_msgstr)
                
        else:
            new_lines.append(line)
            i += 1

    if errors:
        print(f"Found {len(errors)} errors.")
        # for e in errors[:5]: # Show first 5
        #     print(e)
        if autofix:
            print("Applying autofixes...")
            with open(filename, 'w', encoding='utf-8') as f:
                f.writelines(new_lines)
            print("File updated.")
    else:
        print("No errors found.")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        autofix = "--autofix" in sys.argv
        filename = sys.argv[1]
        parse_and_fix_po(filename, autofix)
    else:
        print("Usage: python debug_po.py <path_to_po> [--autofix]")
