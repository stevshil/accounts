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

open (INCFILE, "<../include/help.inc") || die "No such file";
my @INCFILE = <INCFILE>;
close INCFILE;
@INCFILE=doPersonalise(@INCFILE);
print "@INCFILE";

print <<"__END__";
	<td align=left valign=top><h1>Help on Managing companies</h1>
<h2>The main page</h2>
<p>Nothing is displayed on the main page, apart from telling you to make a choice from the menu.<br>
The options you have are;
<table>
<tr><td>Home</td><td>Return to the main options</td></tr>
<tr><td>List / Edit</td><td>To view the companies or edit company details, such as address or contacts for the company</td></tr>
<tr><td>Add</td><td>To add a new company to the system</td></tr>
<tr><td>Delete</td><td>To remove a company from the system</td></tr>
</table>
<h2>List / Edit</h2>
<p>From this screen you will have a choice of;
<ul><li>Editing the company details for the head office (where the invoices should go) by clicking on the ID number column
<li>Adding/Editing or viewing contacts in the company, to whom you would normally send invoices to, but can be used as a contacts database.<br>This is done by clicking on the <b>Add/Edit/View Contacts</b> at the far end of each company.
</ul>
<p>The screens for adding or editing are fairly self explanitory.  However, after adding a company you should always return to the company list to add a contact to it.
<h2>Delete</h2>
<p>In this screen you will be provided with a list of the companies currently in the system.  If you click on the ID that company will be removed from the system.  When we say removed they are hidden from view, not permanently deleted, so you must ask your system administrator to get them put back in.
</table>
</body>
</html>
__END__
