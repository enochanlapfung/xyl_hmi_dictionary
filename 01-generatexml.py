#!/usr/bin/python

import xml.etree.ElementTree as ET
import parse

#-------------------------------------------------------------------------------
# Parsing def file
#-------------------------------------------------------------------------------
uids = []
deffile = open("example.def", 'r')
for line in deffile:
    # Extracting ID and uID
    result = parse.parse("STRING_DEF({}, {:d})", line)
    id  = result.fixed[0]
    uid = result.fixed[1]
    uids.append(uid)

#-------------------------------------------------------------------------------
# Parsing xml file
#-------------------------------------------------------------------------------

# Obtain root of XML tree
tree = ET.parse("english.xml")
root = tree.getroot()

# Obtain the root's attributes
rootAttributes = root.attrib
# We will be expecting the following attributes
attributeLang   = "{http://www.w3.org/XML/1998/namespace}lang"
attributeId     = "id"
# Checking language
language = rootAttributes[attributeLang]

# concept
#     title
#         conbody
#             section
#                 menucascade
#                     uicontrol
#         conbody...

for child in root:
    if child.tag == "conbody":
        conbody = child

for section in conbody.findall("section"):
    menucascade = section.find("menucascade");
    uicontrol = menucascade.find("uicontrol");
    # Extract uid as an integer
    uidRaw = uicontrol.attrib["id"]
    uidInt = parse.parse("u-{:d}", uidRaw).fixed[0];
    # Remove section if uid is not found in uids
    if uidInt not in uids:
        conbody.remove(section)

tree.write("result.xml");
