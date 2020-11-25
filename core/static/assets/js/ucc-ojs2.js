

/*
  Functions to plot OJS data 
  on UCC implementation.
  
*/

var ucc = {}
ucc.minRadius = 2
ucc.width = 860
ucc.height = 350

//Octagon order
ucc.face=[3,1,0,6,7,1,0,6,7,0,6]

ucc.radians=function (deg){
    return deg*2*Math.PI/360
}

ucc.radius= function (){
    return Math.min(ucc.width/(uccJournals.length+4),80)
}
ucc.journalColors = {'co':'#80ba27','di':'#c61552','in':'#ee7d00','ml':'cyan','od':'#2092a8','pe':'#f7d537','ra':'#ec1557','sp':'#888ed2'};

ucc.randomize = function (a){
    var aa = Array.from(a),res=[];
    var r=0,l = aa.length;
    for (i=0;i<l;i++){
	r=Math.floor((Math.random()*aa.length));
	res.push(aa[r]);
	aa.splice(r,1);
    }
    return res
}

ucc.closeTip = function (dvid){
    d3.select("#"+dvid+"-tip")
	.style("pointer-events","none")
	.style("display","none")
	.html("")
}

ucc.defineNeonGlow=function(svg,std,id){
    if (id==undefined) id="glow"
    if (std==undefined) std=5
    var filter=svg.select("defs")
	.append("filter")
	.attr("id",id)
    filter.append("fegaussianblur")
	.attr("class","blur")
	.attr("result","coloredBlur")
	.attr("stdDeviation",std)
    var merge=filter.append("femerge")
    merge.append("femergenode").attr("in","coloredBlur")
    merge.append("femergenode").attr("in","coloredBlur")
    merge.append("femergenode").attr("in","coloredBlur")
    merge.append("femergenode").attr("in","SourceGraphic")
}

ucc.octagonPoints = function (x0,y0,r){
    var delta=r*Math.sin(ucc.radians(45))
    var apo=r*Math.cos(ucc.radians(22.5))
    var points=(x0)+","+(y0-r)+" "
    points+=(x0-delta)+","+(y0-delta)+" "
    points+=(x0-r)+","+y0+" "
    points+=(x0-delta)+","+(y0+delta)+" "
    points+=x0+","+(y0+r)+" "
    points+=(x0+delta)+","+(y0+delta)+" "
    points+=(x0+r)+","+y0+" "
    points+=(x0+delta)+","+(y0-delta)
    return points
}

ucc.showToolTip=function(sel,n){
    d3.selectAll(".tooltip").remove()
    var toolBox=document.getElementById("rev-"+sel.path).getBoundingClientRect()
    if (n<4){
	d3.select("#svg-inicio")
	    .append("div")
	    .attr("class","tooltip tright")
	    .style("position","fixed")
	    .style("border-color",ucc.journalColors[sel.path])
	    .style("left",(toolBox.left+((toolBox.right-toolBox.left)/2)+"px"))
	    .style("top",(toolBox.top)+"px")
	    .style("height",(toolBox.bottom-toolBox.top)+"px")
	    .style("width","0px")
    	    .html(sel.description)
	    .transition()
	    .duration(800)
	    .style("width",45+"vw")
	d3.select(".tright").select("p").style("margin-left",((toolBox.right-toolBox.left)/2)+"px")
    }
    else{
	d3.select("#svg-inicio")
	    .append("div")
	    .attr("class","tooltip tleft")
	    .style("position","fixed")
	    .style("border-color",ucc.journalColors[sel.path])
	    .style("left",(toolBox.left+((toolBox.right-toolBox.left)/2)+"px"))
	    .style("top",(toolBox.top)+"px")
	    .style("height",+(toolBox.bottom-toolBox.top)+"px")
	    .style("width","0px")
    	    .html(sel.description)
	    .transition()
	    .duration(800)
	    .style("width",45+"vw")
	    .style("transform","translate(-45vw)")
	d3.select(".tleft").select("p").style("margin-right",((toolBox.right-toolBox.left)/2)+"px")
    }
}

ucc.hideToolTip=function(){
    d3.selectAll(".tooltip")
	.remove()
}

ucc.drawJournals = function (svg,data,r,x0,y0){
    if (r==undefined) r=ucc.radius()
    var xi,yi,apo=r*Math.cos(ucc.radians(22.5))
    if (x0==undefined) xi=1.5*r
    else xi=x0
    if (y0==undefined) yi=1.5*r
    else yi=y0
    data.forEach(function (d,i){
	d.x1=Math.random()*ucc.width
	d.y1=Math.random()*ucc.height
	if (i>0){
	    xi+=(2*apo*Math.cos(ucc.radians(22.5+(ucc.face[i]*45))))
	    yi+=(2*apo*Math.sin(ucc.radians(22.5+(ucc.face[i]*45))))
	}
	d.x0=xi
	d.y0=yi
    })
    svg
	.on("mouseover",ucc.hideToolTip())
	.attr("viewBox","0 25 "+(ucc.width-20)+" "+ucc.height)
    
    svg.selectAll(".journal-group")
	.data(data).enter()
	.append("g")
	.attr("id",function (d){return "rev-"+d.path})
	.attr("class","journal-group")
	.append("a")
	.attr("xlink:href",function (d){return ucc.baseUrl+"/index.php/"+d.path})
	.append("polygon")
	.attr("class","journal")
	.attr("points",function (d,i){
	    return ucc.octagonPoints(d.x1,d.y1,r)
	})
	.style("stroke",function (d){return ucc.journalColors[d.path] ? ucc.journalColors[d.path] : "cyan"})
	.attr("filter","url(#glow)")
    svg.selectAll(".journal-group").append("image")
    .attr("id",function (d){return "img-"+d.path})
	.attr("xlink:href",function (d){return ucc.baseUrl+"/public/journals/"+d.idjournal+"/"+"w-"+d.path+".svg"})
//	    return d.pageHeaderLogoImage ? d.pageHeaderLogoImage.replace(/.*;s:29:.?"([^"]+)".*/,"w-$1") : "noLogo"})
	.attr("class","jlogo")
	.attr("x",function (d){return d.x1-(1.3*apo*Math.cos(45*2*Math.PI/360))})
	.attr("y",function (d){return d.y1-(apo*Math.sin(45*2*Math.PI/360)/2)})
	.attr("height",(apo*0.75)+"px")
	.attr("width",(apo*1.8)+"px")
	.attr("pointer-events","none")
    
    svg.selectAll(".journal-group").transition()
	.duration(2000)
	.attr("transform",function (d){
	    return "translate("+(d.x0-d.x1)+","+(d.y0-d.y1)+")"
	})
	.ease(d3.easeSinOut)
	.on("end",function(){
	    d3.selectAll(".journal-group")
		.on("mouseover",function(d,i){
		    d3.selectAll(".journal-group")
			.style("opacity",function(d2){
			    return d.path==d2.path ? 1 : 0.1
			})
			d3.select("#img-"+d.path)
			.attr("xlink:href",ucc.baseUrl+"/public/journals/"+d.idjournal+"/"+
			      d.pageHeaderLogoImage.replace(/.*;s:29:.?"([^"]+)".*/,"$1"))
		    ucc.showToolTip(d,i)
		})
	.on("mouseout",function(d){
		    d3.selectAll(".journal-group")
			.style("opacity",1)
			d3.select("#img-"+d.path)
			.attr("xlink:href",ucc.baseUrl+"/public/journals/"+d.idjournal+"/"+"w-"+d.path+".svg")
		    ucc.hideToolTip()})
	})
	 document.getElementById(svg.attr("id")).scrollIntoView(true)
}


// =====================================================
// Network graphics

ucc.colorRange = ["#4D9DE0","#E1BC29","#3BB273","#FF3C38","#7768AE","#FFA630","#326771","#C5E063","#70C1B3","#390832","#D72C6B","#OA0307","#FFFFFF","#000000"]

ucc.network = function (divId){
    var width = 960
    var height = 720
    this.div = d3.select("#"+divId)
    var tooltip = this.div.append("div")
	.attr("class","clustip")
	.attr("id",divId+"-tip")
	.style("position","absolute")
	.style("color","grey")
	.style("line-height","0.8")
	.style("max-width","40vw")
	.style("background-color","white")
	.style("border-radius","10px")
	.style("padding","7px")
	.style("max-height","50vh")
	.style("overflow","scroll")
    var colors=d3.scaleOrdinal().range(ucc.colorRange)
    var node = []
    var link = []
    var strength=-0.5
    var radius = d3.scaleSqrt().range([3,20]).domain([0,300])
    var linkScale = d3.scaleSqrt().range([0,5]).domain([0,100])
    var force = d3.forceSimulation()
	.force("link",d3.forceLink().id(function (d){return d.id}))
	.force("charge",d3.forceManyBody().strength(strength))
	.force("center",d3.forceCenter(width/2,height/2))
	.force("collide",d3.forceCollide()
	       .strength(0.98)
	       .radius(function (d){return radius(d.size)+8}))
    var data = []
    this.div
	.append('svg')
	.attr('id',divId+"-svg")
	.attr('viewBox','0 0 '+width+' '+height)
	.style('preserveAspectRatio','XMidYMid meet')
	.style('width',"100%")
    var svg = this.div.select("svg")
    var data = crossfilter()
    var dimensions={}
    var nodeAccessorId = function (d){return d.affiliation}
    var colorAccessor = function (d){
	return "one category"
    }
    var count=0
    var dtaos=[]
    //Data constructor
    var makeDataFromLinks = function(){
	var nodes=[],links=[],l1,l2,l,g
	data.allFiltered()
	    .map(function (x){
		g = x[linkAccess].map(function (d){return nodeAccessorId(d)})
		g=Array.from(new Set(g))
		for (var k=0;k<g.length;k++){
		    l1 = nodes.findIndex(function (nd){
			return nd.name == g[k]
		    })
		    if (l1<0) {
			l1=nodes.length
			nodes.push({'id':l1,'size':1,'name':g[k]})
		    }
		    else {nodes[l1].size++}
		    
		    for (var j=k+1;j<g.length;j++){
			l2=nodes.findIndex(function (nd){
			    return nd.name == g[j]
			})
			if (l2<0) {
			    l2=nodes.length
			    nodes.push({'id':l2,'size':0,'name':g[j]})
			}
			l=links.findIndex(function (l){
			    return ((l.source==l1 && l.target==l2) || (l.source==l2 && l.target==l1))
			})
			if (l<0){
			    links.push({'source':l1,'target':l2,'size':1})
			}
			else links[l].size++
		    }
		}
	    })
	return {'nodes':nodes,'links':links}
    }

    var drawer = function (){
	 datos = makeDataFromLinks()
	svg.selectAll(".net-items").remove()
	link = svg.append("g")
	    .attr("class","net-items")
	    .selectAll(".link")
	    .data(datos.links)
	    .enter().append("line")
	    .attr("class","link")
	    .style("stroke-width",function (l){
		return linkScale(l.size)
	    })
	node = svg.append("g")
	    .attr("class","net-items")
	    .selectAll(".node")
	    .data(datos.nodes)
	    .enter().append("circle")
	    .attr("class","node")
	    .attr("r",function (d){return radius(d.size)+"px"})
	    .attr("fill",function (n){
		return colors(colorAccessor(n))
	    })
	    .on("click",function (d){
		var dd = data.allFiltered().filter(function (x){
		    return x[linkAccess].find(function (y){return nodeAccessorId(y) == d.name})
		})
			
		var sel = d3.select("#"+divId+"-tip")
		    .style("pointer-events","auto")
		    .style("display","inline")
		    .html("<p><button onclick='ucc.closeTip(\""+divId+"\")'>[X]</button></p>")
		    .append("h5").text(d.name)
		    sel.append("ul").selectAll("li").data(dd)
		    .enter().append("li").html(function (d){
			return d.year+"<a href='https://revistas.ucc.edu.co/index.php/"+d.path+"/article/view/"+
			    d["submission_id"]+"' target='_blank'>"+d.cleanTitle+"</a> "

		    })
	    })
	force.nodes(datos.nodes)
	    .on("tick",ticked)
	force.force("link").links(datos.links)
	force.alpha(1).restart()
    }
    
    var ticked = function (){
	node.attr("cx",function (d){
	    var r = radius(d.size)
	    return d.x = Math.max(r,Math.min(d.x,width-r))
	})
	    .attr("cy",function (d){
		var r = radius(d.size)
		return d.y = Math.max(r,Math.min(d.y,height-r))
	    })
	link.attr("x1",function (d){return d.source.x})
	    .attr("y1",function (d){return d.source.y})
	    .attr("x2",function (d){return d.target.x})
	    .attr("y2",function (d){return d.target.y})
    }
    
    this.svg = function (s){
	if (arguments.lenth==0) return svg
	else{
	    svg = s
	    return this
	}
    }
    this.width=function(w){
	if (arguments.length==0) return width
	else {
	    width = w
	    return this
	}
    }
    this.height=function(h){
	if (arguments.length==0) return height
	else {
	    height = h
	    return this
	}
    }
    this.data = function (d){
	if (arguments.length==0) return data
	else {
	    data = crossfilter(d)
	    return this
	}
    }
    this.force = function(f){
	if (arguments.length==0) return force
	else {
	    force = f
	    return this
	}
    }
    this.colors = function (c){
	if (arguments.length==0) return colors
	else{
	    colors = d3.scaleOrdinal().range(c)
	    return this
	}
    }
    this.r = function (r){
	if (arguments.length==0) return radius
	else{
	    radius = r
	    return this
	}
    }
    this.nodeAccessorId = function (n){
	if (arguments.lentgh==0) return nodeAccessorId
	else{
	    nodeAccessorId=n
	    return this
	}
    }
    this.dimensions = function (d){
	if (arguments.length==0) return dimensions
	else {
	    dimensions={}
	    d.forEach(function (x){
		dimensions[x]=data.dimension(x)
	    })
	    return this
	}
    }
    this.drawer = function (val){
	if (arguments.length==0) return drawer
	else drawer = val
	return this
    }
    this.draw = function (){
	drawer()
	return this
    }
    this.getDim = function(dim){
	return dimensions[dim]
    }
    this.linkAccessor = function (l){
	if (arguments.length==0) return linkAccess
	else linkAccess = l
	return this
    }
    this.colorAccessor = function (c){
	if (arguments.length==0) return colorAccessor
	else colorAccessor = c
	return this
    }
    this.nodes = function (){
        return datos.nodes.length
    }
    this.links = function(){
        return datos.links.length
    }
    return this
}


// ========================================================
// Cluster Graphics
ucc.clusterRadius = 5
ucc.propClust = [{'name':'Autores','prop':'numAutor'},
		 {'name':'Referencias','prop':'numCitas'},
		 {'name':'Revista','prop':'revista'},
		 {'name':'Año','prop':'year'}]
ucc.clustering = function (divId){
    var colorScale = d3.scaleOrdinal().range(ucc.colorRange)
    var width = 960
    var height = 720
    this.div = d3.select("#"+divId)
    var tooltip = this.div.append("div")
	.attr("class","clustip")
	.attr("id",divId+"-tip")
	.style("position","absolute")
	.style("color","grey")
	.style("line-height","0.8")
	.style("max-width","40vw")
	.style("background-color","white")
	.style("border-radius","10px")
	.style("padding","7px")
    var svg = this.div
	.append('svg')
	.attr('id',divId+"-svg")
	.attr('viewBox','0 0 '+(width+250)+' '+height)
	.style('width','100%')
	.style('preserveAspectRatio','XMidYMid meet')
    var data = []
    var numClusters = 0
    var clusters=[]
    var radius = ucc.clusterRadius
    var force = d3.forceSimulation([])
	.force("collide",d3.forceCollide()
	       .strength(0.5)
	       .radius(function (d){return radius}))
    var cballs =[]
    var n,m
    var ticked = function(){
	data.forEach(function (d){
	    var k = 0.1*force.alpha()
	    d.x+=(((d.cluster%n)*(width/n))+(width/(2*n))-d.x)*k
	    d.y+=(((Math.floor(d.cluster/n)*(height/m)))+(height/(2*m))-d.y)*k
	})
	cballs.attr("cx",function (d){ return d.x})
	    .attr("cy",function (d){return  d.y})
    }
    var setClusters = function (prop,attr){
	var l,min,max,a,step
	clusters=[]
	if (typeof data[0][prop] == 'string'){
	    clusters=Array.from(new Set(data.map(function (d){return d[prop]}))).sort()
	    data.map(function (d){
		if (!(d.clabel)) d.clabel={}
		d[attr]=clusters.findIndex(function (x) {return d[prop] == x})
		d.clabel[attr]=d[prop]
	    })
	    numClusters = clusters.length
	}
	else {
	    a=data.map(function(d){return d[prop]}).sort(function (x,y){return x-y})
	    min=a[0]
	    max=a[a.length-1]
	    numClusters=1+(Math.round(Math.log(data.length)/Math.log(2)))
	    data.map(function (d){
		if (!(d.clabel)) d.clabel={}
		d[attr] = Math.floor(numClusters*(d[prop]-min)/(max-min))
		step = Math.floor((max-min)/numClusters)
		d.clabel[attr]="["+(d[attr]*step)+","+((d[attr]+1)*step)+")"
	    })
	}
    }
    this.draw = function (){
	cballs = svg.selectAll(".cball").data(data)
	    .enter().append("circle")
	    .attr("class","cball")
	    .attr("r",ucc.clusterRadius+"px")
	    .attr("cx",function (d){return d.x=(Math.random()*width)})
	    .attr("cy",function (d){return d.y=(Math.random()*height)})
	    .style("fill",ucc.colorRange[0])
	    .on("click",function (d){
		d3.select("#"+divId+"-tip")
		    .style("pointer-events","auto")
		    .style("display","inline")

		    .html("<button onclick='ucc.closeTip(\""+divId+"\")'>[X]</button>"+
			  "<p>"+d.autores.map(function (a){return a.name}).reduce(function (x,y){return x+", "+y})+" "+
			    "("+d.year+"). </p>")
	    })

	return this
    }
    this.cluster = function(prop){
	setClusters(prop,"cluster")
	n = Math.floor(Math.sqrt(numClusters))
	if (numClusters==n*n){m=n}
	else {n=n+1;m=n}
	svg.selectAll(".cball")
	force.nodes(data)
	    .on("tick",ticked)
	force.alpha(1).restart()
	svg.selectAll(".clabel").remove()
	var clabels=svg.selectAll(".clabel").data(d3.nest().key(function (d){return d.cluster}).entries(data))
	    .enter()
	    .append("text")
	    .attr("x",function (d){return ((d.values[0].cluster%n)*(width/n))+(width/(2*n))})
	    .attr("y",function (d){return ((Math.floor(d.values[0].cluster/n)*(height/m)))+(height/(2*m))})
	    .attr("class","clabel")
	    .style("text-anchor","middle")
	    .text(function (d) {return d.values[0].clabel["cluster"]+": "+d.values.length})
	return this
    }
    this.colorBy = function (prop){
	setClusters(prop,"color")
	colorScale = d3.scaleOrdinal().range(ucc.colorRange)
	var n =d3.nest().key(function (d){return d.color})
	    .entries(data)
	n=n.sort(function (x,y){return x.values[0][prop]<y.values[0][prop] ? -1 : 1})
	cballs.style("fill",function (d){return colorScale(d.color)})
	svg.selectAll(".clegend")
	    .remove()
	svg.selectAll(".cleglabel").remove()
	svg.selectAll(".clegend").data(n)
	    .enter()
	    .append("circle")
	    .attr("class","clegend")
	    .attr("r",7)
	    .attr("cx",function (d,i){return (width+30)})
	    .attr("cy",function (d,i){return (height*0.05*i)+20})
	    .style("fill",function (d){return colorScale(d.values[0].color)})
	svg.selectAll(".cleglabel")
	    .data(n).enter()
	    .append("text")
	    .attr("class","cleglabel")
	    .attr("x",function (d){return (width+50)})
	    .attr("y",function (d,i){return (height*0.05*i)+20})
	    .text(function (d){return d.values[0].clabel["color"]+": "+d.values.length})
	return this
    }
    this.data = function (d){
	if (arguments.length==0) return data
	else data = d
	return this
    }
    this.svg = function (s){
	if (arguments.length==0) return svg
	else svg = s
	return this
    }

    this.properties = function (d){
	if (arguments.length==0) return properties
	properties = d
	return this
    }
 /*   var properties = ucc.propClust
    menu.append("text").text("Agrupar por: ")
    var clusterButton = menu.append("select")
	.attr("id",divId+"-cluster")
	.on("change",function (d){cluster(d3.select(this).node().value)})
    clusterButton.selectAll("option").remove()
    clusterButton.selectAll("option")
	.data(properties).enter()
	.append("option")
	.attr("value",function (d){return d.prop})
	.text(function (d){return d.name});

    menu.append("text".text("Colorear por: ")
    var colorButton = menu.append("select")
	.attr("id",divId+"-color")
	.on("change",function (d){colorBy(d3.select(this).node().value)})
    colorButton.selectAll("option").remove()
    colorButton.selectAll("option")
	.data(properties).enter()
	.append("option")
	.attr("value",function (d){return d.prop})
	.text(function (d){return d.name})
*/
    return this
}

//   Red de palabras
// =====================================================

ucc.keyWords = function (divId){
	
    var width = 960
    var height = 720
    this.div = d3.select("#"+divId)
    var menu = this.div
	.append("div")
	.attr("id",divId+"-menu")

    var tooltip = this.div.append("div")
	.attr("class","clustip")
	.attr("id",divId+"-tip")
	.style("position","absolute")
	.style("color","grey")
	.style("line-height","0.8")
	.style("max-width","40vw")
	.style("background-color","white")
	.style("border-radius","10px")
	.style("padding","7px")
	.style("max-height","50vh")
	.style("overflow","scroll")
    var colors=d3.scaleOrdinal().range(ucc.colorRange)
    var node = []
    var link = []
    var strength=-2
    var radius = d3.scaleSqrt().range([0,20])
    var linkScale = d3.scaleSqrt().range([0,2])
    var force = d3.forceSimulation()
	.force("link",d3.forceLink().id(function (d){return d.id}))
	.force("charge",d3.forceManyBody().strength(strength))
    	.force("center",d3.forceCenter(width/2,height/2))
    	.force("collide",d3.bboxCollide(function (d,i) {
	    return [[-d.name.length*radius(d.size)/4, -radius(d.size)/2],[d.name.length*radius(d.size)/4, radius(d.size)/2]]
	})
	       .strength(0.1)
	       .iterations(1)).alpha(0.6)
    var data = []
    var zoom = d3.zoom().on("zoom",function (d){
	svg.select(".everything")
	    .attr("transform", d3.event.transform)})
	.scaleExtent([0.8,10])
    var svg = this.div
	.append('svg')
	.attr('id',divId+"-svg")
	.attr('viewBox','0 0 '+width+' '+height)
	.style('preserveAspectRatio','XMidYMid meet')
    svg.append("g").attr("class","everything")
	.call(zoom)

    var data = crossfilter()
    var dimensions={}
    var nodeAccessorId = function (d){return d}
    var colorAccessor = function (d){
	return "one category"
    }
    var count=0
    //Data constructor
    var makeDataFromLinks = function(){
	var nodes=[],links=[],l1,l2,l,g,max=-1,lmax=-1
	data.allFiltered()
	    .map(function (x){
		g = x[linkAccess].map(function (d){return nodeAccessorId(d)})
		g=Array.from(new Set(g))
		for (var k=0;k<g.length;k++){
		    if (g[k]=="") continue
		    l1 = nodes.findIndex(function (nd){
			return nd.name == g[k]
		    })
		    if (l1<0) {
			l1=nodes.length
			nodes.push({'id':l1,'size':1,'name':g[k]})
		    }
		    else {nodes[l1].size++}
		    if (nodes[l1].size>max) max=nodes[l1].size
		    
		    for (var j=k+1;j<g.length;j++){
			if (g[j]=="") continue
			l2=nodes.findIndex(function (nd){
			    return nd.name == g[j]
			})
			if (l2<0) {
			    l2=nodes.length
			    nodes.push({'id':l2,'size':0,'name':g[j]})
			}
			l=links.findIndex(function (l){
			    return ((l.source==l1 && l.target==l2) || (l.source==l2 && l.target==l1))
			})
			if (l<0){
			    l=links.length
			    links.push({'source':l1,'target':l2,'size':1})
			}
			else links[l].size++
			if (links[l].size>lmax) lmax=links[l].size
		    }
		}
		radius.domain([0,max])
		linkScale.domain([0,lmax])
	    })
	return {'nodes':nodes,'links':links}
    }

    var drawer = function (){
	var datos = makeDataFromLinks()
	losDatos=datos
	svg.selectAll(".net-items").remove()
	link = svg.select(".everything").append("g")
	    .attr("class","net-items")
	    .selectAll(".link")
	    .data(datos.links)
	    .enter().append("line")
	    .attr("class","link net-items")
	    .style("stroke-width",function (l){
		return 0.7
	    })
	node = svg.select(".everything").append("g")
	    .attr("class","net-items")
	    .selectAll(".node")
	    .data(datos.nodes)
	    .enter().append("text")
	    .attr("font-size",function (d){return radius(d.size)})
	    .attr("class","node net-items")
	    .style("fill",function (n){return n.size < 2 ? "#505050" : "#242e3d"})
	    .style("text-anchor","middle")
	    .on("click",function (d){
		var dd = data.allFiltered().filter(function (x){
		    return x[linkAccess].find(function (y){return nodeAccessorId(y) == d.name})
		})
			
		var sel = d3.select("#"+divId+"-tip")
		    .style("pointer-events","auto")
		    .style("display","inline")
		    .html("<p><button onclick='ucc.closeTip(\""+divId+"\")'>[X]</button></p>")
		    .append("h5").text(d.name)
		    sel.append("ul").selectAll("li").data(dd)
		    .enter().append("li").html(function (d){
			return "("+d.year+"). "+d.cleanTitle+"."
		    })
	    })
	    .on("mouseover",function (d){
		var s = d3.select("#"+divId+"-svg").selectAll(".link").classed("active",false).classed("inactive",true)
		var l = d3.select("#"+divId+"-svg").selectAll(".link")
		    .filter(function (x){return x.source.name==d.name || x.target.name==d.name})
		    .classed("active",true).classed("inactive",false)
	    })
	    .on("mouseout",function (d){
		d3.select("#"+divId+"-svg").selectAll(".link").classed("active",false).classed("inactive",false)
	    })
	    .text(function (d){return d.name})
	force.nodes(datos.nodes)
	    .on("tick",ticked)
	force.force("link").links(datos.links)
	force.alpha(1).restart()
    }
    
    var ticked = function (){
	node.attr("x",function (d){
	    var r = d.name.length*7
	    return d.x = Math.max(r,Math.min(d.x,width-r))
	})
	    .attr("y",function (d){
		var r = 2*d.size
		return d.y = Math.max(r,Math.min(d.y,height-r))
	    })
	link.attr("x1",function (d){return d.source.x})
	    .attr("y1",function (d){return d.source.y})
	    .attr("x2",function (d){return d.target.x})
	    .attr("y2",function (d){return d.target.y})
    }
    
    this.svg = function (s){
	if (arguments.lenth==0) return svg
	else{
	    svg = s
	    return this
	}
    }
    this.width=function(w){
	if (arguments.length==0) return width
	else {
	    width = w
	    return this
	}
    }
    this.height=function(h){
	if (arguments.length==0) return height
	else {
	    height = h
	    return this
	}
    }
    this.data = function (d){
	if (arguments.length==0) return data
	else {
	    data = crossfilter(d)
	    return this
	}
    }
    this.force = function(f){
	if (arguments.length==0) return force
	else {
	    force = f
	    return this
	}
    }
    this.colors = function (c){
	if (arguments.length==0) return colors
	else{
	    colors = d3.scaleOrdinal().range(c)
	    return this
	}
    }
    this.r = function (r){
	if (arguments.length==0) return radius
	else{
	    radius = r
	    return this
	}
    }
    this.nodeAccessorId = function (n){
	if (arguments.lentgh==0) return nodeAccessorId
	else{
	    nodeAccessorId=n
	    return this
	}
    }
    this.dimensions = function (d){
	if (arguments.length==0) return dimensions
	else {
	    dimensions={}
	    d.forEach(function (x){
		dimensions[x]=data.dimension(x)
	    })
	    return this
	}
    }
    this.drawer = function (val){
	if (arguments.length==0) return drawer
	else drawer = val
	return this
    }
    this.draw = function (){
	drawer()
    }
    this.getDim = function(dim){
	return dimensions[dim]
    }
    this.linkAccessor = function (l){
	if (arguments.length==0) return linkAccess
	else linkAccess = l
	return this
    }
    this.colorAccessor = function (c){
	if (arguments.length==0) return colorAccessor
	else colorAccessor = c
	return this
    }
    return this
}
