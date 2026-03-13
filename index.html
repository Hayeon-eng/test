<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<title>AI 토론 플랫폼</title>
<style>
body { font-family: Arial; padding: 20px; }
h2 { margin-top: 20px; }
textarea, input { width: 400px; margin: 5px 0; }
button { margin: 5px; }
#discussion { border: 1px solid #ccc; padding: 10px; max-height: 300px; overflow-y: auto; }
</style>
</head>
<body>
<h1>AI 자동 토론 & 분석</h1>

<h2>페르소나 등록</h2>
<input id="persona_name" placeholder="이름"/>
<input id="persona_desc" placeholder="설명"/>
<button onclick="addPersona()">등록</button>
<div id="persona_list"></div>

<h2>URL 등록</h2>
<input id="url_input" placeholder="https://"/>
<button onclick="addURL()">등록</button>
<div id="url_list"></div>

<h2>분석 & 토론</h2>
<button onclick="analyze()">분석 시작</button>
<div id="data_summary"></div>
<div id="content_summary"></div>
<h3>토론</h3>
<div id="discussion"></div>

<script>
async function addPersona(){
    const name = document.getElementById("persona_name").value;
    const desc = document.getElementById("persona_desc").value;
    const res = await fetch("/add_persona", {
        method: "POST",
        body: new URLSearchParams({name, description: desc})
    }).then(r=>r.json());
    renderPersonas(res.personas);
}
function renderPersonas(personas){
    document.getElementById("persona_list").innerHTML = personas.map(p=>p.name + " - " + p.description).join("<br>");
}

async function addURL(){
    const url = document.getElementById("url_input").value;
    const res = await fetch("/add_url", {
        method: "POST",
        body: new URLSearchParams({url})
    }).then(r=>r.json());
    renderURLs(res.urls);
}
function renderURLs(urls){
    document.getElementById("url_list").innerHTML = urls.join("<br>");
}

async function analyze(){
    const persona_name = document.getElementById("persona_name").value;
    const res = await fetch("/analyze", {
        method: "POST",
        body: new URLSearchParams({persona_name})
    }).then(r=>r.json());
    document.getElementById("data_summary").innerText = res.data_summary;
    document.getElementById("content_summary").innerText = res.content_summary;
    document.getElementById("discussion").innerHTML = res.discussion.join("<br>");
}
</script>
</body>
</html>
