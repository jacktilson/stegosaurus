(function(e){function t(t){for(var n,l,r=t[0],s=t[1],c=t[2],u=0,m=[];u<r.length;u++)l=r[u],i[l]&&m.push(i[l][0]),i[l]=0;for(n in s)Object.prototype.hasOwnProperty.call(s,n)&&(e[n]=s[n]);d&&d(t);while(m.length)m.shift()();return o.push.apply(o,c||[]),a()}function a(){for(var e,t=0;t<o.length;t++){for(var a=o[t],n=!0,r=1;r<a.length;r++){var s=a[r];0!==i[s]&&(n=!1)}n&&(o.splice(t--,1),e=l(l.s=a[0]))}return e}var n={},i={app:0},o=[];function l(t){if(n[t])return n[t].exports;var a=n[t]={i:t,l:!1,exports:{}};return e[t].call(a.exports,a,a.exports,l),a.l=!0,a.exports}l.m=e,l.c=n,l.d=function(e,t,a){l.o(e,t)||Object.defineProperty(e,t,{enumerable:!0,get:a})},l.r=function(e){"undefined"!==typeof Symbol&&Symbol.toStringTag&&Object.defineProperty(e,Symbol.toStringTag,{value:"Module"}),Object.defineProperty(e,"__esModule",{value:!0})},l.t=function(e,t){if(1&t&&(e=l(e)),8&t)return e;if(4&t&&"object"===typeof e&&e&&e.__esModule)return e;var a=Object.create(null);if(l.r(a),Object.defineProperty(a,"default",{enumerable:!0,value:e}),2&t&&"string"!=typeof e)for(var n in e)l.d(a,n,function(t){return e[t]}.bind(null,n));return a},l.n=function(e){var t=e&&e.__esModule?function(){return e["default"]}:function(){return e};return l.d(t,"a",t),t},l.o=function(e,t){return Object.prototype.hasOwnProperty.call(e,t)},l.p="/";var r=window["webpackJsonp"]=window["webpackJsonp"]||[],s=r.push.bind(r);r.push=t,r=r.slice();for(var c=0;c<r.length;c++)t(r[c]);var d=s;o.push([0,"chunk-vendors"]),a()})({0:function(e,t,a){e.exports=a("56d7")},"130e":function(e,t,a){},"16a3":function(e,t,a){"use strict";var n=a("130e"),i=a.n(n);i.a},"56d7":function(e,t,a){"use strict";a.r(t);a("cadf"),a("551c"),a("f751"),a("097d");var n=a("5f5b"),i=(a("f9e3"),a("2dd8"),a("2b0e")),o=function(){var e=this,t=e.$createElement,a=e._self._c||t;return a("div",{attrs:{id:"app"}},[a("Navbar"),a("router-view")],1)},l=[],r=function(){var e=this,t=e.$createElement,a=e._self._c||t;return a("b-navbar",{attrs:{toggleable:"lg",sticky:""}},[a("div",{staticClass:"container"},[a("b-navbar-brand",{staticClass:"my-0 mx-3"},[a("img",{attrs:{src:"/static/img/ct_logo.svg",height:"96px"}})]),a("b-navbar-toggle",{staticClass:"my-0 mx-0",attrs:{target:"nav-collapse"}},[a("font-awesome-icon",{attrs:{icon:"bars",size:"2x"}})],1),a("b-collapse",{staticClass:"mx-3",attrs:{id:"nav-collapse","is-nav":""}},[a("b-navbar-nav",{staticClass:"row w-100 text-lg-center"},[a("b-nav-item",{staticClass:"col-lg",attrs:{to:"/about"}},[e._v("About")]),a("b-nav-item",{staticClass:"col-lg",attrs:{to:"/encode"}},[e._v("Encode")]),a("b-nav-item",{staticClass:"col-lg",attrs:{to:"/decode"}},[e._v("Decode")])],1)],1)],1)])},s=[],c={name:"Navbar"},d=c,u=(a("16a3"),a("2877")),m=Object(u["a"])(d,r,s,!1,null,null,null),f=m.exports,b={components:{Navbar:f}},p=b,g=(a("5c0b"),Object(u["a"])(p,o,l,!1,null,null,null)),h=g.exports,v=a("8c4f"),F=function(){var e=this,t=e.$createElement,a=e._self._c||t;return a("b-container",[a("h1",[e._v("This is an about page")])])},w=[],x={},I=Object(u["a"])(x,F,w,!1,null,null,null),_=I.exports,y=function(){var e=this,t=e.$createElement,a=e._self._c||t;return a("b-container",[a("b-row",[a("b-col",{attrs:{sm:"12"}},[a("b-card",{staticClass:"mt-3"},[a("b-card-title",[e._v("Decode Data")]),a("b-card-text",[e._v("lorem ipsum")]),a("form",[a("b-form-group",[a("b-form-file",{attrs:{state:Boolean(e.imgFile),placeholder:"Decode image","drop-placeholder":"Drop your encoded image here to be decoded..."},on:{change:function(t){return e.imgFileChange(t)}},model:{value:e.imgFile,callback:function(t){e.imgFile=t},expression:"imgFile"}})],1),a("b-collapse",{attrs:{id:"imgFilePreviewCollapse"},model:{value:e.imgFile,callback:function(t){e.imgFile=t},expression:"imgFile"}},[a("b-card",{staticClass:"overflow-hidden mb-3",attrs:{"no-body":""}},[a("b-card-img",{staticClass:"rounded-0",attrs:{src:e.imgFileDataString}})],1)],1),a("b-button",{on:{click:e.submit}},[e._v("Decode")])],1)],1)],1)],1)],1)},k=[],C=a("bc3a"),E=a.n(C),D={IMG_FILE_INPUT:0,FORM_SUBMITTED:1,FORM_RESULT:2},S={name:"Decode",data:function(){return{pageState:D.DATA_FILE_INPUT,imgFile:null,imgFileDataString:""}},methods:{submit:function(){var e=new FormData;e.append("imgFile",this.imgFile),E.a.post("/decode",e,{headers:{"Content-Type":"multipart/form-data"}}).then(function(e){alert(e)}).catch(function(e){alert(e)})},imgFileChange:function(e){var t=this,a=e.target;if(a.files&&a.files[0]){var n=new FileReader;n.onload=function(e){t.imgFileDataString=e.target.result},n.readAsDataURL(a.files[0])}}}},O=S,T=Object(u["a"])(O,y,k,!1,null,null,null),B=T.exports,j=function(){var e=this,t=e.$createElement,a=e._self._c||t;return a("b-container",[a("b-row",[a("b-col",{attrs:{sm:"12"}},[a("b-card",{staticClass:"mt-3"},[a("b-card-title",[e._v("Encode Data")]),a("b-card-text",[e._v("Encode some data within a bitmap image file. The algorithm works by changing the colour values of the pixels of an image, embedding the data within the image. If the encoding is good, the\ndata will be undetectable to the naked eye. It overwrites the least significant bits of each colour\nchannel with the data to be hidden, changing the actual value by the smallest amount.")]),a("b-collapse",{model:{value:e.showForm,callback:function(t){e.showForm=t},expression:"showForm"}},[a("form",[a("b-form-group",{attrs:{label:"Image File","label-for":"input-imgFile","label-class":"font-weight-bold",description:e.validInputImgFile?"":"Enter a image file to hide your data inside.",state:e.validInputImgFile,"invalid-feedback":e.feedbackInvalidInputImgFile,"valid-feedback":e.feedbackValidInputImgFile}},[a("b-form-file",{attrs:{id:"input-imgFile",placeholder:"Choose a bmp/png file...","drop-placeholder":"Drop a bmp/png file here to encode to...",state:e.validInputImgFile},on:{change:function(t){return e.imgFileChange(t)}},model:{value:e.imgFile,callback:function(t){e.imgFile=t},expression:"imgFile"}})],1),a("b-collapse",{staticClass:"mb-3",model:{value:e.showImgInfo,callback:function(t){e.showImgInfo=t},expression:"showImgInfo"}},[a("b-card",{staticClass:"overflow-hidden",attrs:{"no-body":""}},[a("b-row",{attrs:{"no-gutters":""}},[a("b-col",{attrs:{lg:"6"}},[a("b-card-img",{staticClass:"rounded-0",attrs:{src:e.imgFileDataString}})],1),a("b-col",{attrs:{lg:"6"}},[a("b-card-body",{attrs:{title:"Image Preview"}},[a("b-card-text",[e._v("To be filled with info about image (width, height, channels, bit depth, estimated space available)")])],1)],1)],1)],1)],1),a("b-collapse",{model:{value:e.showDataInput,callback:function(t){e.showDataInput=t},expression:"showDataInput"}},[a("b-form-group",{attrs:{label:"Data File","label-for":"input-dataFile","label-class":"font-weight-bold",description:e.dataFile?"":"Enter a data file to encode onto the image",state:Boolean(e.dataFile),"valid-feedback":e.dataFile?"Awesome!":""}},[a("b-form-file",{attrs:{state:e.dataFile,placeholder:"Choose file to encode on to image...","drop-placeholder":"Drop file here to encode onto image..."},model:{value:e.dataFile,callback:function(t){e.dataFile=t},expression:"dataFile"}})],1)],1),a("b-collapse",{model:{value:e.showEncodeSettings,callback:function(t){e.showEncodeSettings=t},expression:"showEncodeSettings"}},[a("b-form-group",{attrs:{label:"Encoding Settings","label-class":"font-weight-bold"}},[a("b-form-group",{attrs:{label:"Bits: "+e.nBits,"label-for":"input-nBits","label-cols-lg":"2",description:"The number of bits to overwrite per channel of the image"}},[a("b-form-input",{attrs:{id:"nBitsInput",type:"range",min:"1",max:"8"},model:{value:e.nBits,callback:function(t){e.nBits=t},expression:"nBits"}})],1),a("b-form-group",[a("b-form-checkbox",{model:{value:e.encodeFilename,callback:function(t){e.encodeFilename=t},expression:"encodeFilename"}},[e._v("Encode filename")])],1),a("b-form-group",[a("b-form-checkbox",{model:{value:e.encodeFileExt,callback:function(t){e.encodeFileExt=t},expression:"encodeFileExt"}},[e._v("Encode file extension")])],1)],1)],1),a("b-button",{attrs:{disabled:!e.enableSubmit},on:{click:e.submit}},[e._v("Encode")])],1)]),a("b-collapse",{model:{value:e.showWaiting,callback:function(t){e.showWaiting=t},expression:"showWaiting"}},[a("b-card-text",[e._v("Waiting for a result...")])],1),a("b-collapse",{model:{value:e.showResult,callback:function(t){e.showResult=t},expression:"showResult"}},[a("b-card-text",[e._v("Result and download to go here")])],1)],1)],1)],1)],1)},R=[],P=(a("6762"),a("2fdb"),0),A=1,M=2,N=3,$={name:"Encode",data:function(){return{formState:P,nBits:1,dataFile:null,imgFile:null,imgFileDataString:"",encodeFilename:!0,encodeFileExt:!0}},computed:{validInputImgFile:function(){return Boolean(this.imgFile)&&["image/bmp","image/png"].includes(this.imgFile.type)},feedbackValidInputImgFile:function(){return this.validInputImgFile?"Awesome!":""},feedbackInvalidInputImgFile:function(){return this.imgFile&&!["image/bmp","image/png"].includes(this.imgFile.type)?"Needs to be a .Needs to be a .bmp or a .png":""},showForm:function(){return[P,A].includes(this.formState)},enableSubmit:function(){return this.formState===A},showImgInfo:function(){return this.showForm&&this.validInputImgFile},showDataInput:function(){return this.showForm&&this.validInputImgFile},showEncodeSettings:function(){return this.showForm&&this.showDataInput&&this.dataFile},showWaiting:function(){return this.formState===M},showResult:function(){return this.formState===N}},methods:{submit:function(){var e=this;this.formState=M;var t=new FormData;t.append("dataFile",this.dataFile),t.append("imgFile",this.imgFile),t.append("nBits",this.nBits),t.append("encodeFilename",this.encodeFilename),t.append("encodeFileExt",this.encodeFileExt),E.a.post("/encode",t,{headers:{"Content-Type":"multipart/form-data"}}).then(function(t){e.formState=N,alert(t)}).catch(function(e){alert(e)})},imgFileChange:function(e){var t=this,a=e.target;if(a.files&&a.files[0]){var n=new FileReader;n.onload=function(e){t.imgFileDataString=e.target.result},n.readAsDataURL(a.files[0])}},formChanged:function(e){}}},U=$,L=Object(u["a"])(U,j,R,!1,null,null,null),W=L.exports,G=function(){var e=this,t=e.$createElement,a=e._self._c||t;return a("div",{staticClass:"container"},[a("div",{staticClass:"row mt-5"},[a("div",{staticClass:"col-md-12 text-center"},[a("div",{staticClass:"card"},[a("h1",{staticClass:"card-header text-uppercase"},[e._v("oops")]),a("div",{staticClass:"card-body"},[a("h2",[e._v("This page went extinct by the looks of things...")]),a("h2",[e._v("Are you sure you meant to come here?")]),a("router-link",{staticClass:"btn my-3",attrs:{to:"/encode"}},[e._v("Go Back In Time")])],1)])])])])},J=[],V=(a("ed39"),{}),z=Object(u["a"])(V,G,J,!1,null,null,null),q=z.exports;i["default"].use(v["a"]);var H=new v["a"]({routes:[{path:"/",alias:"/about",name:"About",component:_},{path:"/encode",name:"Encode",component:W},{path:"/decode",name:"Decode",component:B},{path:"*",name:"Error",component:q}]}),K=a("2f62");i["default"].use(K["a"]);var Q=new K["a"].Store({state:{},mutations:{},actions:{}}),X=a("ecee"),Y=a("c074"),Z=a("ad3d");i["default"].use(n["a"]),X["c"].add(Y["a"]),i["default"].component("font-awesome-icon",Z["a"]),i["default"].config.productionTip=!1,new i["default"]({router:H,store:Q,render:function(e){return e(h)}}).$mount("#app")},"5c0b":function(e,t,a){"use strict";var n=a("5e27"),i=a.n(n);i.a},"5e27":function(e,t,a){},"8d9e":function(e,t,a){},ed39:function(e,t,a){"use strict";var n=a("8d9e"),i=a.n(n);i.a}});
//# sourceMappingURL=app.efb26e5c.js.map