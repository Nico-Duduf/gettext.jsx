// Avoid global variables
(function(){

#include "../lib/gettext.js"

    i18n = i18n();

    i18n.setMessages('messages', 'en', {
			'Test failed!': 'Test successfull!',
		}, 'nplurals=2; plural=n>1;');
	i18n.setLocale('en');

	alert(i18n._('Test failed!'));
})();