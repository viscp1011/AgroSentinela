/* AgroSentinela - Painel do Produtor (multi-campo, reativo, 2 IAs) */
const API = "http://localhost:8000";
const CULT = {"soja":{"nome":"Soja","emoji":"🌱","umidade_critica":0.2,"umidade_alvo":0.26,"obs":"Sensível ao déficit hídrico na floração e no enchimento de grãos."},"milho":{"nome":"Milho","emoji":"🌽","umidade_critica":0.2,"umidade_alvo":0.27,"obs":"Alta demanda de água no pendoamento (formação da espiga)."},"cana":{"nome":"Cana-de-açúcar","emoji":"🎋","umidade_critica":0.18,"umidade_alvo":0.24,"obs":"Cultura rústica; tolera períodos secos moderados."},"feijao":{"nome":"Feijão","emoji":"🫘","umidade_critica":0.22,"umidade_alvo":0.28,"obs":"Raiz curta e ciclo rápido; muito sensível à falta de água."},"arroz":{"nome":"Arroz","emoji":"🍚","umidade_critica":0.35,"umidade_alvo":0.42,"obs":"Irrigado por inundação; exige solo encharcado (água alta)."},"algodao":{"nome":"Algodão","emoji":"☁️","umidade_critica":0.19,"umidade_alvo":0.25,"obs":"Demanda hídrica alta no florescimento e formação de maçãs."},"trigo":{"nome":"Trigo","emoji":"🌾","umidade_critica":0.2,"umidade_alvo":0.26,"obs":"Cultura de inverno; déficit no espigamento reduz a produção."},"cafe":{"nome":"Café","emoji":"☕","umidade_critica":0.22,"umidade_alvo":0.28,"obs":"Perene; estresse hídrico afeta floração e enchimento do grão."},"mandioca":{"nome":"Mandioca","emoji":"🥔","umidade_critica":0.15,"umidade_alvo":0.2,"obs":"Muito rústica e tolerante à seca; baixa exigência de água."},"sorgo":{"nome":"Sorgo","emoji":"🟤","umidade_critica":0.16,"umidade_alvo":0.22,"obs":"Tolerante à seca; boa alternativa em regiões secas."}};
const SERIE = [0.1546,0.1553,0.1559,0.1564,0.1569,0.1574,0.1578,0.1582,0.1589,0.1597,0.1606,0.1617,0.163,0.1643,0.1656,0.1669,0.1682,0.1695,0.1708,0.1721,0.1734,0.1748,0.1762,0.1776];
const DEMO = [
  {id:"campo-soja", nome:"Campo da Soja", cultura:"soja", umidade:0.135},
  {id:"campo-milho",nome:"Campo do Milho",cultura:"milho",umidade:0.205},
  {id:"campo-arroz",nome:"Várzea (Arroz)",cultura:"arroz",umidade:0.300},
  {id:"campo-cafe", nome:"Sítio do Café", cultura:"cafe", umidade:0.260},
];
const GANHO=0.012, DECAI=0.04, MAXMM=8.0;
function previsaoAoVivo(u){const d=u-SERIE[0];return SERIE.map(v=>Math.max(0.03,+(v+d).toFixed(4)));}
function cronogramaAoVivo(prev,alvo){let irr=[],com=[],ef=0;for(const base of prev){ef*=(1-DECAI);let us=base+ef,i=0;if(us<alvo){i=Math.min(MAXMM,(alvo-us)/GANHO);ef+=i*GANHO;}irr.push(+i.toFixed(2));com.push(+(base+ef).toFixed(4));}return {irr,com};}
function detalheLocal(dev){const c=CULT[dev.cultura];const prev=previsaoAoVivo(dev.umidade);const {irr,com}=cronogramaAoVivo(prev,c.umidade_alvo);const risco=prev.filter(v=>v<c.umidade_critica).length;return {id:dev.id,nome:dev.nome,cultura:dev.cultura,cultura_nome:c.nome,emoji:c.emoji,obs:c.obs,umidade_critica:c.umidade_critica,umidade_alvo:c.umidade_alvo,umidade_atual:dev.umidade,previsao_umidade:prev,cronograma_mm_por_hora:irr,umidade_com_irrigacao:com,total_agua_mm:+irr.reduce((a,b)=>a+b,0).toFixed(1),em_risco:risco>0,horas_em_risco:[...Array(risco).keys()]};}
let online=false, selId=null, ultimoDetalhe=null;
async function api(path,opt){const r=await fetch(API+path,Object.assign({signal:AbortSignal.timeout(2500)},opt||{}));if(!r.ok)throw 0;return r.json();}
async function carregar(){
  const st=document.getElementById("status"); let lista, clima=null;
  try{const d=await api("/api/dispositivos");lista=d.dispositivos;clima=d.clima_atual;online=true;st.textContent="conectado (dados ao vivo)";st.className="status-conexao online";}
  catch(e){online=false;lista=DEMO.map(dv=>{const x=detalheLocal(dv);return {id:x.id,nome:x.nome,cultura:x.cultura,cultura_nome:x.cultura_nome,emoji:x.emoji,umidade_atual:x.umidade_atual,umidade_critica:x.umidade_critica,umidade_alvo:x.umidade_alvo,em_risco:x.em_risco,total_agua_mm:x.total_agua_mm};});st.textContent="modo demonstração";st.className="status-conexao demo";}
  renderClima(clima);
  if(!lista.length){document.getElementById("campos").innerHTML='<div class="campos-vazio">⏳ Aguardando os sensores enviarem leitura...<br><small>Ligue o ESP32 no Wokwi (ou rode <b>enviar_leitura_teste.py --demo</b>).</small></div>';document.getElementById("detalhe").classList.add("oculto");selId=null;return;}
  renderCampos(lista);
  const ids=lista.map(d=>d.id);
  if(!selId||!ids.includes(selId))selecionar(lista[0].id);else selecionar(selId,true);
}
function renderClima(c){const t=document.getElementById("c-temp"),e=document.getElementById("c-extra");
  if(c&&c.temperatura!=null){t.textContent=Math.round(c.temperatura);e.textContent="umidade do ar "+c.umidade_ar+"% · chuva "+c.precipitacao+" mm · "+c.fonte;}
  else{t.textContent="--";e.textContent="ligue o servidor para o clima ao vivo";}}
function corUmid(u,crit,alvo){if(u<crit)return"#d64545";if(u<alvo)return"#e0a83a";return"#3cb371";}
function rotuloUmid(u,crit,alvo){if(u<crit)return"Terra seca";if(u<alvo)return"Razoável";return"Terra boa";}
function renderCampos(lista){
  const box=document.getElementById("campos");box.innerHTML="";
  for(const d of lista){
    const cor=corUmid(d.umidade_atual,d.umidade_critica,d.umidade_alvo);
    const pct=Math.min(100,Math.round(d.umidade_atual/d.umidade_alvo*100));
    let opts="";for(const k in CULT)opts+=`<option value="${k}" ${k===d.cultura?"selected":""}>${CULT[k].emoji} ${CULT[k].nome}</option>`;
    const conselho=d.total_agua_mm>0.5?`<div class="conselho regar">💧 <b>Regar ~${d.total_agua_mm.toFixed(1)} mm</b> hoje (≈ ${Math.round(d.total_agua_mm)} L por m²).</div>`:`<div class="conselho ok">✅ <b>Sem necessidade de rega</b> agora.</div>`;
    const card=document.createElement("div");card.className="campo-card"+(d.id===selId?" sel":"");card.dataset.id=d.id;
    card.innerHTML=`<div class="campo-topo"><div class="campo-nome">${d.nome}</div><div class="campo-emoji">${d.emoji}</div></div>
      <select class="campo-sel-cultura" data-id="${d.id}">${opts}</select>
      <div class="badge ${d.em_risco?"risco":"ok"}">${d.em_risco?"⚠️ Precisa de água":"👍 Tudo certo"}</div>
      <div class="barra-umid"><div class="barra-fill" style="width:${pct}%;background:${cor}"></div></div>
      <div class="umid-legenda"><span>${rotuloUmid(d.umidade_atual,d.umidade_critica,d.umidade_alvo)}</span><span>${(d.umidade_atual*100).toFixed(0)}%</span></div>${conselho}`;
    card.addEventListener("click",ev=>{if(ev.target.classList.contains("campo-sel-cultura"))return;selecionar(d.id);});
    box.appendChild(card);
  }
  box.querySelectorAll(".campo-sel-cultura").forEach(sel=>{sel.addEventListener("change",async e=>{
    const id=e.target.dataset.id,cultura=e.target.value;
    if(online){try{await api("/api/campo/cultura",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({id,cultura})});}catch(_){}}
    else{const dv=DEMO.find(x=>x.id===id);if(dv)dv.cultura=cultura;}
    selId=id;carregar();});});
}
async function selecionar(id){
  selId=id;let det;
  if(online){try{det=await api("/api/campo?id="+encodeURIComponent(id));}catch(e){det=null;}}
  if(!det||det.erro){const dv=DEMO.find(x=>x.id===id)||DEMO[0];det=detalheLocal(dv);}
  ultimoDetalhe=det;renderDetalhe(det);
}
function renderDetalhe(d){
  document.getElementById("detalhe").classList.remove("oculto");
  document.getElementById("d-nome").textContent=d.nome+" "+d.emoji;
  document.getElementById("d-obs").textContent=d.cultura_nome+" — terra boa a partir de "+(d.umidade_alvo*100).toFixed(0)+"%, risco abaixo de "+(d.umidade_critica*100).toFixed(0)+"%. "+(d.obs||"");
  const st=document.getElementById("d-status");st.textContent=d.em_risco?"⚠️ Precisa de água":"👍 Tudo certo";st.style.color=d.em_risco?"#ff9b9b":"#7be0a0";
  document.getElementById("d-agua").textContent=d.total_agua_mm.toFixed(1);
  document.getElementById("d-agua-litros").textContent="≈ "+Math.round(d.total_agua_mm)+" L por m²";
  document.getElementById("d-umid").textContent=(d.umidade_atual*100).toFixed(0)+"%";
  document.getElementById("d-umid-label").textContent=rotuloUmid(d.umidade_atual,d.umidade_critica,d.umidade_alvo);
  const naive=(d.horas_em_risco?d.horas_em_risco.length:0)*4;
  document.getElementById("d-economia").textContent=naive>0?Math.max(0,Math.round((1-d.total_agua_mm/naive)*100)):0;
  desenhar(d);
  document.querySelectorAll(".campo-card").forEach(c=>c.classList.toggle("sel",c.dataset.id===d.id));
}
let g1,g2;
function desenhar(d){
  const horas=d.previsao_umidade.map((_,i)=>"+"+i+"h");
  if(g1)g1.destroy();
  g1=new Chart(document.getElementById("g-previsao"),{type:"line",data:{labels:horas,datasets:[
    {label:"Zona de risco",data:horas.map(()=>d.umidade_critica),fill:"start",backgroundColor:"rgba(214,69,69,.13)",borderColor:"#e0a83a",borderDash:[6,4],pointRadius:0,order:3},
    {label:"Umidade prevista (IA 1)",data:d.previsao_umidade,borderColor:"#d64545",backgroundColor:"rgba(214,69,69,.05)",tension:.3,fill:false,borderWidth:3,order:1}]},options:opc("Umidade (m³/m³)")});
  if(g2)g2.destroy();
  g2=new Chart(document.getElementById("g-irrigacao"),{data:{labels:horas,datasets:[
    {type:"bar",label:"Água a dar (mm)",data:d.cronograma_mm_por_hora,backgroundColor:"rgba(43,138,214,.55)",yAxisID:"y",order:3},
    {type:"line",label:"Terra COM o plano (IA 2)",data:d.umidade_com_irrigacao,borderColor:"#3cb371",backgroundColor:"rgba(60,179,113,.1)",tension:.3,yAxisID:"y1",borderWidth:3,order:1},
    {type:"line",label:"Terra SEM regar",data:d.previsao_umidade,borderColor:"#d64545",borderDash:[5,4],pointRadius:0,tension:.3,yAxisID:"y1",order:2}]},
    options:{responsive:true,plugins:{legend:{labels:{color:"#eaf3ee",font:{size:11}}}},scales:{
      y:{position:"left",title:{display:true,text:"Água (mm)",color:"#9db5a8"},ticks:{color:"#9db5a8"},grid:{color:"rgba(255,255,255,.05)"},beginAtZero:true},
      y1:{position:"right",title:{display:true,text:"Umidade",color:"#9db5a8"},ticks:{color:"#9db5a8"},grid:{drawOnChartArea:false}},
      x:{ticks:{color:"#9db5a8",maxTicksLimit:12},grid:{color:"rgba(255,255,255,.05)"}}}}});
}
function opc(t){return{responsive:true,plugins:{legend:{labels:{color:"#eaf3ee",font:{size:11}}}},scales:{
  y:{title:{display:true,text:t,color:"#9db5a8"},ticks:{color:"#9db5a8"},grid:{color:"rgba(255,255,255,.05)"}},
  x:{ticks:{color:"#9db5a8",maxTicksLimit:12},grid:{color:"rgba(255,255,255,.05)"}}}};}
document.getElementById("btn-voz").addEventListener("click",()=>{
  if(!("speechSynthesis"in window)){alert("Navegador sem voz.");return;}
  const d=ultimoDetalhe;if(!d)return;
  const msg=d.em_risco?`Atenção produtor. O campo ${d.nome}, com ${d.cultura_nome}, está com risco de falta de água. Recomendamos regar cerca de ${d.total_agua_mm.toFixed(0)} milímetros hoje.`:`Tudo certo no campo ${d.nome}, com ${d.cultura_nome}. A terra deve continuar saudável. Não precisa regar agora.`;
  const f=new SpeechSynthesisUtterance(msg);f.lang="pt-BR";f.rate=.98;window.speechSynthesis.cancel();window.speechSynthesis.speak(f);
});
carregar();setInterval(carregar,8000);
