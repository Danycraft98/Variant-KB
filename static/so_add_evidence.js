function collapse(element, index) {
    var arrow = document.getElementById(element.id.split("_").slice(0,index).join("_") + "_icon")
    if (element.className.includes("collapsed")) {
        arrow.className = arrow.className.replace("down", "up");
    } else {
        arrow.className = arrow.className.replace("up", "down");
    }
}

function add_disease() {
    var container = document.getElementById("diseases")
    var index = container.children.length / 2

    var cln = document.getElementById("add").cloneNode(true);
    cln.querySelectorAll("[id^='d0']").forEach(function(element, test) {
        element.id = element.id.replace(/^d\d/gi, 'd' + index)
    })
    cln.children[0].children[0].setAttribute("data-target", "#d" + index);
    cln.children[0].children[0].removeAttribute("hidden");
    cln.children[1].children[0].remove();
    container.appendChild(cln);

    // Copy the element and its child nodes
    cln = document.getElementById("d0").cloneNode(true);
    cln.querySelectorAll("[id^='d0']").forEach(function(element, test) {
        if (element.tagName != 'SELECT' && element.type != 'checkbox' && !element.id.includes('score') && element.name && !element.name.includes('report')) {
            element.value = '';
        }
        if (element.id.includes("disease")) {
            element.setAttribute("required","");
        }
        if (element.name) {
            element.name = element.name.replace(/^d\d/gi, 'd' + index)
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


function add_f_class(element) {
    var disease_num = element.id.split("_")[0];
    // Get the container
    var container = document.getElementById(disease_num + "_f_classes");
    var fc_num = container.children.length/2

    // Copy the element and its child nodes
    var cln = document.getElementById(disease_num + "_fc0_collapse").cloneNode(true);
    cln.querySelectorAll("[id^='" + disease_num + "_fc']").forEach(function(element, test) {
        element.id = element.id.replace(/fc\d/gi, 'fc' + fc_num)
        if (element.name)
            element.name = element.name.replace(/fc\d/gi, 'fc' + fc_num)
    })
    cln.id = disease_num + "_fc" + fc_num + "_collapse";
    cln.setAttribute("data-target", "#" + disease_num + "_fc" + fc_num)
    cln.removeAttribute('hidden')
    container.appendChild(cln);

    var cln = document.getElementById(disease_num + "_fc0").cloneNode(true);
    cln.querySelectorAll("[id^='" + disease_num + "_fc']").forEach(function(element, test) {
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
    var fc_num = element.id.split("_").slice(0, 2).join("_");

    // Get the container
    var container = document.getElementById(fc_num + "_evidences1");

    // Copy the element and its child nodes
    var cln = document.getElementById(fc_num + "_etype1_1").cloneNode(true);
    cln.querySelectorAll("[id^='" + fc_num + "_etype1_']").forEach(function(element, test) {
        if (element.tagName != 'SELECT') {
            element.value = '';
        }
        element.id = element.id.slice(0,-1) + (container.children.length+1);
    })
    cln.id = fc_num + "_etype1_" + (container.children.length+1);

    // Append the cloned element to container
    container.appendChild(cln);
}

function add_evidence_type2(element) {
    var disease_num = element.id.split("_")[0];
    // Get the container
    var container = document.getElementById(disease_num + "_evidences2");

    // Copy the element and its child nodes
    var cln = document.getElementById(disease_num + "_etype2_1").cloneNode(true);
    cln.querySelectorAll("[id^='" + disease_num + "_etype2_']").forEach(function(element, test) {
        if (element.tagName != 'SELECT') {
            element.value = '';
        }
        element.id = element.id.slice(0,-1) + (container.children.length+1);
    })
    cln.id = disease_num + "_etype2_" + (container.children.length+1);

    // Append the cloned element to container
    container.appendChild(cln);
}

function getElementsByValue(value, tag, id) {
	var search = document.getElementsByTagName(tag);
	var pat = new RegExp(value, "i");
	for (var i=0; i < search.length; i++) {
		if (pat.test(search[i].value)  && search[i].id.includes(id))
			return [document.getElementById(search[i].id.slice(0,-5)), document.getElementById(search[i].id.slice(0,-5) + '_id')]
	}
}