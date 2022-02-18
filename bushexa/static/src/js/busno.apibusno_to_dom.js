// Build a new aside - section part
function buildAside(thead, list, aliasLink) {
    let aside = document.createElement("aside");
    aside.onclick = () => location.href = aliasLink;

    let section = document.createElement("section");
    aside.appendChild(section);

    let table = document.createElement("table");
    table.style.overflowX = "hidden";
    section.appendChild(table);

    table.appendChild(thead);

    for (let tr of list) {
        table.appendChild(tr);
    }

    return aside;
}


function buildTHead(alias, sideText) {
    let thead = document.createElement("thead");
    
    let tr = document.createElement("tr");
    thead.appendChild(tr);

    let th = document.createElement("th");
    th.style.paddingRight = 0;
    th.innerHTML = alias['name'];
    tr.appendChild(th);

    let td = document.createElement("td");
    td.innerHTML = sideText;
    tr.appendChild(td);

    return thead;
}


function buildPosTd(p) {
    let tr = document.createElement("tr");

    let td = document.createElement("td");
    td.innerHTML = `🚌 ${p["prev_stop"]}역 전 (${p["stop_name"]})`;
    tr.appendChild(td);

    return tr;
}


function buildDepTd(d, thealias) {
    let tr = document.createElement("tr");
    
    let td1 = document.createElement("td");
    let hour = d['depart_time'].slice(0,2);
    let minute = d['depart_time'].slice(2,4);
    td1.innerHTML = `🕒 ${hour}:${minute} 출발예정`;
    tr.appendChild(td1);

    let only_departure = false;
    let parts = thealias['part']
    for (let p in parts) {
        let first = parts[p]['first_order'];
        let last = parts[p]['last_order'];
        let lane_key = parts[p]['lane_key'];
        if (lane_key == d['lane_key'] && first == last) {
            only_departure = true;
        }
    }
    if (only_departure) {
        let td2 = document.createElement("td");
        td2.innerHTML = "기점";
        tr.appendChild(td2);
    }

    return tr;
}


function buildNoneTd() {
    let tr = document.createElement("tr");
    let td = document.createElement("td");
    td.innerHTML = "더 이상 버스가 없습니다.";
    tr.appendChild(td);
    return tr;
}


async function processApiBusno(urlToBusno, baseUrlToAlias) {
    const r = await fetch(urlToBusno);
    let data = await r.json();

    let alias = data.alias;
    let arr = data.arrival;
    let dep = data.departure;
    let pos = data.position;

    let sectionRoot = document.querySelector("#sectionRoot");
    while(sectionRoot.firstChild) {sectionRoot.firstChild.remove();}

    for (let a in alias) {
        let thealias = alias[a];
        let adep = dep[a];
        let apos = pos[a];
        
        let sideText = "...";
        let entries = []

        if (apos) {
            sideText = apos[0]['vehicle_no'].slice(2);
            apos.forEach((p) => {
                entries.push(buildPosTd(p));
            });
        }

        let only_departure = true;
        let parts = thealias['part']
        for (let p in parts) {
            let first = parts[p]['first_order'];
            let last = parts[p]['last_order'];
            let lane_key = parts[p]['lane_key'];
            only_departure = only_departure && (first == last);
        }
        if (only_departure) {sideText="기점";}
    


        if (adep) {
            adep.forEach((d) => {
                entries.push(buildDepTd(d, thealias));
            });
        }

        while (entries.length < 2) {
            entries.push(buildNoneTd());
        }
        let aliasLink = baseUrlToAlias + String(a);

        sectionRoot.appendChild(buildAside(buildTHead(thealias, sideText), entries.slice(0,2), aliasLink));
    }
}
