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
<script language=JavaScript>
function addLine()
{
	hidebtn();
	document.InvoiceAdd.submit();
}

function MakeInvoice()
{
	hidebtn();
	document.InvoiceAdd.action="MakeInvoice.cgi";
	document.InvoiceAdd.submit();
}
</script>
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

my $company=param(coname);
my $dbh = DBI->connect("DBI:mysql:database=accounts;host=localhost","$DBUSER","$DBPASS") || die "Unable to connect to database";
my $sth = $dbh->prepare("SELECT CompanyName FROM CustomerDetails WHERE CoID=$company");
$sth->execute();
my $ref = $sth->fetchrow_hashref();

print <<"__END__";
	<td align=left valign=top colspan=3><h1>Create New Invoice for $ref->{'CompanyName'}</h1>
	<form name=InvoiceAdd method=post action="addInvoice.cgi">
__END__
$sth->finish();
my $count=param('counter');
my $items=0;
if ( ! defined(param('counter')) )
{
	$count=1;
}
else
{
	$count++;
}
print "<input type=hidden name=counter value=$count>";

# ask for contact
if ( $count == 1 )
{
	print "<br>Select contact: <select name=CustContactID>";
	$sth = $dbh->prepare("SELECT CustContactID,Name FROM CustomerContacts WHERE CoID=$company");
	$sth->execute();
	while ( my $ref = $sth->fetchrow_hashref() )
	{
		print "<option value=$ref->{CustContactID}>$ref->{Name}</option>\n";
	}
}
print "</select><br><br>";
$dbh->disconnect();

# Get current fields
my @params = param();
foreach $detail (@params)
{
	if ( $detail !~ /^detail/ && $detail !~ /^qty/ && $detail !~ /baseamt/ && $detail !~ /^Add$/ && $detail !~ /^counter/ && $detail !~ /^VAT/ )
	{
		print "<input type=hidden name=$detail value='",param($detail),"'>\n";
	}
	if ( $detail =~ /^detail/ )
	{
		$items++;
	}
}

print "<table>";
print "<tr><td colspan=3><h2>Invoice Detail</h2></td></tr>\n";
print "<tr><th align=center>Detail</th><th align=center>Qty</th><th align=center>Amount in Currency</th><th>VAT Rate</th><th>Tick if Amount inc. VAT</th></tr>\n";

# Check if we have existing items
if ( $items > 0 )
{
	for ( my $x=1; $x <= $items; $x++ )
	{
		my $detailline="detail$x";
		my $detailqty="qty$x";
		my $detailbaseamt="baseamt$x";
		my $detailVAT="VAT$x";
		print "<tr><td><textarea name=detail$x cols=30>",param($detailline),"</textarea></td><td><input type=text name=qty$x value='",param($detailqty),"' size=3></td><td><input type=text name=baseamt$x value='",param($detailbaseamt),"' size=10></td><td><select name=VAT$x>";
		$sth=$dbh->prepare("SELECT * FROM TAXRates ORDER BY TAXRate desc");
		$sth->execute();
		while ( my $refVAT = $sth->fetchrow_hashref() )
		{
			if ( param($detailVAT) eq $refVAT->{TAXID} )
			{
				print "<option value='$refVAT->{TAXID}' selected>$refVAT->{TAXName} - $refVAT->{TAXRate}%</option>";
			}
			else
			{
				print "<option value='$refVAT->{TAXID}'>$refVAT->{TAXName} - $refVAT->{TAXRate}%</option>";
			}
		}
		$sth->finish();
		print "</select></td></tr>\n";
	}
}
# print new line
print "<tr><td><textarea name=detail$count cols=30></textarea></td><td><input type=text name=qty$count size=3></td><td><input type=text name=baseamt$count size=10></td><td><select name=VAT$count>";
$sth=$dbh->prepare("SELECT * FROM TAXRates ORDER BY TAXRate desc");
$sth->execute();
while ( my $refVAT = $sth->fetchrow_hashref() )
{
	print "<option value='$refVAT->{'TAXID'}'>$refVAT->{'TAXName'} - $refVAT->{'TAXRate'}%</option>";
}
$sth->finish();
print "</select></td>\n";
print "<td><input type=checkbox name=incVAT$count></td></tr>\n";

# print button options
print "<tr><td colspan=3 align=center><div id=hideme><input type=button name=Add value='Add Detail' onClick='addLine()'> &nbsp; <input type=button name=Invoice value='Create Invoice' onClick='MakeInvoice()'></div></td></tr>\n";
print "</table>";
print "</form>";

$dbh->disconnect();
print end_html();
