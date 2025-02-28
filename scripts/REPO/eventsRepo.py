import datetime
from ..DOMAIN.event import Event
from ..utils import EventsRepoError

class EventsRepo:
    def __init__(self, filename):
        '''
        Constructor function for repo object
        
        Args:
            filename (string): Path of the file that will be used to store the data
        '''

        self.__events = []
        self.__filename = filename

        self.__load_from_file() #When creating the object, we load the saved content into the program

    def get_events(self):
        '''
        Function that returns the list of events

        Raises:
            EventsRepoError: if there are no stored existing events yet

        Returns:
            A list of all of the current stored objects of type 'Event'
        '''

        if not self.__events:
            raise EventsRepoError("No existing events yet!")
        
        return self.__events

    def delete_event(self, index):
        '''
        Function that deletes the event with the index 'index'
        
        Args:
            index (int): The index of the element that will be deleted
        '''

        self.__events.pop(index)

    def mark_as_done(self, index):
        '''
        Function that sets the event at position 'index' as done
        '''

        self.__events[index].set_as_done()

        self.__load_to_file()

    def __load_from_file(self):
        '''
        Function that loads the content of the stored data file into the program by parsing the
        data and creating objects of type 'Event' with the corresponding information

        Event example in data file: "Title,Description,%d/%m/%Y,%d/%m/%Y"
        '''

        with open(self.__filename, "r") as file:
            line = file.readline()

            while line:
                line = line.strip()
                line = line.split(",")

                name = line[0]
                description = line[1]

                date1 = datetime.date.fromisoformat(line[2])
                
                date2 = datetime.date.fromisoformat(line[3])

                done = line[4] == "True"

                if done and datetime.date.today() > date2:
                    line = file.readline()
                    continue

                event = Event(name, description, date1, date2)
                if done: event.set_as_done()

                self.__events.append(event)

                line = file.readline()

    def __load_to_file(self):
        '''
        Function that loads the current events from the events list to the data file by
        transforming the data into a string that can be parsed back to an object of type
        'Event'

        Event example in data file: "Title,Description,%d/%m/%Y,%d/%m/%Y"
        '''

        with open(self.__filename, "w") as file:
            for el in self.__events:
                name = el.get_name()
                description = el.get_description()
                startingDateStr = el.get_startingDate().strftime("%Y-%m-%d")
                endingDateStr = el.get_endingDate().strftime("%Y-%m-%d")
                done = "True" if el.is_done() == True else "False"

                file.write(name + "," + description + "," + startingDateStr + "," + endingDateStr + "," + done + "\n")
    
    def add_event(self, event):
        '''
        Function that adds the event 'event' to the list of events, then updates the
        date file by calling the '__load_to_file' function
        
        Args:
            event (event object): The event that needs to be added to the list
        '''

        self.__events.append(event)
        self.__load_to_file() #Saving the current content to the data file after modifying it