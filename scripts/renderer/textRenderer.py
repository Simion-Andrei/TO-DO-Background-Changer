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
        
        # Image size
        height = image.get_height()
        width = image.get_width()

        #Layout calculations
        num_cols = 3
        margin_x = int(width * 0.01)
        margin_y = int(height * 0.05)
        column_width = (width - (2 * margin_x)) // num_cols
        column_centers = [margin_x + (column_width // 2) + (column_width * i) for i in range(num_cols)]

        #Style settings
        line_spacing = 20
        text_color = [(173, 0, 0), (255, 230, 0), (34, 255, 0)]
        shadow_color = (0, 0, 0)
        header_color = (255, 255, 255)

        #Font
        try:
            font = ImageFont.truetype("arial.ttf", int(height * 0.02))
        except IOError:
            font = ImageFont.load_default()

        for col_idx, (category, events) in enumerate(zip(["TODAY", "THIS WEEK", "NOT SO SOON"], categorized_events)):
            x = column_centers[col_idx]
            y = margin_y

            #Draw category header
            header_text = category
            bbox = draw.textbbox((x, y), header_text, font=font, anchor="ma")
            draw.text((x+2, y+2), header_text, font=font, fill=shadow_color, anchor="ma")
            draw.text((x, y), header_text, font=font, fill=header_color, anchor="ma")
            y += font.size + line_spacing

            #Draw events in category
            for i, event in enumerate(events, 1):
                event_text = f"{i}.{event.get_name()}"
                text_width = draw.textlength(event_text, font=font)

                draw.text((x+2, y+2), event_text, font=font, fill=shadow_color, anchor="ma")
                draw.text((x, y), event_text, font=font, fill=text_color[col_idx], anchor="ma")
                y += font.size + line_spacing
            
        # Save modified image
        base, ext = os.path.splitext(path)
        output_path = f"{base}{output_suffix}{ext}"
        img.save(output_path)
        return output_path