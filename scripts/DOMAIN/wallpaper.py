class Wallpaper:
    def __init__(self, path, width, height):
        self.__path = path
        self.__width = width
        self.__height = height
        pass

    def get_path(self) -> str:
        return self.__path
    
    def get_width(self) -> int:
        return self.__width
    
    def get_height(self) -> int:
        return self.__height