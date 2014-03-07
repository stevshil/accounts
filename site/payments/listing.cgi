#!/usr/bin/perl

use lib "../include";
use personalise;
use CGI ':standard';
use DBI();

my $rowcount=0;
my $bgcolour="#f3f0f9";

print header();

print <<"__END__";
<html>
<head>
<title>$COMPANYNAME, Accounting System for Invoicing, Payment Options</title>
<link rel="stylesheet" href="../main.css" type="text/css">
<link rel="stylesheet" href="../style.css" type="text/css">
__END__

open (INCFILE, "<../include/payments.inc") || die "No such file";
my @INCFILE = <INCFILE>;
close INCFILE;
@INCFILE=doPersonalise(@INCFILE);
print "@INCFILE";

print <<"__END__";
        <td align=left valign=top><h1>Payments made</h1>
        <p>Click on the Invoice number column number to view payments.<br><br>
        <table width="100%" border=0 cellspacing=0 cellpadding=0>
        <tr><th align=left width=80>Invoice</th><th align=left width=300>Company Name</th><th align=left width=150>Invoice Date</th><th align=right width=200>Invoice Amount(&pound;)</th><th align=right width=200>Amount Paid</th></tr>
__END__

my $dbh = DBI->connect("DBI:mysql:database=accounts;host=localhost","$DBUSER","$DBPASS") || die "Unable to connect to database";

# Get Invoices to pay
my $sthInvoices=$dbh->prepare("SELECT Invoice.InvoiceNo, CompanyName, InvoiceDay, InvoiceMonth, InvoiceYear, sum(GrossAmtUKP*Quantity) As AmtDue From Invoice,InvoiceDetails,CustomerDetails WHERE Invoice.InvoiceNo=InvoiceDetails.InvoiceNo AND Invoice.CoID=CustomerDetails.CoID Group By InvoiceNo");
my $sthPayments=$dbh->prepare("SELECT InvoiceNo, sum(AmtPaidUKP) As AmtPaid From Payments Group By InvoiceNo");
$sthPayments->execute();
my %Payments = ();
while ( my $refPayments = $sthPayments->fetchrow_hashref() )
{
	$Payments{$refPayments->{InvoiceNo}}=$refPayments->{AmtPaid};
}
$sthPayments->finish();
undef $sthPayments;

$sthInvoices->execute();
while ( my $refInvoices = $sthInvoices->fetchrow_hashref() )
{
	my $flag=0;
	if ( exists $Payments{$refInvoices->{InvoiceNo}} )
	{
		$flag = 1 if ( $Payments{$refInvoices->{InvoiceNo}} gt "0.00" );
	}
	else
	{
		$flag = 0;
	}

	if ( $flag == 1 )
	{
		# show invoice
		my $rowcolour="bgcolor='$bgcolour'" if ( ($rowcount % 2) != 0 );
		$rowcount++;
		print "<tr $rowcolour><td align=left><a href='javascript:var win=window.open(\"ViewPayments.cgi?ID=$refInvoices->{InvoiceNo}\")'>$refInvoices->{InvoiceNo}</a></td><td align=left>$refInvoices->{CompanyName}</td><td align=left>$refInvoices->{InvoiceDay}/$refInvoices->{InvoiceMonth}/$refInvoices->{InvoiceYear}</td><td align=right>$refInvoices->{AmtDue}</td><td align=right>$Payments{$refInvoices->{InvoiceNo}}</td></tr>";
	}
}
$sthInvoices->finish();

$dbh->disconnect();
print "</table>";
print end_html();

