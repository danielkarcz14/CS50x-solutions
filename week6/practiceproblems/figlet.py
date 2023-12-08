import sys
from pyfiglet import Figlet
import random


def main():
    # handle invalid usage
    if len(sys.argv) == 2 or len(sys.argv) > 3:
        sys.exit("Invalid usage")
    # use modul
    figlet = Figlet()
    fonts = figlet.getFonts()

    random = random_change(figlet, fonts)
    custom = custom_change(figlet, fonts)
    # random change
    if random:
        print(random)
    # custom change
    else:
        print(custom)


def custom_change(figlet, fonts):
    if len(sys.argv) == 3 and (sys.argv[1] == '-f' or sys.argv[2] == '--font'):
        if sys.argv[2] in fonts:
            text = input("Input: ")
            figlet.setFont(font=sys.argv[2])
            return figlet.renderText(text)
    sys.exit("Invalid usage")

def random_change(figlet, fonts):
    if len(sys.argv) == 1:
        text = input("Input: ")
        figlet.setFont(font=random.choice(fonts))
        return figlet.renderText(text)

main()


