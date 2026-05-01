from pathlib import Path
import os

os.chdir(Path(__file__).parent)

from ui import main_menu


if __name__ == "__main__":
    main_menu()
