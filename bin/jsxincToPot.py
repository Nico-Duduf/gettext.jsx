from genericpath import isfile
import os
import re

source_paths = (
    "../../After-Effects/Duik/inc",
    "../../After-Effects/Duik/DuSan/inc",
    "../../After-Effects/Duik/DuGR/inc",
    "../../After-Effects/Duik/DuIO/inc",
    "../../After-Effects/Duik/DuAEF/inc",
    "../../After-Effects/Duik/DuAEF/DuESF/inc",
)
pot_path = "../../After-Effects/Duik/translation/Duik.pot"

po_str = """# Translations template for Duik.
# Copyright (C) 2022 RxLaboratory
# This file is distributed under the same license as the Duik project.
# RxLaboratory <contact@rxlaboratory.org>, 2022.
#
#, fuzzy
msgid ""
msgstr ""
"Project-Id-Version: Duik 17.0.X\\n"
"POT-Creation-Date: 2022-08-10 17:30\\n"
"PO-Revision-Date: \\n"
"Last-Translator: \\n"
"Language-Team: RxLaboratory <http://rxlaboratory.org>\\n"
"MIME-Version: 1.0\\n"
"Content-Type: text/plain; charset=UTF-8\\n"
"Content-Transfer-Encoding: 8bit\\n"
"Genereated-By: gettext.jsxinc\\n"
"""

po_ids = []

re_source = re.compile('(?:\\s+|\\.)(?:_|__|tr|gettext)\\s*\\(?\\s*("|\')((?:\\\\\\1|(?:(?!\\1).))*)\\1(?:(?:.*\\s*\\/\\/\\\/?\\s*TRANSLATORS:\\s*)(.+))?')
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
        po_str += "\n#. \"" + comment + "\""

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

def extract( source_path ):
    for source_name in os.listdir(source_path):
        source = source_path + "/" + source_name
        if os.path.isfile(source):
            if not source_name.lower().endswith(".jsxinc"):
                continue
            if source_name.lower() == "translator.jsxinc":
                continue
            found = False
            with open(source, 'r', encoding="utf8") as source_file:
                line_num = 1
                for line in source_file.readlines():
                    match = re_source.search( line )
                    if match:
                        found = True
                        insertEntry( match.group(2),
                            comment=match.group(3),
                            source_name=source_name,
                            source_line=line_num
                            ) 
                        
                    match = re_source_plural.search( line )
                    if match:
                        found = True
                        insertEntry(match.group(2),
                            comment=match.group(5),
                            msgid_plural = match.group(4),
                            source_name=source_name,
                            source_line=line_num
                            )
                    
                    match = re_source_context.search( line )
                    if match:
                        found = True
                        insertEntry(match.group(4),
                            comment=match.group(5),
                            msgctxt = match.group(2),
                            source_name=source_name,
                            source_line=line_num
                            ) 
                        
                    
                    line_num += 1

                if found:
                    print("Found strings in " + source)

        elif os.path.isdir(source):
            extract(source)

for source_path in source_paths:
    extract(source_path)

with open(pot_path, 'w', encoding="utf8") as pot_file:
    pot_file.write(po_str)
    print("> DONE! > Extracted to: " + pot_path) 
