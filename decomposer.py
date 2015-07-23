import argparse
import os
import re
import xml.etree.ElementTree as ET

from PIL import Image


def cli():
    parser = argparse.ArgumentParser(description='Utility for decomposing a sprite sheet into individual images.')

    parser.add_argument('-x',
                        dest='xml_file',
                        required=True,
                        help='XML file describing the images in the sprite sheet')

    parser.add_argument('-i',
                        dest='image_file',
                        required=True,
                        help='Sprite sheet image file')

    parser.add_argument('-o',
                        dest='output_directory',
                        required=True,
                        help='Directory to save the individual sprites')

    args = parser.parse_args()

    tree = ET.parse(args.xml_file)
    sprite_sheet = Image.open(args.image_file)

    texture_rect = None
    sprite_name = None
    is_texture_rect = False

    for e in tree.iter():
        print e.tag, e.attrib, e.text
        if e.text:
            if is_texture_rect:
                is_texture_rect = False
                match = re.search(r'\{\{(\d+), (\d+)\}, \{(\d+), (\d+)\}\}', e.text)
                if match and len(match.groups()) == 4:
                    x = int(match.group(1))
                    y = int(match.group(2))
                    w = int(match.group(3))
                    h = int(match.group(4))
                    texture_rect = (x, y, x + w, y + h)
            elif e.text == 'textureRect':
                is_texture_rect = True
            elif e.text.endswith('.png'):
                sprite_name = e.text

            if texture_rect and sprite_name:
                sprite = sprite_sheet.crop(texture_rect)
                sprite.save(os.path.join(args.output_directory, sprite_name))
                texture_rect = None
                sprite_name = None


if __name__ == "__main__":
    cli()
