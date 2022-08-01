# gettext.jsxinc

gettext.jsxinc is a lightweight GNU gettext port for Adobe ExtendScript. Manage your i18n translations the right way in your Adobe projects.

This project is forked from [gettext.js](https://guillaumepotier.github.io/gettext.js/) by [Guillaume Potier](https://github.com/guillaumepotier) (thanks!).

## Usage

### Load your messages

You can load your messages these ways:

```javascript
// i18n.setMessages(domain, locale, messages, plural_form);
i18n.setMessages('messages', 'fr', {
  "Welcome": "Bienvenue",
  "There is %1 apple": [
    "Il y a %1 pomme",
    "Il y a %1 pommes"
  ]
}, 'nplurals=2; plural=n>1;');
```

```javascript
// i18n.loadJSON(jsonData /*, domain */);
var json = {
  "": {
    "language": "fr",
    "plural-forms": "nplurals=2; plural=n>1;"
  },
  "Welcome": "Bienvenue",
  "There is %1 apple": [
    "Il y a %1 pomme",
    "Il y a %1 pommes"
  ]
};
i18n.loadJSON(json, 'messages');
```

See Required JSON format section below for more info.

### Set the locale

```javascript
i18n.setLocale('fr');
```

### Gettext functions

* **`gettext(msgid)`**: Translate a string. Shorthands are **`__()`**, **`_()`**, **`tr()`**.
* **`ngettext(msgid, msgid_plural, n)`**: Translate a pluralizable string. Shorthand is **`_n()`**.
* **`pgettext(msgctxt, msgid)`**: Translate a string specified by context. Shorthand is **`_p()`**.
* **`dcnpgettext(domain, msgctxt, msgid, msgid_plural, n)`**: Translate a potentially pluralizable string, potentially specified by context, and potentially of a different domain (as specified in `setMessages` or `loadJSON`). No shorthand.

### Example

```js
(function() {

 #include "../lib/gettext.js"

  i18n = i18n();

  i18n.setMessages('messages', 'en', {
    'Test failed!': 'Test successfull!',
  }, 'nplurals=2; plural=n>1;');

	i18n.setLocale('en');

	alert(i18n._('Test failed!'));
})();
```

### Variabilized strings

All four functions above can take extra arguments for variablization.

`gettext('There are %1 in the %2', 'apples', 'bowl');` -> "There are apples in the bowl

`ngettext('One %2', '%1 %2', 10, 'bananas');` -> "10 bananas"

It uses the public method `i18n.strfmt("string", var1, var2, ...)` you could reuse elsewhere in your project.

#### Literal percent sign (%)

When you need to have literal percent sign followed by a number (common in Hebrew or Turkish) you can escape it using another percent sign, for example:

`gettext('My credit card has an interest rate of %%%1', 20);` -> "My credit card has an interest rate of %20"

or without variables

`gettext('My credit card has an interest rate of %%20');` -> "My credit card has an interest rate of %20"

## Required JSON format and PO files

You'll find in `/bin` some converters to work with PO files and convert them to/from other formats.

## License

MIT
