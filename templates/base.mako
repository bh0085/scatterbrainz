# -*- coding: utf-8 -*-
<html>
  <head>
    ${self.head_tags()}
  </head>
  <body>
    ${self.body_text()}
  </body>
  <footer>
    <br/> Footer for ${c.username}
  </footer>
</html>

<%def name="head_tags()">
    <title>Head tags section.</title>
</%def>

<%def name="body_text()">
blank base mako for body.
</%def>