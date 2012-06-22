var $, highlight;

$ = jQuery;

highlight = function() {
  var blocks, elem, idoc, iframe, _i, _j, _len, _len2, _ref, _results;
  _ref = $('pre code');
  for (_i = 0, _len = _ref.length; _i < _len; _i++) {
    elem = _ref[_i];
    hljs.highlightBlock(elem);
  }
  iframe = document.getElementsByClassName('wysihtml5-sandbox')[0];
  if (iframe) {
    idoc = iframe.contentDocument || iframe.contentWindow.document;
    blocks = $(idoc).find('pre code');
    _results = [];
    for (_j = 0, _len2 = blocks.length; _j < _len2; _j++) {
      elem = blocks[_j];
      _results.push((function(elem) {
        return hljs.highlightBlock(elem);
      })(elem));
    }
    return _results;
  }
};

$(function() {
  hljs.tabReplace = '    ';
  hljs.initHighlighting();
  highlight();
  $('.entry:odd').css({
    'background-color': '#eee'
  });
  return false;
});
