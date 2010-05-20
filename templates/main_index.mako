<script type="text/javascript" src="/jquery-1.4.2.min.js"></script>
<script type = "text/javascript">
$(document).ready(function(){
	u = $("<ul>");
	u.attr("id","linklist");
	$("#links").append(u);
	u = $("<ul>");
	u.attr("id","proglist");
	$("#progress").append(u);
	$.each(${c.all_controllers}, function(i,item){
	  a = $("<a>");
	  a.attr("href",item);
	  a.text(item);
	  $("#linklist").append($("<li>").append(a));
	});
});

</script>
Welcome to main<br/>
The following controllers (and probably others) are available.<br/>
If you haven't come by here yet, check out <a href="/init">/init</a>.<br/>
<div id=links>
</div>
