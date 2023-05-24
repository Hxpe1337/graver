import os
import importlib.util
from shutil import get_terminal_size
from termcolor import colored


def load_modules(path):
    modules = []
    for filename in os.listdir(path):
        if filename.endswith('.py'):
            spec = importlib.util.spec_from_file_location(filename[:-3], os.path.join(path, filename))
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            modules.append(module)
    return modules

def print_centered_text(text):
    terminal_width = get_terminal_size().columns
    colors = ['red', 'light_red']  # Different shades of purple
    for i, line in enumerate(text.splitlines()):
        print(colored(line.center(terminal_width), colors[i%len(colors)]))

def print_menu(modules):
    terminal_width = get_terminal_size().columns
    width = terminal_width // 3
    divider_line = colored(' ' * terminal_width, 'white')

    for i in range(0, len(modules), 3):
        print(divider_line)
        for j in range(3):
            index = i + j
            if index < len(modules):
                num_str = colored(f'[{index + 1}]', 'white')
                name_str = colored(f'{modules[index].__name__}', 'red')
                print(num_str.ljust(width // 4) + name_str.center(width // 2), end='')
        print()
    print(divider_line)





def main():
    while True:
        # Clear screen
        if os.name == 'nt':
            os.system('cls')
        else:
            os.system('clear')

        # Load ASCII logo
        with open('graver.txt', 'r', encoding='utf-8') as file:
            logo = file.read()

        # Load modules
        modules = load_modules('modules')

        # Print ASCII logo centered
        print_centered_text(logo)

        # Print menu
        print_menu(modules)

        # Wait for user input
        choice = input(colored("\n\n\n[GRAVER?] ", 'white'))
        if choice == 'q':
            break
        else:
            index = int(choice) - 1
            if 0 <= index < len(modules):
                os.system('cls')
                print_centered_text(logo)
                modules[index].run()
                os.system('title ' + modules[index].__name__)
if __name__ == '__main__':
    main()
