<script type="text/javascript" src="/jquery-1.4.2.min.js"></script>
<script type = "text/javascript">
$(document).ready(function(){
	u = $("<ul>");
	u.attr("id","linklist");
	$("#links").append(u);
	u = $("<ul>");
	u.attr("id","proglist");
	$("#progress").append(u);
	$.each(${c.urls}, function(i,item){
	  a = $("<a>");
	  a.attr("href","#");
	  a.text(item);
	  $("#linklist").append($("<li>").append(a));
	  a.click(function(){$.getJSON(item,appendResults)});
	});
});
function appendResults(data){
	 li = $("<li>");
	 li.text(data);
         $("#proglist").append(li);
}
</script>
<div id=links>
</div>
<div id=progress>
Progress:
</div>