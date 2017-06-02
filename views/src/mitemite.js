properties = ['accessKey', 'align', 'alt', 'assignedSlot', 'autocapitalize', 'autocomplete', 'autofocus', 'baseURI', 'checked', 'childElementCount', 'children', 'classList', 'className', 'mite-input"', 'clientLeft', 'clientTop', 'clientWidth', 'contentEditable', 'dataset', 'defaultChecked', 'defaultValue', 'dir', 'dirName', 'disabled', 'draggable', 'files', 'form', 'formAction', 'formEnctype', 'formMethod', 'formNoValidate', 'formTarget', 'height', 'hidden', 'id', 'incremental', 'indeterminate', 'innerHTML', 'innerText', 'isConnected', 'isContentEditable', 'jQuery32100229671262483268631', 'labels', 'lang', 'list', 'localName', 'max', 'maxLength', 'min', 'minLength', 'multiple', 'name', 'namespaceURI', 'nodeName', 'nodeType', 'nodeValue', 'offsetHeight', 'offsetLeft', 'offsetTop', 'offsetWidth', 'onabort', 'onauxclick', 'onbeforecopy', 'onbeforecut', 'onbeforepaste', 'onblur', 'oncancel', 'oncanplay', 'oncanplaythrough', 'onchange', 'onclick', 'onclose', 'oncontextmenu', 'oncopy', 'oncuechange', 'oncut', 'ondblclick', 'ondrag', 'ondragend', 'ondragenter', 'ondragleave', 'ondragover', 'ondragstart', 'ondrop', 'ondurationchange', 'onemptied', 'onended', 'onerror', 'onfocus', 'ongotpointercapture', 'oninput', 'oninvalid', 'onkeydown', 'onkeypress', 'onkeyup', 'onload', 'onloadeddata', 'onloadedmetadata', 'onloadstart', 'onlostpointercapture', 'onmousedown', 'onmouseenter', 'onmouseleave', 'onmousemove', 'onmouseout', 'onmouseover', 'onmouseup', 'onmousewheel', 'onpaste', 'onpause', 'onplay', 'onplaying', 'onpointercancel', 'onpointerdown', 'onpointerenter', 'onpointerleave', 'onpointermove', 'onpointerout', 'onpointerover', 'onpointerup', 'onprogress', 'onratechange', 'onreset', 'onresize', 'onscroll', 'onsearch', 'onseeked', 'onseeking', 'onselect', 'onselectstart', 'onshow', 'onstalled', 'onsubmit', 'onsuspend', 'ontimeupdate', 'ontoggle', 'onvolumechange', 'onwaiting', 'onwebkitfullscreenchange', 'onwebkitfullscreenerror', 'onwheel', 'outerHTML', 'class="mite', 'pattern', 'placeholder', 'prefix', 'readOnly', 'required', 'scrollHeight', 'scrollLeft', 'scrollTop', 'scrollWidth', 'selectionDirection', 'selectionEnd', 'selectionStart', 'shadowRoot', 'size', 'slot', 'spellcheck', 'src', 'step', 'style', 'tabIndex', 'tagName', 'textContent', 'title', 'translate', 'type', 'useMap', 'validationMessage', 'validity', 'value', 'up', 'valueAsNumber', 'webkitEntries', 'webkitdirectory', 'webkitdropzone', 'width', 'willValidate']
attributes = []

 $(document).ready(function(){

    // the "href" attribute of .modal-trigger must specify the modal ID that wants to be triggered
    $('.modal').modal();
    $('.scrollspy').scrollSpy();
    $(".button-collapse").sideNav();
    
    $('.mite-input').each(function () {
    	$(this).on('input', function () {
    		miteUIGet($(this).attr('id'));
    	});
    });

    // ATTENTION
    // THIS BIT IS REAAAAALLLYYYYY IMPORTANT.
    $('.mite').each(function () {
    	props = [];
    	elem = this;
    	$.each(properties, function(x) {
			// this.attributes is not a plain object, but an array
			// of attribute nodes, which contain both the name and value
			console.log(this.name, this.value);
			props.push([properties[x], $(elem).prop(properties[x])]);
		});
		miteUIsetprop(this.id, props);
		
    });

    $('.mite.mite-input').on('change input propertychange paste', function() {
	  // Does some stuff and logs the event to the console
		props = []
		elem = this
		$.each(properties, function(x) {
			// this.attributes is not a plain object, but an array
			// of attribute nodes, which contain both the name and value
			props.push([properties[x], $(elem).prop(properties[x])]);
		});
		miteUIsetprop(this.id, props);
	});

	$('.mite.mite-text').on('DOMSubtreeModified', function() {
	  // Does some stuff and logs the event to the console
		props = []
		elem = this
		$.each(properties, function(x) {
			// this.attributes is not a plain object, but an array
			// of attribute nodes, which contain both the name and value
			props.push([properties[x], $(elem).prop(properties[x])]);
		});
		miteUIsetprop(this.id, props);
	});


	// Executes onReady Function on the script.
	preReadyInit();
 	if (typeof miteUIOnReady !== "undefined") { 

    	miteUIOnReady();
	}

 });


function popup(header, content){
	$('#popup-header').text(header);
	$('#popup-content').text(content);
	$('#popup').modal('open');
}

function miteUIGet(id){
	x = $("#"+id).val();
	//console.log(id+"::"+x);
	miteUIcallback(id, x);
}

function moveTool(event){
	$("#map-container").css({top: event.clientY, left: event.clientX, position:'absolute'});
}