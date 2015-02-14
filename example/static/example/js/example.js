$(function(){
    var statsy = new Statsy();

    $('.like-button').on('click', function() {
        statsy.send(
            {
                'group': 'js',
                'event': 'like',
                'value': 42,
                'related_object_id': $(this).attr('data-id'),
                'related_object_content_type_id': $(this).attr('data-content_type-id')
            }
        );

        return false;
    });

});
