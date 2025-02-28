import datetime

class EventService:
    def __init__(self, repo, validator, eventFactory):
        self.__repo = repo
        self.__validator = validator
        self.__eventFactory = eventFactory
    
    def get_events(self):
        '''
        Function that returns a list of current events
        
        Raises:
            EventRepoError: If the list of events is empty

        Returns:
            list (of events): The list that contains all of the current event objects
        '''

        return self.__repo.get_events()
    
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

        self.__repo.add_event(event)
    
    def delete_event(self, index):
        '''
        Function that deletes the event with the index 'index'
        
        Args:
            index (int): The index of the element that will be deleted
        '''

        self.__repo.delete_event(index)
    
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
        events = self.__repo.get_events()

        for el in events:
            remainingDays = (el.get_endingDate() - datetime.date.today()).days
            if remainingDays <= 1:
                categorizedEvents[0] += [el]
            elif remainingDays <= 7:
                categorizedEvents[1] += [el]
            else:
                categorizedEvents[2] += [el]
        
        return categorizedEvents