#!/usr/bin/perl

use lib "../include";
use personalise;
use CGI ':standard';
use DBI();

my $rowcount=0;
my $bgcolour="#f3f0f9";

my ($sMonth,$sYear,$eMonth,$eYear)=(param('sMonth'),param('sYear'),param('eMonth'),param('eYear'));

print header();

print <<"__END__";
<html>
<head>
<title>$COMPANYNAME, Accounting System for Invoicing, Invoicing Options</title>
<link rel="stylesheet" href="../main.css" type="text/css">
<link rel="stylesheet" href="../style.css" type="text/css">
<script language='javascript'>
function filterit(sMonth,sYear,eMonth,eYear)
{
	location.href='list.cgi?sMonth='+sMonth+'&sYear='+sYear+'&eMonth='+eMonth+'&eYear='+eYear;
}
</script>
__END__

open (INCFILE, "<../include/invoicing.inc") || die "No such file";
my @INCFILE = <INCFILE>;
close INCFILE;
@INCFILE=doPersonalise(@INCFILE);
print "@INCFILE";

print <<"__END__";
	<td align=left valign=top><h1>$COMPANYNAME Invoices </h1>
	<p>Click on the ID column number to view/edit invoice details.<br>
	To filter the invoices select a date range to start from, leave to blank to go to end<br>
__END__

print "<form name=filter>";
print "<table><tr><td>&nbsp;</td><td>Month</td><td>Year</td><td>&nbsp;</td><td>Month</td><td>Year</td></tr><tr><td>Start:</td><td><select name='sMonth'>";
print "<option value=0>0</option>";
for my $counter (1..12)
{
	print "<option value=$counter>$counter</option>";
}
print "</select></td><td><select name='sYear'>";
my $tmpdbh = DBI->connect("DBI:mysql:database=accounts;host=localhost","$DBUSER","$DBPASS") || die "Unable to connect to database";
my $tmpsth = $tmpdbh->prepare("SELECT min(InvoiceYear) as MinYear From Invoice WHERE InvoiceYear != 0");
$tmpsth->execute();
my $lowYear=$tmpsth->fetchrow_hashref();
$tmpsth->finish();
$tmpdbh->disconnect();
undef $tmpsth;
undef $tmpdbh;
my $maxYear=(((localtime())[5])+1900);
for my $counter ( $lowYear->{'MinYear'} .. $maxYear )
{
	print "<option value=$counter>$counter</option>";
}
print "</select></td>";
print "<td>End:</td><td><select name='eMonth'>";
print "<option value=0>0</option>";
for my $counter (1..12)
{
	print "<option value=$counter>$counter</option>";
}
print "</select></td><td><select name='eYear'>";
for my $counter ( $lowYear->{'MinYear'} .. $maxYear )
{
	print "<option value=$counter>$counter</option>";
}
print "</select></td><td><input type=button name=filterbtn value=Filter onClick='filterit(document.filter.sMonth.value,document.filter.sYear.value,document.filter.eMonth.value,document.filter.eYear.value)'></table></form>";

print <<"__END__";
	<br><br>
	<table width="100%" border=0 cellspacing=0 cellpadding=0>
	<tr><th align=left width=25>ID</th><th align=left width=250>Company Name</th><th align=left width=150>Invoice Date</th><th align=right width=200>Amount (&pound;)</th><th align=right width=200>Alternate Currency</th><th align=right width=100>Printed</th><th align=right width=150>Posted</th></tr>
__END__

my $dbh = DBI->connect("DBI:mysql:database=accounts;host=localhost","$DBUSER","$DBPASS") || die "Unable to connect to database";
my $sth;

if ( $sMonth > 0 )
{
	if ( $eMonth == 0 )
	{
		$sth = $dbh->prepare("SELECT InvoiceNo, Invoice.CoID, CompanyName, InvoiceDay, InvoiceMonth, InvoiceYear, PrintedDay, PrintedMonth, PrintedYear, Posted FROM Invoice,CustomerDetails WHERE Invoice.CoID=CustomerDetails.CoID AND Invoice.void is null AND datediff(concat(InvoiceYear,'-',InvoiceMonth,'-',1),'$sYear-$sMonth-1') > 0");
	}
	elsif ( $eYear >= $sYear )
	{
		$sth = $dbh->prepare("SELECT InvoiceNo, Invoice.CoID, CompanyName, InvoiceDay, InvoiceMonth, InvoiceYear, PrintedDay, PrintedMonth, PrintedYear, Posted FROM Invoice,CustomerDetails WHERE Invoice.CoID=CustomerDetails.CoID AND Invoice.void is null AND datediff(concat(InvoiceYear,'-',InvoiceMonth,'-',1),'$sYear-$sMonth-1') > 0 datediff(concat(InvoiceYear,'-',InvoiceMonth,'-',1),'$eYear-$eMonth-1') > 0");
	}
	else
	{
		$sth = $dbh->prepare("SELECT InvoiceNo, Invoice.CoID, CompanyName, InvoiceDay, InvoiceMonth, InvoiceYear, PrintedDay, PrintedMonth, PrintedYear, Posted FROM Invoice,CustomerDetails WHERE Invoice.CoID=CustomerDetails.CoID AND Invoice.void is null");
	}
}
else
{
	$sth = $dbh->prepare("SELECT InvoiceNo, Invoice.CoID, CompanyName, InvoiceDay, InvoiceMonth, InvoiceYear, PrintedDay, PrintedMonth, PrintedYear, Posted FROM Invoice,CustomerDetails WHERE Invoice.CoID=CustomerDetails.CoID AND Invoice.void is null");
}
$sth->execute();


while ( my $ref = $sth->fetchrow_hashref() )
{
	
	my $rowcolour="bgcolor='$bgcolour'" if ( ($rowcount % 2) != 0 );
	$rowcount++;
	print "<tr $rowcolour><td><a href='InvDetails.cgi?id=$ref->{'InvoiceNo'}&DoWhat=Display'>$ref->{'InvoiceNo'}</a></td>";
	print "<td>$ref->{'CompanyName'}</td><td>$ref->{'InvoiceDay'}/$ref->{'InvoiceMonth'}/$ref->{'InvoiceYear'}&nbsp;</td>";
	
	my $sthAmount = $dbh->prepare("SELECT sum(GrossAmtUKP*Quantity) As Amount FROM InvoiceDetails WHERE InvoiceNo = $ref->{'InvoiceNo'}");
	$sthAmount->execute();
	my $refAmount = $sthAmount->fetchrow_hashref();
	print "<td align=right>$refAmount->{'Amount'}&nbsp;</td>";
	undef $sthAmount;
	undef $refAmount;

	my $sthAmount = $dbh->prepare("SELECT sum(AltGrossAmt*Quantity) As Amount FROM InvoiceDetails WHERE InvoiceNo = $ref->{'InvoiceNo'}");
	$sthAmount->execute();
	my $refAmount = $sthAmount->fetchrow_hashref();
	print "<td align=right>$refAmount->{'Amount'}&nbsp;</td>";
	undef $sthAmount;
	undef $refAmount;

	if ( $ref->{'PrintedYear'} > 0 )
	{
		print "<td align=right>$ref->{'PrintedDay'}/$ref->{'PrintedMonth'}/$ref->{'PrintedYear'}&nbsp;</td>";
	}
	else
	{
		print "<td align=right>N&nbsp;</td>";
	}
	print "<td align=right>$ref->{'Posted'}&nbsp;</td>";
	$rowcolour=undef;
}
$sth->finish();
$dbh->disconnect();

print <<"__END__";
	</table>
	</td></tr>
</table>
</body>
</html>
__END__
