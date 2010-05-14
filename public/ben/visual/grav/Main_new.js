var delta = [0,0];
var gforce = [0,100];
var stage = [window.screenX,window.screenY,window.innerWidth,window.innerHeight];
getBrowserDimensions();

var isPlaying = false;
var isMouseDown = false;

var walls = new Array();
var wall_thickness = 200;
var wallsSetted = false;

var worldAABB;
var world;
var iterations = 1;
var timeStep = 1/25;

var mouseJoint;
var mouseX = 0;
var mouseY = 0;

var mouseOnClick = new Array();

var timer = 0;
//var stats = new Stats();
var elements = new Array();
var bodies = new Array();
var properties = new Array();

init()

function init()
{

	canvas = document.getElementById('canvas');
	
	document.onmousedown = onDocumentMouseDown;
	document.onmouseup = onDocumentMouseUp;
	document.onmousemove = onDocumentMouseMove;
	document.ondblclick = onDocumentDoubleClick;
	
	document.onkeypress = onDocumentKeyPress;

	// init box2d
	
	worldAABB = new b2AABB();
	worldAABB.minVertex.Set(-200, -200);
	worldAABB.maxVertex.Set( screen.width + 200, screen.height + 200);

	world = new b2World(worldAABB, new b2Vec2(0, 0), true);
	
	// walls	
	setWalls();

	elements = getElementsByClass("box2d");
		
	for (i = 0; i < elements.length; i++)
	{
		var element = elements[i];
		properties[i] = findPos(element);
		properties[i][2] = element.offsetWidth;
		properties[i][3] = element.offsetHeight;
	}
	
	for (i = 0; i < elements.length; i++)
	{
		var element = elements[i];
		element.style['position'] = 'absolute';
		element.style['left'] = properties[i][0] + 'px';
		element.style['top'] = properties[i][1] + 'px';
		element.style['backgroundColor'] = '#ffff00';
		element.onmousedown = onElementMouseDown;
		element.onmouseup = onElementMouseUp;
		element.onclick = onElementClick;
		
		bodies[i] = createBox(world, properties[i][0] + (properties[i][2] >> 1), properties[i][1] + (properties[i][3] >> 1), properties[i][2] / 2, properties[i][3] / 2, false);		
	}
}

function play()
{
	setInterval(loop, 25);	
}

// .. ACTIONS

function onDocumentMouseDown()
{
	isMouseDown = true;
	return false;
}

function onDocumentMouseUp()
{
	isMouseDown = false;
	return false;
}

function onDocumentMouseMove()
{
	if (!isPlaying)
	{
		isPlaying = true;
		play();
	}
	
	mouseX = window.event.clientX;
	mouseY = window.event.clientY;
}

function onDocumentDoubleClick()
{
	for (i = 0; i < resultBodies.length; i++)
	{
		var body = resultBodies[i]
		canvas.removeChild( body.GetUserData().element );
		world.DestroyBody(body);
		body = null;
	}
	
	resultBodies = new Array();
}

function onDocumentKeyPress(e)
{
	if (e.charCode == 13)
		search();
}

function onElementMouseDown()
{
	mouseOnClick[0] = window.event.clientX;
	mouseOnClick[1] = window.event.clientY;	
	return false;
}

function onElementMouseUp()
{
	return false;
}

function onElementClick()
{
	var range = 5;
	
	if (mouseOnClick[0] > window.event.clientX + range || mouseOnClick[0] < window.event.clientX - range && mouseOnClick[1] > window.event.clientY + range || mouseOnClick[1] < window.event.clientY - range)
		return false;
	
	if (this == document.getElementById('btnG')) search();
	if (this == document.getElementById('btnI')) imFeelingLucky();
	if (this == document.getElementById('q')) document.f.q.focus();
}



function loop()
{
	if (getBrowserDimensions())
		setWalls();

	delta[0] += (0 - delta[0]) * .5;
	delta[1] += (0 - delta[1]) * .5;
	
	world.m_gravity.x =  delta[0] + gforce[0];
	world.m_gravity.y =  delta[1] + gforce[1];

	mouseDrag();
	world.Step(timeStep, iterations);	
	
	for (i = 0; i < elements.length; i++)
	{
		var element = elements[i];
		
		element.style['left'] = (bodies[i].m_position0.x - (properties[i][2] >> 1)) + 'px';
		element.style['top'] = (bodies[i].m_position0.y - (properties[i][3] >> 1)) + 'px';
		
		// webkit
		element.style['-webkit-transform'] = 'rotate(' + (bodies[i].m_rotation0 * 57.2957795) + 'deg)';
		
		// gecko
		element.style['MozTransform'] = 'rotate(' + (bodies[i].m_rotation0 * 57.2957795) + 'deg)';

		// opera
		element.style['OTransform'] = 'rotate(' + (bodies[i].m_rotation0 * 57.2957795) + 'deg)';
	}
}


// .. BOX2D UTILS

function createBox(world, x, y, width, height, fixed, element)
{
	if (typeof(fixed) == 'undefined') fixed = true;
	var boxSd = new b2BoxDef();
	if (!fixed) boxSd.density = 1.0;
	boxSd.extents.Set(width, height);
	var boxBd = new b2BodyDef();
	boxBd.AddShape(boxSd);
	boxBd.position.Set(x,y);
	boxBd.userData = {element: element};
	return world.CreateBody(boxBd)
}

function mouseDrag()
{
	// mouse press
	if (isMouseDown && !mouseJoint)
	{
		var body = getBodyAtMouse();
		
		if (body)
		{
			var md = new b2MouseJointDef();
			md.body1 = world.m_groundBody;
			md.body2 = body;
			md.target.Set(mouseX, mouseY);
			md.maxForce = 30000.0 * body.m_mass;
			md.timeStep = timeStep;
			mouseJoint = world.CreateJoint(md);
			body.WakeUp();
		}
	}
	
	// mouse release
	if (!isMouseDown)
	{
		if (mouseJoint)
		{
			world.DestroyJoint(mouseJoint);
			mouseJoint = null;
		}
	}
	
	// mouse move
	if (mouseJoint)
	{
		var p2 = new b2Vec2(mouseX, mouseY);
		mouseJoint.SetTarget(p2);
	}
}

function getBodyAtMouse()
{
	// Make a small box.
	var mousePVec = new b2Vec2();
	mousePVec.Set(mouseX, mouseY);
	
	var aabb = new b2AABB();
	aabb.minVertex.Set(mouseX - 1, mouseY - 1);
	aabb.maxVertex.Set(mouseX + 1, mouseY + 1);

	// Query the world for overlapping shapes.
	var k_maxCount = 10;
	var shapes = new Array();
	var count = world.Query(aabb, shapes, k_maxCount);
	var body = null;
	
	for (var i = 0; i < count; ++i)
	{
		if (shapes[i].m_body.IsStatic() == false)
		{
			if ( shapes[i].TestPoint(mousePVec) )
			{
				body = shapes[i].m_body;
				break;
			}
		}
	}
	return body;
}

function setWalls()
{
	if (wallsSetted)
	{
		world.DestroyBody(walls[0]);
		world.DestroyBody(walls[1]);
		world.DestroyBody(walls[2]);
		world.DestroyBody(walls[3]);
		
		walls[0] = null; 
		walls[1] = null;
		walls[2] = null;
		walls[3] = null;
	}
	
	walls[0] = createBox(world, stage[2] / 2, - wall_thickness, stage[2], wall_thickness);
	walls[1] = createBox(world, stage[2] / 2, stage[3] + wall_thickness, stage[2], wall_thickness);
	walls[2] = createBox(world, - wall_thickness, stage[3] / 2, wall_thickness, stage[3]);
	walls[3] = createBox(world, stage[2] + wall_thickness, stage[3] / 2, wall_thickness, stage[3]);	
	
	wallsSetted = true;
}

// .. UTILS

function getElementsByClass( searchClass )
{
	var classElements = new Array();
	var els = document.getElementsByTagName('*');
	var elsLen = els.length
	for (i = 0, j = 0; i < elsLen; i++)
	{
		var classes = els[i].className.split(' ');
		for (k = 0; k < classes.length; k++)
			if ( classes[k] == searchClass )
				classElements[j++] = els[i];
	}
	return classElements;
}

function findPos(obj)
{
	var curleft = curtop = 0;
	if (obj.offsetParent)
	{
		do
		{
			curleft += obj.offsetLeft;
			curtop += obj.offsetTop;
		}
		while (obj = obj.offsetParent);
	}
	return [curleft,curtop];
}

function getBrowserDimensions()
{
	var changed = false;
		
	if (stage[0] != window.screenX)
	{
		delta[0] = (window.screenX - stage[0]) * 50;
		stage[0] = window.screenX;
		changed = true;
	}
	
	if (stage[1] != window.screenY)
	{
		delta[1] = (window.screenY - stage[1]) * 50;
		stage[1] = window.screenY;
		changed = true;
	}
	
	if (stage[2] != window.innerWidth)
	{
		stage[2] = window.innerWidth;
		changed = true;
	}
	
	if (stage[3] != window.innerHeight)
	{
		stage[3] = window.innerHeight;
		changed = true;
	}
	
	return changed;
}	
