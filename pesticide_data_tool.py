# File name: pesticide_parser.py
# Author: Frank Tancredi
# Date created: 7/27/2021
# Date last modified: 8/09/2021
# Python Version: 3.0


import bs4 as bs
import urllib

# get_hazard_level returns "low", "moderate", or "high" depending on which is
# stated in the text of the html_string argument. As this string is formatted
# to only contain one of the 3, only one hazard_level value will ever meet
# the requirements to be returned
def get_hazard_level(html_string):
    html_string = str(html_string)
    hazard_levels = {
        html_string.find("Low") : "low",
        html_string.find("Moderate") : "moderate",
        html_string.find("High") : "high"
    }
    for key in hazard_levels:
        if key > 0:
            return hazard_levels[key]

# Only if a pesticide is rated low in each of the three categories will it be
# deemed completely safe. 
def print_safe_pesticides(pesticide, pesticideList):
    total_safe_pesticides = 0
    for pesticide in pesticideList:
        if (pesticide["environmental fate"] == "low"
            and pesticide["ecotoxicity"] == "low"
            and pesticide["human health hazard"] == "low"):
            total_safe_pesticides += 1
            print(pesticide["name"]) 
    if total_safe_pesticides == 0:
        no_safe_found = "There are currently no completely safe pesticides"\
            + " recognized by the University of Hertfordshire's"\
            + " Pesticide Properties Database."
        print (no_safe_found)

pesticideList = []
# The database does not have hazard levels for pesticides where data is not
# yet available for a conclusive result, therfore all three parameters
# are inconclusive by default.
environmental_fate = ecotoxicity = human_health_hazard = "inconclusive"
source = urllib.request.urlopen(
    "http://sitem.herts.ac.uk/aeru/ppdb/en/atoz_insect.htm").read()
soup = bs.BeautifulSoup(source,"lxml")
# The lambda expression in find_all is an efficient way to remove a line or
# two of garbage data that shares the most optimal filters for the data we do
# want.
for link in soup.find_all(
    "a", {"href" : lambda L: L and L.startswith("Reports")}):
    #link.text == pesticide name for use in dictionary.
    print("Fetching data for " + link.text + "...")
    # For each listed pesticide we will go to the associated page to fetch
    # hazard level data we're looking for.
    pesticide_source = urllib.request.urlopen(
            "https://sitem.herts.ac.uk/aeru/ppdb/en/" 
            + link.get("href")).read()
    # This soup contains the hazard data we need.
    pesticide_soup = bs.BeautifulSoup(pesticide_source,"lxml")
    for div in pesticide_soup.find_all("div", {"class":"tooltip2"}):
        if "Environmental fate" in div.text:
            environmental_fate = get_hazard_level(div)
        elif "Ecotoxicity" in div.text:
            ecotoxicity = get_hazard_level(div)
        elif "Human health" in div.text:
            human_health_hazard = get_hazard_level(div)
    pesticide = {
    "name" : link.text,
    "environmental fate" : environmental_fate,
    "ecotoxicity" : ecotoxicity,
    "human health hazard" : human_health_hazard
    }
    pesticideList.append(pesticide.copy())
print("Environmental, Ecotoxic, and Low Human Health Risk Pesticides")
print("-------------------------------------------------------------")
print_safe_pesticides(pesticide, pesticideList)
