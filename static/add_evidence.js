function collapse(element, index) {
    let arrow = document.getElementById(element.id.split("_").slice(0,index).join("_") + "_icon");
    if (arrow.className.includes("down")) {
        arrow.className = arrow.className.replace("down", "up");
        if (element.innerText.includes("Expand")) {
            element.innerHTML = element.innerHTML.replace('Expand', 'Collapse');
        }
    } else {
        arrow.className = arrow.className.replace("up", "down");
        if (element.innerText.includes("Collapse")) {
            element.innerHTML = element.innerHTML.replace('Collapse', 'Expand');
        }
    }
}

function select_evidence(element) {
    document.querySelectorAll("[id^='" + element.id + "']").forEach(function(item, index) {
        if (index > 7) {
            calculate_score(element);
            return;
        }
        if (element.checked === true) {
            item.removeAttribute('disabled');
        } else if (item.id !== element.id && item.id.includes("field") === false) {
            item.setAttribute('disabled','true');
        }
    });
    calculate_score(element);
}

function add_disease(dtype) {
    console.log(dtype == null)
    if (dtype == null) {
        dtype = $("input[type='radio'][name='dtype']:checked").val();
    }

    const container = document.getElementById("diseases")
    const index = (container.children.length + 1) / 2

    let cln = document.getElementById("add").cloneNode(true);
    cln.querySelectorAll("[id^='d0']").forEach(function(element) {
        element.id = element.id.replace(/^d\d/gi, 'd' + index)
    })
    cln.children[0].children[0].setAttribute("data-target", "#d" + index);
    cln.children[0].children[0].removeAttribute("hidden");
    cln.children[1].children[0].remove();
    container.appendChild(cln);

    // Copy the element and its child nodes
    let disease_id;
    if (dtype === "gp") {
        disease_id = "d0";
    } else {
        disease_id = "d1";
    }
    cln = document.getElementById(disease_id).cloneNode(true);
    cln.querySelectorAll("[id^='" + disease_id + "']").forEach(function(element) {
        if (element.tagName !== 'SELECT' && element.type !== 'checkbox' && !element.id.includes('score') && !element.id.includes('type') && !element.id.includes('r_name') && !element.id.includes('disease') && !element.id.includes('branch')) {
            element.value = '';
        }
        if (element.id.includes("disease")) {
            element.setAttribute("required","");
        }
        if (element.name) {
            element.name = element.name.replace(/^d\d/gi, 'd' + index);
        }
        if (element.hasAttribute("data-target")) {
            element.setAttribute("data-target", element.getAttribute("data-target").replace(/d\d/gi, 'd' + index));
        }
        element.id = element.id.replace(/^d\d/gi, 'd' + index)
    })
    cln.id = "d" + index
    cln.removeAttribute("hidden")

    container.appendChild(cln);
    return cln;
}

function add_evidence(element) {
    const sub_id = element.id.slice(0, -3)
    const id = sub_id + "field"
    const container = document.getElementById(id + "s")

    // Copy the element and its child nodes
    const cln = document.getElementById(id).cloneNode(true);
    cln.children[0].children[0].remove();
    cln.children[0].children[0].setAttribute('class', 'col-1 offset-md-1');
    cln.children[0].children[2].remove();

    const index = container.children.length + 1
    cln.querySelectorAll("[id^='" + sub_id + "']").forEach(function(element) {
        if (element.tagName !== 'SELECT') {
            element.value = '';
        }
        element.id = element.id.slice(0,-1) + index;
    })
    container.appendChild(cln);
}

function add_f_class(element) {
    const disease_num = element.id.split("_")[0];
    // Get the container
    const container = document.getElementById(disease_num + "_f_classes");
    const fc_num = container.children.length/2

    // Copy the element and its child nodes
    let cln = document.getElementById(disease_num + "_fc0_collapse").cloneNode(true);
    cln.querySelectorAll("[id^='" + disease_num + "_fc']").forEach(function(element) {
        element.id = element.id.replace(/fc\d/gi, 'fc' + fc_num)
        if (element.name)
            element.name = element.name.replace(/fc\d/gi, 'fc' + fc_num)
    })
    cln.id = disease_num + "_fc" + fc_num + "_collapse";
    cln.setAttribute("data-target", "#" + disease_num + "_fc" + fc_num)
    cln.removeAttribute('hidden')
    container.appendChild(cln);

    cln = document.getElementById(disease_num + "_fc0").cloneNode(true);
    cln.querySelectorAll("[id^='" + disease_num + "_fc']").forEach(function(element) {
        element.id = element.id.replace(/fc\d/gi, 'fc' + fc_num)
        element.name = element.name.replace(/fc\d/gi, 'fc' + fc_num)
        if (element.id.includes("add") && fc_num > 1) {
            element.setAttribute("hidden", "")
        }
    })
    cln.id = disease_num + "_fc" + fc_num;
    cln.removeAttribute('hidden')

    // Append the cloned <li> element to <ul> with id="myList1"
    container.appendChild(cln);
    return cln;
}


function add_evidence_type1(element) {
    //get functional class number
    const fc_num = element.id.split("_").slice(0, 2).join("_");

    // Get the container
    const container = document.getElementById(fc_num + "_evidences1");

    // Copy the element and its child nodes
    const cln = document.getElementById(fc_num + "_etype1_1").cloneNode(true);
    cln.querySelectorAll("[id^='" + fc_num + "_etype1_']").forEach(function(element) {
        if (element.tagName !== 'SELECT') {
            element.value = '';
        }
        element.id = element.id.slice(0,-1) + (container.children.length+1);
    })
    cln.id = fc_num + "_etype1_" + (container.children.length+1);

    // Append the cloned element to container
    container.appendChild(cln);
}

function add_evidence_type2(element) {
    const disease_num = element.id.split("_")[0];
    // Get the container
    const container = document.getElementById(disease_num + "_evidences2");

    // Copy the element and its child nodes
    const cln = document.getElementById(disease_num + "_etype2_1").cloneNode(true);
    cln.querySelectorAll("[id^='" + disease_num + "_etype2_']").forEach(function(element) {
        if (element.tagName !== 'SELECT') {
            element.value = '';
        }
        element.id = element.id.slice(0,-1) + (container.children.length+1);
    })
    cln.id = disease_num + "_etype2_" + (container.children.length+1);

    // Append the cloned element to container
    container.appendChild(cln);
}

function getElementsByValue(value, tag, id) {
    const search = document.getElementsByTagName(tag);
    const pat = new RegExp(value, "i");
    for (let i=0; i < search.length; i++) {
        if (pat.test(search[i].value)  && search[i].id.includes(id))
            return [document.getElementById(search[i].id.slice(0,-5)), document.getElementById(search[i].id.slice(0,-5) + '_id')]
    }
}

function calculate_score(element) {
    const disease_num = element.id.slice(0, 2)
    const checkboxes = document.getElementsByName(disease_num);

    let l_path, path, l_benign, benign = false;
    const dict = {};
    let check_id;
    for (let i = 0; i < checkboxes.length; i++) {
        if (checkboxes[i].checked) {
            check_id = checkboxes[i].id.split('_')[1].replace(/\d/g, '');
            if (dict[check_id]) {
                dict[check_id]++;
            } else {
                dict[check_id] = 1;
            }
        }
    }

    if (dict["PVS"]) {
        if (dict["PS"]) {
            path = true;
        } else if (dict["PM"]) {
            if (dict["PM"] >= 2) {
                path = true;
            } else if (dict["PP"]) {
                path = true;
            } else {
                l_path = true
            }
        } else if (dict["PP"]) {
            if (dict["PP"] >= 2) {
                path = true;
            }
        }
    } else if (dict["PS"]) {
        if (dict["PS"] >= 2) {
            path = true;
        } else if (dict["PM"]) {
            if (dict["PM"] >= 3) {
                path = true;
            } else if (dict["PM"] === 2) {
                if (dict["PP"] >= 2) {
                    path = true;
                } else {
                    l_path = true
                }
            } else if (dict["PM"] === 1) {
                if (dict["PP"] >= 4) {
                    path = true;
                } else {
                    l_path = true;
                }
            }
        } else {
            if (dict["PP"] >= 2) {
                l_path = true;
            }
        }
    } else if (dict["PM"]) {
        if (dict["PM"] >= 3) {
            l_path = true;
        } else if (dict["PM"] === 2) {
            if (dict["PP"] >= 2) {
                l_path = true;
            }
        } else if (dict["PM"] === 1) {
            if (dict["PP"] >= 4) {
                l_path = true;
            }
        }
    }

    let forScore;
    if (path) {
        forScore = "Pathogenic"
    } else if (l_path) {
        forScore = "Likely Pathogenic"
    } else {
        forScore = "Uncertain"
    }
    document.getElementById(disease_num + "_for_score").setAttribute("value", forScore);

    if (dict["BA"]) {
        benign = true;
    } else if (dict["BS"]) {
        if (dict["BS"] >= 2) {
            benign = true;
        } else if (dict["BP"]) {
            l_benign = true;
        }
    } else if (dict["BP"]) {
        if (dict["BP"] >= 2) {
            l_benign = true;
        }
    }

    let againstScore;
    if (benign) {
        againstScore = "Benign"
    } else if (l_benign) {
        againstScore = "Likely Benign"
    } else {
        againstScore = "Uncertain"
    }
    document.getElementById(disease_num + "_against_score").setAttribute("value", againstScore);
}
