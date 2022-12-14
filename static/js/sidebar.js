document.addEventListener("DOMContentLoaded", (function() {
    var e = document.querySelectorAll("[data-bss-chart]");
    for (var t of e) t.chart = new Chart(t, JSON.parse(t.dataset.bssChart))
}), !1),
function() {
    "use strict";
    var e = document.querySelector(".sidebar"),
        t = document.querySelectorAll("#sidebarToggle, #sidebarToggleTop");
    if (e) {
        e.querySelector(".collapse");
        var o = [].slice.call(document.querySelectorAll(".sidebar .collapse")).map((function(e) {
            return new bootstrap.Collapse(e, {
                toggle: !1
            })
        }));
        for (var n of t) n.addEventListener("click", (function(t) {
            if (document.body.classList.toggle("sidebar-toggled"), e.classList.toggle("toggled"), e.classList.contains("toggled"))
                for (var n of o) n.hide()
        }));
        window.addEventListener("resize", (function() {
            if (Math.max(document.documentElement.clientWidth || 0, window.innerWidth || 0) < 768)
                for (var e of o) e.hide()
        }))
    }
    var r = document.querySelector("body.fixed-nav .sidebar");
    r && r.on("mousewheel DOMMouseScroll wheel", (function(e) {
        if (Math.max(document.documentElement.clientWidth || 0, window.innerWidth || 0) > 768) {
            var t = e.originalEvent,
                o = t.wheelDelta || -t.detail;
            this.scrollTop += 30 * (o < 0 ? 1 : -1), e.preventDefault()
        }
    }));
    var l = document.querySelector(".scroll-to-top");
    l && window.addEventListener("scroll", (function() {
        var e = window.pageYOffset;
        l.style.display = e > 100 ? "block" : "none"
    }))
}();