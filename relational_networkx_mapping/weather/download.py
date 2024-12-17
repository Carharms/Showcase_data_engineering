'''#! download.py
"""Makes a request to a url to download a specific date range of data related to 
weather patterns at a specific geography"""

__author__ = "Carter Harms"
__copyright__ = "Copyright, 2024"
__license__ = "GPL"
__version__ = "1.0"
__email__ = "harmsc@uchicago.edu"
'''

# imports
import sys
import datetime
import urllib.request


def save_json(lat, lng, days):
    """
    Make a request to open-meteo.com's weather API for the last
    {days} days of weather information at the given location.

    Writes a file named "weather.json" containing the historical weather
    information.

    Parameters:
        lat: float  : latitude of location
        lng: float  : longitude of location
        days: int   : number of days in past to request
    """
    # You will use urllib.request and datetime for this. Take a look
    # at the documentation for both of these modules to figure out
    # how to use them.


    #    https://docs.python.org/3/library/urllib.request.html
    #    https://docs.python.org/3/library/datetime.html

    # determine date variable as variable for calculations
    current_date = datetime.datetime.now().date()
    # determine the initial date to begin pulling data as variable for calculations
    start_date = current_date - datetime.timedelta(days=days)


    # Open a file in binary-write mode ("wb").
    with open("weather.json", "wb") as file:

    # Make a request using urllib.request
        # base site that will never need to be adjusted
        url_site = "https://archive-api.open-meteo.com/v1/era5?"
        # url components that will be influenced by arguments
        url_parameters = f"latitude={lat}&longitude={lng}&start_date={start_date.strftime('%Y-%m-%d')}&end_date={current_date.strftime('%Y-%m-%d')}&daily=temperature_2m_max,temperature_2m_min&timezone=auto"
        full_url = url_site + url_parameters

        #make the request 
        url_complete = urllib.request.urlopen(full_url)

        # Save the result of reading the response (i.e.: response.read()) to
        file.write(url_complete.read())


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: download.py <lat> <lng> <days>")
    else:
        save_json(float(sys.argv[1]), float(sys.argv[2]), int(sys.argv[3]))
