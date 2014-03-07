#!/usr/bin/perl

use lib "../include";
use personalise;
use CGI ':standard';
use CGI::Carp 'fatalsToBrowser';
use DBI;

sub byPct
{
	my $pctA = $sortHash{$a}[6];
	my $pctB = $sortHash{$b}[6];

	return $pctA <=> $pctB
}

my $rowcount=0;
my $bgcolour="#f3f0f9";

print header();

print <<"__END__";
<html>
<head>
<title>$COMPANYNAME, Accounting System for Invoicing, Rating</title>
<link rel="stylesheet" href="../main.css" type="text/css">
<link rel="stylesheet" href="../style.css" type="text/css">
__END__

open (INCFILE, "<../include/reporting.inc") || die "No such file";
my @INCFILE = <INCFILE>;
close INCFILE;
@INCFILE=doPersonalise(@INCFILE);
print "@INCFILE";

my $dbh = DBI->connect("DBI:mysql:database=accounts:host=localhost","$DBUSER","$DBPASS") || die "Unable to connect to database";
my $sth=$dbh->prepare("SELECT DAYOFMONTH(curdate()) As Day, MONTHNAME(curdate()) As Month, YEAR(curdate()) As Year");
$sth->execute();
my $ref=$sth->fetchrow_hashref();
print <<"__END__";
	<td align=left valign=top><h1>Payment League</h1>
	<h3>Today: $ref->{Day} $ref->{Month} $ref->{Year}</h3>
__END__
$sth->finish();
undef $ref;

# Get all companies and number of invoices
$sth=$dbh->prepare("SELECT CustomerDetails.CompanyName, count(Invoice.CoID) As NumInvoices From Invoice,CustomerDetails Where Invoice.CoID=CustomerDetails.CoID AND Invoice.void is null group by Invoice.CoID") || die "Unable to connect to database";
$sth->execute();
my %refInvCount=();
my $ref;
while ( $ref=$sth->fetchrow_hashref() )
{
	$refInvCount{$ref->{CompanyName}}=$ref->{NumInvoices};
}
$sth->finish();
undef $ref;

# Get each invoice and their customer
# We need Customer Name, Invoice.InvoiceDay/Month/Year, PaymentTerms PaymentTerms(ID), Payments.PaymentDay/Month/Year
$sth=$dbh->prepare("SELECT CompanyName, Invoice.InvoiceNo, InvoiceDay, InvoiceMonth, InvoiceYear, PaymentDay, PaymentMonth, PaymentYear, Left(PaymentTerms,2) PaymentTermsDays, PaymentTerms, NetAmtUKP From CustomerDetails,Invoice,Payments,PaymentTerms, InvoiceDetails WHERE CustomerDetails.CoID=Invoice.CoID AND CustomerDetails.PaymentTermsID=PaymentTerms.PaymentTermsID AND Invoice.InvoiceNo=Payments.InvoiceNo AND Invoice.InvoiceNo=InvoiceDetails.InvoiceNo AND Invoice.void is null");
#Group By CompanyName");
$sth->execute();

# Print late payment details
print "<table border=0 cellpadding=0 cellspacing=0><tr><th align=left width=400>Company</th><th align=left width=150>Payment Terms</th><th align=right width=120># Inv.</th><th align=right width=120>Avg Days</th><th align=right width=120>Min Days</th><th align=right width=120>Max Days</th><th width=120 align=right>% Late</th><th align=right width=150>Total Income &pound;</th></tr>\n";

my %customerHash=();

while ( my $ref=$sth->fetchrow_hashref() )
{
	$pmnt="$ref->{PaymentYear}-$ref->{PaymentMonth}-$ref->{PaymentDay}";
	$invd="$ref->{InvoiceYear}-$ref->{InvoiceMonth}-$ref->{InvoiceDay}";

	$sth2=$dbh->prepare("SELECT DATEDIFF('$pmnt','$invd') MyDays");
	$sth2->execute();
	$refDays=$sth2->fetchrow_hashref();

	my $curDays=$refDays->{MyDays};
	$sth2->finish();

	my $mindays=$customerHash{"$ref->{CompanyName}"}[0];
	my $maxdays=$customerHash{"$ref->{CompanyName}"}[1];
	my $numLate=$customerHash{"$ref->{CompanyName}"}[2];
	my $numInvoices=$customerHash{$ref->{CompanyName}}[3];

	if ( $mindays eq "" )
	{
		$mindays = 30000;
	}
	if ( $maxdays eq "" )
	{
		$maxdays=0;
	}

	if ( $curDays < $mindays )
	{
		$mindays=$curDays;
	}
	if ( $curDays > $maxdays )
	{
		$maxdays=$curDays;
	}
	if ( $curDays > $ref->{PaymentTermsDays} )
	{
		$numLate++;
	}
	$numInvoices=$refInvCount{$ref->{CompanyName}};
	my $totaldays=$customerHash{$ref->{CompanyName}}[6]+$curDays;
	my $totalIncome=$customerHash{$ref->{CompanyName}}[7]+$ref->{NetAmtUKP};

	$customerHash{"$ref->{CompanyName}"}=[$mindays,$maxdays,$numLate,$numInvoices,$ref->{PaymentTerms},$ref->{PaymentTermsDays},$totaldays,$totalIncome];
}
$sth->finish();

foreach $key (keys %customerHash)
{
	my $AvgDays=$customerHash{$key}[6]/$customerHash{$key}[3];
	$AvgDays=~s/\..*//;
	my $pctLate=($customerHash{$key}[2]/$customerHash{$key}[3])*100;
	$pctLate=~s/\..*//;

	# First let's put everything into a hash so we can sort it
	$sortHash{$key}=[$key,$customerHash{$key}[4],$customerHash{$key}[3],$AvgDays,$customerHash{$key}[0],$customerHash{$key}[1],$pctLate,$customerHash{$key}[7]];
	#<tr $rowcolour><td align=left>$key</td><td align=left>$customerHash{$key}[4]</td><td align=right>$customerHash{$key}[3]</td><td align=right>$AvgDays</td><td align=right>$customerHash{$key}[0]</td><td align=right>$customerHash{$key}[1]</td><td align=right>$pctLate</td><td align=right>$customerHash{$key}[7]</td></tr>
}

foreach $key (sort byPct (keys %sortHash))
{
	my $rowcolour="bgcolor='$bgcolour'" if ( ($rowcount % 2) != 0 );
	print <<"__END__";
<tr $rowcolour><td align=left>$key</td><td align=left>$sortHash{$key}[1]</td><td align=right>$sortHash{$key}[2]</td><td align=right>$sortHash{$key}[3]</td><td align=right>$sortHash{$key}[4]</td><td align=right>$sortHash{$key}[5]</td><td align=right>$sortHash{$key}[6]</td><td align=right>$sortHash{$key}[7]</td></tr>
__END__
	$rowcount++;
}

$sth->finish();
undef $sth;
$dbh->disconnect();
undef $dbh;
print <<"__END__";
</table>
</body>
</html>
__END__
