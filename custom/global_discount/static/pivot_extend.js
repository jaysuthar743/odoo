odoo.define( function (require)
{
    'use strict';
//    alert("hello");
    var core = require('web.core');
    var ajax = require('web.ajax');
    var qweb = core.qweb;
    var temp  = ajax.loadXML("/global_discount/static/my_pivot_view.xml", qweb);
    console.log("-------->", temp);

});