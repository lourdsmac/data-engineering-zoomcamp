from pathlib import pathlib

current_dir = Path.cwd()
current_file = Path(__file__).name

print(f"Files in: {current_dir}:")

for filePath in current_dir.iterdir():
    if filePath.name == current_file:
        continue
    print(f"- {filePath.name}")

    if filePath.is_file():
        content = filePath.read_text(encoding="utf-8")
        print(f"  Content:\n{content}")