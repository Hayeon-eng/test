async function submitAnalysis() {
    const url = document.getElementById("url").value;
    const persona = document.getElementById("persona").value;
    const comment = document.getElementById("comment").value;

    if(!url || !persona) { alert("URL과 페르소나를 입력해주세요."); return; }

    const response = await fetch("/analyze", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ url, persona, comment })
    });
    const data = await response.json();
    document.getElementById("analysis").innerText = data.analysis;
    loadComments();
}

async function loadComments() {
    const response = await fetch("/comments");
    const comments = await response.json();
    const container = document.getElementById("comments");
    container.innerHTML = "";
    comments.forEach(c => {
        const div = document.createElement("div");
        div.className = "comment";
        div.innerHTML = `<b>${c.persona}</b> @ ${c.timestamp}<br>URL: ${c.url}<br>코멘트: ${c.comment}<div class="analysis">${c.analysis}</div>`;
        container.appendChild(div);
    });
}

function downloadRaw() {
    window.location.href = "/download_raw";
}

// 초기 로딩
loadComments();
