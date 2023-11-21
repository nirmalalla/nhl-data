import json
from urllib.request import urlopen
import re

# Opening and reading URL
url = "https://www.espn.com/nhl/stats"
page = urlopen(url)
html_bytes = page.read()
html = html_bytes.decode("utf-8")

# Separating data into unparsed HTML containing player point info
start_index_points = html.find("Skating Leaders")
end_index_points = html.find("Goals")
points_leaders_html = html[start_index_points: end_index_points]

# Further separating into a list with elements for each player's info
point_data = re.findall("<tr class=\"Table__TR Table__TR--sm Table__even\" data-idx=\"0\">.*</tr>", points_leaders_html)
separate_players = point_data[0].split("</tr>")

# Removing unused data
separate_players.pop(5)
separate_players.pop(5)

# Reading and parsing data for each player and adding final formatted data to a dict
final_point_data = {}
i = 0
for n in separate_players:
    unparsed_point = re.findall("<td class=\"Table__TD\">.*</td>", separate_players[i])
    parsed_point = re.sub("<.*?>", "", unparsed_point[0])
    

    unparsed_name = re.findall("title.*\" data", separate_players[i])
    parsed_name = re.findall("\".*\"", unparsed_name[0])[0].replace("\"", "")
   
    final_point_data[parsed_name] = parsed_point
    i += 1

# Writing data to JSON file
json_object = json.dumps(final_point_data, indent=4)
with open("../data/point_data.json", "w") as outfile:
    outfile.write(json_object)