#!/usr/bin/perl

use lib "../include";
use personalise;
use CGI ':standard';
use CGI::Carp 'fatalsToBrowser';
use DBI();

sub doRanges
{
	my ($startval,$endval,$inField)=@_;
	for my $tempvar ($startval..$endval)
        {
                if ( $tempvar == $refTODAYDATE->{$inField} )
                {
                        print "<option value=$tempvar selected>$tempvar</option>\n"
                }
                else
                {
                        print "<option value=$tempvar>$tempvar</option>\n"
                }
        }
}

sub DrawEntry
{
	my $dbh = DBI->connect("DBI:mysql:database=accounts;host=localhost","$DBUSER","$DBPASS") || die "Unable to connect to database";
	my $sth=$dbh->prepare("SELECT sum(GrossAmtUKP*Quantity) As AmtDue From InvoiceDetails WHERE InvoiceNo = $InvoiceNo");
	$sth->execute();
	my $ref=$sth->fetchrow_hashref();
	my $invoiceAmt = $ref->{"AmtDue"};
	$sth->finish();

	my $sthPaid=$dbh->prepare("SELECT sum(AmtPaidUKP) As AmtPaid From Payments WHERE InvoiceNo = $InvoiceNo");
	$sthPaid->execute();
	my $refPaid=$sthPaid->fetchrow_hashref();
	my $paidAmt= $refPaid->{"AmtPaid"};
	$sthPaid->finish();

	my $AmtOwed=$invoiceAmt - $paidAmt;

	print "<form name=payment action=MakePayment.cgi method=post>\n";
	print "<input type=hidden name=DoWhat value=Add>\n";
	print "<input type=hidden name=ID value=$InvoiceNo>\n";
	print "<input type=hidden name=AmtDue value=$ref->{AmtDue}>\n";
	print "<table border=0 cellspacing=0 cellpadding=0>\n";
	print "<tr><td colspan=2>&nbsp;</td></tr>\n";
	printf ("<tr><td><h3>Invoice amount:</h3></td><td><h3><b>&pound; %.2f</b></h3></td></tr>\n",$invoiceAmt);
	printf ("<tr><td><h3>Amount paid:</h3></td><td><h3><b>&pound; %.2f</b></h3></td></td></tr>\n",$paidAmt);
	printf ("<tr><td><h3>Amount owing:</h3></td><td><h3><b>&pound; %.2f</b></h3></td></td></tr>\n",$AmtOwed);
	print "<tr><td colspan=2>&nbsp;</td></tr>\n";
	print "<tr><td>Please select payment type:</td><td>";
	print "<select name=paytype><option>---SELECT ONE---</option><option>Bank Transfer, e.g. BACS, or other transfer<option>Cash</option><option>Cheque</option><option>Credit Card</option></select></td></tr>";
	print "<tr><td align=right>Payment Reference:</td><td><input type=text name=payref size=60></td></tr>";
	print "<tr><td colspan=2>&nbsp;</td></tr>\n";
	print "<tr><td align=right>Amount tendered &pound;:</td><td><input type=text name=Amount></td></tr>";

	my $sthDate = $dbh->prepare("SELECT DAYOFMONTH(CURDATE()) AS Day,MONTH(CURDATE()) As Month,YEAR(CURDATE()) As Year");
	$sthDate->execute();
	local $refTODAYDATE=$sthDate->fetchrow_hashref();

	print "<tr><td align=right>Payment Date:</td><td><select name=PaymentDay>";
	doRanges(1,31,"Day");
	print "</select><select name=PaymentMonth>";
	doRanges(1,12,"Month");
	print "</select><select name=PaymentYear>";
	doRanges($refTODAYDATE->{Year}-1,$refTODAYDATE->{Year}+1,"Year");
	print "</select></td></tr>";
	
	print "<tr><td align=left colspan=2><div id=hideme><input type=submit name=go value='Add Payment' onClick='hidebtn()'></div></td></tr>\n";
	print "</table>";
	print "</form>";
	$sthDate->finish();
	$dbh->disconnect();
}

sub MakePayment
{
	my $dbh = DBI->connect("DBI:mysql:database=accounts;host=localhost","$DBUSER","$DBPASS") || die "Unable to connect to database";
	my $AltCurAmt=0;

	# Check if we already have payment
	my $sth=$dbh->prepare("SELECT sum(AmtPaidUKP) As AmtPaid From Payments WHERE InvoiceNo=$InvoiceNo");
	$sth->execute();
	my $ref=$sth->fetchrow_hashref();
	$sth->finish();
	$sth=$dbh->prepare("SELECT CurrencyRate From Invoice WHERE InvoiceNo=$InvoiceNo");
	$sth->execute();
	my $refExRate = $sth->fetchrow_hashref();
	$sth->finish();
	$paidFlag=0;

	if ( $sthPaid->{AmtPaid} == $AmtDue )
	{
		print "<h2>Invoice is already paid up</h2>\n";
	}
	elsif ( ($sthPaid->{AmtPaid} + $Amount) > $AmtDue )
	{
		print "<h2>Amount tendered is greated than the invoice amount</h2>\n";
	}
	else
	{
		# Make payment
		$AltCurAmt = $Amount * $refExRate->{CurrencyRate};
		$payref=~s/'/''/g;
		#my $insertStr="Insert Into Payments (InvoiceNo, PaymentDay, PaymentMonth, PaymentYear, AmtPaidUKP, AmtPaidAltCur, PaymentMethod, PaymentRef) VALUES($InvoiceNo, DAYOFMONTH(CURDATE()),MONTH(CURDATE()),YEAR(CURDATE()),Round($Amount,2),Round($AltCurAmt,2),'$paytype','$payref')";
		my $insertStr="Insert Into Payments (InvoiceNo, PaymentDay, PaymentMonth, PaymentYear, AmtPaidUKP, AmtPaidAltCur, PaymentMethod, PaymentRef) VALUES($InvoiceNo, $payDay, $payMonth, $payYear,Round($Amount,2),Round($AltCurAmt,2),'$paytype','$payref')";
		$dbh->do($insertStr);
		my $sth=$dbh->prepare("SELECT PaymentID FROM Payments WHERE InvoiceNo=$InvoiceNo AND PaymentDay=$payDay AND PaymentMonth=$payMonth AND PaymentYear=$payYear");
		$sth->execute();
		my $ref=$sth->fetchrow_hashref();
		my $PID=$ref->{PaymentID};
		$sth->finish();
		$sth=undef();
		$dbh->do("INSERT INTO History (TableName,ID,Action,ModifiedBy,ModifiedDate) VALUES(?,?,?,?,Now())",undef,"Payments","$PID","INSERT","$ENV{'REMOTE_USER'}");
		$paidFlag=1;
	}

	if ( $paidFlag )
	{
		print "<h2>Payment made</h2>";
		printf ("<p>Exchange rate used: %.2f<br>Amount record &pound;%.2f<br>Amount in other currency: %.2f</p>",$refExRate->{CurrencyRate},$Amount,$AltCurAmt);
		undef $refExRate;
	}
	print "<p>Click back to return to make further payments</p><p><input type=button name=return value=Back onClick='location.href=\"list.cgi\"'></p>";
	$dbh->disconnect();
}

local $InvoiceNo=param("ID");
local $DoWhat=param("DoWhat");
local $AmtDue=param("AmtDue");
local $Amount=param("Amount");
local $paytype=param("paytype");
local $payref=param("payref");
local $payDay=param("PaymentDay");
local $payMonth=param("PaymentMonth");
local $payYear=param("PaymentYear");

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

open(INCFILE, "<../include/hidebtns.inc") || die "No such file";
my @INCFILE=<INCFILE>;
close INCFILE;
print "@INCFILE";

open (INCFILE, "<../include/payments.inc") || die "No such file";
my @INCFILE = <INCFILE>;
close INCFILE;
@INCFILE=doPersonalise(@INCFILE);
print "@INCFILE";

print <<"__END__";
        <td align=left valign=top><h1>Make Payment for Invoice Number: $InvoiceNo</h1>
        <table width="100%" border=0 cellspacing=0 cellpadding=0>
__END__


if ( "$DoWhat" eq "Add" )
{
	MakePayment();
}
else
{
	DrawEntry();
}

print "</table>";
print end_html();
