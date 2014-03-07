#!/usr/bin/perl

use lib "../include";
use personalise;
use CGI ':standard';
use CGI::Carp 'fatalsToBrowser';
use DBI;

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

open (INCFILE, "<../include/payments.inc") || die "No such file";
my @INCFILE = <INCFILE>;
close INCFILE;
@INCFILE=doPersonalise(@INCFILE);
print "@INCFILE";

my $dbh = DBI->connect("DBI:mysql:database=accounts:host=localhost","$DBUSER","$DBPASS") || die "Unable to connect to database";
my $sth = $dbh->prepare("SELECT round(sum(AmtPaidUKP),2) As AmtPAID FROM Payments Where PaymentMonth = MONTH(CURDATE()) AND PaymentYear = YEAR(CURDATE())");
$sth->execute();
my $ref=$sth->fetchrow_hashref();
my $monthPaid = $ref->{AmtPAID};
$sth->finish();
my $sth = $dbh->prepare("SELECT round(sum(AmtPaidUKP),2) As AmtPAID FROM Payments Where PaymentYear = YEAR(CURDATE())");
$sth->execute();
$ref=$sth->fetchrow_hashref();
my $yearPaid = $ref->{AmtPAID};
$sth->finish();
undef $ref;

$monthPaid = "0.00" if ("$monthPaid" eq "");
$yearPaid = "0.00" if ("$yearPaid" eq "");

print <<"__END__";
	<td align=left valign=top><h1>Record or View Payments</h1>
	Please select your choice from the side menu.<br><br>
	<table><tr><td align=left><h3>Amount paid this month:</h3></td><td><h3>$monthPaid</h3></td><tr><td><h3>Amount paid this year:</h3></td><td><h3>$yearPaid</h3></td></td></tr></table>
<br><br><h2>Late payments</h2><br><br>
__END__

# Get all invoices
$sth=$dbh->prepare("SELECT InvoiceNo,InvoiceDay,InvoiceMonth,InvoiceYear FROM Invoice WHERE Invoice.void is null");
$sth->execute();
my %refAllInvoices=();
while ($ref=$sth->fetchrow_hashref())
{
	$ref->{InvoiceMonth} = "0$ref->{InvoiceMonth}" if ( length($ref->{InvoiceMonth}) == 1);
	$ref->{InvoiceDay} = "0$ref->{InvoiceDay}" if ( length($ref->{InvoiceDay}) == 1);
	$refAllInvoices{$ref->{InvoiceNo}}="$ref->{InvoiceYear}$ref->{InvoiceMonth}$ref->{InvoiceDay}"
}
$sth->finish();
undef $ref;
# Get all payments
$sth=$dbh->prepare("SELECT InvoiceNo FROM Payments");
$sth->execute();
my %refAllPayments=();
while ($ref=$sth->fetchrow_hashref())
{
	$refAllPayments{$ref->{InvoiceNo}}=1;
}
$sth->finish();
undef $ref;

# Print late payment details
print "<table border=0 cellpadding=0 cellspacing=0><tr><th align=left width=120>Invoice No</th><th align=left width=400>Company</th><th align=left width=150>Date</th><th align=right>Currency</th><th align=right width=150>Net Currency</th><th align=right width=150>Gross Currency</th></tr>\n";
my @orderedInvoices=(keys %refAllInvoices);
@orderedInvoices=sort {$a <=> $b} @orderedInvoices;
#while ( my ($key,$value) = (each %refAllInvoices) )
foreach $key (@orderedInvoices)
{
	my $flag=0;
	# Check if paid
	foreach $payment (keys(%refAllPayments))
	{
		# Invoice already paid
		$flag=1 if ( $payment == $key );
	}

	if ($flag == 0)
	{
		next if ($key == 101001);
		# print detail
		$sth=$dbh->prepare("SELECT Invoice.InvoiceNo,InvoiceDay,InvoiceMonth,InvoiceYear,Invoice.CoID,CustomerDetails.CompanyName,CustomerDetails.PaymentTermsID,sum(AlternateCurrency*Quantity) As AltCurrency,CurrencyType,sum(AltGrossAmt*Quantity) As AltGrossAmt FROM Invoice,InvoiceDetails,CustomerDetails WHERE Invoice.InvoiceNo=InvoiceDetails.InvoiceNo AND Invoice.CoID=CustomerDetails.CoID AND Invoice.InvoiceNo = $key Group By Invoice.InvoiceNo");
		$sth->execute();
		my $ref = $sth->fetchrow_hashref();

		# Check if overdue
		my $sthChk=$dbh->prepare("SELECT PaymentTerms FROM PaymentTerms WHERE PaymentTermsID = $ref->{PaymentTermsID}");
		$sthChk->execute();
		my $refChk = $sthChk->fetchrow_hashref();
		my $daysAllowed = (split (/ /,$refChk->{PaymentTerms}))[0];
		$sthChk->finish();
		undef $refChk;

		$sthChk=$dbh->prepare("SELECT DATE_FORMAT(DATE_SUB(CURDATE(),INTERVAL $daysAllowed DAY),'%Y%m%d') As DateMinus");
		$sthChk->execute();
		$refChk = $sthChk->fetchrow_hashref();
		my $dueByDate = "$refChk->{DateMinus}";

		#print "$dueByDate - $daysAllowed<br>";
		#print "$refAllInvoices{$key}<br>";
		next if ( $dueByDate < $refAllInvoices{$key} );
		undef $refChk;
		$sthChk->finish();

		my $rowcolour="bgcolor='$bgcolour'" if ( ($rowcount % 2) != 0 );
		print <<"__END__";
		<tr $rowcolour><td align=left><a href='../invoicing/InvDetails.cgi?id=$ref->{InvoiceNo}'>$ref->{InvoiceNo}</a></td><td align=left><a href='../companies/CoDetails.cgi?id=$ref->{CoID}'>$ref->{CompanyName}</a></td><td align=left>$ref->{InvoiceDay}/$ref->{InvoiceMonth}/$ref->{InvoiceYear}</td><td align=center>$ref->{CurrencyType}</td><td align=right>$ref->{AltCurrency}</td><td align=right>$ref->{AltGrossAmt}</td></tr>
__END__
		$sth->finish();
	}
	$rowcount++;
}

undef $sth;
$dbh->disconnect();
undef $dbh;
print <<"__END__";
</table>
</body>
</html>
__END__
