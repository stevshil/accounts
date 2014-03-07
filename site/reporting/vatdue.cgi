#!/usr/bin/perl

use lib "../include";
use personalise;
use CGI ':standard';
use CGI::Carp 'fatalsToBrowser';
use DBI;

my $rowcount=0;
my $bgcolour="#f3f0f9";
my $DoWhat = param("DoWhat");

sub ShowVATForPeriod
{
	my ($inParam)=@_;

	if ( $inParam eq "RANGE" )
	{
		$startYear = param("start");
		$startMonth = substr($startYear,0,2);
		$startYear =~ s,^.*/,,;
		$endYear = param("end");
		$endMonth = substr($endYear,0,2);
		$endYear =~ s,^.*/,,;
		$sqlStartDate="$startYear/$startMonth/01";
		$sqlEndDate="$endYear/$endMonth/01";
	}
	else
	{
		my @curtime=localtime();
		$startYear=$curtime[5]+1900;
		$startMonth=$curtime[4]+1;
		$endYear=$curtime[5]+1900;
		$endMonth=$curtime[4]-2;
		$sqlStartDate="$startYear/$startMonth/01";
		$sqlEndDate="$endYear/$endMonth/01";
	}

	# Since months end with different numbers we increment the month
	# by 1 and then set the day to the 1st of the Month
	$fakeEndMonth=$endMonth+1;
	if ( $fakeEndMonth > 12 ) {
		$fakeEndMonth=1;
		$fakeEndYear=$endYear+1;
	} else {
		$fakeEndMonth=$endMonth+1;
		$fakeEndYear=$endYear;
	}
	$sqlEndDate="$fakeEndYear/$fakeEndMonth/01";

	print "<h3>Period: $startMonth/$startYear To $endMonth/$endYear</h3>";

	my $dbh = DBI->connect("DBI:mysql:database=accounts:host=localhost","$DBUSER","$DBPASS") || die "Unable to connect to database";
	my $sth=$dbh->prepare("SELECT InvoiceNo, sum(Quantity*NetAmtUKP) AS NET, sum(Quantity*GrossAmtUKP) AS GROSS, sum(Quantity*GrossAmtUKP)-sum(Quantity*NetAmtUKP) AS VAT FROM InvoiceDetails WHERE InvoiceNo in (SELECT distinct InvoiceNo FROM Payments WHERE date(concat(PaymentYear,'/',PaymentMonth,'/01')) >= date('$sqlStartDate') AND date(concat(PaymentYear,'/',PaymentMonth,'/01')) < date('$sqlEndDate')) GROUP BY InvoiceNo");
	$sth->execute();

	# Print Invoice details
	print "<table border=0 cellpadding=0 cellspacing=0><tr><th align=left width=400>Invoice #</th><th align=right width=150>Net Amount</th><th align=right width=150>Gross Amount</th><th align=right width=120>VAT</th></tr>\n";

	while (my $ref=$sth->fetchrow_hashref())
	{
		my $rowcolour="bgcolor='$bgcolour'" if ( ($rowcount % 2) != 0 );
		print "<tr $rowcolour><td align=left><a href='../payments/ViewPayments.cgi?ID=$ref->{InvoiceNo}&DoWhat=Display'>$ref->{InvoiceNo}</td><td align=right>$ref->{NET}</td><td align=right>$ref->{GROSS}</td><td align=right>$ref->{VAT}</td></tr>\n";
		$rowcount++;
	}
	$sth->finish();

	# Print totals
	my $sth=$dbh->prepare("SELECT InvoiceNo, sum(Quantity*NetAmtUKP) AS NET, sum(Quantity*GrossAmtUKP) AS GROSS, sum(Quantity*GrossAmtUKP)-sum(Quantity*NetAmtUKP) AS VAT FROM InvoiceDetails WHERE InvoiceNo in (SELECT distinct InvoiceNo FROM Payments WHERE date(concat(PaymentYear,'/',PaymentMonth,'/01')) >= date('$sqlStartDate') AND date(concat(PaymentYear,'/',PaymentMonth,'/01')) < date('$sqlEndDate'))");
	$sth->execute();
	while (my $ref=$sth->fetchrow_hashref())
	{
		my $rowcolour="bgcolor='$bgcolour'" if ( ($rowcount % 2) != 0 );
		print "<tr $rowcolour><th align=left>TOTALS</th><th align=right>$ref->{NET}</th><th align=right>$ref->{GROSS}</th><th align=right>$ref->{VAT}</th></tr>\n";
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
<form name=SelectDates action="vatdue.cgi" method=post>
<input type=hidden name=DoWhat value=Select>
<tr><td>Start Month/Year (mm/yyyy):</td><td><input type=text name=start></td></tr>
<tr><td>End Month/Year (mm/yyyy):</td><td><input type=text name=end></td></tr>
<tr><td colspan=2>Tick box to view entire income <input type=checkbox name=All></td><tr>
<tr><td colspan=2><input type=submit value="View"></td></tr>
</table>
_END_
}

print header();

print <<"__END__";
<html>
<head>
<title>$COMPANYNAME, Accounting System for Invoicing, VAT Due Report</title>
<link rel="stylesheet" href="../main.css" type="text/css">
<link rel="stylesheet" href="../style.css" type="text/css">
__END__

open (INCFILE, "<../include/reporting.inc") || die "No such file";
my @INCFILE = <INCFILE>;
close INCFILE;
@INCFILE=doPersonalise(@INCFILE);
print "@INCFILE";

print <<"__END__";
	<td align=left valign=top><h1>VAT Due Report</h1>
__END__

if ( $DoWhat =~ /Select/ )
{
	$chkbox=param("All");
	if ( $chkbox eq "on" )
	{
		ShowVATForPeriod("ALL");
	}
	else
	{
		ShowVATForPeriod("RANGE");
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
