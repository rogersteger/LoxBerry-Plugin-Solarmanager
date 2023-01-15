#!/usr/bin/perl

use CGI;
use Config::Simple '-strict';
use LoxBerry::System;
use LoxBerry::Web;
use LoxBerry::Log;


#------------------------------------------------------------------------#
# Logging sytem 
#------------------------------------------------------------------------#
my $log = LoxBerry::Log->new (
        name => 'SolarManager4Lox',
        filename => "$lbplogdir/solarmanager.log",
        append => 1,
        addtime => 1
);

LOGSTART "Solarmanager Configuration Logger";

#------------------------------------------------------------------------#
# Variables
#------------------------------------------------------------------------#
my $cgi = CGI->new;
$cgi->import_names('R');
my $version = LoxBerry::System::pluginversion(); #Version of the script
$helplink = "http://www.loxwiki.eu/display/LOXBERRY/CalDAV-4-Lox"; #TODO
$helptemplate = "help.html";
$plugintitle="Solar Manager Plugin";

#------------------------------------------------------------------------#
# Create Header
#------------------------------------------------------------------------#
LOGDEB "create the header";
LoxBerry::Web::lbheader($plugintitle . " V$version",$helplink, $helptemplate);

#------------------------------------------------------------------------#
# Read Settings
#------------------------------------------------------------------------#
LOGDEB "Read system config";
my $cfg = new Config::Simple("$lbpconfigdir/pluginconfig.cfg"); # load configuration

#------------------------------------------------------------------------#
# Initialize template
#------------------------------------------------------------------------#
LOGDEB "create the content";

#initialize template
my $template = HTML::Template->new(
    filename => "$lbptemplatedir/index.html",
    global_vars => 1,
    loop_context_vars => 1,
    die_on_bad_params => 0,
    associate => $cfg,
);

my %L = LoxBerry::Web::readlanguage($template, "language.ini"); #read settings from language file


# Checkboxen, Select-Lists sind mit HTML::Template kompliziert. Einfacher ist es, mit CGI das HTML-Element bauen zu lassen und dann
# das fertige Element ins Template einzufügen. Für die Labels und Auswahlen lesen wir aus der Config $cfg und dem Sprachhash $L.
# Nicht mehr sicher, ob in der Config True, Yes, On, Enabled oder 1 steht? Die LoxBerry-Funktion is_enabled findet's heraus.
my $activated = $cgi->checkbox(-name => 'activated',
                               -checked => is_enabled($cfg{'MAIN.IS_ENABLED'}),
                               -value => 'True',
                               -label => $L{'BASIC.LABEL_ENABLED'},
                               );

# Den so erzeugten HTML-Code schreiben wir ins Template.
$template->param( ACTIVATED => $activated);

print "Use a variable from the config file: <i>" . $cfg->param('SOLARMANAGER_CONFIG.ID') . "</i><br>\n";
print "Use a variable from the config file: <i>" . $R::settingsSmId . "</i><br>\n";
print "Use a variable from the config file: <i>" . $cfg->param('MAIN.IS_ENABLED') . "</i><br>\n";

# Nun wird das Template ausgegeben.
print $template->output();

#------------------------------------------------------------------------#
# Write configuration files
#------------------------------------------------------------------------#
$cfg->param("SOLARMANAGER_CONFIG.ID", "$R::settingsSmId");
$cfg->save();

#------------------------------------------------------------------------#
# Footer
#------------------------------------------------------------------------#
LoxBerry::Web::lbfooter();
