import os
import ctypes
import shutil
import datetime
from PIL import Image, ImageDraw, ImageFont

class Service:
    def __init__(self, validator, eventsRepo, wallpapersRepo, eventFactory, wallpaperFactory):
        '''
        Constructor function for service object
        
        Args:
            validator (Validator object): Object that validates events
            repo (Repo object): Object that stores and manages the data of all events
            eventFactory (Event class): Constructor for objects of type 'Event'
        '''

        self.__validator = validator
        self.__eventsRepo = eventsRepo
        self.__wallpapersRepo = wallpapersRepo
        self.__eventFactory = eventFactory
        self.__wallpaperFactory = wallpaperFactory #May use it if I create an UI for the app
        self.__currentWallpaperPath = self.__get_wallpaper_path()

    def get_events(self):
        '''
        Function that returns a list of current events
        
        Raises:
            EventRepoError: If the list of events is empty

        Returns:
            list (of events): The list that contains all of the current event objects
        '''

        return self.__eventsRepo.get_events()

    def delete_event(self, index):
        '''
        Function that deletes the event with the index 'index'
        
        Args:
            index (int): The index of the element that will be deleted
        '''

        self.__eventsRepo.delete_event(index)

    def get_categorized_events(self):
        '''
        Function that returns three lists of events, based
        on their remaining time until their ending (<1day/<1week/1week<)

        Raises:
            EventsRepoError: If the list of events is empty

        Returns:
            list (event objects): Three lists of events, categorized by their remaining time (<1day/<1week/1week<)
        '''

        categorizedEvents = [[], [], []]
        events = self.__eventsRepo.get_events()

        for el in events:
            remainingDays = (el.get_endingDate() - datetime.date.today()).days
            if remainingDays <= 1:
                categorizedEvents[0] += [el]
            elif remainingDays <= 7:
                categorizedEvents[1] += [el]
            else:
                categorizedEvents[2] += [el]
        
        return categorizedEvents

    def add_event(self, name, description, startingDate, endingDate):
        '''
        Function that creates and validates an object of type event with the
        provided parameters
        
        Args:
            name (string): The name of the event
            description (string): The description of the event
            startingDate (datetime.date): The starting date of the event
            endingDate (datetime.date): The ending date of the event
        
        Raises:
            ValidationError: If the parameters are not valid (empty strings / starting date after ending date)
        '''

        event = self.__eventFactory(name, description, startingDate, endingDate)
        self.__validator.validate_event(event)

        self.__eventsRepo.add_event(event)

    def get_available_wallpapers(self):
        '''
        Function that returns all the available wallpapers
        
        Raises:
            WallpapersRepoError: if there are no stored existing wallpapers yet
        '''

        return self.__wallpapersRepo.get__wallpapers()

    def create_set_wallpaper(self, image):
        '''
        Function that removes all the files from the temp folder,
        creates a new wallpaper with TODOs text written over it
        and sets it as wallpaper

        Args:
            image (Wallpaper object): The wallpaper object that will be modified and set as wallpaper
        
        Raises:
            EventsRepoError: If the list of events is empty
        '''

        #Removing all files from "temp" directory
        files = os.listdir("temp")
        for file in files:
            file_path = os.path.join("temp", file)
            if os.path.isfile(file_path):
                os.remove(file_path)

        #Creating a copy of the image inside "temp" directory
        copyPath = self.__copy_wallpaper(image.get_path(), "temp")

        #Creating the modified image, with text over it, inside "temp" directory
        textWallpaper = self.__add_text_to_wallpaper(image, copyPath)

        #Loading the new, modified wallpaper
        self.__load_wallpaper(textWallpaper)

    def __load_wallpaper(self, new_image):
        '''
        Function that loads the modified wallpaper
        
        Args:
            new_image (string): The path of the image that needs to be loaded
        '''

        #Ensure the path exists
        if not os.path.exists(new_image):
            raise FileNotFoundError(f"The image file '{new_image}' does not exist.")
        
        #Convert path to absolute path
        new_image = os.path.abspath(new_image)

        #Windows API constant for setting the wallpaper
        SPI_SETDESKWALLPAPER = 0x0014

        result = ctypes.windll.user32.SystemParametersInfoW(
            SPI_SETDESKWALLPAPER,
            0,
            new_image,
            3
        )

        if not result:
            raise ctypes.WinError()

    def __add_text_to_wallpaper(self, image, path, output_suffix="with_text"):
        '''
        Function that adds events (text) over the background image
        
        Args:
            image (Wallpaper object): The wallpaper object that will be modified
            path (string): The path of the image that will be modified
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
        x = int(width * 0.03)
        category_spacing = (width - 2 * x) // 2 - int(width * 0.04)
        y = int(height * 0.05)
        line_spacing = 20
        text_color = [(173, 0, 0), (255, 230, 0), (34, 255, 0)]  # Red, Yellow, Green
        shadow_color = (0, 0, 0)      # Black

        #Font settings
        try:
            font = ImageFont.truetype("arial.ttf", height*0.02)
        except:
            font = ImageFont.load_default()

        events = self.get_categorized_events()

        for idx, category in enumerate(events):
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

    def __copy_wallpaper(self, wallpaperPath = None, directoryPath = "wallpapers"):
        '''
        Function that creates a copy of the current wallpaper to a new destination
        
        Args:
            wallpaperPath (string): Path of current wallpaper
            directoryPath (string): Path of where the wallpaper will be copied
        '''
        
        #Set wallpaperPath if it has not been set by the caller
        if not wallpaperPath:
            wallpaperPath = self.__currentWallpaperPath
        
        #Create destinationation directory if it doesen't exist
        directoryPath = os.path.expanduser(directoryPath)
        os.makedirs(directoryPath, exist_ok=True)
        
        #For now it will only be wallpaper.jpg
        destinationPath = os.path.join(directoryPath, "wallpaper.jpg")

        shutil.copy2(wallpaperPath, destinationPath)
        return destinationPath

    def __get_wallpaper_path(self) -> str:
        '''
        Function that returns the path of the windows background image
        
        Raises:
            WinError (Exception): If windows api was unable to get background image path
        '''
        #Necessary Windows API constants
        SPI_GETDESKWALLPAPER = 0x0073
        MAX_PATH = 260

        # Call SystemParametersInfoW to get the wallpaper path
        buffer = ctypes.create_unicode_buffer(MAX_PATH)
        if not ctypes.windll.user32.SystemParametersInfoW(SPI_GETDESKWALLPAPER, MAX_PATH, buffer, 0):
            raise ctypes.WinError()
    
        reported_path = buffer.value
        
        # 1. Check if the reported path exists
        if os.path.exists(reported_path):
            return reported_path
        
        # 2. Check Windows wallpaper cache location
        cached_path = os.path.join(os.getenv('APPDATA'), r'Microsoft\Windows\Themes\TranscodedWallpaper')
        if os.path.exists(cached_path):
            return cached_path
        
        # 3. Check if using solid color
        if reported_path == '(None)':
            raise FileNotFoundError("Wallpaper is set to a solid color, not an image")
        
        # 4. Final fallback check
        raise FileNotFoundError(f"Wallpaper file not found. Originally reported path: {reported_path}")