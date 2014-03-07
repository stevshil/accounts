#!/usr/bin/perl

use lib "../include";
use personalise;
use CGI ':standard';
use DBI();

my $rowcount=0;
my $bgcolour="#f3f0f9";

my $DoWhat=param("DoWhat");
my $InvoiceNo = param("id");

print header();

print <<"__END__";
<html>
<head>
<title>$COMPANYNAME, Accounting System for Invoicing, Cancel/Void</title>
<link rel="stylesheet" href="../main.css" type="text/css">
<link rel="stylesheet" href="../style.css" type="text/css">
__END__

sub ListInvoices
{
	open (INCFILE, "<../include/invoicing.inc") || die "No such file";
	my @INCFILE = <INCFILE>;
	close INCFILE;
	@INCFILE=doPersonalise(@INCFILE);
	print "@INCFILE";

	print <<"__END__";
	<td align=left valign=top><h1>Void/Cancel Invoices </h1>
	<p>Tick the box next to the Invoice you wish to cancel or void.<br>Click the ID to view the invoice.<br><br>
	<form name=print action=void.cgi method=post>
	<input type=hidden name=DoWhat value=Void>
	<table width="100%" border=0 cellspacing=0 cellpadding=0>
	<tr><th align=left width=80>Void?</th><th align=left width=35>ID</th><th align=left width=350>Company Name</th><th align=left width=150>Invoice Date</th><th align=right width=180>Amount (&pound;)</th><th align=right width=250>Alternate Currency</th><th align=right width=100>Printed</th></tr>
__END__

	my $dbh = DBI->connect("DBI:mysql:database=accounts;host=localhost","$DBUSER","$DBPASS") || die "Unable to connect to database";
	my $sth = $dbh->prepare("SELECT InvoiceNo, Invoice.CoID, CompanyName, InvoiceDay, InvoiceMonth, InvoiceYear, PrintedDay, PrintedMonth, PrintedYear FROM Invoice,CustomerDetails WHERE Invoice.CoID=CustomerDetails.CoID AND Invoice.Posted <> 'Y' AND Invoice.void is null");
	$sth->execute();


	while ( my $ref = $sth->fetchrow_hashref() )
	{
	
		my $rowcolour="bgcolor='$bgcolour'" if ( ($rowcount % 2) != 0 );
		$rowcount++;
		print "<tr $rowcolour>";

		print "<td><input type=checkbox name=Print value=$ref->{'InvoiceNo'}></td>";
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
		print "</tr>\n";
		$rowcolour=undef;
	}
	$sth->finish();
	$dbh->disconnect();
	print "<tr><td colspan=8><hr></td></tr>";
	print "<tr><td colspan=8 align=left><input type=submit name=printit value='Void Invoices'></td></tr></form>";
}

sub VoidInvoice
{
	my @Invoices = param("Print");

	my $dbh = DBI->connect("DBI:mysql:database=accounts;host=localhost","$DBUSER","$DBPASS") || die "Unable to connect to database";

	foreach $Invoice (@Invoices)
	{
		my $updateStr = "UPDATE Invoice Set void='Y' WHERE InvoiceNo = $Invoice";
		$dbh->do($updateStr);
		$dbh->do("INSERT INTO History (TableName,ID,Action,ModifiedBy,ModifiedDate) VALUES(?,?,?,?,Now())",undef,"Invoice","$Invoice","Void","$ENV{'REMOTE_USER'}");
		$dbh->commit();
	}
	print "<script language=JavaScript>window.location='void.cgi'</script>";
}

if ( "$DoWhat" eq "Void" )
{
	VoidInvoice();
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
