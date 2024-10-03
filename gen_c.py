import random

def generate_commands(num_commands):
    styles = ['simple', 'noise', 'lines']
    commands = []

    for _ in range(num_commands):
        amount = random.randint(1, 20)  # Random amount between 1 and 20
        width = random.randint(200, 600)  # Random width between 200 and 600
        height = random.randint(100, 300)  # Random height between 100 and 300
        length = random.randint(4, 8)  # Random length between 4 and 8 characters
        output_dir = 'captcha_tests'
        font_size = random.randint(30, 60)  # Random font size between 30 and 60
        blur_level = random.uniform(0, 5)  # Random blur level between 0 and 5

        style = random.choice(styles)

        command = (
            f"python gen.py --amount {amount} --width {width} --height {height} "
            f"--length {length} --output {output_dir} --font_size {font_size} "
            f"--blur_level {blur_level:.1f} --style {style}"
        )
        commands.append(command)

    return commands


def save_commands_to_file(commands, filename):
    with open(filename, 'w') as file:
        for command in commands:
            file.write(command + '\n')
    print(f"Commands saved to {filename}")


def main():
    # Define the number of random commands to generate
    num_commands = 10  # Change this to generate more or fewer commands

    # Generate commands
    commands = generate_commands(num_commands)

    # Save the commands to a file
    save_commands_to_file(commands, 'random_captcha_commands.txt')


if __name__ == "__main__":
    main()
