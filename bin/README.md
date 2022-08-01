# Converters

## dutrToPo.py

Converts old *DuTranslator JSON* files to standard PO files for editing translations.

## dutrToPot.py

Converts old *DuTranslator JSON* files to standard POT (templates) files for editing translations.

## po2json.js

Converter based on the excellent [po2json](https://github.com/mikeedwards/po2json) project that will dump your `.po` files into the proper json format to use with *gettext.jsxinc* below:

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

Use `bin/po2json.js input.po output.json` or `bin/po2json.js input.po output.json -p` for pretty format.