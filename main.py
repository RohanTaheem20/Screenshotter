from utils import *

DELAY = 0.48

def main():
    try:
        # Create output directories
        output_dir, images_dir = create_output_directories()

        num_pages = get_positive_integer_input('How many pages are there? ')
        pdf_filename = get_pdf_filename(output_dir)
        start_x, start_y, end_x, end_y, n_button_x, n_button_y = get_coordinates()

        image_files = []

     # Take screenshots and cut them in half
        for i in range(1, num_pages + 1):
            img_filename = take_screenshot(i, start_x, start_y, end_x, end_y, images_dir)
            image_files.extend(cut_image_in_half(img_filename, images_dir))

            click_next_button(n_button_x, n_button_y)

        convert_images_to_pdf(image_files, pdf_filename)
        delete_images(image_files)

    except Exception as e:
        # Handle any exceptions that occur
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
    print('Completed! Check the output folder for the PDF file.')