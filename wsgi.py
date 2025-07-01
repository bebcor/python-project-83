import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent))

from page_analyzer.app import app

if __name__ == "__main__":
    app.run()


