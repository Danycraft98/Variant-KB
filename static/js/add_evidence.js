$(document).ready(function () {
    $('.required').prop('required', function () {
        return $(this).is(':visible');
    });
});

function change_disease(main_elem) {
    let branch = main_elem.value, div = document.querySelector('div[data-key="' + branch + '"]'), other_divs;
    if (branch === 'gp') {
        other_divs = [document.querySelector('div[data-key="so"]'), document.querySelector('div[data-key="no"]')];
    } else if (branch === 'so') {
        other_divs = [document.querySelector('div[data-key="gp"]'), document.querySelector('div[data-key="no"]')];
    } else {
        other_divs = [document.querySelector('div[data-key="gp"]'), document.querySelector('div[data-key="so"]')];
    }

    div.setAttribute('class', 'tab-pane fade show active empty-form');
    other_divs.forEach(function (element) {
        element.setAttribute('class', 'tab-pane fade empty-form');
    });

    Object.values(div.querySelectorAll('select[id*="branch"] option')).forEach(function (element) {
        element.selected = element.value === branch;
    });

    document.getElementById('empty_link').setAttribute('href', '#' + div.id);
}

function add_evid(element) {
    const form_elem = $(element.parentElement.parentElement.nextElementSibling);
    const form = form_elem.first();

    const form_elem_clone = form_elem.clone();
    const form_idx = form.val();
    form_elem_clone.html(form_elem_clone.html().replace(/__prefix__/g, form_idx));

    form.val(parseInt(form_idx) + 1);
    form_elem_clone.insertAfter(form_elem);
}

function select_evidence(element, prefix) {
    console.log(document.getElementById(element.id + '_evid'), element.checked === true);
    document.getElementById(element.id + '_evid').disabled = element.checked === true;

    document.querySelectorAll("[id^='" + element.id + "_']").forEach(function (item, index) {
        if (index > 7) {
            calculate_score(element, prefix);
        }
    });
    calculate_score(element, prefix);
}

//TODO: Fix calculation
function calculate_score(element, prefix) {
    let forScore, againstScore, score_label, checkboxes;
    checkboxes = document.getElementsByName(element.name);
    forScore = againstScore = 0;
    Object.values(checkboxes).forEach(function (elem) {
        if (elem.checked) {
            score_label = elem.getAttribute('aria-label');
            if (score_label.includes('P') && !score_label.includes('B'))
                forScore += parseInt(elem.value);
            else
                againstScore += parseInt(elem.value);
        }
    });

    if (forScore > 11) {
        forScore = 'Path';
    } else if (forScore > 5){
        forScore = 'Likely Path';
    } else {
        forScore = 'Uncertain';
    }

    if (againstScore > 15) {
        againstScore = 'Benign';
    } else if (againstScore > 1){
        againstScore = 'Likely Benign';
    } else {
        againstScore = 'Uncertain';
    }
    $('#id_' + prefix + '-for_score').val(forScore);
    $('#id_' + prefix + '-against_score').val(againstScore);
}


function calculate_score_(element) {
    const checkboxes = document.getElementsByName(element.name), dict = {};
    let l_path, path, l_benign, check_id, forScore, againstScore, benign = false;
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
    if (path) {
        forScore = "Pathogenic"
    } else if (l_path) {
        forScore = "Likely Pathogenic"
    } else {
        forScore = "Uncertain"
    }
    //document.getElementById(dx_id + "_forScore").setAttribute("value", forScore);

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
    console.log(forScore, againstScore);
    //document.getElementById(dx_id + "_againstScore").setAttribute("value", againstScore);
    //set_ACMG_class(dx_id)
}

function set_reviewed(element) {
    const review_val = $('input[name="' + element.name + '"]:checked').last().val(), select_id = element.id.split('_').splice(0, 2).join('_');
    Object.values(document.querySelectorAll('select[id*="' + select_id + '"] option')).forEach(function (element) {
        element.selected = element.value === review_val;
    });
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

function copyReport(item) {
    Array.prototype.forEach.call(document.getElementsByName(item.name), function (element) {
        element.value = item.value;
    });
}

function collapse(element) {
    if (element.innerText.includes("Expand")) {
        element.innerHTML = element.innerHTML.replace('Expand', 'Collapse');
    } else {
        element.innerHTML = element.innerHTML.replace('Collapse', 'Expand');
    }
}

function set_ACMG_class(dx_id) {
    const forScore = document.getElementById(dx_id + "_forScore").value;
    const againstScore = document.getElementById(dx_id + "_againstScore").value;
    const acmg_class = document.getElementById(dx_id + "_acmg");

    if (forScore.includes('Pathogenic')) {
        if (againstScore === 'Uncertain') {
            acmg_class.setAttribute("value", forScore);
        } else if (againstScore.includes('Benign')) {
            acmg_class.setAttribute("value", 'VUS');
        }
    } else if (againstScore.includes('Benign')) {
        acmg_class.setAttribute("value", againstScore);
    } else {
        acmg_class.setAttribute("value", 'Uncertain');
    }
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

function updateHeader(element) {
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

function updateMsg() {
    const checkboxes = document.querySelectorAll('input[name="review"]:checked');
    if (checkboxes.length > 0) {
        return confirm('Do you want to update?');
    }
    return true;
}