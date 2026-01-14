import sys

def repair_po(filename):
    print(f"Repairing {filename}...")
    with open(filename, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    new_lines = []
    skip_next = False
    
    for i in range(len(lines)):
        if skip_next:
            skip_next = False
            continue
            
        line = lines[i]
        
        # Check if this line is 'msgstr ""\n' and next line is 'msgid_plural'
        if line.strip() == 'msgstr ""' and i + 1 < len(lines):
             next_line = lines[i+1]
             if next_line.strip().startswith('msgid_plural'):
                 print(f"Removing invalid msgstr \"\" before msgid_plural at line {i+1}")
                 continue # Skip this line
        
        new_lines.append(line)

    with open(filename, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
    print("Repair complete.")

if __name__ == "__main__":
    repair_po(sys.argv[1])
