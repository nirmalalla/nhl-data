import json
from urllib.request import urlopen
import re

# Opening and reading URL
url = "https://www.espn.com/nhl/stats"
page = urlopen(url)
html_bytes = page.read()
html = html_bytes.decode("utf-8")

# Separating goal data
start_index = html.find("Goals")
end_index = html.find("Plus/Minus")
goal_leaders_html = html[start_index: end_index]

# Further separating data into specific players
goal_data = re.findall("<tr class=\"Table__TR Table__TR--sm Table__even\" data-idx=\"0\">.*</tr>", goal_leaders_html)
separate_players = goal_data[0].split("</tr>")

# Removing unused data
separate_players.pop(5)
separate_players.pop(5)

# Final formatting to store in dict containing name and goal value
final_goal_data = {}
i = 0
for n in separate_players:
    unparsed_goal = re.findall("<td class=\"Table__TD\">.*</td>", separate_players[i])
    parsed_goal = re.sub("<.*?>", "", unparsed_goal[0])
    
    unparsed_team = re.findall("<span class=\"pl2 n10 leaderCell__teamAbbrev\">.*</span>", separate_players[i])
    parsed_team = re.sub("<.*?>", "", unparsed_team[0])

    unparsed_name = re.findall("title.*\" data", separate_players[i])
    parsed_name = re.findall("\".*\"", unparsed_name[0])[0].replace("\"", "")
   
    final_goal_data[parsed_name] = [parsed_team, parsed_goal]
    i += 1

# Writing data to JSON file
json_object = json.dumps(final_goal_data, indent=4)
with open("../data/goal_data.json", "w") as outfile:
    outfile.write(json_object)