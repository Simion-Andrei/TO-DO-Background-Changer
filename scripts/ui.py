import os
import datetime

class UI:
    def __init__(self, service):
        '''
        Constructor function for UI class
        
        Args:
            service (service object): Object that handles communication between UI and REPO
        '''

        self.__service = service

        self.__actions = {
            1: self.__add_event,
            4: self.__load_wallpaper
        }

        self.__printables = [
            "0.Exit",
            "1.Add a new event",
            "2.Mark event as done",
            "3.See events",
            "4.Load wallpaper"
        ]

    def __add_event(self):
        '''
        Function that gets name, description, starting date and ending date as input from the user,
        then calls the service function that creates and stores an event with read data
    
        Raises:
            AttributeError: If the dates read from user are not valid (not iso format or not valid dates)
            ValidationError: If the name or title are empty strings and if the starting date is after the ending date
        '''

        name = input("Name: ")
        description = input("Description: ")
        try:
            startingDate = datetime.date.fromisoformat(input("Starting date(year-month-day): ")) #Dates are read as iso-format
            endingDate = datetime.date.fromisoformat(input("Ending date(year-month-day): "))
        except ValueError:
            print("Invalid date or format!")
            return

        try:
            self.__service.add_event(name, description, startingDate, endingDate)
            print("Event succesfully added!")
        except Exception as e:
            print(e)

    def __load_wallpaper(self):
        '''
        Function that prints the available wallpapers to modify, and ask the user to input
        the index of the one that they want to use
        '''

        wallpapers = self.__service.get_available_wallpapers()

        for i, el in enumerate(wallpapers, 1):
            print(f"{i}.{el.get_path()}")
        
        try:
            selected = int(input("Type the index of the wallpaper u want to load, or 0 if you want to exit: "))
        except:
            print("The index needs to be a valid number!")
            return
        
        if selected == 0:
            return
        
        try:
            self.__service.create_set_wallpaper(wallpapers[selected-1])
            print("Succesfully loaded wallpaper!")
        except Exception as e:
            print(e)

    def __print_actions(self):
        for el in self.__printables:
            print(el)

    def run(self):
        '''
        Function that runs the main loop of the program
        '''

        while True:
            os.system("CLS") #Clearing the screen after every action
            self.__print_actions()

            try:
                inp = int(input("Type the index of the action you want to execute: "))
            except ValueError:
                print("The input needs to be a natural number!") #If user input is not an int
                os.system("pause")
                continue

            if inp == 0:
                return

            if inp in self.__actions:
                self.__actions[inp]() #Executing the function with the corresponding index
                os.system("pause")
                continue
            else:
                print("Invalid index") #If user input is not a valid index of an action
                os.system("pause")
                continue