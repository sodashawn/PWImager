import re
from colorthief import ColorThief
from PIL import Image
from math import sqrt
import glob
import os


class imagify:
    def __init__(self):
        self.image = Image.open("resources/mallard.jpg").convert('RGBA')
        self.width = 80
        self.height = 57
        self.method = "Average"
        self.loadedblocks = self.load_blocks("resources/All/*")
        self.usedblocks = []
        self.output_image = Image.open("resources/mallard.jpg").convert('RGBA')
        self.output_ingridients = ""

    def preset_block_list(self, preset):
        preset_list = []
        blocks_paths_list = glob.glob(f"resources/{preset}/*") if preset != "Custom" else []
        blocks_list = [re.sub(r"(\w)([A-Z])", r"\1 \2", os.path.basename(entry).replace(".png", "")) for entry in blocks_paths_list]
        for block_loaded in self.loadedblocks:
            if block_loaded['name'] in blocks_list:
                block_loaded['bool'] = True
            else:
                block_loaded['bool'] = False
            preset_list.append(block_loaded)
        return preset_list


    def set_used_block_list(self,used_blocks_names):
        used_blocks = []
        for block in self.loadedblocks:
            if block['name'] in used_blocks_names:
                used_blocks.append(block)
        self.usedblocks = used_blocks


    def save_image(self, path):
        if path == "":
            return
        print("check1")
        im = self.output_image
        print("check2")
        im.save(path, format="PNG")
        print('image saved')

    def save_text(self, path):
        if path == "":
            return
        with open(path, "w") as f:
            f.write(self.output_ingridients)


    def set_image(self, path):

        self.image = Image.open(path).convert('RGBA')
        return self.image

    def load_blocks(self, path):
        if self.method == "Average":
            all_blocks = []
            for entry in glob.glob(path):
                entry_path = entry
                entry_data = Image.open(entry_path).convert('RGBA')
                entry_color = self.method_average(entry_data)
                entry_name = re.sub(r"(\w)([A-Z])", r"\1 \2", os.path.basename(entry_path).replace(".png", ""))
                all_blocks.append({"data": entry_data, "path": entry_path, "name": entry_name, "color": entry_color})
            self.loadedblocks = all_blocks
        else:
            all_blocks = []
            for entry in glob.glob(path):
                entry_path = entry
                entry_data = Image.open(entry_path).convert('RGBA')
                try:
                    entry_color = self.method_dominant(entry_path)
                except:
                    entry_color = self.method_average(entry_data)
                entry_name = re.sub(r"(\w)([A-Z])", r"\1 \2", os.path.basename(entry_path).replace(".png", ""))
                all_blocks.append({"data": entry_data, "path": entry_path, "name": entry_name, "color": entry_color})
            self.loadedblocks = all_blocks
        return all_blocks

    def method_average(self, block_data):
        return block_data.resize((1, 1)).getpixel((0, 0))

    def method_dominant(self, block_path):
        return ColorThief(block_path).get_color(quality=1)

    def get_blocks(self):
        pass

    def calculate_RGBA_difference(self, palette, rgba_tuple):
        r, g, b, a = rgba_tuple
        color_diffs = []
        for block in palette:
            cr, cg, cb, ca = block['color']
            color_diff = sqrt(abs(r - cr) ** 2 + abs(g - cg) ** 2 + abs(b - cb) ** 2)
            block_name = block['name']
            color_diffs.append({"difference": color_diff, "data": block['data'], 'name': block_name})
        close_block = min(color_diffs, key=lambda x: x['difference'])
        return close_block

    def convert(self):
        """Adjust input image to correct size"""
        used_block_list = {}
        im = self.image
        print((self.width, self.height))
        im.thumbnail((self.width, self.height))
        w, h = im.size
        used_blocks = self.usedblocks
        output_image = Image.new('RGBA', (w * 32, h * 32))  # Create output image
        print("convert check1")

        """Iterate over every single pixel and find
            Its pixelworlds block counterpart"""
        for x in range(w):
            for y in range(h):
                rgba = im.getpixel((x, y))
                if rgba != (0,0,0,0):
                    closest_block = self.calculate_RGBA_difference(used_blocks, rgba)
                    output_image.paste(closest_block['data'], (x*32,y*32))
                    used_block_list[closest_block['name']] = used_block_list[closest_block['name']] + 1 if closest_block['name'] in used_block_list.keys() else 1


        print("done with conversion")
        output_image.save("resources/Output.png", format="PNG")

        #image with watermark
        print('conversion check 1')
        fixed_height = output_image.height // 20 if (output_image.height // 20) > 32 else 32
        watermarkbar = Image.new('RGBA', (w * 32, fixed_height), color=(80, 80, 80))
        watermarkimage = Image.open('resources/watermark.png')

        height_percent = (fixed_height / float(watermarkimage.size[1]))
        width_size = int((float(watermarkimage.size[0]) * float(height_percent)))
        watermarkimage = watermarkimage.resize((width_size, fixed_height), Image.NEAREST)
        watermarkbar.paste(watermarkimage,(0,0))
        print('conversion check 2')
        wateredimage = Image.new('RGBA', (w * 32, (h * 32) + (output_image.height // 20)))
        print('conversion check 3')
        wateredimage.paste(output_image, (0,0), output_image)
        print('conversion check 4')
        wateredimage.paste(watermarkbar, (0,h * 32))
        print('conversion check 5')
        self.output_image = wateredimage
        print('conversion check 6')

        self.output_ingridients = "# Thanks for Using PW Imager\n" \
                                  "# Created by Parmashawn \n" \
                                  "# visit https://sodashawn.github.io/ \n" \
                                  "# For more creations! \n" \
                                  "# Enjoy your pixel art!\n" \
                                  "####################################\n\n"

        for block in used_block_list.keys():
            self.output_ingridients += f"x{used_block_list[block]} - {block}\n"



