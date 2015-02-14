(function($) {
    this.Statsy = function() {
        this.url = $('#statsy_send_url').val();
    };

    Statsy.prototype.send = function(data) {
        updateWithCSRF(data);

        $.post(this.url, data);
    };

    function updateWithCSRF(data) {
        data['csrfmiddlewaretoken'] = $('input[name=csrfmiddlewaretoken]').val();
        return data;
    }
}(jQuery));
