#!/usr/bin/perl

use lib "../include";
use personalise;
use CGI ':standard';
use CGI::Carp 'fatalsToBrowser';
use DBI;

my $rowcount=0;
my $bgcolour="#f3f0f9";
my $DoWhat = param("DoWhat");

sub ShowIncomeForPeriod
{
	my ($inParam)=@_;

	if ( $inParam eq "RANGE" )
	{
		$startYear = param("start");
		$endYear = param("end");
	}
	else
	{
		$startYear=2000;
		my @curtime=localtime();
		$endYear=$curtime[5]+1900;
	}

	print "<h3>Period: $startYear To $endYear</h3>";

	my $dbh = DBI->connect("DBI:mysql:database=accounts:host=localhost","$DBUSER","$DBPASS") || die "Unable to connect to database";
	my $sth=$dbh->prepare("SELECT count(CompanyName) As NumInv, sum(AmtPaidUKP) As TotIncome, min(AmtPaidUKP) As MinIncome, max(AmtPaidUKP) As MaxIncome, CompanyName FROM Payments,Invoice,CustomerDetails WHERE Payments.InvoiceNo=Invoice.InvoiceNo AND Invoice.CoID=CustomerDetails.CoID AND PaymentYear BETWEEN $startYear AND $endYear Group By CompanyName Order By 2 desc");
	$sth->execute();

	# Print late payment details
	print "<table border=0 cellpadding=0 cellspacing=0><tr><th align=left width=400>Company</th><th align=right width=150>Min Payment</th><th align=right width=150>Max Payment</th><th align=right width=120>Total Income</th><th align=right width=120>No. Invoices</th></tr>\n";

	while (my $ref=$sth->fetchrow_hashref())
	{
		my $rowcolour="bgcolor='$bgcolour'" if ( ($rowcount % 2) != 0 );
		print "<tr $rowcolour><td align=left>$ref->{CompanyName}</td><td align=right>$ref->{MinIncome}</td><td align=right>$ref->{MaxIncome}</td><td align=right>$ref->{TotIncome}</td><td align=right>$ref->{NumInv}</td></tr>\n";
		$rowcount++;
	}
	$sth->finish();

	# Print total totals
	my $sth=$dbh->prepare("SELECT count(CompanyName) As NumInv, sum(AmtPaidUKP) As TotIncome, min(AmtPaidUKP) As MinIncome, max(AmtPaidUKP) As MaxIncome, CompanyName FROM Payments,Invoice,CustomerDetails WHERE Payments.InvoiceNo=Invoice.InvoiceNo AND Invoice.CoID=CustomerDetails.CoID AND PaymentYear BETWEEN $startYear AND $endYear");
	$sth->execute();
	while (my $ref=$sth->fetchrow_hashref())
	{
		my $rowcolour="bgcolor='$bgcolour'" if ( ($rowcount % 2) != 0 );
		print "<tr $rowcolour><th align=left>TOTALS</th><th align=right>$ref->{MinIncome}</th><th align=right>$ref->{MaxIncome}</th><th align=right>$ref->{TotIncome}</th><th align=right>$ref->{NumInv}</th></tr>\n";
	}
	
	print "</table>";

	$sth->finish();
	undef $sth;
	$dbh->disconnect();
	undef $dbh;
}

sub DrawSelection
{
	print <<"_END_";
<table>
<form name=SelectDates action="income.cgi" method=post>
<input type=hidden name=DoWhat value=Select>
<tr><td>Start Year (yyyy):</td><td><input type=text name=start></td></tr>
<tr><td>End Year (yyyy):</td><td><input type=text name=end></td></tr>
<tr><td colspan=2>Tick box to view entire income <input type=checkbox name=All></td><tr>
<tr><td colspan=2><input type=submit value="View"></td></tr>
</table>
_END_
}

print header();

print <<"__END__";
<html>
<head>
<title>$COMPANYNAME, Accounting System for Invoicing, Income Report</title>
<link rel="stylesheet" href="../main.css" type="text/css">
<link rel="stylesheet" href="../style.css" type="text/css">
__END__

open (INCFILE, "<../include/reporting.inc") || die "No such file";
my @INCFILE = <INCFILE>;
close INCFILE;
@INCFILE=doPersonalise(@INCFILE);
print "@INCFILE";

print <<"__END__";
	<td align=left valign=top><h1>Income Report</h1>
__END__

if ( $DoWhat =~ /Select/ )
{
	$chkbox=param("All");
	if ( $chkbox eq "on" )
	{
		ShowIncomeForPeriod("ALL");
	}
	else
	{
		ShowIncomeForPeriod("RANGE");
	}
}
else
{
	DrawSelection;
}

print <<"__END__";
</table>
</body>
</html>
__END__
