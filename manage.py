import os
import sys
import webbrowser
from threading import Timer

# Flag to track if the browser has been opened
browser_opened = False

def open_browser():
    """
    Function to open the browser to the login page.
    """
    global browser_opened
    if not browser_opened:
        webbrowser.open('http://127.0.0.1:8000/login')
        browser_opened = True

def main():
    """
    Main function to start the Django server and open the browser once
    when the server starts, not during any autoreloader subprocesses.
    """
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Project1.settings')

    # Only start the browser if this is the main server process
    if os.environ.get('RUN_MAIN') == 'true':
        # Open the browser after a short delay
        Timer(1, open_browser).start()

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()