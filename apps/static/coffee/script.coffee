$ = jQuery

highlight = () ->
# Highlights all <pre><code class="...">...</code></pre> on the page.
  for elem in $('pre code')
    hljs.highlightBlock(elem)

  iframe = document.getElementsByClassName('wysihtml5-sandbox')[0]
  if iframe
    idoc = iframe.contentDocument || iframe.contentWindow.document;
    blocks = $(idoc).find('pre code')
    for elem in blocks
      do (elem) ->
        hljs.highlightBlock(elem)

$ ->
  hljs.tabReplace = '    '
  hljs.initHighlighting()
  highlight()

  $('.entry:odd').css('background-color': '#eee');

  return false
