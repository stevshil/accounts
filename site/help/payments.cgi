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
	<td align=left valign=top><h1>Help on Payments</h1>
<h2>Main Screen</h2>
<p>When entering the Payments screen you a provieded with a summary of the amount paid this month/year, as well as a list of late payments.  To view details of the invoice click on the invoice number, or to view the company details click on the company name.
<p>The menu consists of;
<table>
<tr><td>Late Payments</td><td>The same as the main screen.</td></tr>
<tr><td>Make Payments</td><td>To inform the system payment has been made</td></tr>
<tr><td>List Payments</td><td>To view all payments made in the system</td></tr>
</table>
<hr>
<h2>Make Payments</h2>
<p>In this screen you are provided with a list of invoices still requiring payments.<br>
Click on the invoice number to make a payment to that invoice.<br>
Invoice payments can be whole or part, and the system keeps track of how much is paid and owed.<br>
NOTE: Only UK Sterling amounts are shown.  If the amount is blank it means the invoice has not been completed or posted due to it waiting for the bank payment to be made.
<p>When you select the invoice number you will be presented with a screen which asks for;
<table>
<tr><td>Payment type</td><td>An option to select type of payment, for how it was received</td></tr>
<tr><td>Payment reference</td><td>If there is one from the remitence advice not, if not use the date of payment</td></tr>
<tr><td>Amount tendered</td><td>The amount paid against that invoice</td></tr>
</table>
<p>Click on the <b>Add Payment</b> button when you have completed the details and you will be presented with a summary of the amount paid.  Clicking on the <b>Back</b> button will return you to the payments list.<br><br>
If a part payment is made you will still see the invoice listed, with the invoice amount (total) and how much has been paid.

</table>
</body>
</html>
__END__
