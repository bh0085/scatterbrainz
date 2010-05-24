
<script type = text/javascript>
$(document).ready(function(){
  list = ${c.pluglist};
  names =  ${c.plugnames};
  ul = $("<ul>");  
  for ( var i = 0 ; i < list.length ; i ++){
  li = $("<li>").text(list[i] +'----'+ names[i] );
  ul.append(li);
  }
  $("#pluglist").append(ul);  
 });

</script>
<div id="header">
  The following plugins have been installed
</div>
<div id="pluglist"></div>
