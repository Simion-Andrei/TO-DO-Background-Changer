from ..utils import ValidationError

class Validator:
    def validate_event(self, event):
        '''
        Function that validates an event
        
        Args:
            event (Event object): An event

        Raises:
            ValidationError: If the name or description of the event are empty and if the dates of the event ar not valid
        
        Returns:
            -
        '''

        if event.get_name() == "":
            raise ValidationError("Empty name!")

        if event.get_description() == "":
            raise ValidationError("Empty description!")
        
        if event.get_startingDate() > event.get_endingDate():
            raise ValidationError("The ending date needs to be before the starting date!")