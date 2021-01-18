function collapse(element) {
    if (element.innerText.includes("Expand")) {
        element.innerHTML = element.innerHTML.replace('Expand', 'Collapse');
    } else {
        element.innerHTML = element.innerHTML.replace('Collapse', 'Expand');
    }
}

function update_header(element) {
    const dx_id = element.id.split('_')[0],
          dx_label = document.getElementById(dx_id + '_label');
    let dx_review = document.querySelector('input[name="' + dx_id + '_review"][type="checkbox"]');
    let replace_text = dx_label.innerText.split(/[/-]+/)[1]
    dx_label.innerText = dx_label.innerText.replace(replace_text, ' ' + element.value + ' ');

    if (dx_review !== null) {
        dx_review = dx_review.nextElementSibling.innerHTML;
    } else {
        dx_review = 'No Review';
    }
    replace_text = dx_label.innerText.split(/[/-]+/)[2]
    dx_label.innerText = dx_label.innerText.replace(replace_text, ' ' + dx_review);
}

function select_evidence(element) {
    document.querySelectorAll("[id^='" + element.id + "_']").forEach(function (item, index) {
        if (index > 7) {
            calculate_score(element);
        }

        if (element.checked === true) {
            item.removeAttribute('disabled');
        } else if (item.getAttribute('class') && !item.getAttribute('class').includes("check")) {
            item.setAttribute('disabled', 'true');
        }
    });
    calculate_score(element);
}

function add_disease(dtype) {
    if (dtype == null) {
        dtype = $("input[type='radio'][name='dtype']:checked").val();
        $("input[type='radio'][name='dtype']").filter('[value=so]').prop('checked', true);
    }

    const container = document.getElementById("diseases")
    const index = container.children.length - 1

    // Copy the element and its child nodes
    let disease_id;
    if (dtype === "gp") {
        disease_id = "d0";
    } else {
        disease_id = "d1";
    }

    let cln = document.getElementById(disease_id).cloneNode(true);
    cln.querySelectorAll("[id^='" + disease_id + "']").forEach(function (element) {
        if (element.tagName !== 'SELECT' && element.type !== 'checkbox' && !element.id.includes('score') && !element.id.includes('type') && !element.id.includes('r_name') && !element.id.includes('es_name') && !element.id.includes('disease') && !element.id.includes('branch')) {
            element.value = '';
        }
        if (element.id.includes("disease")) {
            element.setAttribute("required", "");
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
    cln.removeAttribute('hidden');
    cln.setAttribute('class', 'card my-5 pb-4');

    container.appendChild(cln);
    return cln;
}

function create_divider(element) {
    const elements = element.querySelectorAll('fieldset'), length = elements.length - 1;
    Object.values(elements).forEach(function (sub_element, index) {
        if (index !== length && sub_element.nextSibling.tagName !== 'HR') {
            const hr = document.createElement('hr');
            hr.setAttribute('class', 'divider');
            element.insertBefore(hr, sub_element.nextSibling);
        }
    });
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
    cln.querySelectorAll("[id^='" + sub_id + "']").forEach(function (element) {
        if (element.tagName !== 'SELECT') {
            element.value = '';
        }
        element.id = element.id.slice(0, -1) + index;
    })
    container.appendChild(cln);
}

function add_f_class(element) {
    const dx_id = element.id.split("_")[0];
    // Get the container
    const container = document.getElementById(dx_id + "_func_classes");
    const fc_num = container.children.length - 1

    let cln = document.getElementById(dx_id + "_fc0").cloneNode(true);
    cln.querySelectorAll("[id^='" + dx_id + "_fc']").forEach(function (element) {
        element.id = element.id.replace(/fc\d/gi, 'fc' + fc_num)
        if (element.name) {
            element.name = element.name.replace(/fc\d/gi, 'fc' + fc_num);
        }
        if (element.id.includes("add") && fc_num > 1) {
            element.setAttribute("hidden", "");
        }
    })
    cln.id = dx_id + "_fc" + fc_num;
    cln.removeAttribute('hidden');
    cln.setAttribute('class', 'mt-2 pt-2 mb-0 double-hr')

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
    cln.querySelectorAll("[id^='" + fc_num + "_etype1_']").forEach(function (element) {
        if (element.tagName !== 'SELECT') {
            element.value = '';
        }
        element.id = element.id.slice(0, -1) + (container.children.length + 1);
    })
    cln.id = fc_num + "_etype1_" + (container.children.length + 1);

    // Append the cloned element to container
    container.appendChild(cln);
    create_divider(container);
}

function add_evidence_type2(element) {
    const dx_id = element.id.split("_")[0];
    // Get the container
    const container = document.getElementById(dx_id + "_evidences2");

    // Copy the element and its child nodes
    const cln = document.getElementById(dx_id + "_etype2_1").cloneNode(true);
    cln.querySelectorAll("[id^='" + dx_id + "_etype2_']").forEach(function (element) {
        if (element.tagName !== 'SELECT') {
            element.value = '';
        }
        element.id = element.id.slice(0, -1) + (container.children.length + 1);
    })
    cln.id = dx_id + "_etype2_" + (container.children.length + 1);

    // Append the cloned element to container
    container.appendChild(cln);
    create_divider(container);
}

function getElementsByValue(value, tag, id) {
    if (value === 'Curation Notes') {
        value = id.toString() + '_notes'
    }
    const search = document.getElementsByTagName(tag);
    const pat = new RegExp(value, "i");
    for (let i = 0; i < search.length; i++) {
        if ((value.includes('notes') && search[i].id.includes(value)) || (pat.test(search[i].value) && search[i].id.includes(id))) {
            const search_id = search[i].id.split('_').slice(0, 2).join('_');
            return [document.getElementById(search_id),
                document.getElementById(search_id + '_id')]
        }
    }
}

function selectChange(element, type) {
    const selected = element.options[element.selectedIndex].value.substring(0, 5);
    let select_id = element.id.split('_').slice(0, 2).join('_') + type + element.id.split(type.slice(-1)).slice(-1)
    const selectElement = document.getElementById(select_id);
    let found = false;
    Object.values(selectElement.children).forEach(function (element) {
        if (!element.innerText.includes(selected)) {
            element.setAttribute('disabled', '');
            element.setAttribute('hidden', '');
        } else {
            if (!found) {
                selectElement.value = element.value;
            }
            element.removeAttribute('disabled');
            element.removeAttribute('hidden');
            found = true;
        }
    });
}

function tierChange(element, options, result) {
    const selected = element.options[element.selectedIndex].value;
    let select_id = element.id.split('_').slice(0, 1).join('_') + '_others';
    const selectElement = document.getElementById(select_id);
    const tier = document.getElementById(element.id.split('_').slice(0, 1).join('_') + '_tier_collapse');
    const selectedTrue = (selected === options[0] || selected === options[1]);
    if (selectedTrue) {
        selectElement.value = result;
        selectElement.setAttribute('readonly', '');
        tier.innerText = tier.innerText.split('- ')[0] + '- ' + result;
    } else {
        selectElement.removeAttribute('readonly');
    }

    let evid_id = element.id.split('_').slice(0, 1).join('_') + '_etype2'
    const btn = document.getElementById(evid_id);
    let index = 1, div = 'Test';
    while (div) {
        div = document.getElementById(evid_id + '_' + index.toString());
        if (result === 'Tier IV' && selectedTrue) {
            btn.setAttribute('disabled', '');
            if (div) {
                div.querySelectorAll("[id^='" + evid_id + "']").forEach(function (element) {
                    if (element.tagName === 'INPUT' || element.tagName === 'TEXTAREA') {
                        element.value = '';
                    }
                })
                div.setAttribute('hidden', '');
                div.setAttribute('disabled', '');
            }
        } else {
            btn.removeAttribute('disabled');
            if (div) {
                div.removeAttribute('hidden');
                div.removeAttribute('disabled');
            }
        }
        index++;
    }
}

function calculate_score(element) {
    const dx_id = element.id.slice(0, 2)
    const checkboxes = document.getElementsByName(dx_id);

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
    document.getElementById(dx_id + "_for_score").setAttribute("value", forScore);

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
    document.getElementById(dx_id + "_against_score").setAttribute("value", againstScore);
    set_ACMG_class(dx_id)
}

function set_ACMG_class(dx_id) {
    const for_score = document.getElementById(dx_id + "_for_score").value;
    const against_score = document.getElementById(dx_id + "_against_score").value;
    const acmg_class = document.getElementById(dx_id + "_acmg");

    if (for_score.includes('Pathogenic')) {
        if (against_score === 'Uncertain') {
            acmg_class.setAttribute("value", for_score);
        } else if (against_score.includes('Benign')) {
            acmg_class.setAttribute("value", 'VUS');
        }
    } else if (against_score.includes('Benign')) {
        acmg_class.setAttribute("value", against_score);
    } else {
        acmg_class.setAttribute("value", 'Uncertain');
    }
}

function updateMsg() {
    const checkboxes = document.querySelectorAll('input[name="review"]:checked');
    if (checkboxes.length > 0) {
        return confirm('Do you want to update?');
    }
    return true;
}