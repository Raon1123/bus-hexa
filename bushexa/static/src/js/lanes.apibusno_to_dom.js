// get data from api, make it visible
async function getApiLanes(urlToLanes, baseUrlToLane) {
    const r = await fetch(urlToLanes);
    let data = await r.json();

    for (let busnum in data) {
        let lanes = data[busnum];
        let aside = document.createElement("aside");
        for (let id in lanes) {
            let p = document.createElement("p");
            p.innerHTML = lanes[id];
            p.onclick = () => location.href = baseUrlToLane + id;
            aside.appendChild(p);
        }
        sectionRoot.appendChild(aside);
    }
}
