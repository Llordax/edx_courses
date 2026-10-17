import os
import sys
from PIL import Image, ImageOps

def main():
    # Verify that the user provided exactly two command-line arguments (input image and output image)
    if len(sys.argv) < 3:
        sys.exit("Too few command-line arguments")
    elif len(sys.argv) > 3:
        sys.exit("Too many command-line arguments")

    # Extract the input and output image paths from the command-line arguments
    input_path = sys.argv[1]
    output_path = sys.argv[2]

    # Define a list of acceptable graphic file extensions
    valid_extensions = [".jpg", ".jpeg", ".png"]

    # Extract the file extension from the lowercase version of both paths using os.path.splitext
    _, input_ext = os.path.splitext(input_path.lower())
    _, output_ext = os.path.splitext(output_path.lower())

    # Validate that the source file has a supported extension format
    if input_ext not in valid_extensions:
        sys.exit("Invalid input")

    # Validate that the destination file has a supported extension format
    if output_ext not in valid_extensions:
        sys.exit("Invalid output")

    # Enforce that the output image must match the exact file format type of the input image
    if input_ext != output_ext:
        sys.exit("Input and output have different extensions")

    try:
        # Load the default overlay image ("shirt.png") and the user-specified source image
        shirt = Image.open("shirt.png")
        user_image = Image.open(input_path)
    # Gracefully catch errors if the user's input image file cannot be found on disk
    except FileNotFoundError:
        sys.exit("Input does not exist")

    # Crop and scale the user's image so it fits the precise pixel dimensions of the shirt image
    cropped_image = ImageOps.fit(user_image, shirt.size)
    
    # Overlay the shirt image onto the cropped background at position coordinates (0, 0)
    # The third argument 'shirt' acts as an alpha mask to preserve transparent areas of the PNG
    cropped_image.paste(shirt, (0, 0), shirt)
    
    # Save the composite final image layout to the specified output file path
    cropped_image.save(output_path)

if __name__ == "__main__":
    main()
