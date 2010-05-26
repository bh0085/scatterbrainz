# -*- coding: utf-8 -*-
<%inherit file="plugin.mako" />

<%def name="body_tags()">
body from what template
</%def>
<%def name="body_text()">
<div id='plugin_description'>
What.cd plugin... 

This plugin is registered for ${c.username}.
<div id='what_artists'>
  artists
</div>
<div id='what_albums'>
  albums
</div>

</div>
</%def>
<%def name="head_tags()">
${c.jsfiles}
<script type = "text/javascript">
  $(document).ready(function(){
	u = $("<ul>");
	$("#what_albums").append(u);

  %for elt in c.albumnames:
    u.append($("<li>").html("${elt}"));
  %endfor
	u = $("<ul>");
	$("#what_artists").append(u);

  %for elt in c.artistnames:
    u.append($("<li>").html("${elt}"));
  %endfor
  });
</script>
</%def>