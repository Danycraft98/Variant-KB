/*!
 * jQuery Textarea AutoSize plugin : https://github.com/javierjulio/textarea-autosize
 * Author: Javier Julio
 * Licensed under the MIT license
 */
!function (t, e, i, n) {
    function s(e, i) {
        this.element = e, this.$element = t(e), this.init()
    }

    var h = "textareaAutoSize", o = "plugin_" + h, r = function (t) {
        return t.replace(/\s/g, "").length > 0
    };
    s.prototype = {
        init: function () {
            var i = parseInt(this.$element.css("paddingBottom")) + parseInt(this.$element.css("paddingTop")) + parseInt(this.$element.css("borderTopWidth")) + parseInt(this.$element.css("borderBottomWidth")) || 0;
            r(this.element.value) && this.$element.height(this.element.scrollHeight - i), this.$element.on("input keyup", function (n) {
                var s = t(e), h = s.scrollTop();
                t(this).height(0).height(this.scrollHeight - i), s.scrollTop(h)
            })
        }
    }, t.fn[h] = function (e) {
        return this.each(function () {
            t.data(this, o) || t.data(this, o, new s(this, e))
        }), this
    }
}(jQuery, window, document);

// Initialize Textarea
$('.textarea-autosize').textareaAutoSize();