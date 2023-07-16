"""
used for coloring the text sent to the client
"""
class ColorText:
    COLOR_CODES = {
        "red": '\033[91m',
        "green": '\033[92m',
        "yellow": '\033[93m',
        "blue": '\033[94m',
        "magenta": '\033[95m',
        "cyan": '\033[96m',
        "white": '\033[97m',
        "reset": '\033[0m'
    }

    @staticmethod
    def colorize(text, color):
        return ColorText.COLOR_CODES[color] + text + ColorText.COLOR_CODES["reset"]
