// get data from api, make it visible
async function getApiLane(urlToLane) {
    const r = await fetch(urlToLane);
    let data = await r.json();

    lane_name_p.innerHTML = "노선명 : " + data["lanename"];
    
    landmark_nodes_p.innerHTML = "주요역 : " + data["landmarknodes"].join(', ');

    for (let tt in data["timetables"]) {
        let td = document.createElement("td");
        td.style.display = "none";
        td.classList.add("tt");
        td.innerHTML = data["timetables"][tt];
        timetables_tr.appendChild(td);
    }
}
