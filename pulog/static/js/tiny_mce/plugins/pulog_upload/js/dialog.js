tinyMCEPopup.requireLangPack();

var UploadDialog = {
	init : function(url) {
		var f = document.forms[0];

		// Get the selected contents as text and place it in the input
		
		//f.somearg.value = tinyMCEPopup.getWindowArg('post_url');
	},

	insert : function(url,alt) {
		// Insert the contents from the input into the document
		tinyMCEPopup.editor.execCommand('mceInsertContent', false,'<img src=\"' + url + '\" alt=\"' + alt + '\" />');
		tinyMCEPopup.close();
	}
};

tinyMCEPopup.onInit.add(UploadDialog.init, UploadDialog);
