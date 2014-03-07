#!/usr/bin/perl

use lib "../include";
use personalise;
use CGI ':standard';
use DBI();

print header();
print <<"__END__";

<html>
<head>
<title>$COMPANYNAME, Accounting System for Invoicing, Create Invoice</title>
<link rel="stylesheet" href="../main.css" type="text/css">
<link rel="stylesheet" href="../style.css" type="text/css">
__END__

# include header file
open(INCFILE, "<../include/hidebtns.inc") || die "No such file";
my @INCFILE=<INCFILE>;
print "@INCFILE";
close INCFILE;

open (INCFILE, "<../include/invoicing.inc") || die "No such file";
my @INCFILE = <INCFILE>;
close INCFILE;
@INCFILE=doPersonalise(@INCFILE);
print "@INCFILE";

print <<"__END__";
	<td align=left valign=top><h1>Create New Invoice</h1>
	<form name=InvoiceAdd method=post action="addInvoice.cgi">
	<table>
	<tr><td>Company Name:</td><td><select name=coname>
__END__
my $dbh = DBI->connect("DBI:mysql:database=accounts;host=localhost","$DBUSER","$DBPASS") || die "Unable to connect to database";
my $sth = $dbh->prepare("SELECT CoID,CompanyName FROM CustomerDetails WHERE Deleted != 'Y' Order By CompanyName");
$sth->execute();
while ( my $refCoDet = $sth->fetchrow_hashref() )
{
	print "<option value='$refCoDet->{'CoID'}'>$refCoDet->{'CompanyName'}</option>\n";
}
$sth->finish();

# Invoice Date
print "</select></td></tr>";
print "<tr><td>Invoice Date</td><td><select name=InvoiceDay>";
for ( my $x = 1; $x <= 31; $x++ )
{
	if ( ((localtime())[3]) == $x )
	{
		print "<option value=$x selected>$x</option>\n";
	}
	else
	{
		print "<option value=$x>$x</option>\n";
	}
}
print "</select> &nbsp; <select name=InvoiceMonth>";
my %months=(1 => "January", 2 => "February", 3 => "March", 4 => "April", 5 => "May", 6 => "June", 7 => "July", 8 => "August", 9 => "September", 10 => "October", 11 => "November", 12 => "December");
for ( my $x = 1; $x <= 12; $x++ )
{
	if ( ((localtime())[4])+1 == $x )
	{
		print "<option value=$x selected>$months{$x}</option>\n";
	}
	else
	{
		print "<option value=$x>$months{$x}</option>\n";
	}
}
print "</select>";
print " &nbsp; <input type=text name=InvoiceYear value=",((localtime())[5])+1900," size=5></td></tr>";
print "<tr><td>Currency Type:</td><td><select name=CurrencyType>";
my $sth = $dbh->prepare("SELECT * FROM CurrencyType ORDER BY CurrencyName");
$sth->execute();
while ( my $refCur = $sth->fetchrow_hashref() )
{
	if ( $refCur->{'CurrencyType'} eq 'GBP' )
	{
		print "<option value=$refCur->{'CurrencyType'} selected>$refCur->{'CurrencyName'}</option>\n";
	}
	else
	{
		print "<option value=$refCur->{'CurrencyType'}>$refCur->{'CurrencyName'}</option>\n";
	}
}
print "</select></td></tr>\n";
$sth->finish();

print "<tr><td>Exchange Rate:</td><td><input type=text name=CurrencyRate size=5 value='1.00'></td></tr>\n";
print "<tr><td>Category:</td><td><select name=CategoryID>";
my $sth = $dbh->prepare("SELECT * FROM Category ORDER BY CatName");
$sth->execute();
while ( my $refCat = $sth->fetchrow_hashref() )
{
	print "<option value=$refCat->{'CategoryID'}>$refCat->{'CatName'}</option>\n";
}
$sth->finish();

print <<"__END__";
	<tr><td>&nbsp;</td></tr>
	<tr><td colspan=2 align=center><div id=hideme><input type=submit value='Add Detail' name='Add'> &nbsp; <input type=reset value='Clear Fields'></div></td></tr>
	</table>
	</td></tr>
</table>
</body>
</html>
__END__
$dbh->disconnect();
