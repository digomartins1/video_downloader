import sys
from src.cli.interface import CLIInterface

def main():
    try:
        app = CLIInterface()
        app.run()
    except KeyboardInterrupt:
        print("\n\nOperação cancelada pelo usuário.")
        sys.exit(0)

if __name__ == "__main__":
    main()