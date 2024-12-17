# imports
import random

def sample(items, number, rate=0.2):
    """
    A generator function that observes items in order, and using a rate
     - determines whether or not to return the item to a final list 

    Parameters:
        items - iterable (of any type, including generators)
        number - int of items to collect for sample
        rate - probability float of an 
    
    Returns:
        elements from items
    """
    
    counter = 0

    for element in items:
        if counter < number:

            # create random float between 0-1 and compare it to the rate
            probability_number = random.random()
            if probability_number < rate:
                counter +=1
                yield element
            else:
                continue
        
        # case of items max numbers yielded
        else:
            break
