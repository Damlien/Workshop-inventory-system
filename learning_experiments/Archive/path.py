from pathlib import Path

i_am_here = Path(__file__)

print(i_am_here)

full_path = i_am_here.resolve()

print(full_path)

my_folder = full_path.parent

print(my_folder)

new_path = my_folder / "inventory.json"

print(new_path)

if new_path.exists():
    print("Found it!")
