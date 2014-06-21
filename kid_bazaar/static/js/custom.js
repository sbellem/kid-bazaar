(function($) {

    $(function() {
        var $bodyContainer = $('.body-container');
        var bodyContainer_paddingTop = parseInt($bodyContainer.css('padding-top').slice(0, -2));

        var fix_heights = function() {
            var alerts = $('.navbar .alert');
            var newPaddingTop = bodyContainer_paddingTop;
            for (var i = 0; i < alerts.length; i++) {
                var $alert = $(alerts[i]);
                newPaddingTop += $alert.outerHeight(true);
            }
            $bodyContainer.css('padding-top', newPaddingTop.toString() + 'px');
        }
      $parent.detach().trigger('closed.bs.alert').remove()
      //$parent.trigger('closed.bs.alert').remove()
        fix_heights();
        $('.navbar .alert').bind('closed.bs.alert', fix_heights);
    });

})(jQuery);

