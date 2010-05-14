/*
Ancestry - jquery.ancestry.js
As discussed in the jQuery Development Google Group.
Released under the MIT license.

Involved: Michael Geary, Diego Perini, John-David Dalton, John Resig, and Nathan Hammond
Compiled: Nathan Hammond
*/

jQuery.comparePosition = function ( element, context ) {
	if ('compareDocumentPosition' in document.documentElement) {
		arguments.callee = function ( element, context ) {
			return !!(element.compareDocumentPosition(context) & 8);
		}
	} else if ('contains' in document.documentElement) {
		arguments.callee = function ( element, context ) {
			return (element	!= context && context.contains(element));
		}
	} else {
		arguments.callee = function ( element, context ) {
			while ( element && element = element.parentNode )
				if ( element == context ) return true;
			return false;
		}
	}
	return arguments.callee( element, context );
};

jQuery.fn.ancestorOf = function ( context ) {
	return this.filter(function() {
		return jQuery.comparePosition( context, this );
	});
};
jQuery.fn.descendantOf = function ( context ) {
	return this.filter(function() {
		return jQuery.comparePosition( this, context );
	});
};

/*
Noted here if you wish to add parallel functionality to $()

if ( selector.nodeType ) {
	// Handle $(DOMElement,	context)
	if ( context &&	!jQuery.comparePosition( selector, context ) ) {
		return jQuery( [] );
	}
	// Handle $(DOMElement)
	this[0]	= selector;
	this.length = 1;
	return this;
}
*/