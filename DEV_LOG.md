# Development Log

**Date: [10/01/26]**

Created repository in GitHub `Workshop-storage-system`

Installed Git on PC

Cloned repository to its own folder on my PC
    	
- guide:
  - 1) open the folder where the repository will be stored on your own PC
  - 2) right click in the folder and choose `open in terminal`
  - 3) get the repository clone link from GitHub, green button with `<>code`  
  	in this case: https://github.com/Damlien/Verksted-Lager-system.git
  - 4) in the terminal write `git clone [url]`  
  	in this case: `git clone https://github.com/Damlien/Workshop-storage-system.git`
  - 5) results in a new folder with the same name as the repository `Workshop-storage-system`

Added extra folders in `workshop-storage-system` on my PC: 
- `learning_experiments` for projects used to learn code
- `src` for source code

Created the text file `DEV_LOG.md` for logging

GitHub must now be updated with changes on the PC. 

- three commands are used:    	

  - `git add .`  
    - the command tells git which changes have been made and what should be included in the next
    - update. In the command, the dot indicates all changes made in the project folder.
  
  - `git commit -m "message"`  
    - for documentation. Locks changes and gives a unique ID number. `-m` stands for message.     			
    - explain what has been done in the message enclosed by `" "`.

  - `git push`  
    - sends all changes and the documentation to GitHub.

In the `learning_experiments` folder, the folder `Data_inventory_test` was created.  
- Testing of JSON for storing data with Python.  
- Created the script `Data_inventory_test.py`. 

	code that was used:

		import json

		list of dictionaries for storing data for components in inventory:
			ex:
				components = [
					{"id": 1, "name": "resistor 10kΩ", "quantity": 100, "shelf": 1},
					{"id": 2, "name": "Arduino Nano",  "quantity": 8,   "shelf": 2},
					{"id": 3, "name": "capacitor",     "quantity": 20,  "shelf": 3}
				]

		with open(filename, mode):

			the purpose of `with` is automatic handling of the file. The file is open for the indented block below. 
			After the block, the file is closed. 

		json.dump(variable, file_object)

		json.load(file_object)

`learning_experiments` – script `Data_inventory_test.py` update  
- made changes in the script `Data_inventory_test.py` inside the folder `Data_inventory_test`  
  - now uses the `Path` class from `pathlib` for modern and tidy handling of file paths. 

	code:

		from pathlib import Path

		BASE_DIR = Path(__file__).resolve().parent 
			first part `Path(__file__)` fetches the path to the Python script, 
			`.resolve()` finds the exact, absolute path to the file or folder.
			`.parent` finds the folder the file is in.
			the result is then the full path to the folder the file is in.
		
		FILE_PATH = BASE_DIR / "inventory.json"
			here you get the path to the actual file.

Created the folder `search` and the file `search_inventory.py`.  
- The script makes it possible to search for components in the file `inventory.json`.  
- Uses simple input for a search word and uses it to compare with names in the inventory list. 

- Uses the `pathlib` library to find the location of `inventory.json`, which lies in a different folder than the script. 

Created the folder `inventory_change` and the scripts: `restock_item.py`, `item_registration.py` and `item_withdrawal.py`.

- `restock_item.py`: look up an item and add to the quantity. 
- `item_withdrawal.py`: look up an item and reduce the quantity.
- `item_registration.py`: add a completely new component. 


Restructuring of the project ("Refactoring")  
- Realized that having separate files for each action (`item_withdrawal.py`, `restock_item.py`) became messy and led to a lot of duplicated code.
- Created the folder `src_learning` to collect the code in a more structured way.
- Split the code into two main parts (modularization):
  - `inventory_service.py`: a "backend" file that contains all the functions (logic) for talking to the "database" (`get_inventory`, `save_inventory`, `search_item`, `new_item`, `change_stock`, `update_item`). This file has no `input()` or `print()`, it only handles data.
  - `my_app.py`: a "frontend" file (CLI / simple UI) that controls the menu and communicates with the user. This imports the functions from `inventory_service.py`. 

Prototyping of GUI (Graphical User Interface)  
- Wanted to explore the possibilities for a visual program rather than a text-based terminal.  
- Created `my_app.py` in `src_learning` as a Tkinter-based GUI that uses `inventory_service.py`.
- **Note:** Parts of this file are generated with the help of AI to demonstrate the potential of the `tkinter` library.
  - **Purpose:** To have a working prototype ("Gold Standard") to navigate by.
  - **Learning point:** Discovered that GUI programming requires a different mindset ("event-driven") than the linear scripts written earlier. The program waits for events (clicks) instead of running from top to bottom.
- The program works and uses the same logic from `inventory_service.py`, but the code is currently too complex to be used as direct learning material. 

Plan going forward:  
- Use `inventory_service.py` as the foundation for further development.  
- Create small, isolated GUI scripts (e.g. `my_gui_start.py`) to learn `tkinter` from scratch, step-by-step, instead of copying large, generated code blocks.
