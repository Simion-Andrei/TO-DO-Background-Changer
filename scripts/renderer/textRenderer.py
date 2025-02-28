from PIL import Image, ImageDraw, ImageFont
import os

class TextRenderer:
    def __init__(self):
        pass

    def add_text_to_wallpaper(self, image, path, categorized_events, output_suffix="with_text"):
        '''
        Function that adds events (text) over the background image
        
        Args:
            image (Wallpaper object): The wallpaper object that will be modified
            path (string): The path of the image that will be modified
            categorized_events (list): A list made of 3 lists, each one containing events categorized by their remaining days
            output_suffix (string): The ending name of the file (defaulted to "with_text")
        
        Raises:
            EventsRepoError: If the events list is empty

        Returns:
            (string): The output path of the new file
        '''

        img = Image.open(path)
        draw = ImageDraw.Draw(img)
        
        # Text positioning
        height = image.get_height()
        width = image.get_width()

        num_cols = 3
        margin_x = 0.03
        margin_y = 0.05

        x = int(width * margin_x)
        category_spacing = (width - 2 * x) // 2 - int(width * 0.04)
        y = int(height * margin_y)
        line_spacing = 20
        text_color = [(173, 0, 0), (255, 230, 0), (34, 255, 0)]  # Red, Yellow, Green
        shadow_color = (0, 0, 0)      # Black

        #Font settings
        try:
            font = ImageFont.truetype("arial.ttf", height*0.02)
        except:
            font = ImageFont.load_default()

        for idx, category in enumerate(categorized_events):
            if idx == 0: text = "TODAY"
            elif idx == 1: text = "THIS WEEK"
            else: text = "NOT SO SOON"

            # Add text shadow
            draw.text((x+2, y+2), text, font=font, fill=shadow_color, align="center")
            # Add main text
            draw.text((x, y), text, font=font, fill=(255, 255, 255), align="center")

            y += font.size + line_spacing
            for i, el in enumerate(category, 1):
                text = f"{i}.{el.get_name()}"

                # Add text shadow
                draw.text((x+2, y+2), text, font=font, fill=shadow_color, align="center")
                # Add main text
                draw.text((x, y), text, font=font, fill=text_color[idx], align="center")

                y += font.size + line_spacing
            
            x += category_spacing
            y = int(height * 0.05)
            
        # Save modified image
        base, ext = os.path.splitext(path)
        output_path = f"{base}{output_suffix}{ext}"
        img.save(output_path)
        return output_path