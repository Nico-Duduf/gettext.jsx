import json

# Load JSON file
jsonPath = "../../After-Effects/Duik/DuGR/inc/tr/DuGR_fr.json"
poPath = "../../After-Effects/Duik/DuGR/translation/DuGR.po"

poStr = """# Translations template for DuGR.
# Copyright (C) 2022 RxLaboratory
# This file is distributed under the same license as the DuGR project.
# RxLaboratory <contact@rxlaboratory.org>, 2022.
#
#, fuzzy
msgid ""
msgstr ""
"Project-Id-Version: DuGR 4.0.X\\n"
"POT-Creation-Date: 2022-08-02 15:56\\n"
"PO-Revision-Date: \\n"
"Last-Translator: \\n"
"Language-Team: RxLaboratory <http://rxlaboratory.org>\\n"
"MIME-Version: 1.0\\n"
"Content-Type: text/plain; charset=UTF-8\\n"
"Content-Transfer-Encoding: 8bit\\n"
"Genereated-By: gettext.jsxinc\\n"
"Language: fr\\n"
"""

with open(jsonPath, "r", encoding="utf8") as jsonFile:
    jsonDoc = json.load(jsonFile)

msgs = jsonDoc["DuGR"][1]["translations"]

for msg in msgs:
    comment =  msg["comment"]
    context =  msg["context"]
    msgid =  msg["source"]
    msgstr =  msg["translation"]

    if msgstr == msgid:
        msgstr = ""

    if comment.strip() == "NEW":
        comment = ""

    if comment != "":
        poStr += "# " + comment + "\n"

    poStr += "#, qt-format\n"

    if context != "":
        poStr += "msgctxt \"" + context + "\"\n"

    poStr += "msgid \"" + msgid.replace("{#}", "%1").replace('"','\\"').replace("\n",'\\n"\n"') + "\"\n"
    poStr += "msgstr \"" + msgstr.replace("{#}", "%1").replace('"','\\"').replace("\n",'\\n"\n"') + "\"\n\n"
    
with open(poPath, "w", encoding="utf8") as poFile:
    poFile.write(poStr)