/*! Django Formset - v0.3.0 - 2014-11-15
* https://github.com/mbertheau/jquery.django-formset
* Copyright (c) 2014 Markus Bertheau; Licensed MIT */

const __hasProp = {}.hasOwnProperty, __extends = function (a, b) {
    function c() {
        this.constructor = a
    }

    for (let d in b) __hasProp.call(b, d) && (a[d] = b[d]);
    return c.prototype = b.prototype, a.prototype = new c, a.__super__ = b.prototype, a
};
!function (a) {
    let b;
    a.fn.djangoFormset = function (b) {
        return new a.fn.djangoFormset.Formset(this, b);
    },
    b = function (a) {
        function b() {
            return b.__super__.constructor.apply(this, arguments)
        }

        return __extends(b, a), b;
    } (Error), a.fn.djangoFormset.Formset = function () {
        function c(c, d) {
            let e, f, g, h;
            if (this.opts = a.extend({}, a.fn.djangoFormset.defaultOptions, d), 0 === c.length)
                throw new b("Empty selector.");

            if (this.template = c.filter("." + this.opts.formTemplateClass), 0 === this.template.length)
                throw new b("Can't find template (looking for ." + this.opts.formTemplateClass + ")");

            if (g = this.template.find("input,select,textarea").first().attr("name"), !g)
                throw new b("Can't figure out form prefix because there's no form element in the form template. Please add one.");

            if (h = g.indexOf("-__prefix__"), -1 === h)
                throw new b("Can't figure out form prefix from template because it doesn't contain '-__prefix__'.");

            if (this.prefix = g.substring(0, h),this.totalForms = a("#id_" + this.prefix + "-TOTAL_FORMS"), 0 === this.totalForms.length)
                throw new b("Management form field 'TOTAL_FORMS' not found for prefix " + this.prefix + ".");

            this._initTabs(), f = c.not("." + this.opts.formTemplateClass), this.initialForms = f.length, a(this).on(this.opts.on), this.forms = f.map(function (b) {
                return function (c, d) {
                    var e, f, g;
                    return b.hasTabs && (g = a.djangoFormset.getTabActivator(d.id), f = new b.opts.tabClass(g.closest(".nav > *"))), e = new b.opts.formClass(a(d), b, c, f), a(b).trigger("formInitialized", [e]), e
                }
            }

            (this)), this.forms.length !== parseInt(this.totalForms.val()), e = this.forms.filter(function () {
                return this.deleteInput.val()
            }),

            e.each(function () {
                return this["delete"]()
            }),

            this.insertAnchor = c.not("." + this.opts.formTemplateClass).last(),
            0 === this.insertAnchor.length && (this.insertAnchor = this.template)
        }

        return c.prototype._initTabs = function () {
            var c, d;
            if (this.hasTabs = this.template.is(".tab-pane"), this.hasTabs) {
                if (c = a.djangoFormset.getTabActivator(this.template.attr("id")), 0 === c.length) throw new b("Template is .tab-pane but couldn't find corresponding tab activator.");
                if (d = c.closest(".nav"), 0 === d.length) throw new b("Template is .tab-pane but couldn't find corresponding .nav.");
                if (this.tabTemplate = d.children("." + this.opts.formTemplateClass), 0 === this.tabTemplate.length) throw new b("Tab nav template not found (looking for ." + this.opts.formTemplateClass + ").")
            }
        },

        c.prototype.addForm = function () {
            let b, c, d, e, f;
            return this.hasTabs && (
                e = this.tabTemplate.clone().removeClass(this.opts.formTemplateClass),
                d = new this.opts.tabClass(e),
                f = this.forms.length > 0 ? this.forms[this.forms.length - 1].tab.elem : this.tabTemplate,
                e.insertAfter(f)), c = this.template.clone().removeClass(this.opts.formTemplateClass),
                b = new this.opts.formClass(c, this, parseInt(this.totalForms.val()), d),
                c.insertAfter(this.insertAnchor),
                this.insertAnchor = c,
                this.forms.push(b),
                this.totalForms.val(parseInt(this.totalForms.val()) + 1),
                this.hasTabs && d.activate(), a(this).trigger('formInitialized', [b]), a(this).trigger('formAdded', [b]), b
        },

        c.prototype.deleteForm = function (a) {
            var b;
            b = this.forms[a], b["delete"]()
        },

        c.prototype.handleFormRemoved = function (a) {
            var b, c, d, e, f;
            for (this.totalForms.val(parseInt(this.totalForms.val()) - 1), this.forms.splice(a, 1), f = this.forms, c = d = 0, e = f.length; e > d; c = ++d) b = f[c], b._updateFormIndex(c);
            this.insertAnchor = 0 === this.forms.length ? this.template : this.forms[this.forms.length - 1].elem
        }, c
    }(),

    a.fn.djangoFormset.Form = function () {
        function b(a, b, c, d) {
            let e;

            this.elem = a,
            this.formset = b,
            this.index = c,
            this.tab = d,
            this.elem.data("djangoFormset.Form", this),
            void 0 !== this.index && this._initFormIndex(this.index), this.deleteInput = this.field("DELETE"),
            /* TODO: FIX*/
            //e = this.index < this.formset.initialForms
            (this.deleteInput.length > 0 || !e) && this._replaceDeleteCheckboxWithButton()
        }

        return b.prototype.getDeleteButton = function () {
            return a("<button type='button' class='btn btn-danger'> " + this.formset.opts.deleteButtonText + " </button>")
        },

        b.prototype.insertDeleteButton = function () {
            this.deleteInput.length > 0 ? this.deleteInput.after(this.deleteButton) : (this.elem.is("TR") ? this.elem.children().last() : this.elem.is("UL") || this.elem.is("OL") ? this.elem.append("li").children().last() : this.elem).append(this.deleteButton)
        },

        b.prototype["delete"] = function () {
            let a, b, c;
            return a = this.index < this.formset.initialForms, 0 === this.deleteInput.length && a ? void console.warn("Tried do delete non-deletable form " + this.formset.prefix + " #" + this.index + ".") : (this.tab && this.tab.elem.is(".active") && (c = this.formset.forms.map(function (a, b) {
                return b.tab.elem[0]
            }), b = c.slice(this.index + 1).filter(":visible").first(), 0 === b.length && (b = c.slice(0, this.index).filter(":visible").last()), b.length > 0 && b.data("djangoFormset.tab").activate()), void (a ? (this.deleteInput.length > 0 && this.deleteInput.val("on"), this.tab && this.tab.elem.hide(), this.hide()) : (this.tab && this.tab.elem.remove(), this.elem.remove(), this.formset.handleFormRemoved(this.index))))
        },

        b.prototype.hide = function () {
            return this.elem.hide()
        },

        b.prototype.field = function (a) {
            return this.elem.find("[name='" + this.formset.prefix + "-" + this.index + "-" + a + "']")
        },

        b.prototype.prev = function () {
            let a, b, c;
            for (c = this.formset.forms.slice(0, +(this.index - 1) + 1 || 9e9), b = c.length - 1; b >= 0; b += -1) {
                if (a = c[b], a.elem.is(":visible"))
                    return a
            }
        },

        b.prototype._replaceDeleteCheckboxWithButton = function () {
            let b, c;
            this.deleteInput.length > 0 && (c = a("<input type='hidden' name='" + this.deleteInput.attr("name") + "' id='" + this.deleteInput.attr("id") + "' value='" + (this.deleteInput.is(":checked") ? "on" : "") + "'/>"), b = this.elem.find("label[for='" + this.deleteInput.attr("id") + "']"), b.has(this.deleteInput).length > 0 ? b.replaceWith(c) : (b.remove(), this.deleteInput.replaceWith(c)), this.deleteInput = c), this.deleteButton = this.getDeleteButton(), this.deleteButton.on("click", function (a) {
                return function () {
                    return a["delete"]()
                }
            }(this)),
            this.insertDeleteButton()
        },

        b.prototype._replaceFormIndex = function (b, c) {
            let d, e, f;
            this.index = c, e = new RegExp("" + this.formset.prefix + "-" + b), d = "" + this.formset.prefix + "-" + c, f = function (a) {

                let b, c, f, g, h, i, j;
                f = {
                    input: ["id", "name"], select: ["id", "name"], textarea: ["id", "name"],
                    label: ["for"], div: ["id"], "*": ["href", "data-target"]
                }

                if (a.length > 0) {
                    g = a.get(0).tagName,
                        c = [], g.toLowerCase() in f && (c = f[g.toLowerCase()]), c.push.apply(c, f["*"]),
                        j = [];

                    for (h = 0, i = c.length; i > h; h++)
                        b = c[h], j.push(a.attr(b) ? a.attr(b, a.attr(b).replace(e, d)) : void 0);
                    return j
                }
            },

            f(this.elem), this.elem.find("input, select, textarea, label").each(function () {
                f(a(this))
            }),

            this.tab && (f(this.tab.elem), this.tab.elem.find("a, button").each(function () {
                f(a(this))
            }))
        },

        b.prototype._initFormIndex = function (a) {
            this._replaceFormIndex("__prefix__", a)
        },

        b.prototype._updateFormIndex = function (a) {
            this._replaceFormIndex("\\d+", a)
        }, b
    }(),

    a.fn.djangoFormset.Tab = function () {
        function a(a) {
            this.elem = a, this.elem.data("djangoFormset.tab", this)
        }

        return a.prototype.activate = function () {
            return this.elem.find("[data-toggle='tab']").trigger("click")
        },

        a.prototype.remove = function () {
            return this.elem.remove()
        }, a
    }(),

    a.fn.djangoFormset.defaultOptions = {formTemplateClass: "empty-form", formClass: a.fn.djangoFormset.Form, tabClass: a.fn.djangoFormset.Tab, deleteButtonText: "Delete"}, a.djangoFormset = {
        getTabActivator: function (b) {
            return a("[href='#" + b + "'], [data-target='#" + b + "']")
        }
    }
}(jQuery);