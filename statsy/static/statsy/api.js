(function($) {
    this.Statsy = function() {

    };

    Statsy.prototype.send = function(data) {
        $.post('/statsy/send/', data);
    };
}(jQuery));
