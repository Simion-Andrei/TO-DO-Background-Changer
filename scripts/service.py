import os

class Service:
    def __init__(self, eventService, wallpaperService, wallpaperSys, textRenderer):
        '''
        Constructor function for service object
        
        Args:
            validator (Validator object): Object that validates events
            repo (Repo object): Object that stores and manages the data of all events
            eventFactory (Event class): Constructor for objects of type 'Event'
        '''

        self.__eventService = eventService
        self.__wallpaperService = wallpaperService
        self.__wallpaperSys = wallpaperSys
        self.__textRenderer = textRenderer

    def get_events(self):
        '''
        Function that returns a list of current events
        
        Raises:
            EventRepoError: If the list of events is empty

        Returns:
            list (of events): The list that contains all of the current event objects
        '''

        return self.__eventService.get_events()

    def delete_event(self, index):
        '''
        Function that deletes the event with the index 'index'
        
        Args:
            index (int): The index of the element that will be deleted
        '''

        self.__eventService.delete_event(index)

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

        self.__eventService.add_event(name, description, startingDate, endingDate)

    def mark_event_as_done(self, index):
        '''
        Function that marks an event as done
        
        Args:
            index (int): The index of the element that will be markes as done
        '''

        self.__eventService.mark_as_done(index)

    def get_available_wallpapers(self):
        '''
        Function that returns all the available wallpapers
        
        Raises:
            WallpapersRepoError: if there are no stored existing wallpapers yet
        '''

        return self.__wallpaperService.get_wallpapers()

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
        self.__wallpaperSys.remove_files_from_dir("temp")

        #Creating a copy of the image inside "temp" directory
        copyPath = self.__wallpaperSys.copy_wallpaper(image.get_path(), "temp")

        #Creating the modified image, with text over it, inside "temp" directory
        textWallpaper = self.__textRenderer.add_text_to_wallpaper(image, copyPath, self.__eventService.get_categorized_events())

        #Loading the new, modified wallpaper
        self.__wallpaperSys.load_wallpaper(textWallpaper)