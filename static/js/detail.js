function onMouseUpdate(e) {
    return tooltip.style('top', (e.pageY - 10) + 'px').style('left', (e.pageX + 10) + 'px');
}

function expand(element_id, element) {
    collapse(element);
    element = document.getElementById(element_id);
    if (element.getAttribute('style').includes(' height')) {
        element.setAttribute('style', 'overflow: hidden; overflow-wrap: break-word; min-height: 48px;');
    } else {
        autosize.update(element);
    }
}

$(document).ready(function () {
    autosize(document.querySelectorAll('textarea'));

    let min_height = 0;
    let tabs = jQuery('.tab-content .tab-pane');
    jQuery.each(tabs, function () {
        this.classList.add('active'); /* make all visible */
        min_height = (this.clientHeight > min_height ? this.clientHeight : min_height);
        if (!jQuery(this).hasClass('show')) {
            this.classList.remove('active'); /* hide again */
        }
    });
    jQuery.each(tabs, function () {
        jQuery(this).css('min-height', min_height);
    });
});

function checked(element) {
    if (element.innerText === 'Selected') {
        element.innerHTML = "Select<a style='visibility: hidden'>ed</a>";
    } else {
        element.innerHTML = 'Selected';
    }
}

function copy() {
    const selected_reports = document.getElementById('selected-reports');
    let report_str = '';
    Object.values(document.querySelectorAll("input[name='report']")).forEach(function (element) {
        const copyText = document.getElementById(element.id.replace('_', '-'));
        if (element.checked === true) {
            /* Copy the text inside the text field to another field */
            console.log(element.value);
            report_str += element.value + ':\n' + copyText.value + '\n\n';
        }
    });
    selected_reports.value = report_str.substring(0, report_str.length - 2);

    /* Get the text field */
    selected_reports.select();
    selected_reports.setSelectionRange(0, 99999); /* For mobile devices */

    /* Copy the text inside the text field */
    document.execCommand('copy');

    /* Alert the copied text*/
    alert("Copied the text: " + selected_reports.value);

}