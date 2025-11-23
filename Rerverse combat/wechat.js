var T = {}

function w(t, p) {
var n = (t & 65535) + (p & 65535),
L = (t >> 16) + (p >> 16) + (n >> 16);
return L << 16 | n & 65535
}
function f(t, p) {
return t << p | t >>> 32 - p
}
function m(t, p, n, L, E, j) {
return w(f(w(w(p, t), w(L, j)), E), n)
}
function _(t, p, n, L, E, j, F) {
return m(p & n | ~p & L, t, p, E, j, F)
}
function u(t, p, n, L, E, j, F) {
return m(p & L | n & ~L, t, p, E, j, F)
}
function l(t, p, n, L, E, j, F) {
return m(p ^ n ^ L, t, p, E, j, F)
}
function g(t, p, n, L, E, j, F) {
return m(n ^ (p | ~L), t, p, E, j, F)
}
function h(t, p) {
t[p >> 5] |= 128 << p % 32;
t[(p + 64 >>> 9 << 4) + 14] = p;
var n, L, E, j, F, o = 1732584193,
c = -271733879,
a = -1732584194,
s = 271733878;
for (n = 0; n < t.length; n += 16) {
    L = o;
    E = c;
    j = a;
    F = s;
    o = _(o, c, a, s, t[n], 7, -680876936);
    s = _(s, o, c, a, t[n + 1], 12, -389564586);
    a = _(a, s, o, c, t[n + 2], 17, 606105819);
    c = _(c, a, s, o, t[n + 3], 22, -1044525330);
    o = _(o, c, a, s, t[n + 4], 7, -176418897);
    s = _(s, o, c, a, t[n + 5], 12, 1200080426);
    a = _(a, s, o, c, t[n + 6], 17, -1473231341);
    c = _(c, a, s, o, t[n + 7], 22, -45705983);
    o = _(o, c, a, s, t[n + 8], 7, 1770035416);
    s = _(s, o, c, a, t[n + 9], 12, -1958414417);
    a = _(a, s, o, c, t[n + 10], 17, -42063);
    c = _(c, a, s, o, t[n + 11], 22, -1990404162);
    o = _(o, c, a, s, t[n + 12], 7, 1804603682);
    s = _(s, o, c, a, t[n + 13], 12, -40341101);
    a = _(a, s, o, c, t[n + 14], 17, -1502002290);
    c = _(c, a, s, o, t[n + 15], 22, 1236535329);
    o = u(o, c, a, s, t[n + 1], 5, -165796510);
    s = u(s, o, c, a, t[n + 6], 9, -1069501632);
    a = u(a, s, o, c, t[n + 11], 14, 643717713);
    c = u(c, a, s, o, t[n], 20, -373897302);
    o = u(o, c, a, s, t[n + 5], 5, -701558691);
    s = u(s, o, c, a, t[n + 10], 9, 38016083);
    a = u(a, s, o, c, t[n + 15], 14, -660478335);
    c = u(c, a, s, o, t[n + 4], 20, -405537848);
    o = u(o, c, a, s, t[n + 9], 5, 568446438);
    s = u(s, o, c, a, t[n + 14], 9, -1019803690);
    a = u(a, s, o, c, t[n + 3], 14, -187363961);
    c = u(c, a, s, o, t[n + 8], 20, 1163531501);
    o = u(o, c, a, s, t[n + 13], 5, -1444681467);
    s = u(s, o, c, a, t[n + 2], 9, -51403784);
    a = u(a, s, o, c, t[n + 7], 14, 1735328473);
    c = u(c, a, s, o, t[n + 12], 20, -1926607734);
    o = l(o, c, a, s, t[n + 5], 4, -378558);
    s = l(s, o, c, a, t[n + 8], 11, -2022574463);
    a = l(a, s, o, c, t[n + 11], 16, 1839030562);
    c = l(c, a, s, o, t[n + 14], 23, -35309556);
    o = l(o, c, a, s, t[n + 1], 4, -1530992060);
    s = l(s, o, c, a, t[n + 4], 11, 1272893353);
    a = l(a, s, o, c, t[n + 7], 16, -155497632);
    c = l(c, a, s, o, t[n + 10], 23, -1094730640);
    o = l(o, c, a, s, t[n + 13], 4, 681279174);
    s = l(s, o, c, a, t[n], 11, -358537222);
    a = l(a, s, o, c, t[n + 3], 16, -722521979);
    c = l(c, a, s, o, t[n + 6], 23, 76029189);
    o = l(o, c, a, s, t[n + 9], 4, -640364487);
    s = l(s, o, c, a, t[n + 12], 11, -421815835);
    a = l(a, s, o, c, t[n + 15], 16, 530742520);
    c = l(c, a, s, o, t[n + 2], 23, -995338651);
    o = g(o, c, a, s, t[n], 6, -198630844);
    s = g(s, o, c, a, t[n + 7], 10, 1126891415);
    a = g(a, s, o, c, t[n + 14], 15, -1416354905);
    c = g(c, a, s, o, t[n + 5], 21, -57434055);
    o = g(o, c, a, s, t[n + 12], 6, 1700485571);
    s = g(s, o, c, a, t[n + 3], 10, -1894986606);
    a = g(a, s, o, c, t[n + 10], 15, -1051523);
    c = g(c, a, s, o, t[n + 1], 21, -2054922799);
    o = g(o, c, a, s, t[n + 8], 6, 1873313359);
    s = g(s, o, c, a, t[n + 15], 10, -30611744);
    a = g(a, s, o, c, t[n + 6], 15, -1560198380);
    c = g(c, a, s, o, t[n + 13], 21, 1309151649);
    o = g(o, c, a, s, t[n + 4], 6, -145523070);
    s = g(s, o, c, a, t[n + 11], 10, -1120210379);
    a = g(a, s, o, c, t[n + 2], 15, 718787259);
    c = g(c, a, s, o, t[n + 9], 21, -343485551);
    o = w(o, L);
    c = w(c, E);
    a = w(a, j);
    s = w(s, F)
}
return [o, c, a, s]
}
function S(t) {
var p, n = "";
for (p = 0; p < t.length * 32; p += 8) {
    n += String.fromCharCode(t[p >> 5] >>> p % 32 & 255)
}
return n
}
function C(t) {
var p, n = [];
n[(t.length >> 2) - 1] = void 0;
for (p = 0; p < n.length; p += 1) {
    n[p] = 0
}
for (p = 0; p < t.length * 8; p += 8) {
    n[p >> 5] |= (t.charCodeAt(p / 8) & 255) << p % 32
}
return n
}
function D(t) {
return S(h(C(t), t.length * 8))
}
function z(t, p) {
var n, L = C(t),
E = [],
j = [],
F;
E[15] = j[15] = void 0;
if (L.length > 16) {
    L = h(L, t.length * 8)
}
for (n = 0; n < 16; n += 1) {
    E[n] = L[n] ^ 909522486;
    j[n] = L[n] ^ 1549556828
}
F = h(E.concat(C(p)), 512 + p.length * 8);
return S(h(j.concat(F), 512 + 128))
}
function q(t) {
var p = "0123456789abcdef",
n = "",
L, E;
for (E = 0; E < t.length; E += 1) {
    L = t.charCodeAt(E);
    n += p.charAt(L >>> 4 & 15) + p.charAt(L & 15)
}
return n
}
function Q(t) {
return unescape(encodeURIComponent(t))
}
function M(t) {
return D(Q(t))
}
function R(t) {
return q(M(t))
}
function B(t, p) {
return z(Q(t), Q(p))
}
function U(t, p) {
return q(B(t, p))
}
function getPwd(t, p, n) {
if (!p) {
    if (!n) {
        return R(t)
    } else {
        return M(t)
    }
}
if (!n) {
    return U(p, t)
} else {
    return B(p, t)
}
}