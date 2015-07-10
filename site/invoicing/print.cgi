#!/usr/bin/perl

use lib "../include";
use personalise;
use CGI ':standard';
use DBI();

my $rowcount=0;
my $bgcolour="#f3f0f9";

my $DoWhat=param("DoWhat");
my $InvoiceNo = param("id");

my $numMonths=param("numMonths");

print header();

print <<"__END__";
<html>
<head>
<title>$COMPANYNAME, Accounting System for Invoicing, Printing</title>
<link rel="stylesheet" href="../main.css" type="text/css">
<link rel="stylesheet" href="../style.css" type="text/css">
<script language='javascript'>
function filterme() {
	location.href='print.cgi?numMonths='+document.list.numMonths.value;
}
</script>
__END__

sub ListInvoices
{
	open (INCFILE, "<../include/invoicing.inc") || die "No such file";
	my @INCFILE = <INCFILE>;
	close INCFILE;
	@INCFILE=doPersonalise(@INCFILE);
	print "@INCFILE";

	print <<"__END__";
	<td align=left valign=top><h1>Print Invoices </h1>
	<p>Click on the ID column number to view an Invoice.<br>Tick the box next to the Invoice if you wish to print it.<br>Click <b>reprint</b> to print a posted invoice.<br><br>
	<form name=list action=print.cgi method=get>
	<p>How many months back to show (-1 = All, or type number): <input type=text name=numMonths size=5><input type=button onClick='filterme()' value='Filter'></p>
	</form>
	<form name=print action=print.cgi method=post>
	<input type=hidden name=DoWhat value=Print>
	<table width="100%" border=0 cellspacing=0 cellpadding=0>
	<tr><th align=left width=80>Print?</th><th align=left width=35>ID</th><th align=left width=350>Company Name</th><th align=left width=150>Invoice Date</th><th align=right width=180>Amount (&pound;)</th><th align=right width=250>Alternate Currency</th><th align=right width=100>Printed</th><th align=right width=80>Posted</th></tr>
__END__

	my $dbh = DBI->connect("DBI:mysql:database=accounts;host=localhost","$DBUSER","$DBPASS") || die "Unable to connect to database";

my $sth;
if ( $numMonths == 0 ) {
	$sth = $dbh->prepare("SELECT InvoiceNo, Invoice.CoID, CompanyName, InvoiceDay, InvoiceMonth, InvoiceYear, PrintedDay, PrintedMonth, PrintedYear, Posted FROM Invoice,CustomerDetails WHERE Invoice.CoID=CustomerDetails.CoID AND Invoice.void is null AND date(concat(PrintedYear,'-',PrintedMonth,'-',DAY(NOW()))) > date_sub(NOW(),INTERVAL 3 MONTH)");
} elsif ( $numMonths == -1 ) {
	$sth = $dbh->prepare("SELECT InvoiceNo, Invoice.CoID, CompanyName, InvoiceDay, InvoiceMonth, InvoiceYear, PrintedDay, PrintedMonth, PrintedYear, Posted FROM Invoice,CustomerDetails WHERE Invoice.CoID=CustomerDetails.CoID AND Invoice.void is null");
} else {
	$sth = $dbh->prepare("SELECT InvoiceNo, Invoice.CoID, CompanyName, InvoiceDay, InvoiceMonth, InvoiceYear, PrintedDay, PrintedMonth, PrintedYear, Posted FROM Invoice,CustomerDetails WHERE Invoice.CoID=CustomerDetails.CoID AND Invoice.void is null AND date(concat(PrintedYear,'-',PrintedMonth,'-',DAY(NOW()))) > date_sub(NOW(),INTERVAL $numMonths MONTH)");
}
	$sth->execute();


	while ( my $ref = $sth->fetchrow_hashref() )
	{
	
		my $rowcolour="bgcolor='$bgcolour'" if ( ($rowcount % 2) != 0 );
		$rowcount++;
		print "<tr $rowcolour>";
		if ( "$ref->{'Posted'}" ne "Y" )
		{
			print "<td><input type=checkbox name=Print value=$ref->{'InvoiceNo'}></td>";
		}
		else
		{
			print "<td><a href='javascript: var win=window.open(\"reprint.cgi?ID=$ref->{InvoiceNo}\")'>Reprint</a></td>";
		}
		print "<td><a href='InvDetails.cgi?id=$ref->{'InvoiceNo'}&DoWhat=Display'>$ref->{'InvoiceNo'}</a></td>";
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
		print "<td align=right>$ref->{'Posted'}&nbsp;</td></tr>\n";
		$rowcolour=undef;
	}
	$sth->finish();
	$dbh->disconnect();
	print "<tr><td colspan=8><hr></td></tr>";
	print "<tr><td colspan=8 align=left><input type=submit name=printit value='Print Invoices'></td></tr></form>";
}

sub PrintInvoice
{
	my @Invoices = param("Print");

	my $dbh = DBI->connect("DBI:mysql:database=accounts;host=localhost","$DBUSER","$DBPASS") || die "Unable to connect to database";

	foreach $Invoice (@Invoices)
	{
		my $updateStr = "UPDATE Invoice Set PrintedYear = YEAR(CURDATE()),PrintedMonth = MONTH(CURDATE()),PrintedDay = DAYOFMONTH(CURDATE()) WHERE InvoiceNo = $Invoice";
		print "<script language=JavaScript>window.open('invoice_tmplt.cgi?ID=$Invoice');</script>";
		$dbh->do($updateStr);
		$dbh->commit();
		$dbh->do("INSERT INTO History (TableName,ID,Action,ModifiedBy,ModifiedDate) VALUES(?,?,?,?,Now())",undef,"Invoice","$Invoice","Printed","$ENV{'REMOTE_USER'}");
		$dbh->commit();
	}
	print "<script language=JavaScript>window.location='print.cgi'</script>";
}

if ( "$DoWhat" eq "Print" )
{
	PrintInvoice();
}
else
{
	ListInvoices();
}

print <<"__END__";
	</table>
	</td></tr>
</table>
</body>
</html>
__END__
