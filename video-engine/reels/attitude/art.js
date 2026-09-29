// SVG illustration library — flat, duotone, brand greens
const C = {dg:'#15402A', g:'#3E9B5B', g2:'#2D7B48', lg:'#DDEFD5', lg2:'#C2E3B6', off:'#F4F7EF', red:'#E4574C', ink:'#1E2922', gold:'#E3A33B'};

// expression variant group
const V = (k, v, on, inner) => `<g data-k="${k}" data-v="${v}" style="opacity:${on?1:0}">${inner}</g>`;

const ART = {
man(o={}){
  const shirt=o.shirt||'#3E8E5E', skin='#F6D0AE', hair='#2B2622', st=`stroke="${hair}" stroke-width="7" stroke-linecap="round" fill="none"`;
  const ms=`stroke="#7A3B2E" stroke-width="6" stroke-linecap="round" fill="none"`;
  return `<svg viewBox="0 0 400 520" class="man">
  <path d="M40 520 C45 430 105 385 200 385 C295 385 355 430 360 520Z" fill="${shirt}"/>
  <path d="M158 389 L200 442 L242 389Z" fill="#F4F7EF"/>
  <path d="M172 300 h56 v92 q-28 16 -56 0z" fill="#E9B893"/>
  <g class="head">
   <ellipse cx="108" cy="205" rx="17" ry="25" fill="#F1C4A0"/><ellipse cx="292" cy="205" rx="17" ry="25" fill="#F1C4A0"/>
   <ellipse cx="200" cy="195" rx="92" ry="108" fill="${skin}"/>
   <path d="M106 200 C92 110 140 70 204 70 C268 70 312 112 296 200 C292 160 274 138 246 130 C214 150 160 150 128 136 C114 150 108 172 106 200Z" fill="${hair}"/>
   ${V('br','n',1,`<path d="M146 168 Q166 158 184 166" ${st}/><path d="M216 166 Q234 158 254 168" ${st}/>`)}
   ${V('br','w',0,`<path d="M146 170 Q166 164 184 154" ${st}/><path d="M216 154 Q234 164 254 170" ${st}/>`)}
   ${V('ey','n',1,`<circle cx="166" cy="200" r="9.5" fill="${hair}"/><circle cx="234" cy="200" r="9.5" fill="${hair}"/>`)}
   ${V('ey','w',0,`<circle cx="166" cy="200" r="17" fill="#fff" stroke="${hair}" stroke-width="3"/><circle cx="234" cy="200" r="17" fill="#fff" stroke="${hair}" stroke-width="3"/><g class="pup"><circle cx="166" cy="202" r="7.5" fill="${hair}"/><circle cx="234" cy="202" r="7.5" fill="${hair}"/></g>`)}
   ${V('ey','c',0,`<path d="M152 202 Q166 192 180 202" ${st}/><path d="M220 202 Q234 192 248 202" ${st}/>`)}
   <path d="M200 208 Q193 230 205 234" stroke="#D9A07A" stroke-width="4" fill="none" stroke-linecap="round"/>
   ${V('mo','smile',1,`<path d="M172 256 Q200 280 228 256" ${ms}/>`)}
   ${V('mo','flat',0,`<path d="M182 264 L218 264" ${ms}/>`)}
   ${V('mo','wob',0,`<path d="M170 264 Q180 255 190 264 Q200 273 210 264 Q220 255 230 264" ${ms}/>`)}
   ${V('mo','open',0,`<path d="M178 252 Q200 248 222 252 Q219 284 200 286 Q181 284 178 252Z" fill="#7A3B2E"/><path d="M186 274 Q200 282 214 274" fill="#E9807A"/>`)}
   ${V('mo','calm',0,`<path d="M180 260 Q202 274 224 258" ${ms}/>`)}
   ${V('bl','1',0,`<ellipse cx="140" cy="242" rx="17" ry="9" fill="#F4A38F" opacity=".55"/><ellipse cx="260" cy="242" rx="17" ry="9" fill="#F4A38F" opacity=".55"/>`)}
   ${V('sw','1',0,`<path class="drop" d="M302 118 C302 118 287 142 287 153 A15 15 0 0 0 317 153 C317 142 302 118 302 118Z" fill="#9AD6F7" stroke="#5AA9D6" stroke-width="3"/>`)}
  </g></svg>`;
},

woman(o={}){
  const top=o.top||'#EBDCC8', skin='#F7D5B8', hair='#4B3426';
  const st=`stroke="${hair}" stroke-width="6" stroke-linecap="round" fill="none"`, ms=`stroke="#C0645A" stroke-width="6" stroke-linecap="round" fill="none"`;
  return `<svg viewBox="0 0 400 520" class="woman">
  <path d="M94 212 C86 110 140 68 200 68 C260 68 314 110 306 212 C314 300 326 390 300 430 L100 430 C74 390 86 300 94 212Z" fill="${hair}"/>
  <path d="M44 520 C48 432 108 388 200 388 C292 388 352 432 356 520Z" fill="${top}"/>
  <path d="M176 300 h48 v92 q-24 16 -48 0z" fill="#EDBE9B"/>
  <path d="M162 390 Q200 430 238 390Z" fill="#EDBE9B"/>
  <g class="head">
   <ellipse cx="200" cy="196" rx="88" ry="104" fill="${skin}"/>
   <path d="M110 196 C104 118 150 82 202 82 C256 82 298 120 292 196 C272 152 244 128 206 124 C190 152 150 176 110 196Z" fill="${hair}"/>
   <circle cx="113" cy="238" r="7" fill="${C.g}"/><circle cx="287" cy="238" r="7" fill="${C.g}"/>
   ${V('br','n',1,`<path d="M150 170 Q168 161 186 168" ${st}/><path d="M214 168 Q232 161 250 170" ${st}/>`)}
   ${V('br','f',0,`<path d="M150 166 L186 170" ${st}/><path d="M214 170 L250 166" ${st}/>`)}
   ${V('br','u',0,`<path d="M150 160 Q168 150 186 158" ${st}/><path d="M214 158 Q232 150 250 160" ${st}/>`)}
   ${V('ey','n',1,`<circle cx="168" cy="200" r="9" fill="${hair}"/><circle cx="232" cy="200" r="9" fill="${hair}"/><path d="M156 192 l-8 -6 M244 192 l8 -6" stroke="${hair}" stroke-width="4" stroke-linecap="round"/>`)}
   ${V('ey','h',0,`<path d="M156 202 L180 202" ${st}/><path d="M220 202 L244 202" ${st}/>`)}
   <path d="M200 212 Q195 228 204 231" stroke="#DDA07E" stroke-width="4" fill="none" stroke-linecap="round"/>
   ${V('mo','smile',1,`<path d="M176 254 Q200 274 224 254" ${ms}/>`)}
   ${V('mo','flat',0,`<path d="M184 262 L216 262" ${ms}/>`)}
   ${V('mo','o',0,`<ellipse cx="200" cy="262" rx="9" ry="11" fill="#C0645A"/>`)}
   ${V('bl','1',1,`<ellipse cx="146" cy="240" rx="16" ry="8" fill="#F4A38F" opacity=".45"/><ellipse cx="254" cy="240" rx="16" ry="8" fill="#F4A38F" opacity=".45"/>`)}
  </g></svg>`;
},

hyena(){
  const f='#C8AA80', d='#8B6B47', dk='#2E2219';
  return `<svg viewBox="0 0 400 440" class="hyena">
  <path d="M70 440 C70 356 122 318 200 318 C278 318 330 356 330 440Z" fill="#B99A70"/>
  <ellipse cx="140" cy="390" rx="16" ry="12" fill="${d}" opacity=".6"/><ellipse cx="262" cy="400" rx="18" ry="12" fill="${d}" opacity=".6"/><ellipse cx="205" cy="372" rx="12" ry="9" fill="${d}" opacity=".6"/>
  <g class="head">
   <path d="M96 156 L64 36 L170 110Z" fill="${f}"/><path d="M100 140 L80 66 L146 112Z" fill="${d}"/>
   <path d="M304 156 L336 36 L230 110Z" fill="${f}"/><path d="M300 140 L320 66 L254 112Z" fill="${d}"/>
   <ellipse cx="200" cy="192" rx="120" ry="102" fill="${f}"/>
   <path d="M146 100 L160 68 L176 98 L190 60 L205 96 L220 62 L233 98 L248 72 L258 104Z" fill="#5E4630"/>
   <ellipse cx="112" cy="196" rx="12" ry="9" fill="${d}" opacity=".7"/><ellipse cx="290" cy="206" rx="13" ry="9" fill="${d}" opacity=".7"/><ellipse cx="128" cy="236" rx="8" ry="6" fill="${d}" opacity=".7"/>
   <ellipse cx="200" cy="248" rx="68" ry="50" fill="#E3CDA6"/>
   <ellipse cx="200" cy="220" rx="25" ry="15" fill="${dk}"/>
   <ellipse cx="156" cy="172" rx="22" ry="24" fill="#fff"/><ellipse cx="244" cy="172" rx="22" ry="24" fill="#fff"/>
   <g class="pup"><circle cx="156" cy="176" r="10" fill="${dk}"/><circle cx="244" cy="176" r="10" fill="${dk}"/></g>
   <path d="M132 140 Q154 140 176 126" stroke="#5E4630" stroke-width="7" stroke-linecap="round" fill="none"/>
   <path d="M224 126 Q246 140 268 140" stroke="#5E4630" stroke-width="7" stroke-linecap="round" fill="none"/>
   <path d="M166 266 Q176 257 186 266 Q196 275 206 266 Q216 257 226 266 Q231 271 236 266" stroke="${dk}" stroke-width="5" fill="none" stroke-linecap="round"/>
   <path class="drop" d="M318 108 C318 108 304 130 304 140 A14 14 0 0 0 332 140 C332 130 318 108 318 108Z" fill="#9AD6F7" stroke="#5AA9D6" stroke-width="3"/>
   <path class="drop2" d="M84 128 C84 128 73 146 73 154 A11 11 0 0 0 95 154 C95 146 84 128 84 128Z" fill="#9AD6F7" stroke="#5AA9D6" stroke-width="3"/>
  </g></svg>`;
},

lion(){
  let mane='';
  for(let i=0;i<18;i++){const a=i/18*Math.PI*2;mane+=`<circle cx="${200+Math.cos(a)*120}" cy="${196+Math.sin(a)*118}" r="46" fill="#D48A2C"/>`;}
  for(let i=0;i<18;i++){const a=(i+.5)/18*Math.PI*2;mane+=`<circle cx="${200+Math.cos(a)*98}" cy="${196+Math.sin(a)*96}" r="40" fill="#E4A342"/>`;}
  const br='#4A2E17', st=`stroke="${br}" stroke-width="6" stroke-linecap="round" fill="none"`;
  return `<svg viewBox="0 0 400 440" class="lion">
  <path d="M84 440 C84 358 130 320 200 320 C270 320 316 358 316 440Z" fill="#EDBE6A"/>
  <path d="M170 440 C172 400 186 380 200 380 C214 380 228 400 230 440Z" fill="#F7DDA4"/>
  <g class="head">${mane}
   <circle cx="126" cy="104" r="26" fill="#F2C86F"/><circle cx="126" cy="104" r="13" fill="#D48A2C"/>
   <circle cx="274" cy="104" r="26" fill="#F2C86F"/><circle cx="274" cy="104" r="13" fill="#D48A2C"/>
   <circle cx="200" cy="198" r="102" fill="#F6CF7D"/>
   <path d="M150 162 Q166 155 182 160" stroke="#B8741F" stroke-width="6" stroke-linecap="round" fill="none"/>
   <path d="M218 160 Q234 155 250 162" stroke="#B8741F" stroke-width="6" stroke-linecap="round" fill="none"/>
   ${V('ey','c',1,`<path d="M150 192 Q165 181 180 192" ${st}/><path d="M220 192 Q235 181 250 192" ${st}/>`)}
   ${V('ey','o',0,`<circle cx="165" cy="192" r="10" fill="${br}"/><circle cx="235" cy="192" r="10" fill="${br}"/><path d="M151 184 Q165 178 179 184 M221 184 Q235 178 249 184" stroke="#F6CF7D" stroke-width="7" fill="none"/>`)}
   <ellipse cx="180" cy="244" rx="30" ry="24" fill="#FCE7BF"/><ellipse cx="220" cy="244" rx="30" ry="24" fill="#FCE7BF"/>
   <path d="M184 218 Q200 211 216 218 Q209 233 200 235 Q191 233 184 218Z" fill="#7A4A2A"/>
   <path d="M200 235 L200 246 M183 252 Q200 265 217 252" stroke="#7A4A2A" stroke-width="5" stroke-linecap="round" fill="none"/>
   <ellipse cx="142" cy="232" rx="16" ry="9" fill="#F2A47C" opacity=".4"/><ellipse cx="258" cy="232" rx="16" ry="9" fill="#F2A47C" opacity=".4"/>
  </g></svg>`;
},

person(fill=C.g, o={}){ // pictogram
  return `<svg viewBox="0 0 100 160" class="pict"><circle cx="50" cy="30" r="24" fill="${fill}"/><path d="M12 160 V104 Q12 64 50 64 Q88 64 88 104 V160Z" fill="${fill}"/></svg>`;
},

// ---- duotone icons 120x120
icon(name, o={}){
  const s=o.stroke||C.dg, f=o.fill||C.lg2, w=o.w||7;
  const st=`stroke="${s}" stroke-width="${w}" stroke-linecap="round" stroke-linejoin="round"`;
  const I={
   speech:`<path d="M18 28 Q18 16 30 16 H92 Q104 16 104 28 V70 Q104 82 92 82 H52 L30 102 V82 H30 Q18 82 18 70Z" fill="${f}" ${st}/><path d="M38 40 H84 M38 58 H70" ${st} fill="none"/>`,
   laugh:`<circle cx="60" cy="60" r="44" fill="${f}" ${st}/><path d="M38 50 Q46 40 54 50 M66 50 Q74 40 82 50" ${st} fill="none"/><path d="M36 66 H84 Q82 92 60 92 Q38 92 36 66Z" fill="#fff" ${st}/>`,
   face:`<circle cx="60" cy="60" r="44" fill="${f}" ${st}/><circle cx="44" cy="52" r="5" fill="${s}"/><circle cx="76" cy="52" r="5" fill="${s}"/><path d="M44 78 H76" ${st}/>`,
   smile:`<circle cx="60" cy="60" r="44" fill="${f}" ${st}/><path d="M38 52 Q46 44 54 52 M66 52 Q74 44 82 52" ${st} fill="none"/><path d="M42 72 Q60 90 78 72" ${st} fill="none"/>`,
   tone:`<path d="M18 28 Q18 16 30 16 H92 Q104 16 104 28 V70 Q104 82 92 82 H52 L30 102 V82 H30 Q18 82 18 70Z" fill="${f}" ${st}/><path d="M36 50 V50 M48 40 V60 M60 32 V68 M72 42 V58 M84 48 V52" ${st}/>`,
   reply:`<rect x="30" y="10" width="60" height="100" rx="14" fill="${f}" ${st}/><path d="M46 36 H74 M46 52 H66" ${st}/><circle cx="92" cy="18" r="16" fill="${C.red}"/><text x="92" y="25" font-size="22" font-weight="900" text-anchor="middle" fill="#fff" font-family="P">1</text>`,
   heart:`<path d="M60 100 C20 74 12 50 20 36 C30 18 52 18 60 36 C68 18 90 18 100 36 C108 50 100 74 60 100Z" fill="${f}" ${st}/>`,
   eye:`<path d="M10 60 Q60 10 110 60 Q60 110 10 60Z" fill="#fff" ${st}/><circle cx="60" cy="60" r="18" fill="${f}" ${st}/><circle cx="60" cy="60" r="6" fill="${s}"/>`,
   ear:`<path d="M40 44 Q40 14 66 14 Q94 14 94 44 Q94 62 80 72 Q70 80 70 94 Q70 108 56 108 Q44 108 42 96" fill="${f}" ${st}/><path d="M56 46 Q56 32 68 32 Q80 32 80 46 Q80 54 72 58" ${st} fill="none"/>`,
   clock:`<circle cx="60" cy="60" r="46" fill="${f}" ${st}/><path d="M60 32 V60 L80 72" ${st} fill="none"/>`,
   doc:`<path d="M26 10 H74 L96 32 V110 H26Z" fill="#fff" ${st}/><path d="M74 10 V32 H96" fill="${f}" ${st}/><path d="M40 52 H82 M40 70 H82 M40 88 H66" ${st}/>`,
   clip:`<rect x="22" y="18" width="76" height="94" rx="12" fill="#fff" ${st}/><rect x="42" y="8" width="36" height="20" rx="6" fill="${f}" ${st}/><path d="M38 56 l8 8 l14 -16 M38 86 l8 8 l14 -16 M70 58 H86 M70 88 H86" ${st} fill="none"/>`,
   leaf:`<path d="M20 100 C20 50 50 18 104 16 C102 70 72 100 20 100Z" fill="${f}" ${st}/><path d="M22 98 C46 72 66 56 84 40" ${st} fill="none"/>`,
   spark:`<path d="M60 8 L70 48 L110 60 L70 72 L60 112 L50 72 L10 60 L50 48Z" fill="${f}" ${st}/>`,
   check:`<circle cx="60" cy="60" r="48" fill="${C.g}"/><path d="M36 62 L54 80 L86 44" stroke="#fff" stroke-width="12" stroke-linecap="round" stroke-linejoin="round" fill="none"/>`,
   x:`<circle cx="60" cy="60" r="48" fill="${C.red}"/><path d="M40 40 L80 80 M80 40 L40 80" stroke="#fff" stroke-width="12" stroke-linecap="round"/>`,
   film:`<rect x="14" y="26" width="92" height="68" rx="10" fill="${f}" ${st}/><path d="M50 44 L76 60 L50 76Z" fill="${s}"/>`,
   food:`<path d="M18 58 H102 Q100 100 60 100 Q20 100 18 58Z" fill="${f}" ${st}/><path d="M44 46 Q40 30 48 20 M62 46 Q58 30 66 20 M80 46 Q76 30 84 20" ${st} fill="none"/>`,
   paw:`<ellipse cx="60" cy="76" rx="26" ry="22" fill="${f}" ${st}/><circle cx="30" cy="46" r="11" fill="${f}" ${st}/><circle cx="50" cy="30" r="11" fill="${f}" ${st}/><circle cx="72" cy="30" r="11" fill="${f}" ${st}/><circle cx="92" cy="46" r="11" fill="${f}" ${st}/>`,
   people:`<circle cx="42" cy="40" r="16" fill="${f}" ${st}/><path d="M14 104 Q14 66 42 66 Q70 66 70 104Z" fill="${f}" ${st}/><circle cx="82" cy="44" r="14" fill="#fff" ${st}/><path d="M62 104 Q62 72 82 72 Q106 72 106 104Z" fill="#fff" ${st}/>`,
   book:`<path d="M60 26 Q40 14 14 18 V96 Q40 92 60 104 Q80 92 106 96 V18 Q80 14 60 26Z" fill="${f}" ${st}/><path d="M60 26 V104" ${st}/>`,
   mag:`<circle cx="50" cy="50" r="34" fill="#fff" fill-opacity=".25" ${st}/><path d="M76 76 L106 106" stroke="${s}" stroke-width="14" stroke-linecap="round"/>`,
   level:`<rect x="8" y="42" width="104" height="36" rx="18" fill="${f}" ${st}/><rect x="44" y="50" width="32" height="20" rx="10" fill="#fff" ${st}/><circle cx="60" cy="60" r="5" fill="${s}"/>`,
   cursor:`<path d="M30 14 L30 96 L50 78 L64 108 L78 102 L64 72 L92 70Z" fill="#fff" ${st}/>`,
   undo:`<path d="M44 30 L16 56 L44 82" ${st} fill="none"/><path d="M18 56 H72 Q102 56 102 84 Q102 104 76 104" ${st} fill="none"/>`,
  };
  const sz=o.size||120;
  return `<svg viewBox="0 0 120 120" width="${sz}" height="${sz}" class="ico">${I[name]}</svg>`;
},

xmark(sz=170){return `<svg viewBox="0 0 120 120" width="${sz}" height="${sz}"><path d="M22 22 L98 98 M98 22 L22 98" stroke="${C.red}" stroke-width="18" stroke-linecap="round"/></svg>`;},
omark(sz=170){return `<svg viewBox="0 0 120 120" width="${sz}" height="${sz}"><circle cx="60" cy="60" r="44" stroke="${C.g}" stroke-width="16" fill="none"/></svg>`;},

heartMeter(){
  const hp='M270 470 C110 360 30 270 40 170 C50 80 130 30 200 50 C235 60 258 84 270 110 C282 84 305 60 340 50 C410 30 490 80 500 170 C510 270 430 360 270 470Z';
  return `<svg viewBox="0 0 540 500" width="560" class="hm"><defs><clipPath id="hclip"><path d="${hp}"/></clipPath></defs>
   <path d="${hp}" fill="#fff"/>
   <g clip-path="url(#hclip)"><rect class="liq" x="0" y="40" width="540" height="480" fill="${C.g}"/>
     <path class="wave" d="M0 40 Q67 20 135 40 T270 40 T405 40 T540 40 V60 H0Z" fill="${C.g}"/>
     <g class="bites"></g></g>
   <path d="${hp}" fill="none" stroke="${C.dg}" stroke-width="12"/></svg>`;
},

dial(label, color=C.lg2){
  let ticks='';
  for(let i=0;i<=10;i++){const a=(-120+i*24)*Math.PI/180;ticks+=`<line x1="${150+Math.sin(a)*118}" y1="${160-Math.cos(a)*118}" x2="${150+Math.sin(a)*(i%5?104:96)}" y2="${160-Math.cos(a)*(i%5?104:96)}" stroke="#fff" stroke-opacity=".6" stroke-width="${i%5?4:7}" stroke-linecap="round"/>`;}
  return `<svg viewBox="0 0 300 300" width="330"><circle cx="150" cy="160" r="134" fill="rgba(255,255,255,.06)" stroke="rgba(255,255,255,.18)" stroke-width="3"/>
   <path d="M${150+Math.sin(-2.094)*126} ${160-Math.cos(-2.094)*126} A126 126 0 1 1 ${150+Math.sin(2.094)*126} ${160-Math.cos(2.094)*126}" stroke="${color}" stroke-opacity=".35" stroke-width="10" fill="none" stroke-linecap="round"/>
   ${ticks}<g class="needle" style="transform-origin:150px 160px"><path d="M150 160 L144 70 L150 46 L156 70Z" fill="${color}"/></g><circle cx="150" cy="160" r="16" fill="${color}"/></svg>`;
},

flag(){
  return `<svg viewBox="0 0 300 520" width="300"><rect x="60" y="30" width="16" height="440" rx="8" fill="${C.dg}"/>
   <path class="cloth" d="M76 44 Q140 20 200 44 T290 44 V170 Q230 146 170 170 T76 170Z" fill="${C.g}"/>
   <rect class="base" x="10" y="460" width="116" height="52" rx="12" fill="${C.dg}"/></svg>`;
},
};
