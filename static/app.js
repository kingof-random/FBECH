/* F-BECH — FEROX BAJA Engineering & Compliance Hub */
'use strict';
const $ = (s, r=document) => r.querySelector(s);
const $$ = (s, r=document) => Array.from(r.querySelectorAll(s));
const esc = (v) => String(v == null ? '' : v).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const escAttr = (v) => esc(v).replace(/\n/g, ' ');
const fmt = (v, d=1) => (v == null || v === '' || isNaN(Number(v))) ? '—' : Number(v).toFixed(d).replace(/\.0$/, '');
const pct = (a,b) => b ? Math.round(100*a/b) : 0;
const STATUS = ['Not Started','In Progress','Pending Verification','Verified','Failed','Not Applicable'];
const STATUS_CLASS = {'Not Started':'ns','In Progress':'ip','Pending Verification':'pv','Verified':'vf','Failed':'fl','Not Applicable':'na'};
const STATUS_SHORT = {'Not Started':'NS','In Progress':'IP','Pending Verification':'PV','Verified':'VF','Failed':'FL','Not Applicable':'NA'};
const SUBSYSTEM = {
  'Structure': ['Roll Cage — General','RRH','RHO','FBM','LDB','SIM','LFS','FAB','Lateral Cross Members','ALC','BLC','CLC','DLC','ELC','FLC','GLC','RLC','UST','Gussets','Butt Joints','Bolted Joints','Drilled Members'],
  'Driver Environment': ['Driver Clearance','Driver Restraint'],
  'Materials & Process': ['Materials & Documentation','Welding & Fabrication','Weld Samples'],
  'Documentation': ['Roll Cage Documentation']
};
function subsystemOf(comp){ for(const k in SUBSYSTEM) if(SUBSYSTEM[k].includes(comp)) return k; return 'Structure'; }
const FIG_PAGES={};
const S = {
  meta:{}, rules:[], checks:[], evidence:[], docs:[], issues:[], revisions:[], stats:{},
  ruleById:{}, checksByRule:{}, evByCheck:{}, treeOpen:{}, xrefStack:[], tab:'official',
  route:'dashboard', params:[], query:{}, ws:{article:'',component:'',status:'',priority:'',subsystem:'',q:''},
  dash:{article:'',component:'',status:'',priority:''}, reportScope:'B.3'
};

function xrefChip(x, extra=''){
  const id = x.target || x.ref;
  const label = esc(x.ref) + (x.target && x.target!==x.ref ? ' → '+esc(x.target) : '');
  if(x.resolved) return `<span class="chip x" data-xref="${escAttr(id)}" ${extra}>${label} ↗</span>`;
  return `<span class="chip x unres" title="Not found in the rulebook" ${extra}>${label} ✕ unresolved</span>`;
}
function statusPill(st){ return `<span class="pill ${STATUS_CLASS[st]||'ns'}">${esc(st)}</span>`; }
function priorityPill(p){ return `<span class="pill ${p==='High'?'hi':p==='Medium'?'md':'lo'}">${esc(p||'—')}</span>`; }
function resultPill(c){
  const r = c.auto_result;
  if(!c.eval || c.eval==='none') return `<span class="result none">Manual verification</span>`;
  if(!r) return `<span class="result none">Enter measurement</span>`;
  return r==='pass' ? `<span class="result pass">✓ Meets criterion</span>` : `<span class="result fail">✕ Does not meet</span>`;
}
function toast(msg, kind=''){ const d=document.createElement('div'); d.className='toast '+kind; d.textContent=msg; $('#toastRoot').appendChild(d); setTimeout(()=>{d.style.opacity='0';d.style.transition='.3s';setTimeout(()=>d.remove(),320)},2600); }
async function api(url, opts){ const r = await fetch(url, opts); if(!r.ok) throw new Error((await r.json().catch(()=>({}))).error || r.status); return r.json(); }
async function apiJSON(url, method, data){ return api(url, {method, headers:{'Content-Type':'application/json','X-CSRF-Token':window.FBECH_CSRF||''}, body:JSON.stringify(data||{})}); }
function showLogin(message=''){
  document.querySelector('.app').style.display='none';
  const root=$('#authRoot'); root.style.display='grid';
  root.innerHTML=`<form id="loginForm" style="width:min(420px,calc(100% - 32px));margin:auto;padding:30px;background:#111923;border:1px solid #344252;border-radius:16px;color:#eef3f8;box-shadow:0 20px 70px #0008">
    <div style="color:#ff8748;font-size:12px;font-weight:800;letter-spacing:2px">FEROX / F-BECH</div>
    <h1 style="margin:12px 0 6px;font-size:26px">Engineering workspace</h1>
    <p style="color:#9eacba;margin:0 0 22px">Sign in to access compliance records, evidence and project data.</p>
    <label style="display:block;margin:12px 0 6px">Username</label><input id="loginUser" autocomplete="username" required style="box-sizing:border-box;width:100%;padding:12px;background:#0b1118;color:#fff;border:1px solid #455466;border-radius:8px">
    <label style="display:block;margin:14px 0 6px">Password</label><input id="loginPass" type="password" autocomplete="current-password" required style="box-sizing:border-box;width:100%;padding:12px;background:#0b1118;color:#fff;border:1px solid #455466;border-radius:8px">
    <p id="loginError" style="color:#ff8c78;min-height:20px;font-size:13px">${esc(message)}</p>
    <button type="submit" style="width:100%;padding:12px;border:0;border-radius:8px;background:#f06a32;color:#fff;font-weight:800;cursor:pointer">Sign in</button>
    <p style="font-size:11px;color:#82909e;margin:18px 0 0">Public rulebook source pages remain accessible without signing in.</p>
  </form>`;
  $('#loginForm').onsubmit=async e=>{e.preventDefault();const b=$('#loginForm button');b.disabled=true;b.textContent='Signing in…';try{const r=await api('/api/login',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({username:$('#loginUser').value,password:$('#loginPass').value})});window.FBECH_CSRF=r.csrf_token;await startApp();}catch(err){$('#loginError').textContent=err.message==='401'?'Incorrect username or password':err.message;b.disabled=false;b.textContent='Sign in';}};
}
async function startApp(){
  $('#authRoot').style.display='none';document.querySelector('.app').style.display='';
  await refresh();
  const fr=await fetch('/figures.json');if(fr.ok)(await fr.json()).forEach(f=>FIG_PAGES[f.figure]=f);
  S.treeOpen['B']=true;S.treeOpen['B.3']=true;
  if(!window.FBECH_LISTENERS){window.addEventListener('hashchange',router);initSearch();$('#menuBtn').onclick=()=>$('#sidebar').classList.toggle('open');$('#printBtn').onclick=()=>{if(S.route!=='report'){location.hash='#/report';setTimeout(()=>window.print(),500);}else window.print();};window.FBECH_LISTENERS=true;}
  router();
}

/* ---------- state ---------- */
function indexState(){
  S.ruleById = {}; S.checksByRule = {}; S.evByCheck = {};
  for(const r of S.rules){ S.ruleById[r.id]=r; if(!S.checksByRule[r.id]) S.checksByRule[r.id]=[]; }
  for(const c of S.checks){ if(!S.checksByRule[c.rule_id]) S.checksByRule[c.rule_id]=[]; S.checksByRule[c.rule_id].push(c); }
  for(const e of S.evidence){ if(!S.evByCheck[e.check_id]) S.evByCheck[e.check_id]=[]; S.evByCheck[e.check_id].push(e); }
  for(const c of S.checks) c._evidence = (S.evByCheck[c.id]||[]).length;
}
async function refresh(){
  const d = await api('/api/bootstrap');
  Object.assign(S, d);
  indexState();
  updateSide();
}
async function refreshStats(){
  try{ S.stats = await api('/api/dashboard'); updateSide(); }catch(e){}
}
function updateSide(){
  const st=S.stats||{}; const p=st.compliance_pct||0;
  $('#sidePct').textContent = p+'%';
  $('#sideBar').style.width = p+'%';
  const open=(S.issues||[]).filter(i=>i.status!=='Closed').length;
  const b=$('#issueBadge'); b.textContent=open; b.classList.toggle('on', open>0);
}

/* ---------- router ---------- */
function parseHash(){
  const h = location.hash.replace(/^#\/?/,'') || 'dashboard';
  const [path, qs] = h.split('?');
  const seg = path.split('/').filter(Boolean);
  S.query = {}; if(qs) qs.split('&').forEach(p=>{const [k,v]=p.split('='); S.query[decodeURIComponent(k)]=decodeURIComponent(v||'');});
  S.route = seg[0]||'dashboard'; S.params = seg.slice(1);
}
function nav(route){ location.hash = '#/'+route; }
async function router(){
  if(window.innerWidth<900) $('#sidebar').classList.remove('open');
  parseHash();
  $$('.nav-item').forEach(a=>a.classList.toggle('active', a.dataset.route===S.route));
  const titles={dashboard:'Dashboard',rules:'Rulebook Navigator',workspace:'Compliance Workspace',components:'Components',docs:'Engineering Documentation',issues:'Outstanding Issues',report:'Compliance Report',coverage:'Rulebook Coverage',settings:'Project Settings',about:'Source & Method',rule:'Rulebook Navigator'};
  $('#crumb').textContent = titles[S.route]||'F-BECH';
  const view=$('#view');
  if(S.route==='dashboard') view.innerHTML = renderDashboard();
  else if(S.route==='rules') view.innerHTML = renderRules();
  else if(S.route==='rule') view.innerHTML = renderRulePage();
  else if(S.route==='workspace') view.innerHTML = renderWorkspace();
  else if(S.route==='components') view.innerHTML = renderComponents();
  else if(S.route==='docs') view.innerHTML = renderDocs();
  else if(S.route==='issues') view.innerHTML = renderIssues();
  else if(S.route==='report') view.innerHTML = renderReport();
  else if(S.route==='coverage') view.innerHTML = renderCoverage();
  else if(S.route==='settings') view.innerHTML = renderSettings();
  else if(S.route==='about') view.innerHTML = renderAbout();
  else view.innerHTML = renderDashboard();
  bindView();
  bindExtra();
  if(S.route==='dashboard') drawRing();
}
function bindView(){
  // generic data-nav
  $$('[data-nav]').forEach(el=>el.onclick=()=>nav(el.dataset.nav));
  // tree toggles
  $$('[data-part]').forEach(el=>el.onclick=()=>{ const p=el.dataset.part; S.treeOpen[p]=!S.treeOpen[p]; const sec=el.closest('.part'); sec.classList.toggle('closed', !S.treeOpen[p]); });
  $$('[data-article]').forEach(el=>el.onclick=()=>{ const a=el.dataset.article; S.treeOpen[a]=!S.treeOpen[a]; const sec=el.closest('.article'); sec.classList.toggle('closed', !S.treeOpen[a]); });
  $$('[data-sec]').forEach(el=>el.onclick=()=>{ S.xrefStack=[]; S.tab='official'; nav('rule/'+el.dataset.sec); });
  $$('[data-tab]').forEach(el=>el.onclick=()=>{ S.tab=el.dataset.tab; router(); });
  $$('[data-xref]').forEach(el=>el.onclick=()=>{ const id=el.dataset.xref; if(!S.ruleById[id]) return; S.xrefStack.push(id); router(); setTimeout(()=>{const t=document.querySelector('[data-xref-id="'+CSS.escape(id)+'"]'); if(t){const y=t.getBoundingClientRect().top+window.scrollY-110; window.scrollTo({top:y,behavior:'smooth'});}},40); });
  $$('[data-xpop]').forEach(el=>el.onclick=()=>{ S.xrefStack=S.xrefStack.slice(0, Number(el.dataset.xpop)); router(); });
  $$('[data-pageimg]').forEach(el=>el.onclick=()=>openPage(Number(el.dataset.pageimg)));
  $$('[data-evdel]').forEach(el=>el.onclick=()=>deleteEvidence(Number(el.dataset.evdel)));
  $$('[data-docedit]').forEach(el=>el.onclick=()=>openDocModal(Number(el.dataset.docedit)));
  $$('[data-docdel]').forEach(el=>el.onclick=()=>deleteDoc(Number(el.dataset.docdel)));
  $$('[data-issuedel]').forEach(el=>el.onclick=()=>deleteIssue(Number(el.dataset.issuedel)));
  $$('[data-issueedit]').forEach(el=>el.onclick=()=>openIssueModal(Number(el.dataset.issueedit)));
  $$('[data-revdel]').forEach(el=>el.onclick=()=>deleteRevision(Number(el.dataset.revdel)));
  $$('[data-compfilter]').forEach(el=>el.onclick=()=>{ S.ws.component=el.dataset.compfilter; S.ws.subsystem=''; nav('workspace'); });
  $$('[data-subsysfilter]').forEach(el=>el.onclick=()=>{ S.ws.subsystem=el.dataset.subsysfilter; S.ws.component=''; nav('workspace'); });
}

/* ---------- global search ---------- */
function initSearch(){
  const inp=$('#globalSearch'), box=$('#searchResults');
  const run=()=>{
    const q=inp.value.trim().toLowerCase();
    if(!q){ box.classList.remove('on'); box.innerHTML=''; return; }
    const all=S.rules.filter(r=>{
      const body=(r.body||[]).join(' ').toLowerCase();
      return r.id.toLowerCase().includes(q)||r.title.toLowerCase().includes(q)||body.includes(q)||(r.article_title||'').toLowerCase().includes(q);
    });
    const hits=all.slice(0,14);
    box.innerHTML = hits.length
      ? hits.map(r=>`<div class="sr-item" data-goto="${escAttr(r.id)}"><b>${esc(r.id)}</b><span>${esc(r.title)}</span><small>p.${r.page}</small></div>`).join('')
        + (all.length>14?`<div class="sr-empty">Showing 14 of ${all.length} matching clauses — refine the query.</div>`:'')
      : `<div class="sr-empty">No rules match “${esc(q)}”.</div>`;
    box.classList.add('on');
    $$('[data-goto]',box).forEach(el=>el.onclick=()=>{ box.classList.remove('on'); inp.value=''; S.xrefStack=[]; nav('rule/'+el.dataset.goto); });
  };
  inp.addEventListener('input', run);
  inp.addEventListener('keydown', e=>{ if(e.key==='Enter'){ const f=box.querySelector('[data-goto]'); if(f) f.click(); } if(e.key==='Escape'){ box.classList.remove('on'); } });
  document.addEventListener('click', e=>{ if(!e.target.closest('.topsearch')) box.classList.remove('on'); });
  document.addEventListener('keydown', e=>{ if(e.key==='/' && !/input|textarea/i.test(document.activeElement.tagName)){ e.preventDefault(); inp.focus(); } });
}
function openPage(n){
  openModal(`<div class="modal page-modal"><div class="modal-h"><h3>Source PDF — page ${n}</h3><button class="x" data-close>×</button></div><img src="/source/page/${n}" alt="Rulebook page ${n}"></div>`);
}
function openModal(html){
  const root=$('#modalRoot'); root.innerHTML=`<div class="modal-bg" data-mbg>${html}</div>`;
  $$('[data-close]',root).forEach(b=>b.onclick=closeModal);
  $('[data-mbg]',root).onclick=e=>{ if(e.target===$('[data-mbg]',root)) closeModal(); };
  $$('[data-close]',root).forEach(b=>b.onclick=closeModal);
}
function closeModal(){ $('#modalRoot').innerHTML=''; }

/* ---------- init ---------- */
(async function(){
  try{
    const auth=await api('/api/session');
    if(!auth.authenticated){showLogin();return;}
    window.FBECH_CSRF=auth.csrf_token;
    await startApp();
  }catch(e){$('#view').innerHTML='<div class="empty">Unable to connect to F-BECH.<br><small>'+esc(e.message)+'</small></div>';}
})();

/* ================= DASHBOARD ================= */
function drawRing(){
  const st=(S.dash.article||S.dash.component||S.dash.status||S.dash.priority) && S.route==='dashboard'
    ? statsFor(S.checks.filter(c=>{
        if(S.dash.article && (S.ruleById[c.rule_id]||{}).article!==S.dash.article) return false;
        if(S.dash.component && c.component!==S.dash.component) return false;
        if(S.dash.status && c.status!==S.dash.status) return false;
        if(S.dash.priority && c.priority!==S.dash.priority) return false;
        return true; }))
    : (S.stats||{});
  const p=st.compliance_pct||0; const c=2*Math.PI*74;
  const fg=$('.ring-fg'); if(!fg) return;
  fg.style.strokeDasharray=c; fg.style.strokeDashoffset=c*(1-p/100);
}
function kpi(label, val, sub, cls=''){ return `<div class="kpi"><div class="k-label">${esc(label)}</div><div class="k-val ${cls}">${esc(val)}</div><div class="k-sub">${esc(sub)}</div></div>`; }
function statsFor(list){
  const n=list.length; const cnt={}; let evid=0;
  list.forEach(c=>{ cnt[c.status]=(cnt[c.status]||0)+1; if((S.evByCheck[c.id]||[]).length) evid++; });
  const na=cnt['Not Applicable']||0, app=n-na;
  return { total_checks:n, applicable:app,
    verified:cnt['Verified']||0, failed:cnt['Failed']||0,
    pending:cnt['Pending Verification']||0, in_progress:cnt['In Progress']||0,
    not_started:cnt['Not Started']||0, not_applicable:na,
    evidence_pct: app?Math.round(100*evid/app):0,
    compliance_pct: app?Math.round(100*(cnt['Verified']||0)/app):0,
    total_rules:S.stats.total_rules, open_issues:S.stats.open_issues, critical_issues:S.stats.critical_issues };
}
function renderDashboard(){
  const st=S.stats||{}; const by=st.by_status||{};
  const filtered = S.checks.filter(c=>{
    if(S.dash.article && (S.ruleById[c.rule_id]||{}).article!==S.dash.article) return false;
    if(S.dash.component && c.component!==S.dash.component) return false;
    if(S.dash.status && c.status!==S.dash.status) return false;
    if(S.dash.priority && c.priority!==S.dash.priority) return false;
    return true;
  });
  const anyF = !!(S.dash.article||S.dash.component||S.dash.status||S.dash.priority);
  const fs = anyF ? statsFor(filtered) : st;
  const comps=[...new Set(S.checks.map(c=>c.component))].sort();
  const articles=(st.article_progress||[]);
  const articleRows = (st.rule_coverage||[]).map(rc=>{
    const ap=articles.find(a=>a.article===rc.article)||{total:0,verified:0,failed:0,na:0,pct:0};
    const r0=S.rules.find(r=>r.article===rc.article)||{};
    const status = rc.validated===rc.rules && rc.rules>0 ? '<span class="pill val">Validated</span>' : (rc.validated>0?'<span class="pill md">Partial</span>':'<span class="pill src">Source text only</span>');
    return `<tr>
      <td class="mono">${esc(rc.article)}</td>
      <td><b>${esc(r0.article_title||'—')}</b><div class="tiny muted">${esc(r0.part_title||'')}</div></td>
      <td class="center">${rc.rules}</td>
      <td class="center">${rc.validated}</td>
      <td class="center">${ap.total||0}</td>
      <td class="center">${ap.verified||0}</td>
      <td class="center">${ap.failed||0}</td>
      <td>${ap.total?`<div class="bar"><i style="width:${ap.pct||0}%"></i></div><span class="tiny muted">${fmt(ap.pct,0)}%</span>`:'<span class="tiny muted">—</span>'}</td>
      <td class="right">${status}</td>
    </tr>`;
  }).join('');
  const compRows=(st.component_progress||[]).slice(0,14).map(cp=>`<tr>
      <td><b>${esc(cp.component)}</b></td>
      <td class="center">${cp.total}</td>
      <td class="center">${cp.verified}</td>
      <td class="center">${cp.failed}</td>
      <td><div class="bar"><i style="width:${cp.pct||0}%"></i></div></td>
      <td class="right tiny">${fmt(cp.pct,0)}%</td>
    </tr>`).join('');
  const issues=(S.issues||[]).filter(i=>i.status!=='Closed');
  const crit=issues.filter(i=>i.severity==='Critical'||i.severity==='High');
  const issueRows=crit.length?crit.map(i=>`<div class="doc-item"><div class="di-body"><h4>${esc(i.title)}</h4><p>${esc(i.detail)}</p><div class="di-meta">${esc(i.severity)} · ${esc(i.status)}${i.rule_id?' · '+esc(i.rule_id):''}${i.owner?' · '+esc(i.owner):''}</div></div><div class="di-actions"><button class="icon-btn" data-issueedit="${i.id}">✎</button></div></div>`).join(''):'<div class="empty">No critical or high issues recorded.</div>';
  const recent=[...S.checks].filter(c=>c.updated_at).sort((a,b)=>b.updated_at.localeCompare(a.updated_at)).slice(0,6);
  return `
  <div class="page-head">
    <div><div class="eyebrow">FEROX · BAJA SAEINDIA CHENNAI 2027 · ICE</div><h1>Compliance Command</h1>
    <p>${esc(S.meta.vehicle||'FEROX 2027 ICE')} — ${esc(S.meta.competition||'')}</p></div>
    <div class="spacer"></div>
    <div style="text-align:right"><div class="tag">Rulebook v1.0 · 01 Sep 2026</div><div class="tag">PDF 1–100</div><div class="tag">Generated ${esc(S.meta.generated||'')}</div></div>
  </div>
  <div class="notice"><span class="ni">⚠</span><div><b>Team self-verification only.</b> A “Verified” status in F-BECH means FEROX has recorded and checked the evidence. It is <b>not</b> official acceptance — Technical Inspection and the BSC Technical Committee decide compliance at the event.</div></div>
  <div class="card hero" style="margin-bottom:14px">
    <div class="hero-ring">
      <div class="ring-wrap">
        <svg width="176" height="176" viewBox="0 0 176 176">
          <defs><linearGradient id="ringGrad" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#ff7a3d"/><stop offset="1" stop-color="#ffb020"/></linearGradient></defs>
          <circle class="ring-bg" cx="88" cy="88" r="74"></circle>
          <circle class="ring-fg" cx="88" cy="88" r="74"></circle>
        </svg>
        <div class="ring-label"><b>${fmt(fs.compliance_pct,0)}%</b><small>Verified / applicable</small></div>
      </div>
      <div class="small" style="color:#aeb9c7;margin-top:10px;text-align:center">${fs.verified||0} of ${fs.applicable||0} applicable checks verified</div>
      <div class="tiny" style="color:#64717f;margin-top:3px">${fs.total_checks||0} checks · ${fs.not_applicable||0} N/A</div>
      ${anyF?'<div class="tiny" style="color:#ffb020;margin-top:6px">Filtered view</div>':''}
    </div>
    <div class="hero-kpis">
      ${kpi('Total requirements',''+(st.total_rules||0),'rules extracted from the PDF','info')}
      ${kpi('Verified',''+(fs.verified||0),'checks with recorded pass','ok')}
      ${kpi('Failed',''+(fs.failed||0),'measured non-conformances','bad')}
      ${kpi('Pending verification',''+(fs.pending||0),'awaiting review / sign-off','warn')}
      ${kpi('In progress',''+(fs.in_progress||0),'work started, not verified','info')}
      ${kpi('Not started',''+(fs.not_started||0),'no measurement recorded yet','')}
      ${kpi('Evidence complete',''+fmt(fs.evidence_pct,0)+'%','checks with at least one file','ok')}
      ${kpi('Open issues',''+(st.open_issues||0),'unresolved design / docs items','warn')}
      ${kpi('Critical issues',''+(st.critical_issues||0),'critical or high severity','bad')}
    </div>
  </div>
  <div class="notice blue"><span class="ni">◈</span><div><b>Extraction status:</b> Part B, Article 3 — Roll Cage is fully processed (${(st.validated_rules||0)} validated rules, ${(st.total_checks||0)} engineering checks). All other articles are extracted as <b>source text only</b> — exact official wording, PDF page and cross-references are searchable, but interpretation and checks are pending Phase 5. See <a href="#/coverage" style="color:#b3410f;font-weight:700">Coverage Matrix</a>.</div></div>
  <div class="card" style="margin-bottom:14px">
    <div class="card-h"><h3>Article-wise progress</h3><span class="sub">checks &amp; rule extraction</span></div>
    <div style="overflow:auto;max-height:470px"><table class="tbl"><thead><tr><th>Article</th><th>Title</th><th class="center">Rules</th><th class="center">Validated</th><th class="center">Checks</th><th class="center">VF</th><th class="center">FL</th><th>Progress</th><th class="right">Status</th></tr></thead><tbody>${articleRows}</tbody></table></div>
  </div>
  <div class="grid g2" style="margin-bottom:14px">
    <div class="card">
      <div class="card-h"><h3>Component-wise progress</h3><span class="sub">verified / applicable</span></div>
      <div style="overflow:auto;max-height:430px"><table class="tbl"><thead><tr><th>Component</th><th class="center">Checks</th><th class="center">VF</th><th class="center">FL</th><th>Progress</th><th class="right">%</th></tr></thead><tbody>${compRows}</tbody></table></div>
    </div>
    <div class="card">
      <div class="card-h"><h3>Critical unresolved issues</h3><span class="sub">${crit.length} critical / high</span></div>
      <div style="max-height:430px;overflow:auto">${issueRows}</div>
      <div class="card-b" style="padding-top:8px"><a class="btn sm" href="#/issues" data-nav="issues">Open issue register →</a></div>
    </div>
  </div>
  <div class="card" style="margin-bottom:14px">
    <div class="card-h"><h3>Recently updated checks</h3><span class="sub">last 6</span></div>
    <div>${recent.length?recent.map(c=>`<div class="doc-item"><div class="di-body"><h4><span class="mono muted">${esc(c.id)}</span> ${esc(c.title)}</h4><p>${esc(c.rule_id)} · ${esc(c.component)}</p><div class="di-meta">${esc(c.updated_at)} · ${esc(c.status)}</div></div><div>${resultPill(c)}</div></div>`).join(''):'<div class="empty">No check has been updated yet.</div>'}</div>
  </div>
  <div class="card">
    <div class="card-h"><h3>Check register</h3><span class="sub">${filtered.length} of ${S.checks.length} checks</span>
      <div style="margin-left:auto;display:flex;gap:6px;flex-wrap:wrap">
        <select data-dashf="article"><option value="">All articles</option>${[...new Set(S.checks.map(c=>(S.ruleById[c.rule_id]||{}).article).filter(Boolean))].sort().map(a=>`<option ${S.dash.article===a?'selected':''}>${esc(a)}</option>`).join('')}</select>
        <select data-dashf="component"><option value="">All components</option>${comps.map(c=>`<option ${S.dash.component===c?'selected':''}>${esc(c)}</option>`).join('')}</select>
        <select data-dashf="status"><option value="">All statuses</option>${STATUS.map(s=>`<option ${S.dash.status===s?'selected':''}>${esc(s)}</option>`).join('')}</select>
        <select data-dashf="priority"><option value="">All priorities</option>${['High','Medium','Low'].map(s=>`<option ${S.dash.priority===s?'selected':''}>${esc(s)}</option>`).join('')}</select>
        ${anyF?'<button class="btn sm" data-dashreset>Reset</button>':''}
      </div>
    </div>
    <div style="overflow:auto;max-height:420px"><table class="tbl"><thead><tr><th>ID</th><th>Rule</th><th>Check</th><th>Component</th><th class="center">Result</th><th class="center">Status</th><th class="center">Priority</th></tr></thead><tbody>
      ${filtered.slice(0,80).map(c=>`<tr><td class="mono">${esc(c.id)}</td><td class="mono">${esc(c.rule_id)}</td><td>${esc(c.title)}</td><td class="small">${esc(c.component)}</td><td class="center">${resultPill(c)}</td><td class="center">${statusPill(c.status)}</td><td class="center">${priorityPill(c.priority)}</td></tr>`).join('')}
    </tbody></table>${filtered.length>80?`<div class="tiny muted" style="padding:8px 10px">Showing first 80 of ${filtered.length}. Use the workspace for the full register.</div>`:''}</div>
  </div>`;
}

/* ================= RULEBOOK NAVIGATOR ================= */
function buildTree(){
  const parts={};
  for(const r of S.rules){
    const p=parts[r.part]||(parts[r.part]={letter:r.part,title:r.part_title||r.part,articles:{}});
    const a=p.articles[r.article]||(p.articles[r.article]={key:r.article,title:r.article_title||r.article,page:r.page,sections:[]});
    a.sections.push(r);
  }
  const sortArt=(a,b)=>{const x=a.split('.').map(Number),y=b.split('.').map(Number);for(let i=0;i<Math.max(x.length,y.length);i++){if((x[i]||0)!==(y[i]||0))return (x[i]||0)-(y[i]||0);}return a.localeCompare(b);};
  const out=[];
  for(const k of Object.keys(parts).sort()){
    const p=parts[k]; out.push({...p,articleList:Object.values(p.articles).sort((a,b)=>sortArt(a.key,b.key))});
  }
  return out;
}
function treeHTML(q){
  if(q){
    const qq=q.toLowerCase();
    const hits=S.rules.filter(r=>r.id.toLowerCase().includes(qq)||r.title.toLowerCase().includes(qq)||((r.body||[]).join(' ').toLowerCase().includes(qq))).slice(0,120);
    if(!hits.length) return `<div class="tree-empty">No rules match “${esc(q)}”.</div>`;
    return `<div class="tiny muted" style="padding:8px 8px 4px">${hits.length} matching rules</div>`+hits.map(r=>`
      <div class="sec" data-sec="${escAttr(r.id)}"><span class="snum">${esc(r.id)}</span><span style="flex:1;overflow:hidden;text-overflow:ellipsis;white-space:nowrap">${esc(r.title)}</span><span class="sflag ${r.status==='validated'?'valid':'source'}"></span></div>`).join('');
  }
  const parts=buildTree();
  return parts.map(p=>{
    const open=S.treeOpen[p.letter]===true;
    return `<div class="part ${open?'':'closed'}">
      <div class="part-h" data-part="${p.letter}"><span class="caret">▾</span> Part ${esc(p.letter)} · ${esc(p.title)}</div>
      <div class="part-body">${p.articleList.map(a=>{
        const aopen=S.treeOpen[a.key]===true;
        return `<div class="article ${aopen?'':'closed'}">
          <div class="article-h" data-article="${escAttr(a.key)}"><span class="anum">${esc(a.key)}</span><span style="flex:1">${esc(a.title)}</span><span class="acount">${a.sections.length}</span></div>
          <div class="article-body">${a.sections.map(s=>`<div class="sec" data-sec="${escAttr(s.id)}"><span class="snum">${esc(s.id)}</span><span style="flex:1;overflow:hidden;text-overflow:ellipsis;white-space:nowrap">${esc(s.title)}</span><span class="sflag ${s.status==='validated'?'valid':'source'}"></span></div>`).join('')}</div>
        </div>`;}).join('')}</div>
    </div>`;}).join('');
}
function renderRules(){
  const q=S.query.q||'';
  const id=S.params[0]?decodeURIComponent(S.params[0]):null;
  const sel=id?S.ruleById[id]:null;
  return `
  <div class="page-head"><div><div class="eyebrow">Official source · exact wording</div><h1>Rulebook Navigator</h1>
  <p>Every numbered clause in the 100-page BSC 2027 ICE Rulebook, with PDF page, original text and clickable cross-references. Green dot = interpreted &amp; checked; purple dot = source text extracted, interpretation pending.</p></div>
  <div class="spacer"></div><div class="tag">${S.rules.length} rules</div><div class="tag">${(S.stats.validated_rules||0)} validated</div><div class="tag">${(S.stats.total_checks||0)} checks</div></div>
  <div class="navigator">
    <div class="card tree-pane">
      <div class="tree-search"><input id="treeSearch" placeholder="Filter sections…" value="${escAttr(q)}"></div>
      <div class="tree" id="tree">${treeHTML(q)}</div>
    </div>
    <div id="ruleDetail">${sel?ruleDetailHTML(sel):(S.route==='rule'?`<div class="card"><div class="empty">Rule not found. Use the tree or search.</div></div>`:`<div class="card"><div class="empty" style="padding:60px 20px"><b style="font-size:16px;color:#2a3542">Select a rule to open it.</b><br><br>Start with <a href="#/rule/B.3.2.6" style="color:#b3410f;font-weight:700">B.3.2.6 — RRH</a> or <a href="#/rule/B.3.2.16" style="color:#b3410f;font-weight:700">B.3.2.16 — Roll Cage Materials</a>.<br><br><span class="muted small">Cross-references inside a rule are clickable; the referenced rule expands below without losing this one.</span></div></div>`)}</div>
  </div>`;
}
function renderRulePage(){ return renderRules(); }
function ruleDetailHTML(r){
  const tabs=[
    {k:'official',l:'Official requirement'},
    {k:'plain',l:'Plain English'},
    {k:'engineering',l:'Engineering interpretation'},
    {k:'xrefs',l:'Cross-references',c:(r.xrefs||[]).length},
    {k:'checks',l:'Verification checks',c:(S.checksByRule[r.id]||[]).length},
    {k:'notes',l:'Ambiguities',c:(r.notes||[]).length}
  ];
  const tab=S.tab||'official';
  return `<div class="card">
    <div class="rule-head">
      <div class="rule-title-row"><span class="rule-num">${esc(r.id)}</span><h2 class="rule-title">${esc(r.title)}</h2>
        <button class="btn sm" data-pageimg="${r.page}">View PDF p.${r.page}</button></div>
      <div class="rule-meta">
        <span class="chip">Part ${esc(r.part)} · ${esc(r.part_title||'')}</span>
        <span class="chip">Article ${esc(r.article)} · ${esc(r.article_title||'')}</span>
        <span class="chip">PDF p.${r.page}</span>
        <span class="chip">${esc(r.kind)}</span>
        ${r.status==='validated'?'<span class="pill val">Interpreted &amp; checked</span>':'<span class="pill src">Source text only</span>'}
        ${priorityPill(r.priority)}
      </div>
      ${S.xrefStack.length?`<div class="crumbs" style="margin-top:10px;margin-bottom:0"><span>Trail:</span><a data-xpop="0">${esc(r.id)}</a>${S.xrefStack.map((x,i)=>`<span class="sep">›</span><a data-xpop="${i+1}">${esc(x)}</a>`).join('')}<span class="sep">·</span><a data-xpop="0" style="color:#8b98a8">clear</a></div>`:''}
    </div>
    <div class="tabs">${tabs.map(t=>`<div class="tab ${tab===t.k?'active':''}" data-tab="${t.k}">${t.l}${t.c?`<span class="cnt">${t.c}</span>`:''}</div>`).join('')}</div>
    <div class="rule-body">${ruleTabHTML(r,tab)}</div>
  </div>
  ${S.xrefStack.map(id=>xrefPanelHTML(id)).join('')}`;
}
function ruleTabHTML(r,tab){
  if(tab==='plain'){
    if(!r.plain||!r.plain.length) return `<div class="notice gray"><span class="ni">◈</span><div><b>Interpretation pending.</b> This article has been extracted as source text only. The plain-English layer will be added in Phase 5. The official wording is complete and searchable.</div></div>`;
    return `<div class="official-label">Plain-English explanation · FEROX interpretation, not official wording</div><div class="rule-text">${r.plain.map(p=>`<p>${esc(p)}</p>`).join('')}</div>`;
  }
  if(tab==='engineering'){
    if(!r.engineering||!r.engineering.length) return `<div class="notice gray"><span class="ni">◈</span><div><b>Engineering interpretation pending.</b> This article has been extracted as source text only. No engineering guidance has been invented for it.</div></div>`;
    return `<div class="official-label">Engineering interpretation · FEROX, not official wording</div><div class="rule-text">${r.engineering.map(p=>`<p>${esc(p)}</p>`).join('')}</div>`;
  }
  if(tab==='notes'){
    if(!r.notes||!r.notes.length) return `<div class="notice gray"><span class="ni">✓</span><div><b>No unresolved ambiguity recorded.</b> The rule is transcribed as printed. If the wording is unclear in use, raise a rules inquiry to BTC.</div></div>`;
    return `<div class="official-label">Source ambiguities &amp; integrity flags</div>`+r.notes.map(n=>`<div class="notice" style="margin-bottom:9px"><span class="ni">!</span><div>${esc(n)}</div></div>`).join('');
  }
  if(tab==='xrefs'){
    const refs=r.xrefs||[];
    const by=S.rules.filter(x=>(x.xrefs||[]).some(y=>y.ref===r.id));
    return `<div class="official-label">Rules referenced by ${esc(r.id)}</div>
      ${refs.length?`<div style="display:flex;gap:6px;flex-wrap:wrap;margin-bottom:18px">${refs.map(x=>xrefChip(x)).join('')}</div>`:'<div class="empty" style="padding:14px;text-align:left">No numbered cross-references in this clause.</div>'}
      <div class="official-label">Rules that reference ${esc(r.id)}</div>
      ${by.length?`<div style="display:flex;gap:6px;flex-wrap:wrap">${by.map(x=>`<span class="chip x" data-xref="${escAttr(x.id)}">${esc(x.id)} · ${esc(x.title)}</span>`).join('')}</div>`:'<div class="empty" style="padding:14px;text-align:left">No other extracted rule references this clause by number.</div>'}
      <div class="notice gray" style="margin-top:16px"><span class="ni">ⓘ</span><div>Clicking a reference expands the target rule <b>below this one</b>, so the current context is preserved. Use the breadcrumb trail to return.</div></div>`;
  }
  if(tab==='checks'){
    const cs=S.checksByRule[r.id]||[];
    if(!cs.length) return `<div class="notice gray"><span class="ni">◈</span><div><b>No engineering checks yet.</b> Checks are added per article in Phase 5. B.3 is the first fully checked module.</div></div>`;
    return `<div class="official-label">FEROX verification checks for this rule</div>`+cs.map(c=>`<div class="doc-item"><div class="di-body"><h4><span class="mono muted">${esc(c.id)}</span> ${esc(c.title)}</h4><p>${esc(c.criterion)}</p><div class="di-meta">${esc(c.component)} · ${esc(c.method)}</div></div><div style="display:flex;flex-direction:column;gap:4px;align-items:flex-end">${resultPill(c)}${statusPill(c.status)}</div></div>`).join('')+`<div style="margin-top:10px"><a class="btn sm" href="#/workspace" data-nav="workspace">Open compliance workspace →</a></div>`;
  }
  // official
  let out=`<div class="official-label">Official requirement · verbatim from BSC 2027 ICE Rulebook v1.0, PDF p.${r.page}</div>`;
  if(r.body&&r.body.length){
    out+=`<div class="rule-text">${r.body.map(p=>`<p>${esc(p)}</p>`).join('')}</div>`;
  } else {
    out+=`<div class="notice gray"><span class="ni">◈</span><div>This is a parent heading with no body text in the source. Its requirements are carried by the subsections listed in the navigator.</div></div>`;
  }
  if(r.table_data){
    const t=r.table_data;
    out+=`<table class="rule-table"><thead><tr>${t.columns.map(c=>`<th>${esc(c)}</th>`).join('')}</tr></thead><tbody>${t.rows.map(row=>`<tr>${row.map(c=>`<td>${esc(c)}</td>`).join('')}</tr>`).join('')}</tbody></table>
    <div class="caption">${esc(t.caption)}</div>${(t.notes||[]).map(n=>`<div class="tiny muted">${esc(n)}</div>`).join('')}`;
  }
  if(r.figures&&r.figures.length){
    const imgs=r.figures.filter(f=>FIG_PAGES[f]).map(f=>`<figure class="fig-card"><a href="/static/img/${FIG_PAGES[f].file}" target="_blank" title="Open full size"><img src="/static/img/${FIG_PAGES[f].file}" alt="Figure ${esc(f)}" loading="lazy"></a><figcaption><b>Figure ${esc(f)}</b><span>PDF p.${FIG_PAGES[f].page}</span></figcaption></figure>`).join('');
    const pages=r.figures.filter(f=>!FIG_PAGES[f]);
    out+=`<div class="official-label" style="margin-top:16px">Figures referenced in this clause</div>
    ${imgs?`<div class="fig-strip">${imgs}</div>`:''}
    ${pages.length?`<div class="fig-strip"><div class="fig-thumb" data-pageimg="${r.page}"><img src="/source/page/${r.page}" alt="PDF page ${r.page}" loading="lazy"><span>PDF p.${r.page} — ${pages.map(f=>esc(f)).join(', ')} (no separate image; see page)</span></div></div>`:''}
    <div class="tiny muted" style="margin-top:6px">Cropped verbatim from the rulebook PDF — click a figure for full size. Rule text and figure numbers are unchanged.</div>`;
  }
  if(r.xrefs&&r.xrefs.length){
    out+=`<div class="official-label" style="margin-top:16px">Cross-references in this clause</div><div style="display:flex;gap:6px;flex-wrap:wrap">${r.xrefs.map(x=>xrefChip(x)).join('')}</div><div class="tiny muted" style="margin-top:5px">Click to expand the referenced rule below without losing this one.</div>`;
  }
  out+=`<div class="notice gray" style="margin-top:16px"><span class="ni">ⓘ</span><div>Official wording is reproduced verbatim. PDF line-break hyphenation artefacts have been normalised; no requirement has been rewritten. Interpretations are kept on separate tabs.</div></div>`;
  return out;
}
function xrefPanelHTML(id){
  const r=S.ruleById[id]; if(!r) return `<div class="card"><div class="empty">Reference ${esc(id)} not found.</div></div>`;
  const idx=S.xrefStack.indexOf(id);
  const mainId=S.params[0]?decodeURIComponent(S.params[0]):'';
  const from=idx===0?mainId:S.xrefStack[idx-1];
  return `<div class="xref-panel" data-xref-id="${escAttr(id)}" style="margin-top:12px">
    <div class="xp-h"><span>↳ referenced from ${esc(from||'')}</span><b>${esc(r.id)}</b><span style="flex:1"></span><a data-xpop="${idx}" style="color:#8a5a00;cursor:pointer;font-weight:700">✕ close</a></div>
    <div class="xp-b">
      <div style="font-weight:800;font-size:14px;margin-bottom:6px">${esc(r.title)}</div>
      <div class="rule-text">${((r.body&&r.body.length)?r.body.slice(0,3):(r.plain&&r.plain.length?r.plain.slice(0,2):['Parent heading with no body text — see its subsections.'])).map(p=>`<p>${esc(p)}</p>`).join('')}${(r.body||[]).length>3?'<p class="muted small">… continued on the rule page</p>':''}</div>
      <div style="display:flex;gap:6px;flex-wrap:wrap;margin-top:8px">
        <span class="chip">PDF p.${r.page}</span>
        ${r.status==='validated'?'<span class="pill val">Interpreted</span>':'<span class="pill src">Source only</span>'}
        ${(r.xrefs||[]).filter(x=>x.resolved).slice(0,6).map(x=>xrefChip(x)).join('')}
        <span class="chip x" data-sec="${escAttr(r.id)}" style="background:#fff3ec;color:#b3410f">Open full rule →</span>
      </div>
    </div>
  </div>`;
}

/* ================= WORKSPACE ================= */
function evalCheck(c,v){
  if(!c.eval||c.eval==='none') return null;
  if(v==null||String(v).trim()==='') return null;
  const n=Number(String(v).replace(',','.'));
  if(isNaN(n)) return null;
  if(c.eval==='min') return n>=Number(c.min_val)?'pass':'fail';
  if(c.eval==='max') return n<=Number(c.max_val)?'pass':'fail';
  if(c.eval==='range') return (n>=Number(c.min_val)&&n<=Number(c.max_val))?'pass':'fail';
  return null;
}
function renderWorkspace(){
  const f=S.ws;
  const comps=[...new Set(S.checks.map(c=>c.component))].sort();
  let list=S.checks.filter(c=>{
    if(f.article&&(S.ruleById[c.rule_id]||{}).article!==f.article) return false;
    if(f.component&&c.component!==f.component) return false;
    if(f.status&&c.status!==f.status) return false;
    if(f.priority&&c.priority!==f.priority) return false;
    if(f.subsystem&&subsystemOf(c.component)!==f.subsystem) return false;
    if(f.q){const q=f.q.toLowerCase(); if(!(c.id.toLowerCase().includes(q)||c.title.toLowerCase().includes(q)||c.rule_id.toLowerCase().includes(q)||c.criterion.toLowerCase().includes(q)||c.component.toLowerCase().includes(q))) return false;}
    return true;
  });
  const order={}; S.rules.forEach((r,i)=>order[r.id]=i);
  const groups={};
  for(const c of list){ (groups[c.rule_id]=groups[c.rule_id]||[]).push(c); }
  const keys=Object.keys(groups).sort((a,b)=>(order[a]??9999)-(order[b]??9999));
  return `
  <div class="page-head"><div><div class="eyebrow">Verification · measurement · evidence</div><h1>Roll Cage Compliance Workspace</h1>
  <p>Part B, Article 3 — every clause converted into a measurable check. Enter the as-designed or as-built value; F-BECH evaluates it against the exact rule threshold and records the evidence.</p></div>
  <div class="spacer"></div><div class="tag">${list.length} checks shown</div><div class="tag">${S.checks.filter(c=>c.status==='Verified').length} verified</div><div class="tag">${S.checks.filter(c=>c.status==='Failed').length} failed</div></div>
  <div class="card" style="margin-bottom:14px">
    <div class="card-h"><h3>Figure B-9 · Secondary member support finder</h3><span class="sub">B.3.2.4 · lookup, not a substitute for the rule</span></div>
    <div class="card-b">
      <div class="finder">
        <div class="field"><label>Member length (mm)</label><input type="number" id="sfLen" placeholder="e.g. 900" min="0" step="1"></div>
        <div class="field"><label>Bend angle (°)</label><input type="number" id="sfAng" placeholder="e.g. 15" min="0" step="1"></div>
        <button class="btn primary" id="sfBtn">Evaluate support requirement</button>
        <div class="field" style="min-width:0"><label>&nbsp;</label><button class="btn" id="sfClr">Reset</button></div>
      </div>
      <div class="finder-result" id="sfOut" style="display:none"></div>
    </div>
  </div>
  <div class="card">
    <div class="filters">
      <label>Article</label><select data-wsf="article"><option value="">All articles</option>${[...new Set(S.checks.map(c=>(S.ruleById[c.rule_id]||{}).article).filter(Boolean))].sort().map(a=>`<option ${f.article===a?'selected':''}>${esc(a)}</option>`).join('')}</select>
      <label>Component</label><select data-wsf="component"><option value="">All components</option>${comps.map(c=>`<option ${f.component===c?'selected':''}>${esc(c)}</option>`).join('')}</select>
      <label>Status</label><select data-wsf="status"><option value="">All statuses</option>${STATUS.map(s=>`<option ${f.status===s?'selected':''}>${esc(s)}</option>`).join('')}</select>
      <label>Priority</label><select data-wsf="priority"><option value="">All priorities</option>${['High','Medium','Low'].map(s=>`<option ${f.priority===s?'selected':''}>${esc(s)}</option>`).join('')}</select>
      <label>Subsystem</label><select data-wsf="subsystem"><option value="">All subsystems</option>${Object.keys(SUBSYSTEM).map(s=>`<option ${f.subsystem===s?'selected':''}>${esc(s)}</option>`).join('')}</select>
      <input type="search" data-wsf="q" placeholder="Search checks…" value="${escAttr(f.q)}" style="margin-left:auto">
      <button class="btn sm" id="wsReset">Reset</button>
    </div>
    <div style="padding:14px">${keys.length?keys.map(k=>{
      const r=S.ruleById[k]||{id:k,title:k,page:''};
      const cs=groups[k]; const vf=cs.filter(c=>c.status==='Verified').length; const fl=cs.filter(c=>c.status==='Failed').length;
      return `<div class="group">
        <div class="group-h"><span class="gnum">${esc(k)}</span><h4>${esc(r.title)}</h4>
          <span class="chip">PDF p.${r.page||'—'}</span>
          <span class="gsub">${vf}/${cs.length} verified${fl?` · <span style="color:#b91c1c">${fl} failed</span>`:''}</span>
          <a class="btn sm" href="#/rule/${encodeURIComponent(k)}" data-nav="rule/${encodeURIComponent(k)}">Open rule</a></div>
        <div class="check-list">${cs.map(checkHTML).join('')}</div>
      </div>`;}).join(''):'<div class="empty">No checks match the current filters.</div>'}</div>
  </div>`;
}
function checkHTML(c){
  const open=false; const ev=S.evByCheck[c.id]||[];
  return `<div class="check ${open?'open':''}" data-check="${escAttr(c.id)}">
    <div class="check-row" data-checkrow="${escAttr(c.id)}">
      <span class="chev">▸</span><span class="check-id">${esc(c.id)}</span>
      <span class="check-title">${esc(c.title)}<span class="crit">${esc(c.criterion)}</span></span>
      <span class="check-badges"><span class="chip">${esc(c.component)}</span>${priorityPill(c.priority)}<span data-result="${escAttr(c.id)}">${resultPill(c)}</span><span data-statuspill="${escAttr(c.id)}">${statusPill(c.status)}</span><span class="tiny muted">${ev.length} file${ev.length===1?'':'s'}</span></span>
    </div>
    <div class="check-detail">
      <div class="check-grid">
        <div>
          <div class="crit-box"><b>Exact acceptance criterion · ${esc(c.rule_id)}</b>${esc(c.criterion)}</div>
          <div class="tiny muted" style="margin:-4px 0 9px">Quoted from the rule. “…” marks omitted context — open the rule for the full clause.</div>
          <div class="grid g2" style="gap:10px">
            <div class="field"><label>Verification method</label><div class="small" style="color:#3b4756">${esc(c.method)}</div></div>
            <div class="field"><label>Evidence required</label><div class="small" style="color:#3b4756">${esc(c.evidence_required)}</div></div>
          </div>
          ${c.eval&&c.eval!=='none'?`<div class="field"><label>${esc(c.label||'Measured value')}</label>
            <div class="meas-row"><input type="number" step="any" data-meas="${escAttr(c.id)}" value="${c.measured!=null?escAttr(c.measured):''}" placeholder="Enter value">
            <span class="unit">${esc(c.unit)}</span><span data-result-inline="${escAttr(c.id)}">${resultPill(c)}</span></div>
            <div class="tiny muted" style="margin-top:5px">${c.eval==='min'?`Must be ≥ ${c.min_val} ${esc(c.unit)}`:c.eval==='max'?`Must be ≤ ${c.max_val} ${esc(c.unit)}`:`Must be between ${c.min_val} and ${c.max_val} ${esc(c.unit)}`} · auto-evaluated from the exact rule threshold.</div></div>`:''}
          <div class="grid g2" style="gap:10px">
            <div class="field"><label>Status</label><select data-status="${escAttr(c.id)}">${STATUS.map(s=>`<option ${c.status===s?'selected':''}>${esc(s)}</option>`).join('')}</select></div>
            <div class="field"><label>Responsible member</label><input type="text" data-assignee="${escAttr(c.id)}" value="${escAttr(c.assignee||'')}" placeholder="Name / roll number"></div>
          </div>
          <div class="field"><label>Remarks · design decisions, observations, unresolved items</label><textarea data-remarks="${escAttr(c.id)}" placeholder="Record how the value was obtained, any deviation, and the reference to the calculation or drawing.">${esc(c.remarks||'')}</textarea></div>
          <div class="field"><label>Evidence · ${ev.length} file${ev.length===1?'':'s'} attached</label>
            <div class="upload"><input type="file" multiple data-evfile="${escAttr(c.id)}" accept=".pdf,.png,.jpg,.jpeg,.webp,.xlsx,.xls,.docx,.doc,.csv,.txt,.zip,.stp,.step,.igs,.iges,.CATPart,.CATDrawing"><span class="tiny muted">CATIA screenshots, drawings, certs, invoices, photos, calcs</span></div>
            <div class="evidence-list" data-evlist="${escAttr(c.id)}">${ev.map(e=>`<div class="ev-item"><span>📎</span><a href="/uploads/${encodeURIComponent(e.stored)}" target="_blank" rel="noopener">${esc(e.filename)}</a><span class="tiny muted">${esc((e.uploaded_at||'').slice(0,10))}</span><button class="del" data-evdel="${e.id}" title="Remove">×</button></div>`).join('')}</div>
          </div>
          <div style="display:flex;gap:6px;flex-wrap:wrap"><a class="btn sm" href="#/rule/${encodeURIComponent(c.rule_id)}" data-nav="rule/${encodeURIComponent(c.rule_id)}">Open rule ${esc(c.rule_id)} →</a><span class="tiny muted" style="align-self:center">Updated ${esc(c.updated_at||'—')}</span></div>
        </div>
        <div>
          <div class="card" style="box-shadow:none;background:#fff">
            <div class="card-h"><h3>Evaluation</h3></div>
            <div class="card-b">
              <div style="margin-bottom:10px" data-result-card="${escAttr(c.id)}">${resultPill(c)}</div>
              ${c.eval&&c.eval!=='none'?`<div class="small muted">Rule threshold: <b>${c.eval==='min'?'≥ '+c.min_val:c.eval==='max'?'≤ '+c.max_val:c.min_val+' – '+c.max_val} ${esc(c.unit)}</b><br>No threshold is invented — the evaluation is configured only from the printed rule.</div>`:`<div class="small muted">This requirement is qualitative. Record the inspection result in the status and describe the method and observation in remarks. F-BECH does not auto-pass qualitative checks.</div>`}
              <div style="border-top:1px solid var(--cline);margin-top:12px;padding-top:10px">
                <div class="tiny muted" style="text-transform:uppercase;letter-spacing:.08em;font-weight:700;margin-bottom:6px">Traceability</div>
                <div class="small">Rule <b>${esc(c.rule_id)}</b> · PDF p.${S.ruleById[c.rule_id]?.page||'?'}<br>Component: ${esc(c.component)}<br>Evidence: ${ev.length} file${ev.length===1?'':'s'}</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>`;
}
function updateResultPills(id){
  const c=S.checks.find(x=>x.id===id); if(!c) return;
  const html=resultPill(c);
  $$('[data-result="'+CSS.escape(id)+'"],[data-result-inline="'+CSS.escape(id)+'"],[data-result-card="'+CSS.escape(id)+'"]').forEach(el=>el.innerHTML=html);
  const row=document.querySelector('[data-checkrow="'+CSS.escape(id)+'"]');
  if(row){ const b=row.querySelector('.tiny.muted'); if(b) b.textContent=(S.evByCheck[id]||[]).length+' file'+((S.evByCheck[id]||[]).length===1?'':'s'); }
  $$('[data-statuspill="'+CSS.escape(id)+'"]').forEach(el=>el.innerHTML=statusPill(c.status));
}
async function saveCheck(id, patch){
  const c=S.checks.find(x=>x.id===id); if(!c) return;
  try{
    const r=await apiJSON('/api/checks/'+id,'POST',patch);
    Object.assign(c,r.check); c.auto_result=r.check.auto_result; c._evidence=r.evidence_count;
    const sel=document.querySelector('[data-status="'+CSS.escape(id)+'"]'); if(sel&&sel.value!==c.status) sel.value=c.status;
    updateResultPills(id); refreshStats();
  }catch(e){ toast('Save failed: '+e.message,'err'); }
}
function debounce(fn,ms){let t;return(...a)=>{clearTimeout(t);t=setTimeout(()=>fn(...a),ms);};}
const saveMeas=debounce((id,v)=>saveCheck(id,{measured:v}),650);
const saveRemarks=debounce((id,v)=>saveCheck(id,{remarks:v}),900);
const saveAssignee=debounce((id,v)=>saveCheck(id,{assignee:v}),700);
function bindWorkspace(){
  $$('[data-checkrow]').forEach(el=>el.onclick=e=>{ if(e.target.closest('.check-detail')) return; const box=el.closest('.check'); box.classList.toggle('open'); });
  $$('[data-meas]').forEach(el=>el.oninput=()=>{
    const id=el.dataset.meas; const c=S.checks.find(x=>x.id===id); if(!c) return;
    c.measured=el.value===''?null:el.value; c.auto_result=evalCheck(c,el.value); updateResultPills(id); saveMeas(id,el.value);
  });
  $$('[data-status]').forEach(el=>el.onchange=()=>saveCheck(el.dataset.status,{status:el.value}));
  $$('[data-remarks]').forEach(el=>el.oninput=()=>saveRemarks(el.dataset.remarks,el.value));
  $$('[data-assignee]').forEach(el=>el.oninput=()=>saveAssignee(el.dataset.assignee,el.value));
  $$('[data-evfile]').forEach(el=>el.onchange=async()=>{
    const id=el.dataset.evfile; if(!el.files||!el.files.length) return;
    const fd=new FormData(); for(const f of el.files) fd.append('files',f);
    try{
      const r=await api('/api/checks/'+id+'/evidence',{method:'POST',headers:{'X-CSRF-Token':window.FBECH_CSRF||''},body:fd});
      for(const e of r.saved){ S.evidence.push(e); if(!S.evByCheck[id]) S.evByCheck[id]=[]; S.evByCheck[id].push(e); }
      const c=S.checks.find(x=>x.id===id); if(c) c._evidence=r.evidence_count;
      const list=document.querySelector('[data-evlist="'+CSS.escape(id)+'"]'); if(list) list.innerHTML=(S.evByCheck[id]||[]).map(e=>`<div class="ev-item"><span>📎</span><a href="/uploads/${encodeURIComponent(e.stored)}" target="_blank" rel="noopener">${esc(e.filename)}</a><span class="tiny muted">${esc((e.uploaded_at||'').slice(0,10))}</span><button class="del" data-evdel="${e.id}" title="Remove">×</button></div>`).join('');
      bindView(); updateResultPills(id); toast('Evidence attached to '+id,'ok'); refreshStats();
    }catch(e){ toast('Upload failed: '+e.message,'err'); }
    el.value='';
  });
  // filters
  $$('[data-wsf]').forEach(el=>{
    const k=el.dataset.wsf;
    const go=()=>{ S.ws[k]=el.value; router(); };
    if(k==='q') el.oninput=debounce(go,220); else el.onchange=go;
  });
  const reset=$('#wsReset'); if(reset) reset.onclick=()=>{ S.ws={article:'',component:'',status:'',priority:'',subsystem:'',q:''}; router(); };
  // support finder
  const b=$('#sfBtn'); if(b) b.onclick=supportFinder;
  const clr=$('#sfClr'); if(clr) clr.onclick=()=>{ $('#sfLen').value=''; $('#sfAng').value=''; $('#sfOut').style.display='none'; };
}
function supportFinder(){
  const len=parseFloat($('#sfLen').value), ang=parseFloat($('#sfAng').value), out=$('#sfOut');
  if(isNaN(len)||isNaN(ang)||len<0||ang<0){ out.style.display='block'; out.innerHTML='<b>Enter both a length and a bend angle.</b>'; return; }
  let n=0, where='', note='';
  if(ang===0){
    if(len>1016){ n=1; where='within 50.8 mm (2 in) of the midpoint of the overall tube length'; note='* midpoint rule'; }
  } else if(ang<=30){
    if(len>838){ n=1; where='within the tangents of the bend'; note='** tangent rule'; }
  } else {
    n=len>838?2:1; where='within the tangents of the bend'+(n===2?' — connect to two unique Named Points':''); note='** tangent rule';
  }
  out.style.display='block';
  out.innerHTML=`<div style="display:flex;gap:12px;align-items:center;flex-wrap:wrap"><b style="font-size:15px">${n===0?'No Additional Support Tube required':n+' Additional Support Tube'+(n>1?'s':'')+' required'}</b><span class="pill ${n?'md':'vf'}">Figure B-9</span></div>
    <div class="small" style="margin-top:4px">Length ${len} mm · bend ${ang}°${n?` · ${where} · ${note}`:' · within the “No Supports Required” band'}.</div>
    <div class="tiny muted" style="margin-top:4px">This is a lookup of Figure B-9 for secondary members only. Confirm the member is Secondary and the dimensions are centreline-to-centreline before relying on it.</div>`;
}

/* ================= COMPONENTS ================= */
function renderComponents(){
  const groups={};
  for(const c of S.checks){ (groups[c.component]=groups[c.component]||[]).push(c); }
  const cards=Object.keys(groups).sort().map(k=>{
    const cs=groups[k]; const vf=cs.filter(c=>c.status==='Verified').length; const fl=cs.filter(c=>c.status==='Failed').length;
    const rules=[...new Set(cs.map(c=>c.rule_id))];
    const p=Math.round(100*vf/cs.length);
    return `<div class="comp-card" data-compfilter="${escAttr(k)}">
      <h4>${esc(k)}</h4><div class="cc-sub">${rules.length} rule${rules.length===1?'':'s'} · ${rules.slice(0,3).map(r=>esc(r)).join(', ')}${rules.length>3?' …':''}</div>
      <div class="bar ${fl?'red':p===100?'green':''}"><i style="width:${p}%"></i></div>
      <div class="cc-nums"><span><b>${cs.length}</b> checks</span><span><b style="color:#15803d">${vf}</b> VF</span>${fl?`<span><b style="color:#b91c1c">${fl}</b> FL</span>`:''}<span style="margin-left:auto"><b>${p}%</b></span></div>
    </div>`;
  }).join('');
  const subs=Object.keys(SUBSYSTEM).map(k=>{
    const cs=S.checks.filter(c=>subsystemOf(c.component)===k); const vf=cs.filter(c=>c.status==='Verified').length; const fl=cs.filter(c=>c.status==='Failed').length;
    return `<div class="comp-card" data-subsysfilter="${escAttr(k)}"><h4>${esc(k)}</h4><div class="cc-sub">${new Set(cs.map(c=>c.component)).size} components</div><div class="bar ${fl?'red':vf===cs.length&&cs.length?'green':''}"><i style="width:${cs.length?Math.round(100*vf/cs.length):0}%"></i></div><div class="cc-nums"><span><b>${cs.length}</b> checks</span><span><b style="color:#15803d">${vf}</b> VF</span>${fl?`<span><b style="color:#b91c1c">${fl}</b> FL</span>`:''}<span style="margin-left:auto"><b>${cs.length?Math.round(100*vf/cs.length):0}%</b></span></div></div>`;
  }).join('');
  return `<div class="page-head"><div><div class="eyebrow">Rulebook terminology · no invented names</div><h1>Component Workspace</h1>
  <p>Checks are organised around the members and joints named in Article 3 — RRH, RHO, FBM, LDB, SIM, LFS, FAB, the lateral cross members, UST, gussets, butt joints, weld samples, materials, driver clearance and documentation. Click a component to open its checks.</p></div></div>
  <div class="card" style="margin-bottom:14px"><div class="card-h"><h3>Engineering subsystems</h3><span class="sub">derived from the rulebook's component names</span></div><div class="card-b"><div class="grid g4" style="gap:10px">${subs}</div></div></div>
  <div class="grid g3" style="margin-bottom:14px">${cards}</div>
  <div class="card"><div class="card-h"><h3>Component → rules map</h3></div><div style="overflow:auto"><table class="tbl"><thead><tr><th>Component</th><th>Rules</th><th class="center">Checks</th><th class="center">VF</th><th class="center">FL</th><th>Progress</th></tr></thead><tbody>
  ${Object.keys(groups).sort().map(k=>{const cs=groups[k],vf=cs.filter(c=>c.status==='Verified').length,fl=cs.filter(c=>c.status==='Failed').length;return `<tr><td><b>${esc(k)}</b></td><td class="small">${[...new Set(cs.map(c=>c.rule_id))].map(r=>`<span class="tag">${esc(r)}</span>`).join('')}</td><td class="center">${cs.length}</td><td class="center">${vf}</td><td class="center">${fl}</td><td><div class="bar"><i style="width:${Math.round(100*vf/cs.length)}%"></i></div></td></tr>`;}).join('')}
  </tbody></table></div></div>`;
}

/* ================= DOCS ================= */
function renderDocs(){
  const cats=['Design Assumptions','CAD Measurements','Material Selection','Procurement Records','Welding & Fabrication','Engineering Calculations','Inspection Records','Evidence & Photographs','Design Revision History'];
  if(!S.docCat) S.docCat=cats[0];
  const docs=S.docs.filter(d=>d.category===S.docCat);
  return `<div class="page-head"><div><div class="eyebrow">Design record · audit trail</div><h1>Engineering Documentation</h1>
  <p>Design assumptions and justifications, CAD measurements, material selection and procurement, welding and fabrication records, calculations, inspection records, evidence and revision history. Every entry is stored against the project, not against a PDF page.</p></div>
  <div class="spacer"></div><button class="btn primary" id="addDoc">+ Add entry</button></div>
  <div class="doc-tabs">${cats.map(c=>`<span class="doc-tab ${S.docCat===c?'active':''}" data-doccat="${escAttr(c)}">${esc(c)}</span>`).join('')}</div>
  <div class="card" style="margin-bottom:16px">
    <div class="card-h"><h3>${esc(S.docCat)}</h3><span class="sub">${docs.length} entr${docs.length===1?'y':'ies'}</span></div>
    <div>${docs.length?docs.map(d=>`<div class="doc-item"><div class="di-body"><h4>${esc(d.title)}</h4><p>${esc(d.body)}</p><div class="di-meta">${esc(d.created_at)}${d.ref?' · Ref: '+esc(d.ref):''}${d.updated_at&&d.updated_at!==d.created_at?' · updated '+esc(d.updated_at):''}</div></div><div class="di-actions"><button class="icon-btn" data-docedit="${d.id}" title="Edit">✎</button><button class="icon-btn" data-docdel="${d.id}" title="Delete">×</button></div></div>`).join(''):'<div class="empty">No entries in this category yet.</div>'}</div>
  </div>
  <div class="grid g2">
    <div class="card"><div class="card-h"><h3>Design revision history</h3><span class="sub">${S.revisions.length} revisions</span></div>
      <div>${S.revisions.length?`<table class="tbl"><thead><tr><th>Rev</th><th>Date</th><th>Author</th><th>Description</th><th></th></tr></thead><tbody>${S.revisions.map(r=>`<tr><td class="mono"><b>${esc(r.rev)}</b></td><td class="nowrap">${esc(r.date)}</td><td>${esc(r.author)}</td><td>${esc(r.description)}</td><td class="right"><button class="icon-btn" data-revdel="${r.id}">×</button></td></tr>`).join('')}</tbody></table>`:'<div class="empty">No revisions recorded.</div>'}</div>
      <div class="card-b" style="border-top:1px solid var(--cline)"><div class="finder"><div class="field"><label>Rev</label><input id="revRev" placeholder="A"></div><div class="field"><label>Date</label><input id="revDate" type="date"></div><div class="field"><label>Author</label><input id="revAuthor" placeholder="Name"></div><div class="field" style="flex:1;min-width:220px"><label>Description</label><input id="revDesc" placeholder="What changed and why"></div><button class="btn primary" id="addRev">Add</button></div></div>
    </div>
    <div class="card"><div class="card-h"><h3>Roll Cage Documentation Package</h3><span class="sub">B.3.7</span></div>
      <div class="card-b small">
        <p style="margin-top:0"><b>B.3.7.1 — Required documents:</b> Roll Cage Specification Sheet, material documentation (invoices, certifications, calculations) and a single isometric diagram of the frame highlighting professional fabrication.</p>
        <p><b>B.3.7.2 — Submission:</b> Google Drive folder with (a) spec sheet, (b) material invoice, (c) material test/certification, (d) calculations per B.3.2.16, (e) outsourced/professionally fabricated parts diagram. Share the link for DR 2 by email to <span class="mono">bsc@saeiss.org</span>.</p>
        <p><b>B.3.7.3 — Process:</b> first come, first served; typical review 30 days after the deadline; rejected packages must be corrected and resubmitted until marked Accepted.</p>
        <div class="notice" style="margin-bottom:0"><span class="ni">!</span><div><b>Track this as a project gate.</b> The package is not accepted until the BSCTI marks it Accepted. Use the issue register to track rejection items.</div></div>
      </div>
    </div>
  </div>`;
}

/* ================= ISSUES ================= */
function renderIssues(){
  const iss=S.issues||[];
  return `<div class="page-head"><div><div class="eyebrow">Open items · blockers · ambiguities</div><h1>Outstanding Issues</h1>
  <p>Design decisions, unresolved rule ambiguities, documentation gaps and inspection findings. Severity drives the dashboard's critical-issue count; closing an issue does not close the underlying check.</p></div>
  <div class="spacer"></div><button class="btn primary" id="addIssue">+ Add issue</button></div>
  <div class="card"><div class="card-h"><h3>Issue register</h3><span class="sub">${iss.filter(i=>i.status!=='Closed').length} open</span></div>
  <div style="overflow:auto"><table class="tbl"><thead><tr><th>ID</th><th>Issue</th><th>Severity</th><th>Status</th><th>Rule</th><th>Owner</th><th>Updated</th><th></th></tr></thead><tbody>
  ${iss.length?iss.map(i=>`<tr><td class="mono">#${i.id}</td><td><b>${esc(i.title)}</b><div class="tiny muted">${esc(i.detail)}</div></td><td><span class="pill ${i.severity==='Critical'?'hi':i.severity==='High'?'hi':i.severity==='Medium'?'md':'lo'}">${esc(i.severity)}</span></td><td><span class="pill ${i.status==='Closed'?'ns':i.status==='Blocked'?'fl':i.status==='In Progress'?'ip':'pv'}">${esc(i.status)}</span></td><td class="mono">${esc(i.rule_id||'—')}</td><td>${esc(i.owner||'—')}</td><td class="nowrap tiny">${esc(i.updated_at||'')}</td><td class="right nowrap"><button class="icon-btn" data-issueedit="${i.id}">✎</button> <button class="icon-btn" data-issuedel="${i.id}">×</button></td></tr>`).join(''):'<tr><td colspan="8"><div class="empty">No issues recorded. Add an issue for every unresolved rule ambiguity or documentation gap.</div></td></tr>'}
  </tbody></table></div></div>`;
}

/* ================= REPORT ================= */
function renderReport(){
  const scope=S.reportScope||'B.3';
  const checks=S.checks.filter(c=>scope==='all'||c.rule_id.startsWith('B.3.'));
  const vf=checks.filter(c=>c.status==='Verified').length, fl=checks.filter(c=>c.status==='Failed').length;
  const applicable=checks.filter(c=>c.status!=='Not Applicable').length;
  const p=applicable?Math.round(100*vf/applicable):0;
  const issues=(S.issues||[]).filter(i=>i.status!=='Closed');
  return `<div class="page-head no-print"><div><div class="eyebrow">Printable · traceable · FEROX-branded</div><h1>Compliance Report</h1>
  <p>Generated from recorded checks, not estimates. Every row traces to a rule number and a PDF page. Print or save as PDF from the browser.</p></div>
  <div class="spacer"></div>
  <select id="rpScope"><option value="B.3" ${scope==='B.3'?'selected':''}>Part B · Article 3 — Roll Cage</option><option value="all" ${scope==='all'?'selected':''}>All checks (currently B.3 only)</option></select>
  <button class="btn primary" id="rpPrint">Print / Save PDF</button></div>
  <div class="report-page">
    <div class="rp-head">
      <svg class="rp-mark" viewBox="0 0 64 64"><polygon points="32,2 58,17 58,47 32,62 6,47 6,17" fill="none" stroke="#ff5a1f" stroke-width="3"/><path d="M22 18h22v7H30v6h12v7H30v10h-8z" fill="#ff5a1f"/><path d="M40 33l8 8-8 8" fill="none" stroke="#ffb020" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/></svg>
      <div><h1>FEROX · BAJA ENGINEERING &amp; COMPLIANCE HUB</h1><div class="rp-sub">Roll Cage Compliance Report · ${esc(S.meta.vehicle||'FEROX 2027 ICE')}</div></div>
      <div class="rp-meta"><b>${esc(S.meta.team||'FEROX')}</b><br>${esc(S.meta.competition||'BAJA SAEINDIA Chennai 2027 — ICE')}<br>Rulebook: ${esc(S.meta.rulebook||'')}<br>Report date: ${esc(new Date().toISOString().slice(0,10))}</div>
    </div>
    <h2 class="rp-title">Roll Cage Compliance Status</h2>
    <p class="small muted" style="margin:4px 0 0">Part B, Article 3 (B.3.1 – B.3.7.3) · PDF pages 17–36 · ${checks.length} checks · generated from recorded verification data.</p>
    <div class="rp-section"><h2>1. Project &amp; competition details</h2>
      <table class="rp-table"><tbody>
        <tr><th style="width:22%">Team</th><td>${esc(S.meta.team||'FEROX')}</td><th style="width:22%">Vehicle</th><td>${esc(S.meta.vehicle||'FEROX 2027 ICE')}</td></tr>
        <tr><th>Competition</th><td>${esc(S.meta.competition||'')}</td><th>Event dates</th><td>${esc(S.meta.event_dates||'')}</td></tr>
        <tr><th>Car number</th><td>${esc(S.meta.car_number||'—')}</td><th>Roll cage lead</th><td>${esc(S.meta.lead||'—')}</td></tr>
        <tr><th>Venue</th><td colspan="3">${esc(S.meta.venue||'')}</td></tr>
      </tbody></table>
    </div>
    <div class="rp-section"><h2>2. Summary</h2>
      <div class="rp-kpis">
        <div class="rp-kpi"><b>${checks.length}</b><small>Total checks</small></div>
        <div class="rp-kpi"><b>${vf}</b><small>Verified</small></div>
        <div class="rp-kpi"><b>${fl}</b><small>Failed</small></div>
        <div class="rp-kpi"><b>${checks.filter(c=>c.status==='Pending Verification').length}</b><small>Pending</small></div>
        <div class="rp-kpi"><b>${checks.filter(c=>c.status==='Not Applicable').length}</b><small>N/A</small></div>
        <div class="rp-kpi"><b>${p}%</b><small>Verified / applicable</small></div>
      </div>
      <div class="rp-note"><b>Status basis:</b> “Verified” means FEROX has recorded a measurement or inspection result and supporting evidence against the exact rule criterion. It is team self-verification, not official acceptance. Technical Inspection and the BSC Technical Committee decide compliance at the event. ${esc(S.meta.note||'')}</div>
    </div>
    <div class="rp-section"><h2>3. Detailed verification register</h2>
      <table class="rp-table"><thead><tr><th style="width:6%">ID</th><th style="width:7%">Rule</th><th style="width:14%">Component</th><th style="width:22%">Acceptance criterion (source wording)</th><th style="width:9%">Measured</th><th style="width:8%">Result</th><th style="width:8%">Status</th><th style="width:12%">Evidence</th><th>Remarks</th></tr></thead><tbody>
      ${checks.map(c=>{
        const ev=(S.evByCheck[c.id]||[]).map(e=>e.filename).join('; ');
        const res=c.auto_result==='pass'?'Meets':c.auto_result==='fail'?'Does not meet':'—';
        return `<tr><td class="mono">${esc(c.id)}</td><td class="mono">${esc(c.rule_id)}</td><td>${esc(c.component)}</td><td>${esc(c.criterion)}</td><td>${c.measured!=null&&c.measured!==''?esc(c.measured)+' '+esc(c.unit):'—'}</td><td>${res}</td><td>${esc(c.status)}</td><td>${esc(ev||'—')}</td><td>${esc(c.remarks||'')}</td></tr>`;
      }).join('')}
      </tbody></table>
    </div>
    <div class="rp-section"><h2>4. Outstanding issues &amp; pending items</h2>
      ${issues.length?`<table class="rp-table"><thead><tr><th style="width:6%">ID</th><th style="width:26%">Issue</th><th>Detail</th><th style="width:10%">Severity</th><th style="width:10%">Status</th><th style="width:9%">Rule</th><th style="width:12%">Owner</th></tr></thead><tbody>${issues.map(i=>`<tr><td>#${i.id}</td><td>${esc(i.title)}</td><td>${esc(i.detail)}</td><td>${esc(i.severity)}</td><td>${esc(i.status)}</td><td>${esc(i.rule_id||'—')}</td><td>${esc(i.owner||'—')}</td></tr>`).join('')}</tbody></table>`:'<p class="small muted">No open issues recorded. This does not mean the vehicle is compliant — it means no issue has been raised yet.</p>'}
    </div>
    <div class="rp-section"><h2>5. Declaration</h2>
      <p class="small">This report records the FEROX team's internal verification state as of the report date. It is generated from the F-BECH database and is traceable to the BAJA SAEINDIA Chennai 2027 ICE Rulebook, Version 1.0, dated 01 September 2026. It does not constitute official technical inspection or acceptance.</p>
      <div class="rp-foot"><div class="sig">Team Captain / Roll Cage Lead — name &amp; signature</div><div class="sig">Faculty Advisor — name &amp; signature</div></div>
    </div>
  </div>`;
}

/* ================= COVERAGE ================= */
function renderCoverage(){
  const cov=S.stats.rule_coverage||[];
  const unres=[]; const seen=new Set();
  for(const r of S.rules) for(const x of (r.xrefs||[])) if(!x.resolved){ const k=r.id+'→'+x.ref; if(!seen.has(k)){seen.add(k); unres.push({from:r.id,ref:x.ref});} }
  return `<div class="page-head"><div><div class="eyebrow">Architecture · what is real</div><h1>Rulebook Coverage Matrix</h1>
  <p>Every article in the 100-page rulebook is inventoried and searchable. B.3 is fully interpreted and converted into checks; the remaining articles are extracted as source text with page references and cross-references, pending Phase 5.</p></div></div>
  <div class="notice"><span class="ni">⚠</span><div><b>Honest status:</b> only Part B, Article 3 has engineering checks. Other articles show <b>0 checks</b> deliberately — F-BECH does not fabricate compliance data. Their exact official text is available in the navigator.</div></div>
  <div class="card"><div class="card-h"><h3>Article coverage</h3><span class="sub">${cov.reduce((a,b)=>a+b.rules,0)} rules · ${cov.reduce((a,b)=>a+b.validated,0)} validated</span></div>
  <div style="overflow:auto"><table class="tbl"><thead><tr><th>Part</th><th>Article</th><th>Title</th><th class="center">Rules</th><th class="center">Validated</th><th class="center">Checks</th><th>Status</th></tr></thead><tbody>
  ${cov.map(c=>{const r0=S.rules.find(r=>r.article===c.article)||{};const ap=(S.stats.article_progress||[]).find(a=>a.article===c.article)||{};const st=c.validated===c.rules&&c.rules>0?'<span class="pill val">Validated</span>':c.validated>0?'<span class="pill md">Partial</span>':'<span class="pill src">Source text only</span>';return `<tr><td class="mono">${esc(c.article.split('.')[0])}</td><td class="mono"><a href="#/rule/${encodeURIComponent((S.rules.find(r=>r.article===c.article)||{}).id||'')}" style="color:#b3410f;font-weight:700">${esc(c.article)}</a></td><td>${esc(r0.article_title||'—')}</td><td class="center">${c.rules}</td><td class="center">${c.validated}</td><td class="center">${ap.total||0}</td><td>${st}</td></tr>`;}).join('')}
  </tbody></table></div></div>
  <div class="grid g2" style="margin-top:14px">
    <div class="card"><div class="card-h"><h3>Unresolved cross-references</h3><span class="sub">${unres.length} flagged</span></div>
      <div>${unres.length?`<table class="tbl"><thead><tr><th>From</th><th>Reference</th></tr></thead><tbody>${unres.map(u=>`<tr><td class="mono">${esc(u.from)}</td><td class="mono" style="color:#b91c1c">${esc(u.ref)} — not found</td></tr>`).join('')}</tbody></table>`:'<div class="empty">All numbered cross-references resolved to an extracted rule.</div>'}</div>
      <div class="card-b small muted">A reference can be unresolved because the target article is not yet extracted as a separate section, because the reference is to an article rather than a numbered clause (e.g. B.12), or because the source itself has a broken reference. Each is flagged rather than silently ignored.</div>
    </div>
    <div class="card"><div class="card-h"><h3>Source integrity flags</h3></div>
      <div class="card-b small">
        <p><b>TOC entry with no article:</b> Part B, Article 14 — Electric Powertrain is listed in the Table of Contents with “Error! Bookmark not defined.” and has no corresponding article in the 100-page document. It is not fabricated; it is flagged here.</p>
        <p><b>PDF text extraction:</b> line-break hyphenation artefacts were normalised (e.g. “front- half” → “front-half”, “Figure B- 12” → “Figure B-12”). No requirement was rewritten.</p>
        <p><b>B.3 validation:</b> every B.3 clause was compared against the rendered PDF pages 17–36. Ambiguous sentences are recorded on the rule's “Ambiguities” tab rather than corrected by assumption.</p>
        <p><b>Layer separation:</b> official wording, plain-English explanation and FEROX engineering interpretation are stored as separate fields and rendered on separate tabs.</p>
      </div>
    </div>
  </div>`;
}

/* ================= SETTINGS ================= */
function renderSettings(){
  const m=S.meta;
  return `<div class="page-head"><div><div class="eyebrow">Project identity · report header</div><h1>Project Settings</h1><p>These fields populate the dashboard, the printable report and the document index. They are stored in the F-BECH database.</p></div></div>
  <div class="card" style="max-width:900px"><div class="card-h"><h3>FEROX · BAJA SAEINDIA Chennai 2027 · ICE</h3></div>
  <div class="card-b"><div class="grid g2">
    <div class="field"><label>Team</label><input id="m_team" value="${escAttr(m.team||'')}"></div>
    <div class="field"><label>Vehicle</label><input id="m_vehicle" value="${escAttr(m.vehicle||'')}"></div>
    <div class="field"><label>Competition</label><input id="m_competition" value="${escAttr(m.competition||'')}"></div>
    <div class="field"><label>Car number</label><input id="m_car_number" value="${escAttr(m.car_number||'')}"></div>
    <div class="field"><label>Roll cage lead</label><input id="m_lead" value="${escAttr(m.lead||'')}"></div>
    <div class="field"><label>Event dates</label><input id="m_event_dates" value="${escAttr(m.event_dates||'')}"></div>
    <div class="field" style="grid-column:1/-1"><label>Venue</label><input id="m_venue" value="${escAttr(m.venue||'')}"></div>
    <div class="field" style="grid-column:1/-1"><label>Rulebook version</label><input id="m_rulebook" value="${escAttr(m.rulebook||'')}"></div>
    <div class="field" style="grid-column:1/-1"><label>Report disclaimer</label><textarea id="m_note">${esc(m.note||'')}</textarea></div>
  </div><div style="display:flex;gap:8px"><button class="btn primary" id="saveMeta">Save settings</button><span class="tiny muted" style="align-self:center">Changes are reflected on the next render and in the report header.</span></div></div></div>`;
}

/* ================= ABOUT ================= */
function renderAbout(){
  return `<div class="page-head"><div><div class="eyebrow">Source integrity · method · limits</div><h1>Source &amp; Method</h1>
  <p>How F-BECH reads the rulebook, what it stores, and what it deliberately refuses to invent.</p></div></div>
  <div class="grid g2">
    <div class="card"><div class="card-h"><h3>Controlling source</h3></div><div class="card-b small">
      <p><b>Document:</b> BAJA SAEINDIA Chennai 2027 ICE Rulebook, Version 1.0, dated 01 September 2026. 100 PDF pages.</p>
      <p><b>Processing:</b> the entire PDF was text-extracted page by page and every page was rendered to an image for visual verification. Every numbered heading was inventoried: <b>${S.rules.length}</b> rules across Parts A–D. B.3 (38 rules, pages 17–36) was then transcribed clause by clause against the page images.</p>
      <p><b>Official wording:</b> reproduced verbatim. Only PDF line-break hyphenation artefacts were normalised. Where the printed source is grammatically defective or internally inconsistent, the text is kept and the problem is recorded on the rule's “Ambiguities” tab.</p>
      <p><b>No invention:</b> no dimension, material, tolerance, exception or acceptance criterion has been added. A numeric auto-evaluation exists only where the rule states a threshold. Qualitative requirements stay manual.</p>
    </div></div>
    <div class="card"><div class="card-h"><h3>Three information layers</h3></div><div class="card-b small">
      <p><b>1 · Official requirement</b> — exact wording, rule number, article, PDF page, figures, tables and notes. This is the only layer that can be quoted as the rule.</p>
      <p><b>2 · Plain-English explanation</b> — a FEROX reading aid. It breaks the sentence into points but does not replace the official text.</p>
      <p><b>3 · Engineering interpretation</b> — how the rule affects design, CAD, fabrication and verification. Explicitly labelled as interpretation.</p>
      <p><b>4 · Verification checks</b> — measurable checks derived from the official criterion, with method, required evidence, measured value, automatic result where supported, status and remarks.</p>
    </div></div>
  </div>
  <div class="grid g2" style="margin-top:14px">
    <div class="card"><div class="card-h"><h3>What is implemented</h3></div><div class="card-b small">
      <ul style="margin:0;padding-left:18px;line-height:1.8">
        <li>Full 100-page rulebook inventory: ${S.rules.length} rules, all searchable, all with PDF page and cross-reference resolution.</li>
        <li>Part B Article 3 fully processed: 38 rules, plain-English and engineering layers, ${S.stats.total_checks||0} verification checks, numeric evaluation, evidence upload, persistent storage.</li>
        <li>${Object.keys(FIG_PAGES).length} rulebook figures cropped verbatim from the PDF (B-4 … B-63) and linked from the clauses that cite them.</li>
        <li>Rule navigator with nested, expandable cross-references and a return trail.</li>
        <li>Dashboard computed from recorded checks only; article and component progress; critical issues; evidence completion.</li>
        <li>Engineering documentation register, issue register, revision history, printable compliance report.</li>
        <li>SQLite persistence and file storage for evidence. Export to JSON.</li>
      </ul>
    </div></div>
    <div class="card"><div class="card-h"><h3>What is not implemented</h3></div><div class="card-b small">
      <ul style="margin:0;padding-left:18px;line-height:1.8">
        <li>Interpretation and checks for Parts A, C, D and Part B Articles 1–2, 4–13: source text and cross-references only. They show 0 checks by design.</li>
        <li>Part B Article 14 (Electric Powertrain): listed in the TOC but absent from the document body; flagged, not fabricated.</li>
        <li>Official BSC forms (Roll Cage Specification Sheet template, cost report forms) are external documents and are not reproduced here.</li>
        <li>No official technical inspection result is stored or implied. “Verified” is always team verification.</li>
      </ul>
    </div></div>
  </div>
  <div class="card" style="margin-top:14px"><div class="card-h"><h3>Recorded source ambiguities in B.3</h3></div>
    <div>${S.rules.filter(r=>r.id.startsWith('B.3')&&(r.notes||[]).length).map(r=>`<div class="doc-item"><div class="di-body"><h4><span class="mono" style="color:#b3410f">${esc(r.id)}</span> ${esc(r.title)}</h4>${r.notes.map(n=>`<p>${esc(n)}</p>`).join('')}</div></div>`).join('')||'<div class="empty">No ambiguities recorded.</div>'}</div>
  </div>`;
}

/* ================= MODALS & CRUD ================= */
function bindExtra(){
  if(S.route==='workspace') bindWorkspace();
  $$('[data-dashf]').forEach(el=>el.onchange=()=>{ S.dash[el.dataset.dashf]=el.value; router(); });
  const dr=$('[data-dashreset]'); if(dr) dr.onclick=()=>{ S.dash={article:'',component:'',status:'',priority:''}; router(); };
  $$('[data-doccat]').forEach(el=>el.onclick=()=>{ S.docCat=el.dataset.doccat; router(); });
  const ad=$('#addDoc'); if(ad) ad.onclick=()=>openDocModal();
  const ai=$('#addIssue'); if(ai) ai.onclick=()=>openIssueModal();
  const sm=$('#saveMeta'); if(sm) sm.onclick=saveMeta;
  const rs=$('#rpScope'); if(rs) rs.onchange=()=>{ S.reportScope=rs.value; router(); };
  const rp=$('#rpPrint'); if(rp) rp.onclick=()=>window.print();
  const ar=$('#addRev'); if(ar) ar.onclick=addRevision;
  const ts=$('#treeSearch'); if(ts) ts.oninput=debounce(()=>{ const q=ts.value.trim(); S.query.q=q; $('#tree').innerHTML=treeHTML(q); bindView(); },180);
}
function openDocModal(id){
  const d=id?S.docs.find(x=>x.id===id):null;
  const cats=['Design Assumptions','CAD Measurements','Material Selection','Procurement Records','Welding & Fabrication','Engineering Calculations','Inspection Records','Evidence & Photographs','Design Revision History'];
  openModal(`<div class="modal"><div class="modal-h"><h3>${d?'Edit':'Add'} documentation entry</h3><button class="x" data-close>×</button></div>
  <div class="modal-b">
    <div class="field"><label>Category</label><select id="d_cat">${cats.map(c=>`<option ${d&&d.category===c?'selected':''}>${esc(c)}</option>`).join('')}</select></div>
    <div class="field"><label>Title</label><input id="d_title" value="${escAttr(d?d.title:'')}" placeholder="e.g. RRH inclination assumption — 12° from vertical"></div>
    <div class="field"><label>Reference (drawing, calculation, rule)</label><input id="d_ref" value="${escAttr(d?d.ref:'')}" placeholder="e.g. CATIA rev C / B.3.2.6"></div>
    <div class="field"><label>Body</label><textarea id="d_body" style="min-height:150px" placeholder="Assumption, justification, measurement, decision, or observation.">${esc(d?d.body:'')}</textarea></div>
  </div>
  <div class="modal-f"><button class="btn" data-close>Cancel</button><button class="btn primary" id="d_save">${d?'Save changes':'Add entry'}</button></div></div>`);
  $('#d_save').onclick=async()=>{
    const payload={category:$('#d_cat').value,title:$('#d_title').value,body:$('#d_body').value,ref:$('#d_ref').value};
    try{
      if(d){ await apiJSON('/api/docs/'+d.id,'PUT',payload); Object.assign(d,payload); }
      else { const r=await apiJSON('/api/docs','POST',payload); S.docs.unshift(r.doc); }
      S.docCat=payload.category; closeModal(); router(); toast('Documentation entry saved','ok');
    }catch(e){ toast('Save failed: '+e.message,'err'); }
  };
}
async function deleteDoc(id){
  if(!confirm('Delete this documentation entry?')) return;
  await apiJSON('/api/docs/'+id,'DELETE',{}); S.docs=S.docs.filter(d=>d.id!==id); router(); toast('Entry deleted','ok');
}
function openIssueModal(id){
  const i=id?S.issues.find(x=>x.id===id):null;
  openModal(`<div class="modal"><div class="modal-h"><h3>${i?'Edit':'Add'} issue</h3><button class="x" data-close>×</button></div>
  <div class="modal-b">
    <div class="field"><label>Title</label><input id="i_title" value="${escAttr(i?i.title:'')}" placeholder="Short, specific description"></div>
    <div class="field"><label>Detail</label><textarea id="i_detail" style="min-height:100px" placeholder="What is unresolved, what decision is needed, and what evidence is missing.">${esc(i?i.detail:'')}</textarea></div>
    <div class="grid g2">
      <div class="field"><label>Severity</label><select id="i_sev">${['Critical','High','Medium','Low'].map(s=>`<option ${i&&i.severity===s?'selected':''}>${esc(s)}</option>`).join('')}</select></div>
      <div class="field"><label>Status</label><select id="i_status">${['Open','In Progress','Blocked','Closed'].map(s=>`<option ${i&&i.status===s?'selected':''}>${esc(s)}</option>`).join('')}</select></div>
      <div class="field"><label>Related rule</label><input id="i_rule" value="${escAttr(i?i.rule_id:'')}" placeholder="e.g. B.3.2.6"></div>
      <div class="field"><label>Owner</label><input id="i_owner" value="${escAttr(i?i.owner:'')}" placeholder="Name / subsystem lead"></div>
    </div>
  </div>
  <div class="modal-f"><button class="btn" data-close>Cancel</button><button class="btn primary" id="i_save">${i?'Save changes':'Add issue'}</button></div></div>`);
  $('#i_save').onclick=async()=>{
    const payload={title:$('#i_title').value,detail:$('#i_detail').value,severity:$('#i_sev').value,status:$('#i_status').value,rule_id:$('#i_rule').value,owner:$('#i_owner').value};
    try{
      if(i){ await apiJSON('/api/issues/'+i.id,'PUT',payload); Object.assign(i,payload); }
      else { const r=await apiJSON('/api/issues','POST',payload); S.issues.unshift(r.issue); }
      closeModal(); router(); toast('Issue saved','ok'); refreshStats();
    }catch(e){ toast('Save failed: '+e.message,'err'); }
  };
}
async function deleteIssue(id){
  if(!confirm('Delete this issue?')) return;
  await apiJSON('/api/issues/'+id,'DELETE',{}); S.issues=S.issues.filter(i=>i.id!==id); router(); toast('Issue deleted','ok'); refreshStats();
}
async function deleteEvidence(id){
  if(!confirm('Remove this evidence file?')) return;
  const e=S.evidence.find(x=>x.id===id);
  await apiJSON('/api/evidence/'+id,'DELETE',{});
  if(e){ S.evidence=S.evidence.filter(x=>x.id!==id); if(S.evByCheck[e.check_id]) S.evByCheck[e.check_id]=S.evByCheck[e.check_id].filter(x=>x.id!==id); const c=S.checks.find(c=>c.id===e.check_id); if(c) c._evidence=(S.evByCheck[e.check_id]||[]).length; }
  router(); toast('Evidence removed','ok');
}
async function deleteRevision(id){
  if(!confirm('Delete this revision entry?')) return;
  await apiJSON('/api/revisions/'+id,'DELETE',{}); S.revisions=S.revisions.filter(r=>r.id!==id); router(); toast('Revision deleted','ok');
}
async function addRevision(){
  const payload={rev:$('#revRev').value,date:$('#revDate').value,author:$('#revAuthor').value,description:$('#revDesc').value};
  if(!payload.rev||!payload.date){ toast('Revision and date are required','err'); return; }
  const r=await apiJSON('/api/revisions','POST',payload); S.revisions.unshift(r.revision); router(); toast('Revision added','ok');
}
async function saveMeta(){
  const keys=['team','vehicle','competition','car_number','lead','event_dates','venue','rulebook','note'];
  const payload={}; keys.forEach(k=>payload[k]=$('#m_'+k).value);
  await apiJSON('/api/meta','POST',payload); Object.assign(S.meta,payload); toast('Project settings saved','ok'); router();
}
