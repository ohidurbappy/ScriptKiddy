from PIL import Image
import os

def resize_image(input_path, output_path, max_width, max_height):
    # Open the image using Pillow
    print("Resizing {0} and saving it to {1}".format(input_path, output_path))
    image = Image.open(input_path)

    # Get the current dimensions of the image
    width, height = image.size

    # Calculate the new dimensions while maintaining the aspect ratio
    if width > max_width or height > max_height:
        aspect_ratio = width / height
        if width > height:
            new_width = max_width
            new_height = int(max_width / aspect_ratio)
        else:
            new_height = max_height
            new_width = int(max_height * aspect_ratio)
    else:
        # If the image is smaller than the max dimensions, keep it as is
        new_width = width
        new_height = height

    # Resize the image
    resized_image = image.resize((new_width, new_height))

    # Save the resized image to the output path
    resized_image.save(output_path,optimize=True,quality=80)

def convert_and_resize_images(input_folder, output_folder, max_width, max_height):
    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Loop through all files in the input folder
    for filename in os.listdir(input_folder):
        if filename.endswith(".jpg") or filename.endswith(".png"):
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, filename)
            # Resize and save the image
            resize_image(input_path, output_path, max_width, max_height)

            # check if it's a folder then call the function recursively
        elif os.path.isdir(os.path.join(input_folder, filename)):
            new_input_folder = os.path.join(input_folder, filename)
            new_output_folder = os.path.join(output_folder, filename)
            convert_and_resize_images(new_input_folder, new_output_folder, max_width, max_height)

if __name__ == "__main__":
    current_dir = os.getcwd()
    input_folder = os.path.join(current_dir, "images")
    output_folder = os.path.join(current_dir, "resized_images")
    max_width = 1008  # Replace with your desired max width
    max_height = 800  # Replace with your desired max height

    convert_and_resize_images(input_folder, output_folder, max_width, max_height)
