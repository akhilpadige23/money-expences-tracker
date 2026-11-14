import json
import os
from flask import Flask, request, jsonify

app = Flask(__name__)

# data is saved next to app.py, so it is still there after you restart
FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data.json")
CATEGORIES = ["Travel", "Household", "Food", "Entertainment"]


def load():
    if os.path.exists(FILE):
        with open(FILE) as f:
            return json.load(f)
    return {"balance": 0, "expenses": {c: [] for c in CATEGORIES}}


def save():
    with open(FILE, "w") as f:
        json.dump(data, f, indent=2)


data = load()


@app.route("/")
def home():
    return HTML


@app.route("/api/state")
def state():
    return jsonify(data)


@app.route("/api/balance", methods=["POST"])
def set_balance():
    data["balance"] = max(0, float(request.json["balance"]))
    save()
    return jsonify(data)


@app.route("/api/add", methods=["POST"])
def add():
    category = request.json["category"]
    price = float(request.json["price"])
    if category in data["expenses"] and price > 0:
        data["expenses"][category].append(
            {"name": request.json["item"], "price": price}
        )
        save()
    return jsonify(data)


@app.route("/api/delete", methods=["POST"])
def delete():
    category = request.json["category"]
    index = int(request.json["index"])
    if category in data["expenses"] and 0 <= index < len(data["expenses"][category]):
        data["expenses"][category].pop(index)
        save()
    return jsonify(data)


HTML = r"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Money Tracker</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700&family=Rajdhani:wght@500;600&display=swap" rel="stylesheet">
<style>
:root{--bg:#060918;--panel:rgba(18,24,62,.6);--line:rgba(120,160,255,.22);--cyan:#3df5ff;--pink:#ff3d9a;--text:#e6ecff;--dim:#8b97c9}
*{box-sizing:border-box;margin:0}
body{min-height:100vh;color:var(--text);font:600 18px/1.4 'Rajdhani',system-ui,sans-serif;
 background:radial-gradient(900px 500px at 10% -10%,rgba(40,70,200,.35),transparent),radial-gradient(800px 500px at 100% 0%,rgba(190,30,140,.3),transparent),var(--bg)}
body::before{content:"";position:fixed;inset:0;pointer-events:none;opacity:.22;
 background-image:linear-gradient(var(--line) 1px,transparent 1px),linear-gradient(90deg,var(--line) 1px,transparent 1px);
 background-size:48px 48px;-webkit-mask-image:radial-gradient(circle at 50% 25%,#000,transparent 70%);mask-image:radial-gradient(circle at 50% 25%,#000,transparent 70%)}
.wrap{position:relative;max-width:1080px;margin:0 auto;padding:26px 18px 60px}
h1,h2,.num{font-family:'Orbitron',system-ui,sans-serif}
h1{font-size:1.45rem;letter-spacing:.06em}
h1 span{color:var(--cyan);text-shadow:0 0 14px rgba(61,245,255,.6)}
h2{font-size:1rem;font-weight:500;color:var(--dim);margin-bottom:14px}
.panel{position:relative;background:var(--panel);border:1px solid var(--line);border-radius:18px;padding:22px;backdrop-filter:blur(10px);box-shadow:0 0 40px rgba(61,245,255,.05)}
.panel::before{content:"";position:absolute;left:22px;right:22px;top:-1px;height:2px;background:linear-gradient(90deg,var(--cyan),var(--pink));opacity:.7;border-radius:2px}
.hero{display:grid;grid-template-columns:300px 1fr;gap:26px;align-items:center;margin:22px 0}
.gauge{position:relative;width:260px;height:260px;margin:auto}
.gauge svg{transform:rotate(-90deg);width:100%;height:100%}
.gauge circle{fill:none;stroke-width:14;stroke-linecap:round}
#ring{transition:stroke-dashoffset .9s cubic-bezier(.2,.8,.2,1);filter:drop-shadow(0 0 8px rgba(61,245,255,.7))}
.gauge .mid{position:absolute;inset:0;display:grid;place-content:center;text-align:center}
.gauge .num{font-size:1.7rem;font-weight:700}
.gauge small{color:var(--dim);font-size:.95rem}
.stats{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-top:14px}
.stat{border:1px solid var(--line);border-radius:12px;padding:12px 14px}
.stat small{color:var(--dim)}
.stat .num{font-size:1.15rem;margin-top:2px}
.row{display:flex;gap:10px;flex-wrap:wrap}
input,button{font:inherit;color:var(--text)}
input{flex:1;min-width:120px;background:rgba(5,8,28,.7);border:1px solid var(--line);border-radius:10px;padding:10px 12px}
input:focus-visible,button:focus-visible{outline:2px solid var(--cyan);outline-offset:2px}
.btn{background:linear-gradient(90deg,var(--cyan),#7a5cff);color:#04061a;font-weight:600;border:0;border-radius:10px;padding:10px 18px;cursor:pointer;transition:transform .15s,box-shadow .15s}
.btn:hover{box-shadow:0 0 18px rgba(61,245,255,.55);transform:translateY(-1px)}
.main{display:grid;grid-template-columns:340px 1fr;gap:22px}
.chips{display:flex;flex-wrap:wrap;gap:8px;margin-bottom:14px}
.chip{background:transparent;border:1px solid var(--line);border-radius:999px;padding:6px 14px;cursor:pointer}
.chip.on{border-color:var(--cyan);color:var(--cyan);box-shadow:0 0 12px rgba(61,245,255,.35) inset}
.form{display:grid;gap:10px}
.cards{display:grid;grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:14px;align-content:start}
.card{border:1px solid var(--line);border-radius:14px;padding:16px;cursor:pointer;background:rgba(10,14,44,.5);transition:border-color .2s,box-shadow .2s}
.card:hover,.card.open{border-color:var(--cyan);box-shadow:0 0 20px rgba(61,245,255,.18)}
.card .top{display:flex;justify-content:space-between;align-items:center}
.card .ico{font-size:1.5rem}
.card .num{font-size:1.2rem;margin:6px 0}
.bar{height:6px;border-radius:6px;background:rgba(255,255,255,.08);overflow:hidden}
.bar i{display:block;height:100%;width:0;background:linear-gradient(90deg,var(--cyan),var(--pink));transition:width .7s}
.items{list-style:none;padding:0;margin-top:12px;display:grid;gap:6px}
.items li{display:flex;justify-content:space-between;gap:8px;font-size:.95rem;border-top:1px dashed var(--line);padding-top:6px}
.items button{background:none;border:0;color:var(--pink);cursor:pointer;font-size:1rem}
.empty{color:var(--dim);font-size:.95rem;margin-top:8px}
#toast{position:fixed;left:50%;bottom:24px;transform:translate(-50%,30px);opacity:0;background:#0d1440;border:1px solid var(--cyan);padding:10px 18px;border-radius:12px;transition:.3s;pointer-events:none}
#toast.show{opacity:1;transform:translate(-50%,0)}
.alert{margin-top:18px;padding:14px 18px;border-radius:14px;border:1px solid;font-weight:600}
.alert[hidden]{display:none}
.alert.warn{color:#ffd36b;border-color:#ffd36b;background:rgba(255,200,60,.1)}
.alert.danger{color:#ff7ab8;border-color:var(--pink);background:rgba(255,61,154,.14);box-shadow:0 0 24px rgba(255,61,154,.35)}
.gauge.hot svg{animation:pulse 1.4s ease-in-out infinite}
@keyframes pulse{50%{filter:drop-shadow(0 0 16px #ff3d9a)}}
@media (max-width:860px){.hero,.main{grid-template-columns:1fr}}
@media (prefers-reduced-motion:reduce){*{transition:none!important}}
</style>
</head>
<body>
<div class="wrap">
  <h1>MONEY<span>TRACKER</span></h1>
  <div id="alert" class="alert" role="alert" hidden></div>

  <section class="panel hero">
    <div class="gauge">
      <svg viewBox="0 0 200 200">
        <defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#3df5ff"/><stop offset="1" stop-color="#ff3d9a"/></linearGradient></defs>
        <circle cx="100" cy="100" r="90" stroke="rgba(255,255,255,.08)"/>
        <circle id="ring" cx="100" cy="100" r="90" stroke="url(#g)" stroke-dasharray="565.5" stroke-dashoffset="565.5"/>
      </svg>
      <div class="mid"><small>Money left</small><div class="num" id="left">0</div><small id="pct"></small></div>
    </div>
    <div>
      <h2>How much money do you have?</h2>
      <form class="row" id="balForm">
        <input id="bal" type="number" min="0" step="0.01" placeholder="Enter your starting balance" aria-label="Starting balance">
        <button class="btn">Set balance</button>
      </form>
      <div class="stats">
        <div class="stat"><small>Starting balance</small><div class="num" id="start">0</div></div>
        <div class="stat"><small>Total spent</small><div class="num" id="spent">0</div></div>
      </div>
    </div>
  </section>

  <div class="main">
    <section class="panel">
      <h2>Add an expense</h2>
      <div class="chips" id="chips"></div>
      <form class="form" id="addForm">
        <input id="item" placeholder="What did you buy? (e.g. fruits)" aria-label="Item name">
        <input id="price" type="number" min="0" step="0.01" placeholder="Price" aria-label="Price">
        <button class="btn">Add expense</button>
      </form>
    </section>
    <section class="cards" id="cards"></section>
  </div>
</div>
<div id="toast" role="status"></div>

<script>
const CUR = "₹";   // change this to "$" or "€" if you like
const ICON = {Travel:"🚀", Household:"🏠", Food:"🍔", Entertainment:"🎮"};
let S = {balance:0, expenses:{}}, pick = "Food", openCat = null, lastLevel = 0;
const $ = s => document.querySelector(s);
const esc = t => t.replace(/[&<>"']/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
const money = n => CUR + Number(n).toLocaleString("en-IN", {maximumFractionDigits:2});
const calm = matchMedia("(prefers-reduced-motion: reduce)").matches;
const shown = new WeakMap();

async function api(url, body){
  const r = await fetch(url, body ? {method:"POST", headers:{"Content-Type":"application/json"}, body:JSON.stringify(body)} : {});
  return r.json();
}
function toast(msg, ms = 2200){
  const t = $("#toast"); t.textContent = msg; t.classList.add("show");
  clearTimeout(t.id2); t.id2 = setTimeout(() => t.classList.remove("show"), ms);
}
function tween(el, to){
  const from = shown.get(el) || 0; shown.set(el, to);
  if (calm){ el.textContent = money(to); return; }
  const t0 = performance.now();
  (function step(t){
    const p = Math.min(1, (t - t0) / 600);
    el.textContent = money(from + (to - from) * (1 - Math.pow(1 - p, 3)));
    if (p < 1) requestAnimationFrame(step);
  })(t0);
}

function render(){
  const cats = Object.keys(S.expenses);
  const totals = cats.map(c => S.expenses[c].reduce((a, i) => a + i.price, 0));
  const spent = totals.reduce((a, b) => a + b, 0);
  const left = S.balance - spent;
  const pct = S.balance > 0 ? Math.max(0, Math.min(1, left / S.balance)) : 0;

  const ring = $("#ring");
  ring.style.strokeDashoffset = 565.5 * (1 - pct);
  ring.setAttribute("stroke", S.balance > 0 && pct < .2 ? "#ff3d9a" : "url(#g)");
  tween($("#left"), left); tween($("#spent"), spent); tween($("#start"), S.balance);
  $("#pct").textContent = S.balance > 0 ? Math.round(pct * 100) + "% remaining" : "Set a balance to begin";

  // alert: level 1 = 80% spent (warning), level 2 = balance reached or passed (danger)
  const level = S.balance > 0 && spent >= S.balance ? 2 : (S.balance > 0 && spent >= S.balance * .8 ? 1 : 0);
  const box = $("#alert");
  box.hidden = level === 0;
  box.className = "alert " + (level === 2 ? "danger" : "warn");
  box.textContent = level === 2
    ? (spent > S.balance ? "Over budget: you have spent " + money(spent - S.balance) + " more than you have."
                         : "Balance used up: your expenses have reached your balance.")
    : level === 1 ? "Careful: you have used " + Math.round(spent / S.balance * 100) + "% of your money. Only " + money(left) + " is left." : "";
  $(".gauge").classList.toggle("hot", level === 2);
  if (level > lastLevel) toast(level === 2 ? "Alert: your expenses have reached your balance!" : "Warning: 80% of your money is spent.", 4500);
  lastLevel = level;

  $("#chips").innerHTML = cats.map(c =>
    `<button type="button" class="chip ${c === pick ? "on" : ""}" onclick="pick='${c}';render()">${ICON[c] || ""} ${c}</button>`).join("");

  $("#cards").innerHTML = cats.map((c, k) => {
    const list = S.expenses[c], share = spent ? totals[k] / spent * 100 : 0, isOpen = openCat === c;
    const rows = list.length
      ? `<ul class="items">${list.map((it, i) => `<li><span>${esc(it.name)}</span><span>${money(it.price)} <button title="Delete" onclick="event.stopPropagation();del('${c}',${i})">✕</button></span></li>`).join("")}</ul>`
      : `<p class="empty">Nothing here yet. Add your first ${c.toLowerCase()} expense.</p>`;
    return `<div class="card ${isOpen ? "open" : ""}" onclick="openCat=openCat==='${c}'?null:'${c}';pick='${c}';render()">
      <div class="top"><b>${c}</b><span class="ico">${ICON[c] || ""}</span></div>
      <div class="num">${money(totals[k])}</div>
      <div class="bar"><i style="width:${share}%"></i></div>
      <small style="color:var(--dim)">${list.length} item${list.length === 1 ? "" : "s"}</small>
      ${isOpen ? rows : ""}</div>`;
  }).join("");
}

async function del(cat, index){
  S = await api("/api/delete", {category:cat, index}); render(); toast("Deleted");
}

$("#balForm").onsubmit = async e => {
  e.preventDefault();
  const v = parseFloat($("#bal").value);
  if (!(v >= 0)) return toast("Enter a balance of 0 or more.");
  S = await api("/api/balance", {balance:v}); $("#bal").value = ""; render(); toast("Balance set");
};

$("#addForm").onsubmit = async e => {
  e.preventDefault();
  const item = $("#item").value.trim(), price = parseFloat($("#price").value);
  if (!item || !(price > 0)) return toast("Enter an item name and a price above 0.");
  S = await api("/api/add", {category:pick, item, price});
  $("#item").value = ""; $("#price").value = ""; $("#item").focus();
  openCat = pick; toast("Added " + item + " to " + pick); render();
};

api("/api/state").then(d => { S = d; render(); });
</script>
</body>
</html>
"""

if __name__ == "__main__":
    app.run(debug=True)
