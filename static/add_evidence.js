function collapse(element, index) {
    var arrow = document.getElementById(element.id.split("_").slice(0,index).join("_") + "_icon");
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
        if (element.checked == true) {
            item.removeAttribute('disabled');
        } else if (item.id != element.id && item.id.includes("field") == false) {
            item.setAttribute('disabled','true');
        }
    });
    calculate_score(element);
}

function add_disease(dtype) {
    if (!dtype) {
        var dtype = $("input[type='radio'][name='dtype']:checked").val();
    }

    var container = document.getElementById("diseases")
    var index = (container.children.length + 1) / 2

    var cln = document.getElementById("add").cloneNode(true);
    cln.querySelectorAll("[id^='d0']").forEach(function(element, test) {
        element.id = element.id.replace(/^d\d/gi, 'd' + index)
    })
    cln.children[0].children[0].setAttribute("data-target", "#d" + index);
    cln.children[0].children[0].removeAttribute("hidden");
    cln.children[1].children[0].remove();
    container.appendChild(cln);

    // Copy the element and its child nodes
    if (dtype == "gp") {
        disease_id = "d0";
    } else {
        disease_id = "d1";
    }
    cln = document.getElementById(disease_id).cloneNode(true);
    cln.querySelectorAll("[id^='" + disease_id + "']").forEach(function(element) {
        if (element.tagName != 'SELECT' && element.type != 'checkbox' && !element.id.includes('score')&& !element.id.includes('type')) {
            element.value = '';
        }
        if (element.id.includes("disease")) {
            element.setAttribute("required","");
        }
        if (element.name) {
            element.name = element.name.replace(/^d\d/gi, 'd' + index);
        }
        element.id = element.id.replace(/^d\d/gi, 'd' + index)
    })
    cln.id = "d" + index
    cln.removeAttribute("hidden")

    container.appendChild(cln);
}

function add_evidence(element) {
    var sub_id = element.id.slice(0, -3)
    var id = sub_id + "field"
    var container = document.getElementById(id + "s")

    // Copy the element and its child nodes
    var cln = document.getElementById(id).cloneNode(true);
    cln.children[0].children[0].remove();
    cln.children[0].children[0].setAttribute('class', 'col-1 offset-md-1');
    cln.children[0].children[2].remove();

    var index = container.children.length + 1
    cln.querySelectorAll("[id^='" + sub_id + "']").forEach(function(element, test) {
        if (element.tagName != 'SELECT') {
            element.value = '';
        }
        element.id = element.id.slice(0,-1) + index;
    })
    container.appendChild(cln);
}

function calculate_score(element) {
    var disease_num = element.id.slice(0, 2)
    var checkboxes = document.getElementsByName(disease_num);

    var path = l_path = false;
    var benign = l_benign = false;
    var dict = {};
    for (var i=0; i<checkboxes.length; i++) {
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
            } else if (dict["PM"] == 2) {
                if (dict["PP"] >= 2) {
                    path = true;
                } else {
                    l_path = true
                }
            } else if (dict["PM"] == 1) {
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
        } else if (dict["PM"] == 2) {
            if (dict["PP"] >= 2) {
                l_path = true;
            }
        } else if (dict["PM"] == 1) {
            if (dict["PP"] >= 4) {
                l_path = true;
            }
        }
    }

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

    if (benign) {
        againstScore = "Benign"
    } else if (l_benign) {
        againstScore = "Likely Benign"
    } else {
        againstScore = "Uncertain"
    }
    document.getElementById(disease_num + "_against_score").setAttribute("value", againstScore);
}