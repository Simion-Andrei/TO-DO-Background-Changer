import os
import ctypes
import shutil

class WallpaperSys:
    """Handles OS-level wallpaper operations"""
    
    #WINDOWS API CONSTANTS
    SPI_SETDESKWALLPAPER = 0x0014
    SPI_GETDESKWALLPAPER = 0x0073
    MAX_PATH = 260

    @staticmethod
    def remove_files_from_dir(dir):
        '''
        Function that removes all of the files from the given dir
        
        Args:
            dir (string): The path of the directory of which content will be erased
        '''

        files = os.listdir(dir)
        for file in files:
            file_path = os.path.join("temp", file)
            if os.path.isfile(file_path):
                os.remove(file_path)

    @staticmethod
    def copy_wallpaper(wallpaperPath, directoryPath = "wallpapers"):
        '''
        Function that creates a copy of the current wallpaper to a new destination
        
        Args:
            wallpaperPath (string): Path of current wallpaper
            directoryPath (string): Path of where the wallpaper will be copied
        '''
        
        #Create destinationation directory if it doesen't exist
        directoryPath = os.path.expanduser(directoryPath)
        os.makedirs(directoryPath, exist_ok=True)
        
        #For now it will only be wallpaper.jpg
        destinationPath = os.path.join(directoryPath, "wallpaper.jpg")

        shutil.copy2(wallpaperPath, destinationPath)
        return destinationPath

    @staticmethod
    def get_wallpaper_path() -> str:
        '''
        Function that returns the path of the windows background image
        
        Raises:
            WinError (Exception): If windows api was unable to get background image path
        '''

        #WINDOWS API CONSTANTS
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
    
    @staticmethod
    def load_wallpaper(new_image):
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

        #WINDOWS API CONSTANTS
        SPI_SETDESKWALLPAPER = 0x0014

        result = ctypes.windll.user32.SystemParametersInfoW(
            SPI_SETDESKWALLPAPER,
            0,
            new_image,
            3
        )

        if not result:
            raise ctypes.WinError()