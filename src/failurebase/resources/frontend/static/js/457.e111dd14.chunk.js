"use strict";(self.webpackChunkfailurebase_client=self.webpackChunkfailurebase_client||[]).push([[457],{5661:function(e,n,t){t.r(n),t.d(n,{default:function(){return _}});var i=t(4942),r=t(1413),l=t(4925),s=t(9142),c=t(3433),a=t(9439),o=t(2791),d=t(7689),u=t(1087),h=t(4447),p=t(3223);var x=t.p+"static/media/add.1e46d46361ac47a0548aca7f0a4495e2.svg",f=t(7940),m=t(8390),j=t(1944),g=t(5687),v=t(8430),Z=t(5265),C=t(9489),b=t(9141),k=t(9672),S=t(4165),y=t(5861),N=t(5301),A=function(){var e=(0,y.Z)((0,S.Z)().mark((function e(n){return(0,S.Z)().wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return e.next=2,(0,N.Z)("/api/clients",n.toString());case 2:return e.abrupt("return",e.sent);case 3:case"end":return e.stop()}}),e)})));return function(n){return e.apply(this,arguments)}}(),T=function(){var e=(0,y.Z)((0,S.Z)().mark((function e(n,t){var i;return(0,S.Z)().wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return i={method:"POST",body:JSON.stringify({ids:n}),headers:{Accept:"application/json","Content-Type":"application/json;charset=UTF-8","Api-Key":t}},e.next=3,(0,N.Z)("/api/clients/delete","",i);case 3:return e.abrupt("return",e.sent);case 4:case"end":return e.stop()}}),e)})));return function(n,t){return e.apply(this,arguments)}}(),P=function(){var e=(0,y.Z)((0,S.Z)().mark((function e(n){var t;return(0,S.Z)().wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return t={method:"POST",headers:{Accept:"application/json","Content-Type":"application/json;charset=UTF-8","Api-Key":n}},e.next=3,(0,N.Z)("/api/clients","",t);case 3:return e.abrupt("return",e.sent);case 4:case"end":return e.stop()}}),e)})));return function(n){return e.apply(this,arguments)}}(),w=function(){var e=(0,y.Z)((0,S.Z)().mark((function e(n,t){var i;return(0,S.Z)().wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return i={method:"PUT",headers:{Accept:"application/json","Content-Type":"application/json;charset=UTF-8","Api-Key":t}},e.next=3,(0,N.Z)("/api/clients/".concat(n),"",i);case 3:return e.abrupt("return",e.sent);case 4:case"end":return e.stop()}}),e)})));return function(n,t){return e.apply(this,arguments)}}(),K={getAll:A,deleteGiven:T,add:P,update:w},D=t(2278),I=t(9925),O=t(1733),E=t(184),F=[{id:"uid-collumn",label:"UID",order:m.K.ASC},{id:"secret-collumn",label:"Secret",order:m.K.NULL},{id:"created-collumn",label:"Created",order:m.K.ASC}],_=function(){var e,n=(0,d.s0)(),t=(0,f.$)(),S=t.setLoading,y=t.selectedClients,N=t.setSelectedClients,A=(0,u.lr)(),T=(0,a.Z)(A,2),P=T[0],w=T[1],_=(0,o.useState)({}),U=(0,a.Z)(_,2),M=U[0],V=U[1],G=(0,o.useState)(0),q=(0,a.Z)(G,2),$=q[0],L=q[1],R=(0,o.useState)([]),B=(0,a.Z)(R,2),J=B[0],z=B[1],H=(0,o.useState)(0),Q=(0,a.Z)(H,2),W=Q[0],X=Q[1],Y=(0,o.useState)(!1),ee=(0,a.Z)(Y,2),ne=ee[0],te=ee[1],ie=(0,o.useState)(!1),re=(0,a.Z)(ie,2),le=re[0],se=re[1],ce=(0,o.useState)(0),ae=(0,a.Z)(ce,2),oe=ae[0],de=ae[1],ue=(0,o.useState)(0),he=(0,a.Z)(ue,2),pe=he[0],xe=he[1],fe=(0,o.useState)(!1),me=(0,a.Z)(fe,2),je=me[0],ge=me[1],ve=(0,o.useState)(),Ze=(0,a.Z)(ve,2),Ce=Ze[0],be=Ze[1],ke=(0,o.useState)(),Se=(0,a.Z)(ke,2),ye=Se[0],Ne=Se[1],Ae=(0,o.useState)(""),Te=(0,a.Z)(Ae,2),Pe=Te[0],we=Te[1],Ke=function(){S(!0),K.getAll(P).then((function(e){var n=e.items.map((function(e){return function(e){return{id:e.id.toString(),data:[{id:"uid",label:e.uid,onClick:function(){Ne(e),(0,v.h7)("detail-modal")}},{id:"secret",label:e.secret},{id:"created",label:e.created.replace("T","  ")}]}}(e)})),t=document.querySelectorAll("#filter-modal input"),i={};t.forEach((function(e){var n,t=null!==(n=e.id.split("-").slice(1,-1).join("_"))&&void 0!==n?n:"",r=P.getAll(t);r.length>0&&(t.includes("created")?i[t]=(0,O.d$)(new Date(r[0])):i[t]=r[0])}));var r=0!==y.length&&n.filter((function(e){return y.includes(e.id)})).length===n.length;z(n),X(e.page_number),se(e.prev_page),te(e.next_page),de(e.count),xe(e.page_limit),ge(r),V(i),S(!1)})).catch((function(e){console.error(e),S(!1)}))};(0,o.useEffect)(Ke,[window.location.href]),(0,o.useEffect)((function(){L(Object.keys(M).length)}),[M]);var De=function(e){var n=e.target.id.split("-").slice(1,-1).join("_"),t=n.includes("created")?(0,O.d$)(new Date(e.target.value)):e.target.value;if(""===e.target.value&&n in M){M[n];var c=(0,l.Z)(M,[n].map(s.Z));V(c)}else V((0,r.Z)((0,r.Z)({},M),{},(0,i.Z)({},n,t)))};return(0,E.jsxs)(E.Fragment,{children:[(0,E.jsxs)("div",{className:"filters",children:[(0,E.jsx)("div",{className:"row",children:(0,E.jsxs)("div",{className:"col filter-button",children:[(0,E.jsx)("span",{className:"brand",children:"Clients"}),(0,E.jsxs)(j.Z,{onClick:function(e){(0,v.h7)("filter-modal"),document.querySelectorAll("#filter-modal input").forEach((function(e){var n,t=null!==(n=P.get(e.id.split("-").slice(1,-1).join("_")))&&void 0!==n?n:"";""!==t&&(e.id.includes("created")?e.value=(0,O.d$)(new Date(t)):e.value=t)}))},children:[(0,E.jsx)("img",{src:h.Z,alt:"Filter SVG"}),$>0&&(0,E.jsx)(g.Z,{text:$})]}),(0,E.jsx)(j.Z,{onClick:function(e){(0,v.h7)("add-modal")},children:(0,E.jsx)("img",{src:x,alt:"Add SVG"})}),(0,E.jsx)(j.Z,{onClick:function(e){(0,v.h7)("delete-modal")},children:(0,E.jsx)("img",{src:p.Z,alt:"Delete SVG"})})]})}),(0,E.jsxs)(v.ZP,{id:"filter-modal",children:[(0,E.jsx)(Z.Z,{children:(0,E.jsx)("span",{className:"text-primary",children:"Filter clients"})}),(0,E.jsxs)(C.Z,{children:[(0,E.jsxs)("p",{children:[(0,E.jsx)("label",{htmlFor:"filter-uid-input",children:"UID"}),(0,E.jsx)("input",{id:"filter-uid-input",type:"text",placeholder:"Type phrase to search",onChange:De})]}),(0,E.jsxs)("p",{children:[(0,E.jsx)("label",{htmlFor:"filter-start-created-input",children:"Start created"}),(0,E.jsx)("input",{id:"filter-start-created-input",type:"datetime-local",onChange:De})]}),(0,E.jsxs)("p",{children:[(0,E.jsx)("label",{htmlFor:"filter-end-created-input",children:"End created"}),(0,E.jsx)("input",{id:"filter-end-created-input",type:"datetime-local",onChange:De})]})]}),(0,E.jsxs)(b.Z,{children:[(0,E.jsx)("button",{className:"button primary",onClick:function(e){for(var n=0,t=Object.entries(M);n<t.length;n++){var i=(0,a.Z)(t[n],2),r=i[0],l=i[1];P.set(r,String(l))}P.delete("page"),w(P),N([]),ge(!1),(0,v.Mr)("filter-modal")},children:"Submit"}),(0,E.jsx)("button",{className:"button",onClick:function(e){document.querySelectorAll("#filter-modal input").forEach((function(e){e.value="",P.delete(e.id.split("-").slice(1,-1).join("_"))})),V({}),w(P)},children:"Clear"}),(0,E.jsx)("button",{className:"button",onClick:function(e){(0,v.Mr)("filter-modal")},children:"Close"})]})]}),(0,E.jsxs)(v.ZP,{id:"delete-modal",children:[(0,E.jsx)(Z.Z,{children:(0,E.jsx)("span",{className:"text-primary",children:"Delete clients"})}),(0,E.jsxs)(C.Z,{children:[function(){if(0===y.length)return(0,E.jsx)("strong",{children:"No clients selected to deletion."});var e=y.length>1?"s":"";return(0,E.jsxs)("strong",{children:[y.length," client",e," selected to deletion. "]})}(),(0,E.jsx)(I.Z,{id:"api-key-delete-modal",labelClassName:"",inputClassName:"",labelText:"API Key",inputValue:Pe,onInputChange:function(e){we(e.target.value)}}),(0,E.jsxs)(k.ZP,{id:"deletion-in-progress",children:[(0,E.jsx)("div",{style:{marginBottom:"10px"},children:(0,E.jsx)("span",{children:"Deleting..."})}),(0,E.jsx)(D.Z,{})]}),(0,E.jsxs)(k.ZP,{id:"deletion-done",children:[(0,E.jsx)("span",{className:"text-primary",children:"Result:"}),(0,E.jsx)("br",{}),(0,E.jsx)("span",{children:Ce})]})]}),(0,E.jsxs)(b.Z,{children:[(0,E.jsx)("button",{className:"button primary",onClick:function(e){0!==y.length&&((0,k.Kc)("deletion-in-progress"),K.deleteGiven(y,Pe).then((function(e){var n=(0,O.TI)(e);be(n),setTimeout((function(){N([]),(0,k.Ov)("deletion-in-progress"),(0,k.Kc)("deletion-done")}),1e3)})).catch((function(e){var n,t;be((0,E.jsx)("p",{className:"text-error",children:"Deletion error"})),setTimeout((function(){(0,k.Ov)("deletion-in-progress"),(0,k.Kc)("deletion-done")}),1e3),console.error("Error details: ".concat(String(null!==(n=null===e||void 0===e||null===(t=e.response)||void 0===t?void 0:t.detail)&&void 0!==n?n:"no details ")))})))},disabled:""===Pe,children:"Confirm"}),(0,E.jsx)("button",{className:"button",onClick:function(e){be(""),we(""),(0,k.Ov)("deletion-done"),(0,v.Mr)("delete-modal"),""!==Ce&&Ke()},children:"Close"})]})]}),(0,E.jsxs)(v.ZP,{id:"unselect-modal",children:[(0,E.jsx)(Z.Z,{children:"Unselect items"}),(0,E.jsx)(C.Z,{children:"Do you confirm unselection of all items?"}),(0,E.jsxs)(b.Z,{children:[(0,E.jsx)("button",{className:"button primary",onClick:function(e){ge(!1),N([]),(0,v.Mr)("unselect-modal")},children:"Confirm"}),(0,E.jsx)("button",{className:"button",onClick:function(e){(0,v.Mr)("unselect-modal")},children:"Close"})]})]}),(0,E.jsxs)(v.ZP,{id:"detail-modal",children:[(0,E.jsx)(Z.Z,{children:(0,E.jsx)("span",{className:"text-primary",children:"Details"})}),(0,E.jsxs)(C.Z,{children:[(0,E.jsx)("strong",{children:"UID:"}),(0,E.jsx)("p",{children:null===ye||void 0===ye?void 0:ye.uid}),(0,E.jsx)("strong",{children:"Secret:"}),(0,E.jsx)("p",{children:null===ye||void 0===ye?void 0:ye.secret}),(0,E.jsx)("strong",{children:"Created:"}),(0,E.jsx)("p",{children:null===ye||void 0===ye||null===(e=ye.created)||void 0===e?void 0:e.replace("T","  ")}),(0,E.jsx)(I.Z,{id:"api-key-detail-modal",labelClassName:"",inputClassName:"",labelText:"Enter API Key to check secret",inputValue:Pe,onInputChange:function(e){we(e.target.value)}}),(0,E.jsxs)(k.ZP,{id:"checking-done",children:[(0,E.jsx)("span",{className:"text-primary",children:"Result:"}),(0,E.jsx)("br",{}),(0,E.jsx)("span",{children:Ce})]})]}),(0,E.jsxs)(b.Z,{children:[(0,E.jsx)("button",{className:"button",onClick:function(e){if((0,k.Ov)("checking-done"),void 0===ye)return(0,k.Kc)("checking-done"),void be((0,E.jsx)(E.Fragment,{children:"Could not send request"}));K.update(ye.id,Pe).then((function(e){console.log(e),"uid"in e?Ne(e):"detail"in e?(be((0,E.jsx)("p",{className:"text-error",children:e.detail})),setTimeout((function(){(0,k.Kc)("checking-done")}),1e3)):(be((0,E.jsx)("p",{className:"text-error",children:"Checking error"})),setTimeout((function(){(0,k.Kc)("checking-done")}),1e3)),we("")})).catch((function(e){var n,t;be((0,E.jsx)("p",{className:"text-error",children:"Checking error"})),setTimeout((function(){(0,k.Kc)("checking-done")}),1e3),console.error("Error details: ".concat(String(null!==(n=null===e||void 0===e||null===(t=e.response)||void 0===t?void 0:t.detail)&&void 0!==n?n:"no details ")))}))},children:"Check"}),(0,E.jsx)("button",{className:"button",onClick:function(e){we(""),(0,v.Mr)("detail-modal")},children:"Close"})]})]}),(0,E.jsxs)(v.ZP,{id:"add-modal",children:[(0,E.jsx)(Z.Z,{children:"Add new client"}),(0,E.jsxs)(C.Z,{children:["Do you confirm adding new client?",(0,E.jsx)(I.Z,{id:"api-key-add-modal",labelClassName:"",inputClassName:"",labelText:"API Key",inputValue:Pe,onInputChange:function(e){we(e.target.value)}}),(0,E.jsxs)(k.ZP,{id:"adding-in-progress",children:[(0,E.jsx)("div",{style:{marginBottom:"10px"},children:(0,E.jsx)("span",{children:"Adding..."})}),(0,E.jsx)(D.Z,{})]}),(0,E.jsxs)(k.ZP,{id:"adding-done",children:[(0,E.jsx)("span",{className:"text-primary",children:"Result:"}),(0,E.jsx)("br",{}),(0,E.jsx)("span",{children:Ce})]})]}),(0,E.jsxs)(b.Z,{children:[(0,E.jsx)("button",{className:"button primary",onClick:function(e){(0,k.Kc)("adding-in-progress"),(0,k.Ov)("adding-done"),K.add(Pe).then((function(e){be("uid"in e?(0,E.jsxs)(E.Fragment,{children:[(0,E.jsx)("strong",{children:"UID: "}),null===e||void 0===e?void 0:e.uid,(0,E.jsx)("br",{}),(0,E.jsx)("strong",{children:"Secret: "}),null===e||void 0===e?void 0:e.secret]}):"detail"in e?(0,E.jsx)("p",{className:"text-error",children:e.detail}):(0,E.jsx)("p",{className:"text-error",children:"Adding error"})),setTimeout((function(){(0,k.Ov)("adding-in-progress"),(0,k.Kc)("adding-done"),we("")}),1e3)})).catch((function(e){var n,t;be((0,E.jsx)("p",{className:"text-error",children:"Adding error"})),setTimeout((function(){(0,k.Ov)("adding-in-progress"),(0,k.Kc)("adding-done")}),1e3),console.error("Error details: ".concat(String(null!==(n=null===e||void 0===e||null===(t=e.response)||void 0===t?void 0:t.detail)&&void 0!==n?n:"no details ")))}))},children:"Confirm"}),(0,E.jsx)("button",{className:"button",onClick:function(e){we(""),(0,k.Ov)("adding-done"),(0,v.Mr)("add-modal"),""!==Ce&&Ke()},children:"Close"})]})]})]}),(0,E.jsx)(m.Z,{header:F,data:J,selectedItemsInfo:0===y.length?"":1===y.length?"1 row selected":"".concat(y.length," rows selected"),pageInfo:"page ".concat(W+1," of ").concat(0!==oe?Math.ceil(oe/pe):1),secectedItems:y,selectAllChecked:je,prevPageDisabled:!le,nextPageDisabled:!ne,onSortClick:function(e,t){var i=e.replace("-collumn","").replaceAll("-","_"),r="".concat(t===m.K.DESC?"-":"").concat(i);P.set("ordering",r),w(P),n({pathname:"/clients",search:"?"+String(P)})},onSelectAllChange:function(e){if(ge(!je),je){var n=J.map((function(e){return e.id})),t=y.filter((function(e){return!n.includes(e)}));N(t)}else{var i=J.filter((function(e){return!y.includes(e.id)})).map((function(e){return e.id})),r=[].concat((0,c.Z)(y),(0,c.Z)(i));N(r)}},onSelectOneChange:function(e){var n=e.target,t=n.id,i=n.checked?[].concat((0,c.Z)(y),[t]):y.filter((function(e){return e!==t})),r=J.filter((function(e){return i.includes(e.id)})).length===J.length;ge(r),N(i)},onNextPageClick:function(e){P.set("page",String(W+1)),w(P)},onPrevPageClick:function(e){P.set("page",String(W-1)),w(P)},onSelectedItemsClearClick:function(e){(0,v.h7)("unselect-modal")}})]})}}}]);
//# sourceMappingURL=457.e111dd14.chunk.js.map