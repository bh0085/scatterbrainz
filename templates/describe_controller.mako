<script type="text/javascript" src="/jquery-1.4.2.min.js"></script>
<script type = "text/javascript">
$(document).ready(function(){
	u = $("<ul>");
	u.attr("id","linklist");
	$("#links").append(u);
	$.each(${c.methods}, function(i,item){
	console.log(item)
	  a = $("<a>");
	  v = '${c.cname}';
	  var2 = item['n'];
	  a.attr("href",'/'+v+'/'+var2);
	  a.text(item['n']);
	  d = $("<div>").text(item['d']);
	  $("#linklist").append($("<li>").append(a).append(d));
	});
});

</script>
Welcome to ${c.cname}<br/>
<br/>
${c.cdesc}
<br/>
<br/>
The following methods (and probably others) are available.<br/>
<div id=links>
</div>
