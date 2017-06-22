/*jslint devel: true, browser: true, jquery: true */
(function($) {
  $(document).ready(function () {
    $('.article').each(function (_, article) {
      $(article).find('.hide_button').click(function() {
        $(article).css({ display: 'none' });
      });

      $(article).find('a.upvote').click(function (event) {
        event.preventDefault();
        $(article).find('.amount_wrapper').toggle('hide');
      });

      $(article).find('.amount').bind("enterKey", function (event) {
        event.preventDefault();
        $(article).find('.amount_submit').click();
      });

      $(article).find('.amount_submit').click(function (event) {
        event.preventDefault();
        var amount = $(article).find('.amount').val();
        var article_id = $(article).find('.upvote').data('id');
        window.location.href = '/upvote/' + article_id + '?amount=' + amount;
      });
    });

    // Show the text "Log out" on hover
    $('#username_display').hover(
      function() {
        var $this = $(this); // caching $(this)
        $this.data('initialText', $this.text());
        $this.text("Log out");
      },
      function() {
        var $this = $(this); // caching $(this)
        $this.text($this.data('initialText'));
      }
    );


    // var onSubmit = function (event) {
    //   event.preventDefault();
    //   var title = $('#submit_title').val();
    //   var link = $('#submit_link').val();
    //   window.location.href = '/create-article?title=' + title + '&link=' + link;
    // };
    // $('#submit_button').click(onSubmit);
    // $('#submit_title').bind("enterKey", onSubmit);
    // $('#submit_link').bind("enterKey", onSubmit);
  });
})(jQuery);
