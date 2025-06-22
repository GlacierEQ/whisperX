"""
scan_and_compile_repos.py
Recursively scans provided directories for useful repos and codebases.
Outputs a Markdown table of findings.
"""
import os

# List of directories to scan (customize as needed)
DIRECTORIES = [
    r"C:\Users\casey\.sequential-thinking\Downloads\Compressed - Sorted By 4-Organizer Ultra",
    r"C:\Users\casey\.sequential-thinking\Downloads",
    r"C:\Users\casey\OneDrive\Documents\GitHub",
    r"C:\Users\casey\.sequential-thinking\.vscode\extensions\bitlang.cobol-25.4.30\resources\mermaid\chunks"
]

CODE_EXTENSIONS = {'.py', '.js', '.ts', '.java', '.go', '.cpp', '.c', '.cs', '.rb', '.php', '.sh', '.ipynb'}
NOTEWORTHY_FILES = {'README.md', 'requirements.txt', 'package.json', 'setup.py', 'Pipfile', 'environment.yml'}

results = []

def scan_dir(root):
    for dirpath, dirnames, filenames in os.walk(root):
        # Check for git repo
        if '.git' in dirnames:
            results.append({
                'type': 'Git Repo',
                'path': dirpath,
                'noteworthy': [f for f in filenames if f in NOTEWORTHY_FILES]
            })
            # Don't descend into .git
            dirnames.remove('.git')
        # Check for code folder
        code_files = [f for f in filenames if os.path.splitext(f)[1] in CODE_EXTENSIONS]
        if code_files:
            results.append({
                'type': 'Code Folder',
                'path': dirpath,
                'noteworthy': [f for f in filenames if f in NOTEWORTHY_FILES]
            })
        # Optionally, check for compressed archives (not extracting for now)
        # archives = [f for f in filenames if os.path.splitext(f)[1] in {'.zip', '.rar', '.7z'}]
        # if archives:
        #     results.append({'type': 'Archive', 'path': dirpath, 'noteworthy': archives})

def main():
    for d in DIRECTORIES:
        if os.path.exists(d):
            scan_dir(d)
    # Output Markdown table
    with open('useful_repos.md', 'w', encoding='utf-8') as f:
        f.write('| Type | Path | Noteworthy Files |\n')
        f.write('|------|------|------------------|\n')
        for r in results:
            nf = ', '.join(r['noteworthy']) if r['noteworthy'] else '-'
            f.write(f"| {r['type']} | {r['path']} | {nf} |\n")
    print(f"Scan complete. Results saved to useful_repos.md ({len(results)} entries).")

if __name__ == '__main__':
    main()
