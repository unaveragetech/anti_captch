import os
import pytesseract
from PIL import Image
import time

# Function to display menu and let the user choose a CAPTCHA file
def select_captcha(directory):
    files = [f for f in os.listdir(directory) if f.endswith('.png')]
    
    if not files:
        print("No CAPTCHA images found in the directory.")
        return None
    
    print("Select a CAPTCHA to solve:")
    for i, file in enumerate(files):
        print(f"{i + 1}. {file}")

    choice = input("Enter the number corresponding to the CAPTCHA: ")

    try:
        choice_index = int(choice) - 1
        if 0 <= choice_index < len(files):
            return os.path.join(directory, files[choice_index])
        else:
            print("Invalid choice.")
            return None
    except ValueError:
        print("Invalid input. Please enter a number.")
        return None


# Function to solve a CAPTCHA using pytesseract and print details
def solve_captcha(image_path):
    print(f"Loading CAPTCHA image from: {image_path}")
    captcha_image = Image.open(image_path)

    # Display the CAPTCHA image to the user
    captcha_image.show()

    print("Attempting to solve the CAPTCHA...")
    time.sleep(1)

    # Convert image to grayscale
    print("Converting image to grayscale for better OCR recognition.")
    captcha_image = captcha_image.convert('L')  # Convert to grayscale
    captcha_image.show()

    # Optionally, apply thresholding for better OCR accuracy
    print("Applying thresholding to binarize the image.")
    captcha_image = captcha_image.point(lambda p: p > 128 and 255)
    captcha_image.show()

    # Run the image through pytesseract to get the CAPTCHA text
    print("Sending image to pytesseract for OCR processing...")
    time.sleep(1)
    captcha_text = pytesseract.image_to_string(captcha_image, config='--psm 6')

    print(f"CAPTCHA Solution Attempt: {captcha_text.strip()}")

    return captcha_text.strip()


# Main function to handle menu and solving process
def main():
    # Specify the directory where CAPTCHA images are stored
    captcha_dir = 'captcha_tests'

    # Prompt the user to select a CAPTCHA
    captcha_file = select_captcha(captcha_dir)
    
    if captcha_file:
        # Solve the CAPTCHA and show process details
        captcha_solution = solve_captcha(captcha_file)
        print("\nFinal CAPTCHA Solution:", captcha_solution)
    else:
        print("No CAPTCHA selected or found.")


if __name__ == "__main__":
    main()
