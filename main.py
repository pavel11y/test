from src.library import Library
from src.storage import Storage
from src.gui import LibraryGUI

def main():
    storage = Storage()
    library = Library(storage)
    app = LibraryGUI(library)
    app.run()

if __name__ == "__main__":
    main()