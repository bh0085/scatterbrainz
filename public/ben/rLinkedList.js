function rCircularLinkedList(){
    this.nodeFirst = null;

    this.insertAtEnd = function(content){
	nodeNext = this.first;
	return this.insertBeforeNode(nodeNext,content);
    }

    this.insertBeforeNode = function(nodeNext,content){
	node = new rLinkedNode();
	node.contents = content;
	if (!nodeNext){
	    this.first = node;
	    node.next = node;
	    node.prev = node;
	} else {
	    node.next = nodeNext;
	    node.prev = nodeNext.prev;

	}
	node.prev.next = node;
	node.next.prev = node;
	return node;
    }
    
    this.destroyNode = function(node){
	node.next.prev = node.prev;
	node.prev.next = node.next;
	node = null;
    }
}

function rLinkedNode(){
    
}