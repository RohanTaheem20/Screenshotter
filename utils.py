import os
import pyautogui
from PIL import Image
import img2pdf


def get_positive_integer_input(prompt: str) -> int:
    while True:
        try:
            value = int(input(prompt))
            if value <= 0:
                print("Please enter a positive integer.")
            else:
                return value
        except ValueError:
            print("Invalid input. Please enter an integer.")


def get_pdf_filename(output_dir: str) -> str:
    filename = input('What do you want the file to be called? ').strip()
    return os.path.join(output_dir, f"{filename}.pdf")


def get_coordinates() -> tuple:
    start_x, start_y = get_position('Capture starting coordinates')
    end_x, end_y = get_position('Capture ending coordinates')
    n_button_x, n_button_y = get_position('Capture next button coordinates')
    return start_x, start_y, end_x, end_y, n_button_x, n_button_y


def get_position(prompt: str) -> tuple:
    print(prompt)
    pyautogui.sleep(2)
    return pyautogui.position()


def take_screenshot(counter: int, start_x: int, start_y: int, end_x: int, end_y: int, images_dir: str) -> str:
    """
    Take screenshot.

    Args:
    counter (int): Screenshot counter.
    start_X (int): Starting X coordinate.
    start_Y (int): Starting Y coordinate.
    end_X (int): Ending X coordinate.
    endY (int): Ending Y coordinate.
    images_dir (str): Images directory.

    Returns:
    str: Screenshot filename.
    """
    region = (start_x, start_y, end_x - start_x, end_y - start_y)
    img = pyautogui.screenshot(region=region)
    filename = os.path.join(images_dir, f"page{counter}.png")
    img.save(filename)
    return filename


def click_next_button(n_button_x: int, n_button_y: int) -> None:
    pyautogui.moveTo(n_button_x, n_button_y)
    pyautogui.click()


def cut_image_in_half(filename: str, images_dir: str) -> list:
    with Image.open(filename) as img:
        width, height = img.size

        left_box = (0, 0, width // 2, height)
        right_box = (width // 2, 0, width, height)

        left_half = img.crop(left_box)
        right_half = img.crop(right_box)

        left_filename = f"left_{os.path.basename(filename)}"
        right_filename = f"right_{os.path.basename(filename)}"

        left_half.save(os.path.join(images_dir, left_filename))
        right_half.save(os.path.join(images_dir, right_filename))

        return [left_filename, right_filename]


def convert_images_to_pdf(image_files: list, pdf_filename: str) -> None:
    with open(pdf_filename, "wb") as f:
        f.write(img2pdf.convert([os.path.join("images", img) for img in image_files]))


def delete_images(image_files: list) -> None:
    for img in image_files:
        os.remove(os.path.join("images", img))


def create_output_directories() -> tuple:
    """
    Create output directories.

    Returns:
    tuple: Output directory and images directory.
    """
    output_dir = input("Enter the output directory (leave blank for default): ")

    if not output_dir:
        output_dir = "output"

    if not os.path.isabs(output_dir):
        output_dir = os.path.abspath(output_dir)

    try:
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
    except OSError as e:
        print(f"Error creating directory: {e}")
        return None, None

    images_dir = os.path.join(output_dir, "images")

    try:
        if not os.path.exists(images_dir):
            os.makedirs(images_dir)
    except OSError as e:
        print(f"Error creating directory: {e}")
        return None, None

    return output_dir, images_dir