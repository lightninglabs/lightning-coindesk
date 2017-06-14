(function($) {
  $(document).ready(function () {
    $('.post').each(function (_, post) {
      $(post).find('.hide_button').click(function() {
        $(post).css({ display: 'none' });
      });

      $(post).find('a.upvote').click(function (event) {
        event.preventDefault();
        $(post).find('.amount_wrapper').toggle('hide');
      });

      $(post).find('.amount').bind("enterKey", function (event) {
        event.preventDefault();
        $(post).find('.amount_submit').click();
      });

      $(post).find('.amount_submit').click(function (event) {
        event.preventDefault();
        var amount = $(post).find('.amount').val();
        var post_id = $(post).find('.upvote').data('id');
        window.location.href = '/upvote/' + post_id + '?amount=' + amount;
      });
    });

    // var onSubmit = function (event) {
    //   event.preventDefault();
    //   var title = $('#submit_title').val();
    //   var link = $('#submit_link').val();
    //   window.location.href = '/create-post?title=' + title + '&link=' + link;
    // };
    // $('#submit_button').click(onSubmit);
    // $('#submit_title').bind("enterKey", onSubmit);
    // $('#submit_link').bind("enterKey", onSubmit);
  });
})(jQuery);
