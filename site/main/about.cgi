#!/usr/bin/perl

use lib "../include";
use personalise;
use CGI ':standard';
use CGI::Carp 'fatalsToBrowser';

print header();

print <<"__END__";
<html>
<head>
<title>$COMPANYNAME, Accounting System</title>
<link rel="stylesheet" href="../main.css" type="text/css">
<link rel="stylesheet" href="../style.css" type="text/css">
__END__

open (INCFILE, "<../include/about.inc") || die "No such file";
my @INCFILE = <INCFILE>;
close INCFILE;
@INCFILE=doPersonalise(@INCFILE);
print "@INCFILE";

print <<"__END__";
	<td align=left valign=top><h1>About this system</h1>
	This system was created by Steve Shilling in 2005 to enable easy of creation of Invoices in multiple currencies, and enable the system to add the UKP amount after the foreign invoice was created.  This allowed the foreign companies to be build like any other company and for us to generate the correct UKP amount for UK tax and accounting purposes.
<br><br>
The system is built around Apache web server, or IIS for Windows as long as Perl is installed and configured.  This provides the front end and allows the system to be used from anywhere.  The backend storage is MySQL.</td></tr>
</table>
</body>
</html>
__END__
