#!/usr/bin/python

import xml.etree.ElementTree as ET
import parse

# languages = {
#     "zh-CN":"chinese",
#     "en-US":"english"
# }

# TODO Could just insert all the file names and paths in the script
# and just check whether the fields exist or not

#-------------------------------------------------------------------------------
# User inputs
#-------------------------------------------------------------------------------
masterXMLPath   = str(raw_input("Master library XML path: "))
defPath         = str(raw_input(".def file path: "))
language        = str(raw_input("Language: ")) # TODO: This can be extracted from the master library

#-------------------------------------------------------------------------------
# Parsing def file
#-------------------------------------------------------------------------------
uids = []
deffile = open(defPath, 'r')
for line in deffile:
    # Extracting ID and uID
    result = parse.parse("STRING_DEF({}, {:d})", line)
    idString    = result.fixed[0]
    uid         = result.fixed[1]
    uids.append(uid)

#-------------------------------------------------------------------------------
# Parsing xml file
#-------------------------------------------------------------------------------

# Obtain root of XML tree
tree = ET.parse(masterXMLPath)
root = tree.getroot()

# Obtain the root's attributes
rootAttributes = root.attrib
# We will be expecting the following attributes
attributeLang   = "{http://www.w3.org/XML/1998/namespace}lang"
attributeId     = "id"
# Checking language
# language = rootAttributes[attributeLang]

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

tree.write(language + ".xml");
