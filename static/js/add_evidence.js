$(document).ready(function () {
    $(window).scroll(function () {
        if ($(this).scrollTop() > 50) {
            $('#back-to-top').fadeIn();
        } else {
            $('#back-to-top').fadeOut();
        }
    });
    // scroll body to 0px on click
    $('#back-to-top').click(function () {
        const body = $('body,html');
        if ($('anchor')) body.animate({scrollTop: 400}, 400);
        else body.animate({scrollTop: 0}, 400);
        return false;
    });

    $(":input:not([class*='form-control'], [type='hidden'], [role='tab'], select, button, :checkbox, :radio)").addClass('form-control');
    $('select').addClass('form-select');

    const element = document.getElementsByName('key')[0];
    //calculate_score(element, 'score-' + element.id.split('-')[1]);

    const dx_names = $("input[name^='dx'][name$='name']");
    if (dx_names) dx_names.attr('oninput', 'set_header(this)');
});

function set_header(element) {
    let dx_id = element.id.slice(0, -4),
        dx_label = $('#' + dx_id + 'label'),
        dx_review = $('input[id*="' + dx_id + 'reviewed"]:checked');

    if (dx_review.length > 1) dx_review = dx_review.last().text();
    else dx_review = 'Not Reviewed';
    dx_label.text(element.value + ' / ' + dx_review)
}

function collapse(element) {
    if (element.innerText.includes("Expand")) {
        element.innerHTML = element.innerHTML.replace('Expand', 'Collapse');
    } else {
        element.innerHTML = element.innerHTML.replace('Collapse', 'Expand');
    }
}

$('#file').on('change', function () {
    const fileName = $(this).val();
    $(this).next('.custom-file-label').html(fileName.replace(/^.*[\\\/]/, ''));
});

$("form:not([action='/upload/'])").submit(function (e) {
    $(':disabled').each(function (e) {
        $(this).removeAttr('disabled');
    })
});

//new bootstrap.Modal(document.getElementById('uploadModal')).show();


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
    let tab_div = $(main_elem).parent().prev();
    tab_div.find("[id!='empty_link'][hidden]")
        .first().removeAttr('hidden')
        .tab('show').val('New Interpretation');
    tab_div.children().first()
        .removeClass('active')
        .attr('hidden', '');
}


function add_item(element, is_cat = false) {
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


/* PVS = 10; PS = 7; PM = 2; PP = 1
 * P:  12-14, 17; LP: 6, 9, 11, 12
 * ==================================
 * BA = 16; BS = 8; BP = 1
 * B:  16; LB: 2, 9
 */
function calculate_score(element) {
    let forScore, againstScore, score_label;
    forScore = againstScore = 0;
    $('.' +  element.className.split(' ')[1]).each(function () {
        if (this.checked) {
            score_label = this.getAttribute('aria-label')
            if (score_label === 'P') forScore += parseInt(this.value);
            else againstScore += parseInt(this.value);
        }
    })

    if (forScore > 11) forScore = 'Pathogenic';
    else if (forScore > 5) forScore = 'Likely Pathogenic';
    else forScore = 'Uncertain';

    if (againstScore > 15) againstScore = 'Benign';
    else if (againstScore > 1) againstScore = 'Likely Benign';
    else againstScore = 'Uncertain';

    const prefix = 'score-' + element.id.split('-')[1];
    $('#id_' + prefix + '-for_score').val(forScore);
    $('#id_' + prefix + '-against_score').val(againstScore);

    const acmgClass = $('#id_' + prefix + '-content');
    if (forScore.includes('Pathogenic')) {
        if (againstScore === 'Uncertain') acmgClass.val(forScore);
        else if (againstScore.includes('Benign')) acmgClass.val('VUS');
    } else if (againstScore.includes('Benign')) acmgClass.val(againstScore);
    else acmgClass.val('Uncertain');
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


function tierChange(element, options, result) {
    let temp = $(element).parent().parent().parent().parent().parent().prev()[0],
        selected = element.options[element.selectedIndex].value,
        selectElement = $('#' + temp.id.split('_').slice(0, 2).join('_').slice(0,-3) + 'others'),
        //tier = $(temp.id.split('_').slice(0, 1).join('_') + '_tier_collapse'),
        selectedTrue = (selected === options[0] || selected === options[1]);

    if (selectedTrue) {
        selectElement.val(result);
        selectElement.attr('readonly', '');
        //tier.text(tier.text().split('- ')[0] + '- ' + result);
    } else selectElement.removeAttr('readonly');

    let evid_id = temp.id.split('_').slice(0, 1).join('_') + '_etype2', div = $('div'), btn = $(evid_id);
    $("div[id^='inner_form']").each(function(index) {
        div = $(evid_id + '_' + index.toString());
        if (result === 'Tier IV' && selectedTrue) {
            btn.attr('disabled', '');
            if (div) {
                div.find("[id^='" + evid_id + "']").each(function (element) {
                    if (element.tagName === 'INPUT' || element.tagName === 'TEXTAREA') element.value = '';
                })
                div.attr('hidden', '');
                div.attr('disabled', '');
            }
        } else {
            btn.removeAttr('disabled');
            if (div) {
                div.removeAttr('hidden');
                div.removeAttr('disabled');
            }
        }
    });
}


function updateMsg() {
    const checkboxes = document.querySelectorAll('input[name="review"]:checked');
    if (checkboxes.length > 0) {
        return confirm('Do you want to update?');
    }
    return true;
}