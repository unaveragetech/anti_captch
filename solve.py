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
    print(f"\n=== Solving CAPTCHA: {image_path} ===\n")

    # Open and display the CAPTCHA image
    captcha_image = Image.open(image_path)
    captcha_image.show()

    # Convert image to grayscale for better OCR recognition
    print("Converting image to grayscale for better OCR recognition.")
    captcha_image = captcha_image.convert('L')  # Convert to grayscale
    captcha_image.show()

    # Apply thresholding (binarization)
    print("Applying thresholding to binarize the image.")
    captcha_image = captcha_image.point(lambda p: p > 128 and 255)
    captcha_image.show()

    # Run the image through pytesseract to extract text
    print("Sending image to pytesseract for OCR processing...")
    time.sleep(1)
    captcha_text = pytesseract.image_to_string(captcha_image, config='--psm 6')

    # Clean the text result
    captcha_solution = captcha_text.strip()

    print(f"\nBest guess for the CAPTCHA: '{captcha_solution}'")

    return captcha_solution


# Main function to handle menu, solving process, and results display
def main():
    # Specify the directory where CAPTCHA images are stored
    captcha_dir = 'captcha_tests'

    # Prompt the user to select a CAPTCHA
    captcha_file = select_captcha(captcha_dir)
    
    if captcha_file:
        # Solve the CAPTCHA and show process details
        captcha_solution = solve_captcha(captcha_file)

        # Display the final result in a formatted output
        print("\n====================================")
        print(f"File: {captcha_file}")
        print(f"Result: {captcha_solution}")
        print("====================================\n")
    else:
        print("No CAPTCHA selected or found.")


if __name__ == "__main__":
    main()
