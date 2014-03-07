#!/usr/bin/perl

use lib "../include";
use personalise;
use CGI ':standard';
use CGI::Carp 'fatalsToBrowser';
use DBI();

my $rowcount=0;
my $bgcolour="#f3f0f9";

print header();

print <<"__END__";
<html>
<head>
<title>$COMPANYNAME, Accounting System for Invoicing, Company Options</title>
<link rel="stylesheet" href="../main.css" type="text/css">
<link rel="stylesheet" href="../style.css" type="text/css">
__END__

open (INCFILE, "<../include/invoicing.inc") || die "No such file";
my @INCFILE = <INCFILE>;
close INCFILE;
@INCFILE=doPersonalise(@INCFILE);
print "@INCFILE";

my $dbh = DBI->connect("DBI:mysql:database=accounts:host=localhost","$DBUSER","$DBPASS") || die "Unable to connect to database";
my $sth = $dbh->prepare("SELECT InvoiceNo From Payments");
$sth->execute();
my %invNosPaid=();
while ( my $ref = $sth->fetchrow_hashref() )
{
	$invNosPaid{"$ref->{InvoiceNo}"}=1;
}
$sth->finish();
$sth = $dbh->prepare("SELECT InvoiceNo From Invoice");
$sth->execute();
$topay=0;
while ( my $ref = $sth->fetchrow_hashref() )
{
	next if ( $ref->{InvoiceNo} == 101001 );

	if (! exists $invNosPaid{"$ref->{InvoiceNo}"} )
	{
		$topay++;
	}
}
$sth->finish();

print <<"__END__";
	<td align=left valign=top><h1>Invoicing</h1>
	Please select your choice from the side menu.<br>Or chose an Invoice number to view<br><br><h3>Number of unpaid invoices: $topay<br><hr>
__END__

# Display Unpaid Invoices;
print "<table border=0 cellspacing=0 cellpadding=0><tr><th align=left width=100>Invoice No</th><th align=left width=400>Company</th><th align=left width=150>Date</th><th align=right>Currency</th><th align=right width=150>Gross Currency</th></tr>";

$sth = $dbh->prepare("SELECT Invoice.InvoiceNo, CompanyName, InvoiceDay, InvoiceMonth, InvoiceYear, CurrencyType, sum(Quantity*AltGrossAmt) As Total FROM Invoice,CustomerDetails,InvoiceDetails WHERE Invoice.InvoiceNo = InvoiceDetails.InvoiceNo AND Invoice.CoID=CustomerDetails.CoID AND Invoice.void is null Group By Invoice.InvoiceNo");
$sth->execute();
while ( my $ref = $sth->fetchrow_hashref() )
{
	if (! exists $invNosPaid{"$ref->{InvoiceNo}"} )
	{
		my $rowcolour="bgcolor='$bgcolour'" if ( ($rowcount % 2) != 0 );

		print "<tr $rowcolour><td align=left><a href='../invoicing/InvDetails.cgi?id=$ref->{InvoiceNo}&DoWhat=Display'>$ref->{InvoiceNo}</a></td><td align=left>$ref->{CompanyName}</td><td align=left>$ref->{InvoiceDay}/$ref->{InvoiceMonth}/$ref->{InvoiceYear}</td><td align=right>$ref->{CurrencyType}</td><td align=right>$ref->{Total}</td></tr>";
		$rowcount++;
	}
}
print "</table></td></tr>";
$sth->finish();
$dbh->disconnect();

print <<"__END__";
</table>
</body>
</html>
__END__
