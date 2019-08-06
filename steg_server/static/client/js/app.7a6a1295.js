(function(e){function t(t){for(var i,l,s=t[0],r=t[1],c=t[2],u=0,m=[];u<s.length;u++)l=s[u],n[l]&&m.push(n[l][0]),n[l]=0;for(i in r)Object.prototype.hasOwnProperty.call(r,i)&&(e[i]=r[i]);d&&d(t);while(m.length)m.shift()();return o.push.apply(o,c||[]),a()}function a(){for(var e,t=0;t<o.length;t++){for(var a=o[t],i=!0,s=1;s<a.length;s++){var r=a[s];0!==n[r]&&(i=!1)}i&&(o.splice(t--,1),e=l(l.s=a[0]))}return e}var i={},n={app:0},o=[];function l(t){if(i[t])return i[t].exports;var a=i[t]={i:t,l:!1,exports:{}};return e[t].call(a.exports,a,a.exports,l),a.l=!0,a.exports}l.m=e,l.c=i,l.d=function(e,t,a){l.o(e,t)||Object.defineProperty(e,t,{enumerable:!0,get:a})},l.r=function(e){"undefined"!==typeof Symbol&&Symbol.toStringTag&&Object.defineProperty(e,Symbol.toStringTag,{value:"Module"}),Object.defineProperty(e,"__esModule",{value:!0})},l.t=function(e,t){if(1&t&&(e=l(e)),8&t)return e;if(4&t&&"object"===typeof e&&e&&e.__esModule)return e;var a=Object.create(null);if(l.r(a),Object.defineProperty(a,"default",{enumerable:!0,value:e}),2&t&&"string"!=typeof e)for(var i in e)l.d(a,i,function(t){return e[t]}.bind(null,i));return a},l.n=function(e){var t=e&&e.__esModule?function(){return e["default"]}:function(){return e};return l.d(t,"a",t),t},l.o=function(e,t){return Object.prototype.hasOwnProperty.call(e,t)},l.p="/";var s=window["webpackJsonp"]=window["webpackJsonp"]||[],r=s.push.bind(s);s.push=t,s=s.slice();for(var c=0;c<s.length;c++)t(s[c]);var d=r;o.push([0,"chunk-vendors"]),a()})({0:function(e,t,a){e.exports=a("56d7")},"130e":function(e,t,a){},"16a3":function(e,t,a){"use strict";var i=a("130e"),n=a.n(i);n.a},"56d7":function(e,t,a){"use strict";a.r(t);a("cadf"),a("551c"),a("f751"),a("097d");var i=a("5f5b"),n=(a("f9e3"),a("2dd8"),a("2b0e")),o=function(){var e=this,t=e.$createElement,a=e._self._c||t;return a("div",{attrs:{id:"app"}},[e._m(0),a("div",{staticClass:"content"},[a("Navbar"),a("router-view")],1)])},l=[function(){var e=this,t=e.$createElement,a=e._self._c||t;return a("div",{attrs:{id:"background"}},[a("div",{staticClass:"layer",attrs:{"data-depth":"0.025"}},[a("div",{staticClass:"layer-6"})]),a("div",{staticClass:"layer",attrs:{"data-depth":"0.05"}},[a("div",{staticClass:"layer-5"})]),a("div",{staticClass:"layer",attrs:{"data-depth":"0.1"}},[a("div",{staticClass:"layer-4"})]),a("div",{staticClass:"layer",attrs:{"data-depth":"0.15"}},[a("div",{staticClass:"layer-3"})]),a("div",{staticClass:"layer",attrs:{"data-depth":"0.2"}},[a("div",{staticClass:"layer-2"})]),a("div",{staticClass:"layer",attrs:{"data-depth":"0.25"}},[a("div",{staticClass:"layer-1"})])])}],s=function(){var e=this,t=e.$createElement,a=e._self._c||t;return a("b-navbar",{attrs:{toggleable:"lg",sticky:""}},[a("div",{staticClass:"container"},[a("b-navbar-brand",{staticClass:"my-0 mx-3"},[a("img",{attrs:{src:"ct_logo.svg",height:"96px"}})]),a("b-navbar-toggle",{staticClass:"my-0 mx-0",attrs:{target:"nav-collapse"}},[a("font-awesome-icon",{attrs:{icon:"bars",size:"2x"}})],1),a("b-collapse",{staticClass:"mx-3",attrs:{id:"nav-collapse","is-nav":""}},[a("b-navbar-nav",{staticClass:"row w-100 text-lg-center"},[a("b-nav-item",{staticClass:"col-lg",attrs:{to:"/about"}},[e._v("About")]),a("b-nav-item",{staticClass:"col-lg",attrs:{to:"/encode"}},[e._v("Encode")]),a("b-nav-item",{staticClass:"col-lg",attrs:{to:"/decode"}},[e._v("Decode")])],1)],1)],1)])},r=[],c={name:"Navbar"},d=c,u=(a("16a3"),a("2877")),m=Object(u["a"])(d,s,r,!1,null,null,null),p=m.exports,h=a("a5ab"),b=a.n(h),f={components:{Navbar:p},mounted:function(){new b.a(document.getElementById("background"))}},g=f,v=(a("5c0b"),Object(u["a"])(g,o,l,!1,null,null,null)),F=v.exports,w=a("8c4f"),I=function(){var e=this,t=e.$createElement,a=e._self._c||t;return a("b-container",[a("b-row",[a("b-col",{attrs:{sm:"12"}},[a("b-card",{staticClass:"mt-3"},[a("b-card-title",[e._v("What is Stegosaurus?")]),a("b-card-text",[e._v("Stegosaurus is a steganography tool designed to allow users to encode data within image files.We are using a method of steganography known as LSB (Least significant bit) steganography")])],1)],1)],1)],1)},x=[],y={},_=Object(u["a"])(y,I,x,!1,null,null,null),C=_.exports,S=function(){var e=this,t=e.$createElement,a=e._self._c||t;return a("b-container",[a("b-row",[a("b-col",{attrs:{sm:"12"}},[a("b-card",{staticClass:"mt-3"},[a("b-card-title",[e._v("Decode Data")]),a("b-card-text",[e._v("Decode data from your encoded image which you created on the other page. Once you have uploaded the image, you are presented with a button to download the contents.")]),a("form",[a("b-form-group",{attrs:{label:"Encoded Image File","label-for":"input-imgFile","label-class":"font-weight-bold",description:e.validInputImgFile?"":"Enter your encoded image file to decode the data inside",state:e.validInputImgFile,"invalid-feedback":e.feedbackInvalidInputImgFile,"valid-feedback":e.feedbackValidInputImgFile}},[a("b-form-file",{attrs:{id:"input-imgFile",placeholder:"Choose a bmp/png file...","drop-placeholder":"Drop a bmp/png file here to encode to...",state:e.validInputImgFile},on:{change:function(t){return e.imgFileChange(t)}},model:{value:e.imgFile,callback:function(t){e.imgFile=t},expression:"imgFile"}})],1),a("b-collapse",{attrs:{id:"imgFilePreviewCollapse"},model:{value:e.imgFile,callback:function(t){e.imgFile=t},expression:"imgFile"}},[a("b-card",{staticClass:"overflow-hidden mb-3",attrs:{"no-body":""}},[a("b-card-img",{staticClass:"rounded-0",attrs:{src:e.imgFileDataString}})],1)],1),a("b-button",{on:{click:e.submit}},[e._v("Decode")])],1)],1)],1)],1)],1)},D=[],k=a("bc3a"),E=a.n(k),B={IMG_FILE_INPUT:0,FORM_SUBMITTED:1,FORM_RESULT:2},M={name:"Decode",data:function(){return{pageState:B.DATA_FILE_INPUT,imgFile:null,imgFileDataString:""}},methods:{submit:function(){var e=new FormData;e.append("imgFile",this.imgFile),E.a.post("/decode",e,{headers:{"Content-Type":"multipart/form-data"}}).then(function(e){alert(e)}).catch(function(e){alert(e)})},imgFileChange:function(e){var t=this,a=e.target;if(a.files&&a.files[0]){var i=new FileReader;i.onload=function(e){t.imgFileDataString=e.target.result},i.readAsDataURL(a.files[0])}}}},O=M,T=Object(u["a"])(O,S,D,!1,null,null,null),j=T.exports,A=function(){var e=this,t=e.$createElement,a=e._self._c||t;return a("b-container",[a("b-row",[a("b-col",{attrs:{sm:"12"}},[a("b-card",{staticClass:"mt-3"},[a("b-card-title",[e._v("Encode Data")]),a("b-card-text",[e._v("Encode some data within a bitmap image file. The algorithm works by changing the colour values of the pixels of an image, embedding the data within the image. If the encoding is good, the\ndata will be undetectable to the naked eye. It overwrites the least significant bits of each colour\nchannel with the data to be hidden, changing the actual value by the smallest amount.")]),a("b-collapse",{model:{value:e.showForm,callback:function(t){e.showForm=t},expression:"showForm"}},[a("form",[a("b-form-group",{attrs:{label:"Image File","label-for":"input-imgFile","label-class":"font-weight-bold",description:e.validInputImgFile?"":"Enter a image file to hide your data inside.",state:e.validInputImgFile,"invalid-feedback":e.feedbackInvalidInputImgFile,"valid-feedback":e.feedbackValidInputImgFile}},[a("b-form-file",{attrs:{id:"input-imgFile",placeholder:"Choose a bmp/png file...","drop-placeholder":"Drop a bmp/png file here to encode to...",state:e.validInputImgFile},model:{value:e.imgFile,callback:function(t){e.imgFile=t},expression:"imgFile"}})],1),a("b-collapse",{staticClass:"mb-3",model:{value:e.showImgInfo,callback:function(t){e.showImgInfo=t},expression:"showImgInfo"}},[a("b-card",{staticClass:"overflow-hidden",attrs:{"no-body":""}},[a("b-row",{attrs:{"no-gutters":""}},[a("b-col",{attrs:{lg:"6"}},[a("b-card-img",{staticClass:"rounded-0",attrs:{src:e.imgFileDataString}})],1),a("b-col",{attrs:{lg:"6"}},[a("b-card-body",{attrs:{title:"Image: "+(e.imgFile?e.imgFile.name:"")}},[a("b-row",[a("b-col",{attrs:{md:"auto"}},[a("b-card-text",[e._v("Dimensions: "+e._s(e.imgMeta.width)+" x "+e._s(e.imgMeta.height))])],1),a("b-col",{attrs:{md:"auto"}},[a("b-card-text",[e._v("Channels: "+e._s(e.imgMeta.channels))])],1),a("b-col",{attrs:{md:"auto"}},[a("b-card-text",[e._v("Bit Depth: "+e._s(e.imgMeta.bitDepth))])],1)],1),a("b-card-text",[e._v("Estimated Space "+e._s(e.estimatedSpace)+" Bytes")])],1)],1)],1)],1)],1),a("b-collapse",{model:{value:e.showDataInput,callback:function(t){e.showDataInput=t},expression:"showDataInput"}},[a("b-form-group",{attrs:{label:"Data File","label-for":"input-dataFile","label-class":"font-weight-bold",description:e.dataFile?"":"Enter a data file to encode onto the image",state:Boolean(e.dataFile),"valid-feedback":e.dataFile?"Awesome!":""}},[a("b-form-file",{attrs:{state:e.dataFile,placeholder:"Choose file to encode on to image...","drop-placeholder":"Drop file here to encode onto image..."},model:{value:e.dataFile,callback:function(t){e.dataFile=t},expression:"dataFile"}})],1)],1),a("b-collapse",{model:{value:e.showEncodeSettings,callback:function(t){e.showEncodeSettings=t},expression:"showEncodeSettings"}},[a("b-form-group",{attrs:{label:"Encoding Settings","label-class":"font-weight-bold"}},[a("b-form-group",{attrs:{label:"Bits: "+e.nBits,"label-for":"input-nBits","label-cols-lg":"2",description:"The number of bits to overwrite per channel of the image"}},[a("b-form-input",{attrs:{id:"nBitsInput",type:"range",min:"1",max:e.imgMeta.bitDepth},on:{change:e.updateSpaceAvailable},model:{value:e.nBits,callback:function(t){e.nBits=t},expression:"nBits"}})],1),a("b-form-group",[a("b-form-checkbox",{on:{change:e.updateSpaceAvailable},model:{value:e.encodeFilename,callback:function(t){e.encodeFilename=t},expression:"encodeFilename"}},[e._v("Encode filename")])],1),a("b-form-group",[a("b-form-checkbox",{on:{change:e.updateSpaceAvailable},model:{value:e.encodeFileExt,callback:function(t){e.encodeFileExt=t},expression:"encodeFileExt"}},[e._v("Encode file extension")])],1)],1)],1),a("b-button",{attrs:{disabled:!e.enableSubmit},on:{click:e.submit}},[e._v("Encode")])],1)]),a("b-collapse",{model:{value:e.showWaiting,callback:function(t){e.showWaiting=t},expression:"showWaiting"}},[a("b-card-text",[e._v("Waiting for a result...")])],1),a("b-collapse",{model:{value:e.showResult,callback:function(t){e.showResult=t},expression:"showResult"}},[a("b-card-text",[e._v("Result and download to go here")])],1)],1)],1)],1)],1)},R=[],P=(a("7f7f"),a("6762"),a("2fdb"),a("df7c")),$=a.n(P),L=0,N=1,W=2,U=3,V={name:"Encode",data:function(){return{formState:L,nBits:1,dataFile:null,imgFile:null,imgFileDataString:"",imgMeta:{width:1024,height:1920,channels:3,bitDepth:8},encodeFilename:!1,encodeFileExt:!1,transactionID:"",estimatedSpace:0}},computed:{validInputImgFile:function(){return Boolean(this.imgFile)&&["image/bmp","image/png"].includes(this.imgFile.type)},feedbackValidInputImgFile:function(){return this.validInputImgFile?"Awesome!":""},feedbackInvalidInputImgFile:function(){return this.imgFile&&!["image/bmp","image/png"].includes(this.imgFile.type)?"Needs to be a .Needs to be a .bmp or a .png":""},showForm:function(){return[L,N].includes(this.formState)},enableSubmit:function(){return this.formState===N},showImgInfo:function(){return this.showForm&&this.validInputImgFile},showDataInput:function(){return this.showForm&&this.validInputImgFile},showEncodeSettings:function(){return this.showForm&&this.showDataInput&&this.dataFile},showWaiting:function(){return this.formState===W},showResult:function(){return this.formState===U}},watch:{imgFile:function(e,t){var a=this;if(this.validInputImgFile){var i=new FileReader;i.onload=function(e){a.imgFileDataString=e.target.result},i.readAsDataURL(this.imgFile)}var n=new FormData;n.append("imgFile",this.imgFile),E.a.post("/encode/upload",n,{headers:{"Content-Type":"multipart/form-data"}}).then(function(e){a.transactionID=e.data.trans_id,a.imgMeta.width=e.data.width,a.imgMeta.height=e.data.height,a.imgMeta.channels=e.data.channels,a.imgMeta.bitDepth=e.data.bitdepth,a.updateSpaceAvailable()}).catch(function(e){alert(e)})}},methods:{submit:function(){var e=this;this.formState=W;var t=new FormData;t.append("dataFile",this.dataFile),t.append("imgFile",this.imgFile),t.append("nBits",this.nBits),t.append("encodeFilename",this.encodeFilename),t.append("encodeFileExt",this.encodeFileExt),E.a.post("/encode",t,{headers:{"Content-Type":"multipart/form-data"}}).then(function(t){e.formState=U,alert(t)}).catch(function(e){alert(e)})},updateSpaceAvailable:function(){var e=this,t={transID:this.transactionID};if(this.dataFile){var a=$.a.extname(this.dataFile.name),i=$.a.basename(this.dataFile,a);this.encodeFilename&&(t.filename=i),this.encodeFileExt&&(t.ext=a)}this.nBits>1&&(t.nBits=this.nBits),E.a.get("/encode/space",{params:t}).then(function(t){e.estimatedSpace=t.data.space_available}).catch(function(e){alert(e)})},validateForm:function(){this.validInputImgFile&&this.dataFile&&this.nBits<=this.imgMeta.bitDepth&&(this.formState=N)}}},G=V,J=Object(u["a"])(G,A,R,!1,null,null,null),z=J.exports,q=function(){var e=this,t=e.$createElement,a=e._self._c||t;return a("div",{staticClass:"container"},[a("div",{staticClass:"row mt-5"},[a("div",{staticClass:"col-md-12 text-center"},[a("div",{staticClass:"card"},[a("h1",{staticClass:"card-header text-uppercase"},[e._v("oops")]),a("div",{staticClass:"card-body"},[a("h2",[e._v("This page went extinct by the looks of things...")]),a("h2",[e._v("Are you sure you meant to come here?")]),a("router-link",{staticClass:"btn my-3",attrs:{to:"/encode"}},[e._v("Go Back In Time")])],1)])])])])},H=[],K=(a("ed39"),{}),Q=Object(u["a"])(K,q,H,!1,null,null,null),X=Q.exports;n["default"].use(w["a"]);var Y=new w["a"]({routes:[{path:"/",alias:"/about",name:"About",component:C},{path:"/encode",name:"Encode",component:z},{path:"/decode",name:"Decode",component:j},{path:"*",name:"Error",component:X}]}),Z=a("2f62");n["default"].use(Z["a"]);var ee=new Z["a"].Store({state:{},mutations:{},actions:{}}),te=a("ecee"),ae=a("c074"),ie=a("ad3d");n["default"].use(i["a"]),te["c"].add(ae["a"]),n["default"].component("font-awesome-icon",ie["a"]),n["default"].config.productionTip=!1,new n["default"]({router:Y,store:ee,render:function(e){return e(F)}}).$mount("#app")},"5c0b":function(e,t,a){"use strict";var i=a("5e27"),n=a.n(i);n.a},"5e27":function(e,t,a){},"8d9e":function(e,t,a){},ed39:function(e,t,a){"use strict";var i=a("8d9e"),n=a.n(i);n.a}});
//# sourceMappingURL=app.7a6a1295.js.map