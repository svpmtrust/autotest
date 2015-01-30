(function($) {
	$(function(){
		$(document).ready(function(){

		$('ul.accordion li').click(function () {
			$(this).each(function() {
				$('ul.accordion li').removeClass('active');
				});
			$(this).addClass('active');
		});
		
		$('ul.accordion').accordion({
			active: ".active",
			autoHeight: false,
			header: ".opener",
			collapsible: true,
			event: "click"
		});
	});
	});
})(jQuery);

// background resize init
function initBackgroundResize() {
	var holder = document.getElementById('bg');
	if(holder) {
		var images = holder.getElementsByTagName('img');
		for(var i = 0; i < images.length; i++) {
			BackgroundStretcher.stretchImage(images[i]);
		}
		BackgroundStretcher.setBgHolder(holder);
	}
}

if (window.addEventListener) window.addEventListener("load", initBackgroundResize, false);
else if (window.attachEvent) window.attachEvent("onload", initBackgroundResize);

// image stretch module
BackgroundStretcher = {
	images: [],
	holders: [],
	viewWidth: 0,
	viewHeight: 0,
	ieFastMode: true,
	stretchBy: 'window', // "window", "page", "block-id", or block
	init: function(){
		this.addHandlers();
		this.resizeAll();
		return this;
	},
	stretchImage: function(origImg) {
		// wrap image and apply smoothing
		var obj = this.prepareImage(origImg);
		
		// handle onload
		var img = new Image();
		img.onload = this.bind(function(){
			obj.iRatio = img.width / img.height;
			this.resizeImage(obj);
		});
		img.src = origImg.src;
		this.images.push(obj);
	},
	prepareImage: function(img) {
		var wrapper = document.createElement('span');
		img.parentNode.insertBefore(wrapper, img);
		wrapper.appendChild(img);
	
		if(/MSIE (6|7|8)/.test(navigator.userAgent) && img.tagName.toLowerCase() === 'img') {
			wrapper.style.position = 'absolute';
			wrapper.style.display = 'block';
			wrapper.style.zoom = 1;
			if(this.ieFastMode) {
				img.style.display = 'none';
				wrapper.style.filter = 'progid:DXImageTransform.Microsoft.AlphaImageLoader(src="'+img.src+'", sizingMethod="scale")'; // enable smoothing in IE6
				return wrapper;
			} else {
				img.style.msInterpolationMode = 'bicubic'; // IE7 smooth fix
				return img;
			}
		} else {
			return img;
		}
	},
	setBgHolder: function(obj) {
		this.holders.push(obj);
		this.resizeAll();
	},
	resizeImage: function(obj) {
		if(obj.iRatio) {
			// calculate dimensions
			var dimensions = this.getProportion({
				ratio: obj.iRatio,
				maskWidth: this.viewWidth,
				maskHeight: this.viewHeight
			});
			// apply new styles
			obj.style.width = dimensions.width + 'px';
			obj.style.height = dimensions.height + 'px';
			obj.style.top = dimensions.top + 'px';
			obj.style.left = dimensions.left +'px';
		}
	},
	resizeHolder: function(obj) {
		obj.style.width = this.viewWidth+'px';
		obj.style.height = this.viewHeight+'px';
	},
	getProportion: function(data) {
		// calculate element coords to fit in mask
		var ratio = data.ratio || (data.elementWidth / data.elementHeight);
		var slideWidth = data.maskWidth, slideHeight = slideWidth / ratio;
		if(slideHeight < data.maskHeight) {
			slideHeight = data.maskHeight;
			slideWidth = slideHeight * ratio;
		}
		return {
			width: slideWidth,
			height: slideHeight,
			top: (data.maskHeight - slideHeight) / 2,
			left: (data.maskWidth - slideWidth) / 2
		}
	},
	resizeAll: function() {
		// crop holder width by window size
		for(var i = 0; i < this.holders.length; i++) {
			this.holders[i].style.width = '100%'; 
		}
		
		// delay required for IE to handle resize
		clearTimeout(this.resizeTimer);
		this.resizeTimer = setTimeout(this.bind(function(){
			// hide background holders
			for(var i = 0; i < this.holders.length; i++) {
				this.holders[i].style.display = 'none';
			}
			
			// calculate real page dimensions with hidden background blocks
			if(typeof this.stretchBy === 'string') {
				// resize by window or page dimensions
				if(this.stretchBy === 'window' || this.stretchBy === 'page') {
					this.viewWidth = this.stretchFunctions[this.stretchBy].width();
					this.viewHeight = this.stretchFunctions[this.stretchBy].height();
				}
				// resize by element dimensions (by id)
				else {
					var maskObject = document.getElementById(this.stretchBy);
					this.viewWidth = maskObject ? maskObject.offsetWidth : 0;
					this.viewHeight = maskObject ? maskObject.offsetHeight : 0;
				}
			} else {
				this.viewWidth = this.stretchBy.offsetWidth;
				this.viewHeight = this.stretchBy.offsetHeight;
			}
			
			// show and resize all background holders
			for(i = 0; i < this.holders.length; i++) {
				this.holders[i].style.display = 'block';
				this.resizeHolder(this.holders[i]);
			}
			for(i = 0; i < this.images.length; i++) {
				this.resizeImage(this.images[i]);
			}
		}),10);
	},
	addHandlers: function() {
		if (window.addEventListener) {
			window.addEventListener('resize', this.bind(this.resizeAll), false);
			window.addEventListener('orientationchange', this.bind(this.resizeAll), false);
		} else if (window.attachEvent) {
			window.attachEvent('onresize', this.bind(this.resizeAll));
		}
	},
	stretchFunctions: {
		window: {
			width: function() {
				return typeof window.innerWidth === 'number' ? window.innerWidth : document.documentElement.clientWidth;
			},
			height: function() {
				return typeof window.innerHeight === 'number' ? window.innerHeight : document.documentElement.clientHeight;
			}
		},
		page: {
			width: function() {
				return !document.body ? 0 : Math.max(
					Math.max(document.body.clientWidth, document.documentElement.clientWidth),
					Math.max(document.body.offsetWidth, document.body.scrollWidth)
				);
			},
			height: function() {
				return !document.body ? 0 : Math.max(
					Math.max(document.body.clientHeight, document.documentElement.clientHeight),
					Math.max(document.body.offsetHeight, document.body.scrollHeight)
				);
			}
		}
	},
	bind: function(fn, scope, args) {
		var newScope = scope || this;
		return function() {
			return fn.apply(newScope, args || arguments);
		}
	}
}.init();
// clear inputs on focus
function initInputs() {
	// replace options
	var opt = {
		clearInputs: true,
		clearTextareas: true,
		clearPasswords: true
	}
	// collect all items
	var inputs = [].concat(
		PlaceholderInput.convertToArray(document.getElementsByTagName('input')),
		PlaceholderInput.convertToArray(document.getElementsByTagName('textarea'))
	);
	// apply placeholder class on inputs
	for(var i = 0; i < inputs.length; i++) {
		if(inputs[i].className.indexOf('default') < 0) {
			var inputType = PlaceholderInput.getInputType(inputs[i]);
			if((opt.clearInputs && inputType === 'text') ||
				(opt.clearTextareas && inputType === 'textarea') || 
				(opt.clearPasswords && inputType === 'password')
			) {
				new PlaceholderInput({
					element:inputs[i],
					wrapWithElement:false,
					showUntilTyping:false,
					getParentByClass:false,
					placeholderAttr:'value'
				});
			}
		}
	}
}

// input type placeholder class
;(function(){
	PlaceholderInput = function() {
		this.options = {
			element:null,
			showUntilTyping:false,
			wrapWithElement:false,
			getParentByClass:false,
			placeholderAttr:'value',
			inputFocusClass:'focus',
			inputActiveClass:'text-active',
			parentFocusClass:'parent-focus',
			parentActiveClass:'parent-active',
			labelFocusClass:'label-focus',
			labelActiveClass:'label-active',
			fakeElementClass:'input-placeholder-text'
		}
		this.init.apply(this,arguments);
	}
	PlaceholderInput.convertToArray = function(collection) {
		var arr = [];
		for (var i = 0, ref = arr.length = collection.length; i < ref; i++) {
		 arr[i] = collection[i];
		}
		return arr;
	}
	PlaceholderInput.getInputType = function(input) {
		return (input.type ? input.type : input.tagName).toLowerCase();
	}
	PlaceholderInput.prototype = {
		init: function(opt) {
			this.setOptions(opt);
			if(this.element && this.element.PlaceholderInst) {
				this.element.PlaceholderInst.refreshClasses();
			} else {
				this.element.PlaceholderInst = this;
				if(this.elementType == 'text' || this.elementType == 'password' || this.elementType == 'textarea') {
					this.initElements();
					this.attachEvents();
					this.refreshClasses();
				}
			}
		},
		setOptions: function(opt) {
			for(var p in opt) {
				if(opt.hasOwnProperty(p)) {
					this.options[p] = opt[p];
				}
			}
			if(this.options.element) {
				this.element = this.options.element;
				this.elementType = PlaceholderInput.getInputType(this.element);
				this.wrapWithElement = (this.elementType === 'password' || this.options.showUntilTyping ? true : this.options.wrapWithElement);
				this.setOrigValue( this.options.placeholderAttr == 'value' ? this.element.defaultValue : this.element.getAttribute(this.options.placeholderAttr) );
			}
		},
		setOrigValue: function(value) {
			this.origValue = value;
		},
		initElements: function() {
			// create fake element if needed
			if(this.wrapWithElement) {
				this.element.value = '';
				this.element.removeAttribute(this.options.placeholderAttr);
				this.fakeElement = document.createElement('span');
				this.fakeElement.className = this.options.fakeElementClass;
				this.fakeElement.innerHTML += this.origValue;
				this.fakeElement.style.color = getStyle(this.element, 'color');
				this.fakeElement.style.position = 'absolute';
				this.element.parentNode.insertBefore(this.fakeElement, this.element);
			}
			// get input label
			if(this.element.id) {
				this.labels = document.getElementsByTagName('label');
				for(var i = 0; i < this.labels.length; i++) {
					if(this.labels[i].htmlFor === this.element.id) {
						this.labelFor = this.labels[i];
						break;
					}
				}
			}
			// get parent node (or parentNode by className)
			this.elementParent = this.element.parentNode;
			if(typeof this.options.getParentByClass === 'string') {
				var el = this.element;
				while(el.parentNode) {
					if(hasClass(el.parentNode, this.options.getParentByClass)) {
						this.elementParent = el.parentNode;
						break;
					} else {
						el = el.parentNode;
					}
				}
			}
		},
		attachEvents: function() {
			this.element.onfocus = bindScope(this.focusHandler, this);
			this.element.onblur = bindScope(this.blurHandler, this);
			if(this.options.showUntilTyping) {
				this.element.onkeydown = bindScope(this.typingHandler, this);
				this.element.onpaste = bindScope(this.typingHandler, this);
			}
			if(this.wrapWithElement) this.fakeElement.onclick = bindScope(this.focusSetter, this);
		},
		togglePlaceholderText: function(state) {
			if(this.wrapWithElement) {
				this.fakeElement.style.display = state ? '' : 'none';
			} else {
				this.element.value = state ? this.origValue : '';
			}
		},
		focusSetter: function() {
			this.element.focus();
		},
		focusHandler: function() {
			this.focused = true;
			if(!this.element.value.length || this.element.value === this.origValue) {
				if(!this.options.showUntilTyping) {
					this.togglePlaceholderText(false);
				}
			}
			this.refreshClasses();
		},
		blurHandler: function() {
			this.focused = false;
			if(!this.element.value.length || this.element.value === this.origValue) {
				this.togglePlaceholderText(true);
			}
			this.refreshClasses();
		},
		typingHandler: function() {
			setTimeout(bindScope(function(){
				if(this.element.value.length) {
					this.togglePlaceholderText(false);
					this.refreshClasses();
				}
			},this), 10);
		},
		refreshClasses: function() {
			this.textActive = this.focused || (this.element.value.length && this.element.value !== this.origValue);
			this.setStateClass(this.element, this.options.inputFocusClass,this.focused);
			this.setStateClass(this.elementParent, this.options.parentFocusClass,this.focused);
			this.setStateClass(this.labelFor, this.options.labelFocusClass,this.focused);
			this.setStateClass(this.element, this.options.inputActiveClass, this.textActive);
			this.setStateClass(this.elementParent, this.options.parentActiveClass, this.textActive);
			this.setStateClass(this.labelFor, this.options.labelActiveClass, this.textActive);
		},
		setStateClass: function(el,cls,state) {
			if(!el) return; else if(state) addClass(el,cls); else removeClass(el,cls);
		}
	}
	
	// utility functions
	function hasClass(el,cls) {
		return el.className ? el.className.match(new RegExp('(\\s|^)'+cls+'(\\s|$)')) : false;
	}
	function addClass(el,cls) {
		if (!hasClass(el,cls)) el.className += " "+cls;
	}
	function removeClass(el,cls) {
		if (hasClass(el,cls)) {el.className=el.className.replace(new RegExp('(\\s|^)'+cls+'(\\s|$)'),' ');}
	}
	function bindScope(f, scope) {
		return function() {return f.apply(scope, arguments)}
	}
	function getStyle(el, prop) {
		if (document.defaultView && document.defaultView.getComputedStyle) {
			return document.defaultView.getComputedStyle(el, null)[prop];
		} else if (el.currentStyle) {
			return el.currentStyle[prop];
		} else {
			return el.style[prop];
		}
	}
}());

if (window.addEventListener) window.addEventListener("load", initInputs, false);
else if (window.attachEvent) window.attachEvent("onload", initInputs);
// init rounded corners
function initRoundedCorners() {
	var images = document.getElementsByTagName('img');
	for(var i = 0; i < images.length; i++) {
		if(images[i].className.indexOf('rounded-corner-') != -1) {
			var radValue = parseInt(images[i].className.replace(/.*rounded-corner-(\d+).*/, '$1'),10);
			if(!isNaN(radValue)) {
				new ImgCorner({
					image: images[i],
					radius: radValue
				});
			}
		}
	}
}

// DOM ready
function domReady(handler){
	var called = false
	function ready() {
		if (called) return;
		called = true
		handler()
	}
	if (document.addEventListener) {
		document.addEventListener( "DOMContentLoaded", ready, false )
	} else if (document.attachEvent) {
		if (document.documentElement.doScroll && window == window.top) {
			function tryScroll(){
				if (called) return
				if (!document.body) return
				try {
					document.documentElement.doScroll("left")
					ready()
				} catch(e) {
					setTimeout(tryScroll, 0)
				}
			}
			tryScroll()
		}
		document.attachEvent("onreadystatechange", function(){
			if ( document.readyState === "complete" ) {
				ready()
			}
		})
	}
	if (window.addEventListener) window.addEventListener('load', ready, false)
	else if (window.attachEvent) window.attachEvent('onload', ready)
}

domReady(initRoundedCorners);



// rounded image module
;(function(window){
	// init VML for IE6, IE7, IE8
	var IE = /(MSIE (6|7|8))/.test(navigator.userAgent);
	if(IE) {
		var ns = 'rcr';
		if(document.namespaces && !document.namespaces[ns]) {
			// add VML namespace
			document.namespaces.add(ns,'urn:schemas-microsoft-com:vml','#default#VML'); 
			// create stylesheets
			var screenStyleSheet, printStyleSheet;
			screenStyleSheet = document.createElement('style');
			screenStyleSheet.setAttribute('media', 'screen');
			document.documentElement.firstChild.insertBefore(screenStyleSheet, document.documentElement.firstChild.firstChild);
			if (screenStyleSheet.styleSheet) {
				try {
					// add screen-media rule
					screenStyleSheet = screenStyleSheet.styleSheet;
					screenStyleSheet.addRule(ns + '\\:*', '{behavior:url(#default#VML); display:inline-block}');
					// add a print-media stylesheet
					printStyleSheet = document.createElement('style');
					printStyleSheet.setAttribute('media', 'print');
					document.documentElement.firstChild.insertBefore(printStyleSheet, screenStyleSheet);
					printStyleSheet = printStyleSheet.styleSheet;
					printStyleSheet.addRule(ns + '\\:*', '{display: none !important;}');
				} catch(e) {}
			}
		}
	}

	// browsers techniques support detection
	var supportCanvas = !!document.createElement('canvas').getContext;
	var supportBorderRadius = (function(){
		var cssAttributeNames = ['borderRadius','BorderRadius','MozBorderRadius','WebkitBorderRadius','OBorderRadius','KhtmlBorderRadius']; 
		for (var i = 0; i < cssAttributeNames.length; i++) {
			var attributeName = cssAttributeNames[i];
			if (document.documentElement.style[attributeName] !== undefined) {
				return true;
				break;
			}
		}
		return false;
	}());
	
	// rounded image class
	ImgCorner = function() {
		this.options = {
			radius: 0,
			image: null,
			roundedClass: 'img-rounded'
		}
		this.init.apply(this, arguments);
	}
	ImgCorner.prototype = {
		init: function(options) {
			for(var p in options) {
				if(options.hasOwnProperty(p)) {
					this.options[p] = options[p];
				}
			}
			this.initImage();
		},
		initImage: function() {
			// create image to calculate dimensions
			if(this.options.image) {
				// check borders
				this.realImage = this.options.image;
				this.borderWidth = parseInt(this.getStyle(this.realImage, 'borderTopWidth')) || 0;
				this.borderColor = this.getStyle(this.realImage, 'borderTopColor') || '#333';
			
				this.tmpImage = new Image();
				this.tmpImage.onload = this.bind(function() {
					this.realWidth = this.tmpImage.width;
					this.realHeight = this.tmpImage.height;
					this.onImageComplete();
				},this);
				this.tmpImage.src = this.realImage.src;
			}
		},
		onImageComplete: function() {
			if(IE) {
				this.createVMLNode();
			} else {
				if(supportBorderRadius) {
					this.createCSS3Node();
				} else if(supportCanvas) {
					this.createCanvasNode();
				}
			}
		},
		createCanvasNode: function() {
			var canvas = document.createElement('canvas'), ctx;
			canvas.width = this.realWidth + this.borderWidth*2;
			canvas.height = this.realHeight + this.borderWidth*2;
			if(typeof canvas.getContext === 'function') {
				// create path function
				var createPath = function(dc,x,y,w,h,r,bw) {
					var a = Math.PI/180;
					r -= bw;
					dc.beginPath();
					dc.moveTo(x+r,y);
					dc.lineTo(x+w-r,y);
					dc.arc(x+w-r,y+r,r,a*270,a*360,false);
					dc.lineTo(x+w,y+h-r);
					dc.arc(x+w-r,y+h-r,r,a*0,a*90,false);
					dc.lineTo(x+r,y+h);
					dc.arc(x+r,y+h-r,r,a*90,a*180,false);
					dc.lineTo(x,y+r);
					dc.arc(x+r,y+r,r,a*180,a*270,false); 
				}
			
				// create rounded path
				ctx = canvas.getContext('2d');
				ctx.save();
				createPath(ctx, this.borderWidth,this.borderWidth,this.realWidth,this.realHeight,this.options.radius, this.borderWidth);

				// draw border only if needed
				if(this.borderWidth) {
					ctx.strokeStyle = this.borderColor;
					ctx.lineWidth = this.borderWidth*2;
					ctx.stroke();
				}
				ctx.clip();
				ctx.drawImage(this.tmpImage,this.borderWidth,this.borderWidth);
				ctx.restore();

				// append canvas image
				this.realImage.style.display = 'none';
				this.realImage.parentNode.insertBefore(canvas, this.realImage);
			}
		},
		createVMLNode: function() {
			var w = this.realWidth, h = this.realHeight, r = this.options.radius;
			var vmlBox = document.createElement('corner');
			var sh = document.createElement(ns + ':shape');
			var filler = document.createElement(ns + ':fill');
			vmlBox.style.cssText = 'width:'+this.realWidth+'px;height:'+this.realHeight+'px;margin:0;padding:0;border:0;';
			sh.appendChild(filler);
			sh.style.cssText = 'width:'+this.realWidth+'px;height:'+this.realHeight+'px;display:inline-block;';
			sh.path = 'm '+r+',0 l '+(w-r)+',0 qx '+w+','+r+' l '+w+','+(h-r)+' qy '+(w-r)+','+h+' l '+r+','+h+' qx 0,'+(h-r)+' l 0,'+r+' qy '+r+',0 e';
			sh.coordorigin = "-1 -1";
			sh.coordsize = w+' '+h;

			// draw border if needed
			if(this.borderWidth) {
				sh.strokecolor = this.borderColor;
				sh.strokeweight = this.borderWidth/2;
				sh.stroked = true;
			} else {
				sh.stroked = false;
			}
			
			filler.style.display = 'inline-block';
			filler.setAttribute('type', 'frame');
			filler.setAttribute('src', this.realImage.src);
			vmlBox.appendChild(sh);
			vmlBox.innerHTML = vmlBox.innerHTML;
			this.realImage.style.display = 'none';
			this.realImage.parentNode.insertBefore(vmlBox, this.realImage);
		},
		createCSS3Node: function() {
			var borderAttr = ['borderRadius', 'MozBorderRadius', 'WebkitBorderRadius', 'OBorderRadius']; 
			var span = document.createElement('span');
			span.style.width = this.realWidth+'px';
			span.style.height = this.realHeight+'px';
			span.style.display = 'inline-block';
			span.style.background = 'url('+this.realImage.src+')';
			span.style.overflow = 'hiddden';
			
			for(var i = 0; i < borderAttr.length; i++) {
				span.style[borderAttr[i]] = this.options.radius + 'px';
			}
			
			// draw border if needed
			if(this.borderWidth) {
				span.style.border = this.borderWidth+'px solid '+this.borderColor;
			}
			
			this.realImage.style.border = '0';
			this.realImage.style.display = 'none';
			this.realImage.parentNode.insertBefore(span, this.realImage);
			span.appendChild(this.realImage);
			return span;
		},
		getStyle: function(el, prop) {
			if (document.defaultView && document.defaultView.getComputedStyle) {
				return document.defaultView.getComputedStyle(el, null)[prop];
			} else if (el.currentStyle) {
				return el.currentStyle[prop];
			} else {
				return el.style[prop];
			}
		},
		bind: function(fn, scope, args) {
			return function() {
				return fn.apply(scope, args || arguments);
			}
		} 
	}
})(this);
/*! HTML5 Shiv pre3.5 | @afarkas @jdalton @jon_neal @rem | MIT/GPL2 Licensed
  Uncompressed source: https://github.com/aFarkas/html5shiv  */
;(function(){
    /*@cc_on(function(a,b){function h(a,b){var c=a.createElement("p"),d=a.getElementsByTagName("head")[0]||a.documentElement;return c.innerHTML="x<style>"+b+"</style>",d.insertBefore(c.lastChild,d.firstChild)}function i(){var a=l.elements;return typeof a=="string"?a.split(" "):a}function j(a){var b={},c=a.createElement,f=a.createDocumentFragment,g=f();a.createElement=function(a){l.shivMethods||c(a);var f;return b[a]?f=b[a].cloneNode():e.test(a)?f=(b[a]=c(a)).cloneNode():f=c(a),f.canHaveChildren&&!d.test(a)?g.appendChild(f):f},a.createDocumentFragment=Function("h,f","return function(){var n=f.cloneNode(),c=n.createElement;h.shivMethods&&("+i().join().replace(/\w+/g,function(a){return b[a]=c(a),g.createElement(a),'c("'+a+'")'})+");return n}")(l,g)}function k(a){var b;return a.documentShived?a:(l.shivCSS&&!f&&(b=!!h(a,"article,aside,details,figcaption,figure,footer,header,hgroup,nav,section{display:block}audio{display:none}canvas,video{display:inline-block;*display:inline;*zoom:1}[hidden]{display:none}audio[controls]{display:inline-block;*display:inline;*zoom:1}mark{background:#FF0;color:#000}")),g||(b=!j(a)),b&&(a.documentShived=b),a)}function p(a){var b,c=a.getElementsByTagName("*"),d=c.length,e=RegExp("^(?:"+i().join("|")+")$","i"),f=[];while(d--)b=c[d],e.test(b.nodeName)&&f.push(b.applyElement(q(b)));return f}function q(a){var b,c=a.attributes,d=c.length,e=a.ownerDocument.createElement(n+":"+a.nodeName);while(d--)b=c[d],b.specified&&e.setAttribute(b.nodeName,b.nodeValue);return e.style.cssText=a.style.cssText,e}function r(a){var b,c=a.split("{"),d=c.length,e=RegExp("(^|[\\s,>+~])("+i().join("|")+")(?=[[\\s,>+~#.:]|$)","gi"),f="$1"+n+"\\:$2";while(d--)b=c[d]=c[d].split("}"),b[b.length-1]=b[b.length-1].replace(e,f),c[d]=b.join("}");return c.join("{")}function s(a){var b=a.length;while(b--)a[b].removeNode()}function t(a){var b,c,d=a.namespaces,e=a.parentWindow;return!o||a.printShived?a:(typeof d[n]=="undefined"&&d.add(n),e.attachEvent("onbeforeprint",function(){var d,e,f,g=a.styleSheets,i=[],j=g.length,k=Array(j);while(j--)k[j]=g[j];while(f=k.pop())if(!f.disabled&&m.test(f.media)){for(d=f.imports,j=0,e=d.length;j<e;j++)k.push(d[j]);try{i.push(f.cssText)}catch(l){}}i=r(i.reverse().join("")),c=p(a),b=h(a,i)}),e.attachEvent("onafterprint",function(){s(c),b.removeNode(!0)}),a.printShived=!0,a)}var c=a.html5||{},d=/^<|^(?:button|form|map|select|textarea|object|iframe)$/i,e=/^<|^(?:a|b|button|code|div|fieldset|form|h1|h2|h3|h4|h5|h6|i|iframe|img|input|label|li|link|ol|option|p|param|q|script|select|span|strong|style|table|tbody|td|textarea|tfoot|th|thead|tr|ul)$/i,f,g;(function(){var c=b.createElement("a");c.innerHTML="<xyz></xyz>",f="hidden"in c,f&&typeof injectElementWithStyles=="function"&&injectElementWithStyles("#modernizr{}",function(b){b.hidden=!0,f=(a.getComputedStyle?getComputedStyle(b,null):b.currentStyle).display=="none"}),g=c.childNodes.length==1||function(){try{b.createElement("a")}catch(a){return!0}var c=b.createDocumentFragment();return typeof c.cloneNode=="undefined"||typeof c.createDocumentFragment=="undefined"||typeof c.createElement=="undefined"}()})();var l={elements:c.elements||"abbr article aside audio bdi canvas data datalist details figcaption figure footer header hgroup mark meter nav output progress section summary time video",shivCSS:c.shivCSS!==!1,shivMethods:c.shivMethods!==!1,type:"default",shivDocument:k};a.html5=l,k(b);var m=/^$|\b(?:all|print)\b/,n="html5shiv",o=!g&&function(){var c=b.documentElement;return typeof b.namespaces!="undefined"&&typeof b.parentWindow!="undefined"&&typeof c.applyElement!="undefined"&&typeof c.removeNode!="undefined"&&typeof a.attachEvent!="undefined"}();l.type+=" print",l.shivPrint=t,t(b)})(this,document);@*/
}());