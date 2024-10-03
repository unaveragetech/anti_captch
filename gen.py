import os
import argparse
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import random


# Function to generate a single distorted CAPTCHA with styles
def generate_captcha(width, height, length, output_dir, file_num, style, bg_color, text_color, font_size, blur_level):
    characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    captcha_text = ''.join(random.choice(characters) for _ in range(length))

    # Create an image with a customizable background color
    image = Image.new('RGB', (width, height), color=bg_color)
    font = ImageFont.truetype('arial.ttf', size=font_size)

    draw = ImageDraw.Draw(image)

    # Apply random rotation and distortion to each character
    for i, char in enumerate(captcha_text):
        char_image = Image.new('RGBA', (50, 50), (255, 255, 255, 0))
        char_draw = ImageDraw.Draw(char_image)
        char_draw.text((10, 10), char, text_color, font=font)

        # Apply random rotation
        char_image = char_image.rotate(random.randint(-30, 30), expand=1)

        # Apply random distortion based on the chosen style
        if style == "simple":
            distorted_image = char_image
        elif style == "noise":
            distorted_image = add_noise(char_image)
        elif style == "lines":
            distorted_image = add_random_lines(char_image)
        else:
            distorted_image = char_image

        # Paste the distorted image into the main captcha image
        image.paste(distorted_image, (i * 40 + 10, 10), distorted_image)

    # Apply Gaussian blur if specified
    image = image.filter(ImageFilter.GaussianBlur(radius=blur_level))

    # Save the image in the output directory
    image_path = os.path.join(output_dir, f'captcha_{file_num}.png')
    image.save(image_path)


# Function to add random noise to the captcha
def add_noise(image):
    noise_image = Image.new('RGBA', image.size)
    for x in range(image.width):
        for y in range(image.height):
            if random.random() > 0.9:  # Adjust noise probability
                noise_image.putpixel((x, y), (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), 255))
            else:
                noise_image.putpixel((x, y), image.getpixel((x, y)))
    return noise_image


# Function to add random lines to the captcha
def add_random_lines(image):
    draw = ImageDraw.Draw(image)
    for _ in range(10):  # Number of random lines
        x1 = random.randint(0, image.width)
        y1 = random.randint(0, image.height)
        x2 = random.randint(0, image.width)
        y2 = random.randint(0, image.height)
        draw.line([(x1, y1), (x2, y2)], fill=(0, 0, 0), width=2)
    return image


# CLI tool function to create captchas with various styles
def create_captchas(amount, width, height, length, output_dir, style, bg_color, text_color, font_size, blur_level):
    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Generate the specified number of captchas
    for i in range(amount):
        generate_captcha(width, height, length, output_dir, i, style, bg_color, text_color, font_size, blur_level)

    print(f"{amount} captchas saved to {output_dir}")


# Function to display a menu for selecting captcha styles
def select_style():
    print("Select Captcha Style:")
    print("1. Simple (No distortion)")
    print("2. Noise (Random pixel noise)")
    print("3. Lines (Random lines across characters)")
    print("4. Custom Colors (Choose your own background and text colors)")

    choice = input("Enter the number for the captcha style you want: ")

    if choice == '1':
        return 'simple'
    elif choice == '2':
        return 'noise'
    elif choice == '3':
        return 'lines'
    elif choice == '4':
        return 'custom_colors'
    else:
        print("Invalid choice, defaulting to Simple.")
        return 'simple'


# CLI argument parsing
def main():
    parser = argparse.ArgumentParser(description="Generate distorted CAPTCHA images with various styles.")
    parser.add_argument('--amount', type=int, default=5, help="Number of captchas to generate")
    parser.add_argument('--width', type=int, default=300, help="Width of the captcha images")
    parser.add_argument('--height', type=int, default=100, help="Height of the captcha images")
    parser.add_argument('--length', type=int, default=6, help="Number of characters in each captcha")
    parser.add_argument('--output', type=str, default='captcha_tests', help="Directory to save the captchas")
    parser.add_argument('--font_size', type=int, default=40, help="Font size of the captcha text")
    parser.add_argument('--blur_level', type=float, default=1, help="Level of Gaussian blur to apply")

    # Prompt user for captcha style
    style = select_style()

    # If the user chooses custom colors, prompt for color inputs
    if style == 'custom_colors':
        bg_color = tuple(map(int, input("Enter background color as R,G,B (e.g., 255,255,255): ").split(',')))
        text_color = tuple(map(int, input("Enter text color as R,G,B (e.g., 0,0,0): ").split(',')))
    else:
        bg_color = (255, 255, 255)
        text_color = (0, 0, 0)

    args = parser.parse_args()

    # Call the function to create captchas
    create_captchas(args.amount, args.width, args.height, args.length, args.output, style, bg_color, text_color, args.font_size, args.blur_level)


if __name__ == "__main__":
    main()
