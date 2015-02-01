var fs = require('fs');
var request = require('request');
var cheerio = require('cheerio');
//var stringify = require('stringify-object');
var sprintf = require('sprintf-js').sprintf
var url = 'http://www.windalert.co.il';
var sites = [];
request.post(
    'http://www.windalert.co.il/Spot/SpotTable',
    { form: { var1: '0', var2:'' } },
    function (error, response, html) {
        if (!error && response.statusCode == 200) {
            var obj = JSON.parse(html);
            html = obj.html;
            var $ = cheerio.load(html);
            $('.line').find('.link').each(function(i){
              var cur_site = {};
              cur_site.name = $(this).text();
              $(this).parent().parent().find('.speedGust').each(function(i){
                  cur_site.wind = $(this).children().first().text();
                  $(this).siblings('.time').each(function(i){
                    cur_site.time = $(this).text().trim();
                  });
                  $(this).siblings('.direction').each(function(i){
                    cur_site.direction = $(this).children().last().text();
                  });
              });
              sites[i]=cur_site;
            });
        }
    var i;
    var poi = {};
    var bat_yam = "בת ים, לגונה"
    poi[bat_yam] = 1;
        for (i=0; i < sites.length; ++i) {
            var cur = sites[i];
            //if (poi[cur.name] == 1 && cur.wind > 12 && cur.time != "N/A" )  {
           if (cur.time != Object.undefined ) {
               if (cur.time == "לא זמין")
                    cur.time = 'N/A'
              console.log(sprintf("%s:\t%s\t\t%s\t%s <br>", cur.time, cur.name, cur.wind, cur.direction));
           }
//              console.log(cur.time + ": " + cur.name + " " + cur.wind);
            //}
        }
    }
);
