#!/Users/pranav.sharma/Documents/MLprojects/explore-etoro-signals/.conda/env/bin/python

from PIL import Image, ImageDraw, ImageFont
import os

# Sample tile definitions. Each tile has:
#   "x", "y": the top-left corner where the tile should be placed
#   "width", "height": the tile's size
#   "type": either "image" or "text"
#   "content": path to an image file (if type="image") or the text to display (if type="text")
#   "font_size": (optional) font size for text tiles
#   "bg_color": (optional) background color for text tile
# You can add other parameters as needed (like text color, alignment, etc.).
tiles = [
    {
        "x": 20, "y": 20,
        "width": 300, "height": 200,
        "type": "image",
        "content": "image_files/cpp-logo.png"
    },
    {
        "x": 340, "y": 20,
        "width": 200, "height": 200,
        "type": "image",
        "content": "image_files/saa-logo.png"
    },
    {
        "x": 560, "y": 20,
        "width": 200, "height": 100,
        "type": "text",
        "content": "Live Stickers",
        "font_size": 32,
        "bg_color": (252, 234, 197, 128)
    },
    {
        "x": 560, "y": 140,
        "width": 200, "height": 80,
        "type": "text",
        "content": "iOS 17",
        "font_size": 40,
        "bg_color": (252, 234, 197, 128)
    },
    {
        "x": 540, "y": 240,
        "width": 220, "height": 150,
        "type": "text",
        "content": "This is a larger text block.\nWe can have multiple lines.",
        "font_size": 24,
        "bg_color": (252, 234, 197, 128)
    }
]

def create_collage_with_background(
    background_file="image_files/base.jpg",  # path to your background image
    output_path="image_files/collage_output.png"
):
    # Open your background image and convert to RGBA for transparency support.
    if not os.path.isfile(background_file):
        raise FileNotFoundError(f"Background image '{background_file}' not found.")
    
    collage = Image.open(background_file).convert("RGBA")
    canvas_width, canvas_height = collage.size

    draw = ImageDraw.Draw(collage)
    """
    Create a collage-like image with multiple tiles of images or text.
    """

    draw = ImageDraw.Draw(collage)

    # Load a default font or specify a TTF path
    # On many systems, you might have something like "/usr/share/fonts/.../DejaVuSans.ttf"
    # or on Windows "C:/Windows/Fonts/Arial.ttf"
    # For demonstration, we'll just try a basic PIL font if no TTF is available.
    default_font = ImageFont.load_default()

    for tile in tiles:
        x = tile["x"]
        y = tile["y"]
        w = tile["width"]
        h = tile["height"]
        tile_type = tile["type"]
        content = tile["content"]

        # Draw a rectangle around the tile if you want a border (optional)
        # draw.rectangle([x, y, x+w, y+h], outline="black")

        if tile_type == "image":
            # Open the image
            if not os.path.isfile(content):
                print(f"Warning: image file {content} not found. Skipping.")
                continue
            img = Image.open(content).convert("RGBA")
            # Rescale to fit the tile while preserving aspect ratio
            img_w, img_h = img.size
            scale_factor = min(w / img_w, h / img_h)
            new_size = (int(img_w * scale_factor), int(img_h * scale_factor))
            img = img.resize(new_size, Image.LANCZOS)

            # Compute top-left coords to center the image in the tile
            paste_x = x + (w - new_size[0]) // 2
            paste_y = y + (h - new_size[1]) // 2

            # Paste the image
            collage.paste(img, (paste_x, paste_y), img)

        elif tile_type == "text":
            # Optionally fill a background for the text tile
            bg_color = tile.get("bg_color")
            if bg_color:
                draw.rectangle([x, y, x + w, y + h], fill=bg_color)

            # Get the font size if specified, else default
            font_size = tile.get("font_size", 20)
            # For a better result, use a TTF font if available:
            # font = ImageFont.truetype("path/to/font.ttf", font_size)
            font = ImageFont.load_default()

            # Measure the text to center it in the tile using textbbox.
            lines = content.split("\n")
            line_heights = []
            max_line_width = 0
            for line in lines:
                bbox = draw.textbbox((0, 0), line, font=font)
                line_width = bbox[2] - bbox[0]
                line_height = bbox[3] - bbox[1]
                line_heights.append(line_height)
                if line_width > max_line_width:
                    max_line_width = line_width
            total_text_height = sum(line_heights)

            # Compute starting coords so that the text is centered in the tile.
            text_x = x + (w - max_line_width) // 2
            text_y = y + (h - total_text_height) // 2

            # Draw each line.
            for line_height, line in zip(line_heights, lines):
                draw.text((text_x, text_y), line, fill="black", font=font)
                text_y += line_height

        else:
            print(f"Warning: Unknown tile type '{tile_type}'")

    # Save the final collage
    collage.save(output_path)
    print(f"Collage saved to {output_path}")

if __name__ == "__main__":
    create_collage_with_background()
