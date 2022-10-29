from genericpath import isfile
import json
import os
import polib

po_path = "../../After Effects/Duik/DuGR/translation/DuGR_zh.po"
json_path = "../../After Effects/Duik/DuGR/inc/tr/DuGR_zh.json"
#po_path = "examples/template.po"
#json_path = "examples/test.json"

includeFuzzyEntries=True

# defaults
json_data = {
    "": {
        "language": "en",
        "plural-forms": "nplurals=2; plural=(n!=1);"
    }
}

# gets an entry
def entryToJson(entry):
    msgid = ""
    if entry.msgctxt:
        msgid = entry.msgctxt + "\u0004" + entry.msgid
    else:
        msgid = entry.msgid

    msgstr = ""
    if entry.msgstr_plural:
        msgstr = []
        for k in entry.msgstr_plural:
            msgstr.append(entry.msgstr_plural[k])
    else:
        msgstr = entry.msgstr

    json_data[msgid] = msgstr


if os.path.isfile(po_path):
    # Parse metadata (polib does not)
    with open(po_path, 'r', encoding='utf8') as po_file:
        line = po_file.readline().strip()
        while line != "":
            # got language
            if line.startswith('"Language:'):
                json_data[""]["language"] = line.replace('"Language:', '').replace('\\n"', '').strip()
            # got plural forms
            elif line.startswith('"Plural-Forms:'):
                json_data[""]["plural-forms"] = line.replace('"Plural-Forms:', '').replace('\\n"', '').strip()
            line = po_file.readline().strip()

    po_file = polib.pofile(po_path)

    for entry in po_file.translated_entries():
        entryToJson(entry)

    if includeFuzzyEntries:
        for entry in po_file.fuzzy_entries():
            entryToJson(entry)

    with open(json_path, 'w', encoding='utf8') as json_file:
        json.dump(json_data, json_file)
    
    print("JSON created at " + json_path)

else:
    print("PO File not found.")
