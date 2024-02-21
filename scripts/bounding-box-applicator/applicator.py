import os
import re
import json
from PIL import Image, ImageDraw


# Returns None if path did not exist and creates it, otherwise returns the list of paths in the directory that are images.
def find_images_in_directory(path: str) -> list[str] | None:
    if os.path.exists(path):
        dir_list = os.listdir(path)

        image_list: list[str] = []
        for file in dir_list:
            # Search for supported file types (PIL Image).
            is_image = re.search(r'^.*\.(png|jpe?g|ppm|gif|tiff|bmp)$', file)

            # File is an image; add path to valid list.
            if is_image:
                image_list.append(file)

        # No images found - still return None!
        if len(image_list) == 0:
            return None

        return image_list

    # Directory does not exist; create it!
    os.mkdir(path)
    print(f'Created "{path}" since it did not exist previously.')


def pair_images_with_json_data(image_paths: list[str]) -> list[tuple[str]]:
    pairs: list[tuple[str]] = []

    for image_file_name in image_paths:
        json_file_name = image_file_name.split('.')[0] + ".json"

        json_file_path = os.path.join(INPUT_IMAGES_PATH, json_file_name)
        image_file_path = os.path.join(INPUT_IMAGES_PATH, image_file_name)

        if os.path.exists(image_file_path) and os.path.exists(json_file_path):
            pair: tuple[str] = (image_file_path, json_file_path)
            pairs.append(pair)

    return pairs


def find_extreme_points(screen_space_data: dict) -> tuple[float]:
    min_x = float('inf')
    max_x = float('-inf')
    min_y = float('inf')
    max_y = float('-inf')

    for point in screen_space_data:
        x = point['position']['x']
        y = point['position']['y']

        min_x = min(min_x, x)
        max_x = max(max_x, x)
        min_y = min(min_y, y)
        max_y = max(max_y, y)

    return (min_x, min_y, max_x, max_y)


# Essential directories that will be required throughout the script.
CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))
BASE_PATH = os.path.join(CURRENT_PATH, '..', '..')
INPUT_IMAGES_PATH = os.path.join(BASE_PATH, 'images', 'input')
OUTPUT_IMAGES_PATH = os.path.join(BASE_PATH, 'images', 'output')


# Find any images in the input directory - return their file names in a list if so.
input_images = find_images_in_directory(INPUT_IMAGES_PATH)

# ...otherwise, exit.
if not input_images:
    print(
        f'There were no images found in "{INPUT_IMAGES_PATH}" - there must be some to carry on execution. Please place at least 1 image (PNG, JP(E)G, PPM, GIF, TIFF, or BMP) here to continue.')
    exit(1)

# Ensure output directory is present:
if not os.path.exists(OUTPUT_IMAGES_PATH):
    os.mkdir(OUTPUT_IMAGES_PATH)


# Attempt to pair images up with their screen space data (JSON) counterparts:
image_json_pairs = pair_images_with_json_data(input_images)


for files in image_json_pairs:  # 'files' => (img, json)
    image = Image.open(files[0])

    with open(files[1]) as json_file:
        space_data = json.load(json_file)

        # Accounts for scale options from aidanjuma.live, from JSON export.
        expected_canvas_size = space_data['canvasSize']

        expected_dimensions = (
            expected_canvas_size['x'], expected_canvas_size['y'])

        # If dimensions are mismatched, skip image.
        if image.size != expected_dimensions:
            print(
                f'There are mismatched dimensions between "{files[0]}" and "{files[1]}" - skipping...')
            image.close()
            continue

        # Extract screen space data from the JSON, and then find the extreme points of the object.
        screen_space_data = space_data['space']['screenSpace']
        extreme_points: tuple[float] = find_extreme_points(screen_space_data)

        # Draw object recognition rectangle.
        draw = ImageDraw.Draw(image)
        draw.rectangle(extreme_points, outline="red")
        del draw

        # Save to output directory!
        image_file_name = files[0].split(os.sep)[-1]
        output_image = os.path.join(OUTPUT_IMAGES_PATH, image_file_name)
        image.save(output_image)

    image.close()
