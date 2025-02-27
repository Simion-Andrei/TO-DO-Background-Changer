class Event:
    def __init__(self, name, description, startingDate, endingDate):
        '''
        Constructor function for 'Event' type object

        Args:
            name (string): The name of the event
            description (string): Quick description of the event
            startingDate (datetime): The starting date of the event
            endingDate (datetime): The ending date of the event
        '''
        
        self.__name = name
        self.__description = description
        self.__startingDate = startingDate
        self.__endingDate = endingDate

    def get_name(self):
        return self.__name

    def get_description(self):
        return self.__description

    def get_startingDate(self):
        return self.__startingDate
    
    def get_endingDate(self):
        return self.__endingDate