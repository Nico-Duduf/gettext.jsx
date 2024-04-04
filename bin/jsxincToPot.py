from genericpath import isfile
import os
import re

source_paths = (
    "../../After-Effects/Duik/src",
)
pot_path = "../../After-Effects/Duik/translation/Duik.pot"


"""source_paths = (
    "../../After-Effects/Duik/DuSan/inc",
    "../../After-Effects/Duik/DuSan/DuAEF/inc",
    "../../After-Effects/Duik/DuSan/DuAEF/DuESF/inc",
)"""

"""source_paths = (
    "../../After-Effects/Duik/DuGR/inc",
    "../../After-Effects/Duik/DuGR/DuAEF/inc",
    "../../After-Effects/Duik/DuGR/DuAEF/DuESF/inc",
)
pot_path = "../../After-Effects/Duik/DuGR/translation/DuGR.pot"
"""

po_str = """# Translations template for Duik.
# Copyright (C) 2022-2024 RxLaboratory
# This file is distributed under the same license as the Duik project.
# RxLaboratory <contact@rxlaboratory.org>, 2024.
#
#, fuzzy
msgid ""
msgstr ""
"Project-Id-Version: Duik 17.X.X\\n"
"POT-Creation-Date: 2024-03-26 10:30\\n"
"PO-Revision-Date: \\n"
"Last-Translator: \\n"
"Language-Team: RxLaboratory <http://rxlaboratory.org>\\n"
"MIME-Version: 1.0\\n"
"Content-Type: text/plain; charset=UTF-8\\n"
"Content-Transfer-Encoding: 8bit\\n"
"Genereated-By: gettext.jsxinc\\n"
"""

po_ids = []

re_source = re.compile('(?:\\s+|\\.)(?:_|__|tr|gettext)\\s*\\(?\\s*("|\')((?:\\\\\\1|(?:(?!\\1).))*)\\1(?:(?:.*\\s*\\/\\/\\/\\s*TRANSLATORS:\\s*)(.+))?')
re_source_plural = re.compile('(?:\\s+|\\.)(?:_n|ngettext)\\s*\\(?\\s*("|\')((?:\\\\\\1|(?:(?!\\1).))*)\\1\\s*,\\s*("|\')((?:\\\\\\3|(?:(?!\\3).))*)\\3(?:(?:.*\\s*\\/\\/\\/?\\s*TRANSLATORS:\\s*)(.+))?')
re_source_context = re.compile('(?:\\s+|\\.)(?:_p|pgettext)\\s*\\(?\\s*("|\')((?:\\\\\\1|(?:(?!\\1).))*)\\1\\s*,\\s*("|\')((?:\\\\\\3|(?:(?!\\3).))*)\\3(?:(?:.*\\s*\\/\\/\\/?\\s*TRANSLATORS:\\s*)(.+))?')
# TODO re_source_all

def insertEntry(msgid, msgid_plural=None, msgctxt=None, comment=None, source_name=None, source_line=None):
    global po_str
    global po_ids

    # already there
    if msgid in po_ids:
        return

    if comment:
        comment = comment.split("\n")
        po_str += '\n#. "' + '"\n#. "'.join(comment) + '"'

    if source_name and source_line is not None:
        po_str += "\n#: " + source_name + ":" + str(source_line)
    elif source_name:
        po_str += "\n#: " + source_name
    elif source_line:
        po_str += "\n#: source:" + str(source_line)
    
    po_str += "\n#, qt-format"

    if msgctxt:
        po_str += "\nmsgctxt \"" + msgctxt + "\""
    
    po_str += "\nmsgid \"" + msgid + "\""

    if msgid_plural:
        po_str += "\nmsgid_plural \"" + msgid_plural + "\""

    po_str += "\nmsgstr \"\"\n"

    po_ids.append(msgid)

entries = {}

def extract( source_path ):
    for source_name in os.listdir(source_path):
        source = source_path + "/" + source_name
        if os.path.isfile(source):
            if not source_name.lower().endswith(".jsxinc") and not source_name.lower().endswith(".jsx"):
                continue
            if source_name.lower() == "translator.jsxinc" or source_name.lower() == "translator.jsx":
                continue
            found = False
            print("> Scanning " + source)
            with open(source, 'r', encoding="utf8") as source_file:
                line_num = 1
                for line in source_file.readlines():
                    match = re_source.search( line )
                    entry = {
                        "msgid": "",
                        "msgid_plural": None,
                        "msgctxt": None,
                        "comment": None,
                        "source_name": None,
                        "source_line": None
                    }
                    if match:
                        found = True
                        entry["msgid"] =  match.group(2)
                        entry["comment"] =  match.group(3)
                        entry["source_name"] = source_name
                        entry["source_line"] = line_num
                        
                    match = re_source_plural.search( line )
                    if match:
                        found = True
                        entry["msgid"] =  match.group(2)
                        entry["comment"] =  match.group(5)
                        entry["msgid_plural"] =  match.group(4)
                        entry["source_name"] =  source_name
                        entry["source_line"] =  line_num
                    
                    match = re_source_context.search( line )
                    if match:
                        found = True
                        entry["msgid"] =  match.group(4)
                        entry["comment"] =  match.group(5)
                        entry["msgctxt"] =  match.group(2)
                        entry["source_name"] =  source_name
                        entry["source_line"] =  line_num

                    # Decode special characters
                    entry["msgid"] = entry["msgid"].encode( 'utf-8' ).decode( 'unicode-escape' )
                    # Except new lines
                    entry["msgid"] = entry["msgid"].replace("\n","\\n")

                    # Add/Update
                    if entry["msgid"] != "":
                        h = entry["msgid"]
                        if entry["msgctxt"]:
                            h = h +  entry["msgctxt"]

                        # Update
                        if h in entries:
                            if entries[h]["comment"] and entry["comment"]:
                                if entries[h]["comment"] != entry["comment"]:
                                    entries[h]["comment"] = entries[h]["comment"] + "\n" + entry["comment"]
                            elif entry["comment"]:
                                entries[h]["comment"] = entry["comment"]
                        else:
                            entries[h] = entry
                    
                    line_num += 1

                if found:
                    print("Found strings in " + source)

        elif os.path.isdir(source):
            extract(source)

for source_path in source_paths:
    extract(source_path)

for e in entries:
    insertEntry(
        entries[e]["msgid"],
        msgid_plural=entries[e]["msgid_plural"],
        msgctxt=entries[e]["msgctxt"],
        comment=entries[e]["comment"],
        source_name=entries[e]["source_name"],
        source_line=entries[e]["source_line"]
    )

with open(pot_path, 'w', encoding="utf8") as pot_file:
    pot_file.write(po_str)
    print("> DONE! > Extracted to: " + pot_path) 
