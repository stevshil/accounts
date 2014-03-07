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
<title>$COMPANYNAME, Accounting System for Invoicing, Posting</title>
<link rel="stylesheet" href="../main.css" type="text/css">
<link rel="stylesheet" href="../style.css" type="text/css">
__END__
open(INCFILE, "<../include/hidebtns.inc") || die "No such file";
my @INCFILE=<INCFILE>;
print "@INCFILE";
close INCFILE;

open (INCFILE, "<../include/invoicing.inc") || die "No such file";
my @INCFILE = <INCFILE>;
close INCFILE;
@INCFILE=doPersonalise(@INCFILE);
print "@INCFILE";

print "<td align=left valign=top><h1>Post Invoices </h1>";

sub ListInvoices
{
	print <<"__END__";
	<p>Click on the ID column number to view an Invoice.<br>Tick the box next to the Invoice if you wish to post it.<br><br><b>NOTE: Posting an invoice will prevent you from editing it any further.</b><br><br>
	<form name=print action=post.cgi method=post>
	<input type=hidden name=DoWhat value=Post>
	<table width="100%" border=0 cellspacing=0 cellpadding=0>
	<tr><th align=left width=80>Post?</th><th align=left width=35>ID</th><th align=left width=350>Company Name</th><th align=left width=150>Invoice Date</th><th align=right width=180>Amount (&pound;)</th><th align=right width=250>Alternate Currency</th><th align=right width=100>Printed</th><th align=right width=80>Posted</th></tr>
__END__
	my $dbh = DBI->connect("DBI:mysql:database=accounts;host=localhost","$DBUSER","$DBPASS") || die "Unable to connect to database";
	my $sth = $dbh->prepare("SELECT InvoiceNo, Invoice.CoID, CompanyName, InvoiceDay, InvoiceMonth, InvoiceYear, PrintedDay, PrintedMonth, PrintedYear, Posted FROM Invoice,CustomerDetails WHERE Invoice.CoID=CustomerDetails.CoID AND Posted = 'N' AND PrintedYear is Not Null AND Invoice.void is null");
	$sth->execute();


	while ( my $ref = $sth->fetchrow_hashref() )
	{
	
		my $rowcolour="bgcolor='$bgcolour'" if ( ($rowcount % 2) != 0 );
		$rowcount++;
		print "<tr $rowcolour><td><input type=checkbox name=PostIt value=$ref->{'InvoiceNo'}></td><td><a href='InvDetails.cgi?id=$ref->{'InvoiceNo'}&DoWhat=Display'>$ref->{'InvoiceNo'}</a></td>";
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
	print "<tr><td colspan=8 align=left><div id=hideme><input type=submit name=printit value='Post Invoices' onclick='hidebtn()'></div></td></tr></form>";
}

sub PostInvoice
{
	my $Invoice;
	my @Invoices = param("PostIt");
	my $dbh = DBI->connect("DBI:mysql:database=accounts;host=localhost","$DBUSER","$DBPASS") || die "Unable to connect to database";

	foreach $Invoice ( @Invoices )
	{
		print "Posting Invoice number $Invoice....";
		my $updateStr = "UPDATE Invoice Set Posted = 'Y' WHERE InvoiceNo = $Invoice";
		$dbh->do($updateStr);
		$dbh->commit();
		$dbh->do("INSERT INTO History (TableName,ID,Action,ModifiedBy,ModifiedDate) VALUES(?,?,?,?,Now())",undef,"Invoice","$Invoice","Posted","$ENV{'REMOTE_USER'}");
		$dbh->commit();

		print "<font color=green>[POSTED OK]</font><br>\n";
	}
	$dbh->disconnect();
	print "<br>Invoice Posting complete<br>";
	print "<br><a href='post.cgi'>Click here to return to list</a><br>";
}

if ( "$DoWhat" eq "Post" )
{
	PostInvoice();
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
