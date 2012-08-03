// Opens Terms and Services page in overlay window    
$().ready(function() { 
	$(document).ready(function() {
		$('#signupForm a').each(function() {
			var $link = $(this);
			var $dialog = $('<div id="terms" class="dialog"></div>')
				.load($link.attr('href') + ' .bod')
				.dialog({
					autoOpen: false,
					title: "Terms and Conditions",
                    width: 600,
                    height: 400,
                    modal: true,
                    resizable: false,
				});

			$link.click(function() {
				$dialog.dialog('open');

				return false;
			});
		});
	});
});
