function textCounter(e, t, n) {
    if (e.value.length > n) {
        e.value = e.value.substring(0, n)
    } else {
        t.value = n - e.value.length
    }
}

function setbg(e, t) {
    document.getElementById(t).style.background = e
}

function PopUp(e, t) {
    document.getElementById(e).style.display = "block";
    document.getElementById(e).style.top = "auto";
    document.getElementById(e).style.left = "auto";
    document.getElementById(e).style.height = "auto";
    document.getElementById(e).style.width = t + "px"
}

function sendFree() {
    xajax.$("submit").disabled = true;
    xajax.$("submit").value = "Please wait...";
    xajax_processMsg(xajax.getFormValues("smsform"));
    return false
}

function refreshimage() {
    ord = Math.random();
    ord = ord * 10000000000000000000;
    i = "/image.php?o=";
    io = document.getElementById("captcha");
    io.src = i + ord;
}

function RDset(e) {
    var t = new Date;
    var n = window.location.hostname;
    t.setTime(t.getTime() + e * 24 * 60 * 60 * 1e3);
    var r = "expires=" + t.toGMTString();
    document.cookie = "rd=" + n + "; " + r
}

function createCookie(e, t, n) {
    if (n) {
        var r = new Date;
        r.setTime(r.getTime() + n * 24 * 60 * 60 * 1e3);
        var i = "; expires=" + r.toGMTString()
    } else var i = "";
    document.cookie = e + "=" + t + i + "; path=/"
}

function eraseCookie(e) {
    createCookie(e, "", -1)
}
popUp = function (e, t) {
    function l(e) {
        if (!e) {
            return
        }
        e = e.replace("px", "");
        if (isNaN(e)) {
            return 0
        }
        return parseInt(e)
    }
    t = t || {};
    var n = t.HasBackground != null ? t.HasBackground : true;
    var r = t.BackgroundColor || "#000000";
    var i = t.BackgroundOpacity || 50;
    i = i > 0 ? i : 1;
    var s = t.BackgroundOnClick || function () {};
    var o = t.BackgroundCursorStyle || "default";
    var u = t.Zindex || 9e4;
    var a = t.AddLeft || 0;
    var f = t.AddTop || 0;
    var c = document.getElementById(e);
    if (!c) {
        return
    }
    var h = document.layers || document.getElementById && !document.all ? window.outerWidth : document.all ? document.body.clientWidth : 0;
    var p = window.innerHeight ? window.innerHeight : document.getBoxObjectFor ? Math.min(document.documentElement.clientHeight, document.body.clientHeight) : document.documentElement.clientHeight != 0 ? document.documentElement.clientHeight : document.body ? document.body.clientHeight : 0;
    c.style.display = "block";
    c.style.visibility = "visible";
    var d;
    if (c.currentStyle) {
        d = c.currentStyle
    } else if (window.getComputedStyle) {
        d = document.defaultView.getComputedStyle(c, null)
    } else {
        d = c.style
    }
    var v = c.offsetWidth - l(d.marginLeft) - l(d.marginRight) - l(d.borderLeftWidth) - l(d.borderRightWidth);
    var m = c.offsetHeight - l(d.marginTop) - l(d.marginBottom) - l(d.borderTopWidth) - l(d.borderBottomWidth);
    c.style.position = "fixed";
    c.style.left = h / 2 - v / 2 + a + "px";
    c.style.top = p / 2 - m / 2 + f - 10 + "px";
    c.style.zIndex = u + 1;
    if (n) {
        if (!popUp._BackgroundDiv) {
            popUp._BackgroundDiv = document.createElement("div");
            popUp._BackgroundDiv.style.display = "none";
            popUp._BackgroundDiv.style.width = "100%";
            popUp._BackgroundDiv.style.position = "absolute";
            popUp._BackgroundDiv.style.top = "0px";
            popUp._BackgroundDiv.style.left = "0px";
            document.body.appendChild(popUp._BackgroundDiv)
        }
        popUp._BackgroundDiv.onclick = s;
        popUp._BackgroundDiv.style.background = r;
        popUp._BackgroundDiv.style.height = document.all ? Math.max(Math.max(document.documentElement.offsetHeight, document.documentElement.scrollHeight), Math.max(document.body.offsetHeight, document.body.scrollHeight)) : (document.body ? document.body.scrollHeight : document.documentElement.scrollHeight != 0 ? document.documentElement.scrollHeight : 0) + "px";
        popUp._BackgroundDiv.style.filter = "progid:DXImageTransform.Microsoft.Alpha(opacity=" + i + ")";
        popUp._BackgroundDiv.style.MozOpacity = i / 100;
        popUp._BackgroundDiv.style.opacity = i / 100;
        popUp._BackgroundDiv.style.zIndex = u;
        popUp._BackgroundDiv.style.cursor = o;
        popUp._BackgroundDiv.style.display = ""
    }
};
popUp.Close = function (e) {
    if (e) {
        document.getElementById(e).style.display = "none";
        document.getElementById(e).style.visibility = "hidden"
    }
    if (popUp._BackgroundDiv) {
        popUp._BackgroundDiv.style.display = "none"
    }
}