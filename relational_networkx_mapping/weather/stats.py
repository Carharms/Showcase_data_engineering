'''#! stats.py
"""Summarize weather data metrics over a set period of time by using 
subcategories of min and max temperatures"""

__author__ = "Carter Harms"
__copyright__ = "Copyright, 2024"
__license__ = "GPL"
__version__ = "1.0"
__email__ = "harmsc@uchicago.edu"
'''

import json
import statistics
from math import isnan


def summarize_weather(filename):
    """
    Reads weather data from a JSON file and summarizes it.

    Inputs:
        filename (str): Filename for weather data.

    Returns:
        Dictionary with the following keys:
           start_date:      Date of first entry (string)
           end_date:        Date of last entry (string)
           max_high:        Maximum high temperature in the data (float).
           min_low:         Minimum low temperature in the data (float).
           mean_high:    Computed mean of high temperatures (float).
           mean_low:     Computed mean of low temperatures (float).
           std_dev_high:    Computed standard deviation of high temperatures (float).
           std_dev_low:     Computed standard deviation of low temperatures (float).
    """

    # open file & read data as a string.
    with open(filename, "r") as weather_file:

        # transform data from a string to Python objects.
        altered_state = json.load(weather_file)
        
        # create list to add all high temperature values from .json file
        high_temp_list = []

        for temp in altered_state['daily']['temperature_2m_max']:
            # remove null temperatures from the calculations
            if temp is not None:
                high_temp_list.append(temp)               


        # create list to add all low temperature values from .json file
        low_temp_list = []

        for temp in altered_state['daily']['temperature_2m_min']:
            # remove null temperatures from the calculations
            if temp is not None:
                low_temp_list.append(temp)

        # compute & return statistics as shown in docstring.
        # high temp calculations
        max_high_calc = max(high_temp_list[:])
        mean_high_calc = statistics.mean(high_temp_list)
        stdev_high_calc = statistics.stdev(high_temp_list)

        # low temp calculations
        min_low_calc = min(low_temp_list[:])
        mean_low_calc = statistics.mean(low_temp_list)
        stedev_low_calc = statistics.stdev(low_temp_list)

        # summary dictionary taking values from above and prepping them for output
        summary = {
            # high temp values
            "max_high": max_high_calc,
            "mean_high": mean_high_calc,
            "std_dev_high": stdev_high_calc,
            # low temp values
            "min_low": min_low_calc,
            "mean_low": mean_low_calc,  
            "std_dev_low": stedev_low_calc,
            # dates
            "start_date": altered_state["daily"]["time"][0],
            "end_date": altered_state["daily"]["time"][-1]

        }
        return summary


    # Relevant modules:
    #   statistics: https://docs.python.org/3/library/statistics.html
    #   json: https://docs.python.org/3/library/json.html

def main():
    """
    Reads in weather data from weather.json and prints out a summary.
    """
    summary = summarize_weather()
    print(
        """       Weather Report
===========================
{start_date}       {end_date}
===========================
High Temperature:   {max_high:>6.1f}
     Average:       {mean_high:>6.1f}
     Std. Dev:      {std_dev_high:>6.1f}
Low Temperature:    {min_low:>6.1f}
     Average:       {mean_low:>6.1f}
     Std. Dev:      {std_dev_low:>6.1f}
          """.format(**summary)
    )


if __name__ == "__main__":
    main()
