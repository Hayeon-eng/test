const regForm = document.getElementById("regForm");
const personaList = document.getElementById("personaList");
const urlList = document.getElementById("urlList");
const discussionList = document.getElementById("discussionList");
const dataAnalysisDiv = document.getElementById("dataAnalysis");
const contentAnalysisDiv = document.getElementById("contentAnalysis");

regForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const formData = new FormData(regForm);
    const res = await fetch("/register", { method: "POST", body: formData });
    const data = await res.json();
    updateLists(data);
    regForm.reset();
    updateAnalysis();
});

function updateLists(data) {
    personaList.innerHTML = "";
    urlList.innerHTML = "";
    data.personas.forEach(p => {
        const li = document.createElement("li");
        li.textContent = `${p.name} (${p.desc})`;
        personaList.appendChild(li);
    });
    data.urls.forEach(u => {
        const li = document.createElement("li");
        li.textContent = u;
        urlList.appendChild(li);
    });
}

async function updateDiscussion() {
    const res = await fetch("/discussions");
    const data = await res.json();
    discussionList.innerHTML = "";
    data.discussions.forEach(d => {
        const li = document.createElement("li");
        li.textContent = d;
        discussionList.appendChild(li);
    });
}

async function updateAnalysis() {
    const res = await fetch("/analysis");
    const data = await res.json();
    dataAnalysisDiv.textContent = data.data_analysis;
    contentAnalysisDiv.textContent = data.content_analysis;
}

// 20~60초 주기로 자동 업데이트
setInterval(() => {
    updateDiscussion();
    updateAnalysis();
}, 30000);  // 30초
