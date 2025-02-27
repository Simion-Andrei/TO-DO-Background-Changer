from ..utils import WallpaperRepoError
from ..DOMAIN.wallpaper import Wallpaper
import glob
import os
from PIL import Image

class WallpapersRepo:
    def __init__(self):
        self.__wallpapers = []
        
        self.__load_existing_wallpapers()
    
    def __load_existing_wallpapers(self):
        '''
        Function that searches for all the wallpapers existing in the 'wallpapers' directory,
        then creates object corresponding with each wallpaper
        '''

        existingWallpapers = sorted(
            glob.glob(os.path.join("wallpapers", '*.[jJ][pP][gG]')) + 
            glob.glob(os.path.join("wallpapers", '*.[pP][nN][gG]')) + 
            glob.glob(os.path.join("wallpapers", '*.[gG][iI][fF]'))
        )

        for el in existingWallpapers:
            with Image.open(el) as image:
                width, height = image.size
                newWallpaper = Wallpaper(el, width, height)
                self.__wallpapers.append(newWallpaper)

    def get__wallpapers(self):
        '''
        Function that returns the list of wallpapers

        Raises:
            WallpapersRepoError: if there are no stored existing wallpapers yet

        Returns:
            A list of all of the current stored objects of type 'Wallpaper'
        '''

        if not self.__wallpapers:
            raise WallpaperRepoError("No existing wallpapers yet!")

        return self.__wallpapers