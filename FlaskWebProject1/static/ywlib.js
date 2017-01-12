function DrawPad(unitWidthInPx, unitHeightInPx, nRow, nCol) {
	this.unitWidthInPx = unitWidthInPx;
	this.unitHeightInPx = unitHeightInPx;
	this.nRow = nRow;
	this.nCol = nCol;
	this.isMouseDown = false;

	var data = new Array();
	var xpos = 1; //starting xpos and ypos at 1 so the stroke will show when we make the grid below
	var ypos = 1;
	var click = 0;
	
	// iterate for rows	
	for (var row = 0; row < nRow; row++) {
		data.push( new Array() );
		
		// iterate for cells/columns inside rows
		for (var column = 0; column < nCol; column++) {
			data[row].push({
				x: xpos,
				y: ypos,
				width: unitWidthInPx,
				height: unitHeightInPx,
				click: click
			})
			// increment the x position. I.e. move it over by 10 (width variable)
			xpos += unitWidthInPx;
		}
		// reset the x position after a row is complete
		xpos = 1;
		// increment the y position for the next row. Move it down 10 (height variable)
		ypos += unitHeightInPx;	
	}

	this.data = data;
}

DrawPad.prototype.Bind = function(svgId, mouseOverFunc, mouseDownFunc, mouseUpFunc)
{
	this.svgId = svgId;

	var drawPad = d3.select(svgId)
		.attr("width",(this.unitWidthInPx * (this.nCol + 1)).toString() + "px")
		.attr("height",(this.unitHeightInPx * (this.nRow + 1)).toString() + "px");
		
	var bigrow = drawPad.selectAll(".row")
		.data(this.data)
		.enter().append("g")
		.attr("class", "row");
		
	var bigcolumn = bigrow.selectAll(".square")
		.data(function(d) { return d; })
		.enter().append("rect")
		.attr("class","square")
		.attr("x", function(d) { return d.x; })
		.attr("y", function(d) { return d.y; })
		.attr("width", function(d) { return d.width; })
		.attr("height", function(d) { return d.height; })
		.style("fill", "#fff")
		.style("stroke", "#222")
		.on('mouseover', mouseOverFunc)
	    .on('mousedown', mouseDownFunc)
    	.on('mouseup', mouseUpFunc);
}

DrawPad.prototype.ToJson = function()
{
	var sample  = [];
	for(var rowNo = 0; rowNo < this.data.length; rowNo++)
	{
		for(var colNo = 0; colNo < this.data[rowNo].length; colNo++)
		{
			sample.push(this.data[rowNo][colNo].click);
		}
	}

	return sample;
}


DrawPad.prototype.Clear = function()
{
	for(var rowNo = 0; rowNo < this.data.length; rowNo++)
	{
		for(var colNo = 0; colNo < this.data[rowNo].length; colNo++)
		{
			this.data[rowNo][colNo].click = 0;
		}
	}

	var drawPad = d3.select(this.svgId);

	var bigrow = drawPad.selectAll(".row")
		.data(this.data);

	var bigcolumn = bigrow.selectAll(".square")
		.data(function(d) { return d; })
		.style("fill", "#fff");
}


function ClassProbTuple(className, prob)
{
	this.className = className;
	this.prob = prob;
}

function SoftMaxOutput()
{
	this.nClass = 10;
	this.RandInit();
}

SoftMaxOutput.prototype.RandInit = function()		
{
	var softMaxOutput = [];
	var unnormalizedProbSum = 0;
	for(var i=0; i<this.nClass; i++)
	{
		unnormalizedProb = Math.random()
		unnormalizedProbSum += unnormalizedProb;
		softMaxOutput.push(new ClassProbTuple(i, unnormalizedProb));

	}
	for(var i=0; i<this.nClass; i++)
	{
		softMaxOutput[i].prob /= unnormalizedProbSum;
	}

	softMaxOutput.sort(function(d0, d1) {return d1.prob - d0.prob;})
	this.softMaxOutput = softMaxOutput;
}

SoftMaxOutput.prototype.Init = function(data)		
{
	var softMaxOutput = [];
	for(var i=0; i<this.nClass; i++)
	{
		softMaxOutput.push(new ClassProbTuple(i, data[i]));

	}

	softMaxOutput.sort(function(d0, d1) {return d1.prob - d0.prob;})
	this.softMaxOutput = softMaxOutput;			
}


SoftMaxOutput.prototype.Get = function()
{
	return this.softMaxOutput;
}

