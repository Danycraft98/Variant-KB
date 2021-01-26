$(document).ready(function () {
    $("input[type='text'], input[type='number'], textarea").addClass('form-control');
    $("select").addClass('form-select');

    $('.required').prop('required', function () {
        return $(this).is(':visible');
    });
});

function change_disease(main_elem) {
    const branch = main_elem.value, div = $("div[data-key='" + branch + "']"), other_divs = $("div[data-key!='" + branch + "']")

    div.addClass('show active');
    other_divs.removeClass('show active');
    div.find('select[id*="branch"]').val(branch);
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
    document.getElementById(element.id + '_evid').disabled = element.checked !== true;

    document.querySelectorAll("[id^='" + element.id + "_']").forEach(function (item, index) {
        if (index > 7) {
            calculate_score(element, prefix);
        }
    });
    calculate_score(element, prefix);
}

/* PVS = 10; PS = 7; PM = 2; PP = 1
 * P:  12-14, 17; LP: 6, 9, 11, 12
 * ==================================
 * BA = 16; BS = 8; BP = 1
 * B:  16; LB: 2, 9
 */
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
        forScore = 'Pathogenic';
    } else if (forScore > 5) {
        forScore = 'Likely Pathogenic';
    } else {
        forScore = 'Uncertain';
    }

    if (againstScore > 15) {
        againstScore = 'Benign';
    } else if (againstScore > 1) {
        againstScore = 'Likely Benign';
    } else {
        againstScore = 'Uncertain';
    }
    $('#id_' + prefix + '-for_score').val(forScore);
    $('#id_' + prefix + '-against_score').val(againstScore);
    const acmgClass = $('#id_' + prefix + '-content');

    if (forScore.includes('Pathogenic')) {
        if (againstScore === 'Uncertain') {
            acmgClass.val(forScore);
        } else if (againstScore.includes('Benign')) {
            acmgClass.val( 'VUS');
        }
    } else if (againstScore.includes('Benign')) {
        acmgClass.val( againstScore);
    } else {
        acmgClass.val( 'Uncertain');
    }
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