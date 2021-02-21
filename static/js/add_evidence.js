$('form').submit(function (e) {
    $(':disabled').each(function (e) {
        $(this).removeAttr('disabled');
    })
});


Array.prototype.remove = function () {
    let what, a = arguments, L = a.length, ax;
    while (L && this.length) {
        what = a[--L];
        while ((ax = this.indexOf(what)) !== -1) {
            this.splice(ax, 1);
        }
    }
    return this;
};


$(document).ready(function () {
    $(":input:not([class*='form-control'], [type='hidden'], [role='tab'])").addClass('form-control');
    $('select, button, :checkbox, :radio').removeClass('form-control');
    $('select').addClass('form-select');

    const element = document.getElementsByName('key')[0]
    calculate_score(element, 'score-' + element.id.split('-')[1]);
});


function change_required() {
    $(":input:not([name='csrfmiddlewaretoken'], [name*='FORMS'])")
        .attr('value', function () {
            const element = $(this)
            if (!element.val()) {
                if (this.name.includes('name')) return '';
                else if (!element.is(':visible')) return '';
            }
        })
        .prop('required', function () {
            return $(this).is(':visible')
        });
}


function change_disease(main_elem) {
    const div_id = main_elem.id.split('-').slice(0, 2).join('-');
    let branch = main_elem.value,
        current = $('[id*=' + div_id + ']'),
        div = $("[data-key='" + branch + "']"),
        cloneDiv = div.clone(),
        index = main_elem.id.split('-')[1],
        other_branch = ['no', 'gp', 'so'];

    other_branch.remove(branch);
    other_branch.forEach(function (elem) {
        $("[data-key='" + elem + "']").remove();
    })
    current.removeClass('show active');
    cloneDiv.addClass('show active');
    cloneDiv.find(':input,label,div').each(function () {
        let elem = $(this)
        if (elem.attr('for')) elem.attr('for', elem.attr('for').replace('__prefix__', index.toString()));
        if (elem.attr('id')) elem.attr('id', elem.attr('id').replace('__prefix__', index.toString()));
        if (elem.attr('name')) elem.attr('name', elem.attr('name').replace('__prefix__', index.toString()));
        if (elem.attr('class')) elem.removeClass('empty-form');
    })
    cloneDiv.attr('id', cloneDiv.attr('id').replace('__prefix__', index.toString()));
    cloneDiv.removeClass('empty-form');

    cloneDiv.find('select[id*="branch"]').val(branch).attr('disabled', '');
    cloneDiv.attr('id', '');
    div.parent().append(cloneDiv);
}


function add_disease(main_elem) {
    let nav_tab = $(main_elem).parent().prev().find('[hidden]').first();
    nav_tab.removeAttr('hidden');
    nav_tab.val('New Interpretation');
}


function add_item(element, is_cat=false) {
    let jq_elem = $(element.parentElement.parentElement);
    if (is_cat) jq_elem = jq_elem.next();
    const elem_clone = jq_elem.clone();
    elem_clone.find(':input').val('').removeClass('disabled');
    jq_elem.parent().append(elem_clone);
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
            score_label = elem.getAttribute('aria-label')
            console.log(score_label, elem.getAttribute('aria-label'));
            if (score_label === 'P') forScore += parseInt(elem.value);
            else againstScore += parseInt(elem.value);
        }
    });

    if (forScore > 11) forScore = 'Pathogenic';
    else if (forScore > 5) forScore = 'Likely Pathogenic';
    else forScore = 'Uncertain';


    if (againstScore > 15) againstScore = 'Benign';
    else if (againstScore > 1) againstScore = 'Likely Benign';
    else againstScore = 'Uncertain';

    $('#id_' + prefix + '-for_score').val(forScore);
    $('#id_' + prefix + '-against_score').val(againstScore);

    const acmgClass = $('#id_' + prefix + '-content');
    if (forScore.includes('Pathogenic')) {
        if (againstScore === 'Uncertain') acmgClass.val(forScore);
        else if (againstScore.includes('Benign')) acmgClass.val('VUS');
    } else if (againstScore.includes('Benign')) acmgClass.val(againstScore);
    else acmgClass.val('Uncertain');
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