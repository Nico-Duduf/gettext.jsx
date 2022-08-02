# Converters

These are Python scripts (because who wants to use ESTK or launch After Effects or Indesign to run simple scripts?) to help you convert to and from *PO* translation files.

## dutrToPo.py

Converts old *DuTranslator JSON* files to standard PO files for editing translations.

## dutrToPot.py

Converts old *DuTranslator JSON* files to standard POT (templates) files for editing translations.

## po2json.py

Converter that will dump your `.po` files into the proper json format to use with *gettext.jsxinc* below:

```json
{
    "": {
        "language": "en",
        "plural-forms": "nplurals=2; plural=(n!=1);"
    },
    "simple key": "It's tranlation",
    "another with %1 parameter": "It's %1 tranlsation",
    "a key with plural": [
        "a plural form",
        "another plural form",
        "could have up to 6 forms with some languages"
    ],
    "a context\u0004a contextualized key": "translation here"
}
```

You need polib to run this script: `pip install polib`

## jsxincToPot.py

Extracts strings from a jsxinc source file.
For now there are a few limitations:

- There must be a single string per line
- Translators comments must be at the end of the same line. They must start with `// TRANSLATORS:` or `/// TRANSLATORS:`