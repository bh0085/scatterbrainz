var r_last_column_set;
var rcol_list = new rCircularLinkedList();

function rColumnHasBeenSet(rcol){
    r_last_column_set = rcol;
}

function rGetGenericTargetColumn(){
    if (!r_last_column_set){
	return rcol_list.first.contents;
    } else {
	console.log(r_last_column_set.colname);

	return r_last_column_set.my_node.next.contents;
    }
}


function rGetColumnClickEventTargetColumn(rcol){
    if (!rcol){
	return rcol_list.first.contents;
    } else {
	return rcol.my_node.next.contents;
    }
}
function rManagerMakeColumn(parent){
    rcol = new rCol2(parent);
    rcol.my_node = rcol_list.insertAtEnd(rcol);
    
    return rcol;
}


