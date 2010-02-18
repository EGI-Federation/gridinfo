	var alwayscombo={
		//Position of com box from window edge ["top|bottom", "left|right"]
		location: ["top", "right"],
		//Additional offset from specified location above [vertical, horizontal]
		addoffset: [190, window.innerWidth/2-470],
		//ID of div containing the floating element
		comboid: "entry",
	
		floatcombo:function(){
			var docElement=(document.compatMode=='CSS1Compat')? document.documentElement: document.body
			this.comboref.height=window.innerHeight-200;
			if (this.location[0]=="top") {
				this.comboref.style.top=0+this.addoffset[0]+"px";
			} else if (this.location[0]=="bottom")
				this.comboref.style.bottom=0+this.addoffset[0]+"px"
			if (this.location[1]=="left")
				this.comboref.style.left=0+this.addoffset[1]+"px"
			else if (this.location[1]=="right")
				this.comboref.style.right=0+this.addoffset[1]+"px"
		},
	
		init:function(){
			this.comboref=document.getElementById(this.comboid)
			this.comboref.style.visibility="visible"
			this.floatcombo()
		}
	}


	if (window.addEventListener)
		window.addEventListener("load", function(){alwayscombo.init()}, false)
	else if (window.attachEvent)
		window.attachEvent("onload", function(){alwayscombo.init()})

