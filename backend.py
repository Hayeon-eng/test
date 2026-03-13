<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<title>RAG 토론 테스트</title>
<style>
body { font-family: Arial; margin: 20px; }
input, textarea { width: 300px; margin-bottom: 10px; }
button { margin-top: 10px; }
#discussion { border:1px solid #ccc; padding:10px; height:200px; overflow-y:scroll; }
.analysis { border:1px solid #aaa; margin-top:10px; padding:10px; }
</style>
</head>
<body>
<h2>페르소나 + URL 입력</h2>
<input id="persona" placeholder="Persona 설명">
<textarea id="urls" placeholder="URL 여러개 , 로 구분"></textarea><br>
<button onclick="register()">등록</button>

<h3>등록된 페르소나/URL</h3>
<select id="persona_list" size="5" style="width:400px;"></select>

<h3>분석 결과</h3>
<div id="analysis"></div>

<h3>자동 토론</h3>
<div id="discussion"></div>

<script>
async function register(){
    let persona = document.getElementById('persona').value;
    let urls = document.getElementById('urls').value;
    if(!persona || !urls) return alert("둘다 입력 필요");
    await fetch("/register", {
        method:"POST",
        body:new URLSearchParams({persona, urls})
    });
    document.getElementById('persona').value='';
    document.getElementById('urls').value='';
    loadPersonas();
}

async function loadPersonas(){
    let res = await fetch("/analyze");
    let data = await res.json();
    let sel = document.getElementById('persona_list');
    sel.innerHTML='';
    data.results.forEach(e=>{
        let opt = document.createElement('option');
        opt.text = `${e.persona} - ${e.urls.join(', ')}`;
        sel.add(opt);
    });
    displayAnalysis(data.results);
    displayDiscussion(data.discussion_log);
}

function displayAnalysis(results){
    let container = document.getElementById('analysis');
    container.innerHTML='';
    results.forEach(e=>{
        let div = document.createElement('div');
        div.className='analysis';
        div.innerHTML=`<strong>${e.persona}</strong><br>
        <em>Data 분석:</em> ${e.data_analysis}<br>
        <em>Content 분석:</em> ${e.content_analysis}`;
        container.appendChild(div);
    });
}

function displayDiscussion(log){
    let div = document.getElementById('discussion');
    div.innerHTML = log.map(l=>`<div>${l}</div>`).join('');
    div.scrollTop = div.scrollHeight;
}

// 5초마다 새로고침
setInterval(loadPersonas, 5000);
loadPersonas();
</script>
</body>
</html>
