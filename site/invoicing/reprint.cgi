#!/usr/bin/perl

use lib "../include";
use personalise;
use CGI ':standard';
use CGI::Carp 'fatalsToBrowser';
use DBI;

my $InvoiceNo = param("ID");
#my $InvoiceNo=3;
my $tab="&nbsp; "x8;

sub DrawLine
{
	my ($currency) = @_;
	if ("$currency" ne "GBP")
	{	
		print "<tr><td colspan=9 bgcolor=#000000 height=2></td></tr>\n" ;
	}
	else
	{
		print "<tr><td colspan=6 bgcolor=#000000 height=2></td></tr>\n" ;
	}
}

sub DrawLine2
{
	my ($currency) = @_;
	if ("$currency" ne "GBP")
	{	
		print "<tr><td bgcolor=#000000 width=1 height=5></td><td colspan=4></td><td bgcolor=#000000 width=1></td><td colspan=2></td><td bgcolor=#000000></td></tr>\n";
	}
	else
	{
		print "<tr><td bgcolor=#000000 width=1></td><td colspan=5></td><td bgcolor=#000000 width=1></td></tr></td>\n";
	}
}

print header();
my $dbh = DBI->connect("DBI:mysql:database=accounts;host=localhost","$DBUSER","$DBPASS") || die "Unable to connect to database";

my $sthInvOrCred = $dbh->prepare("SELECT sum(AltGrossAmt*Quantity) AS InvCred FROM InvoiceDetails WHERE InvoiceNo=$InvoiceNo");
$sthInvOrCred->execute();
my $InvOrCred=$sthInvOrCred->fetchrow_hashref();
$InvOrCred=$InvOrCred->{'InvCred'};
$sthInvOrCred->finish();

my $sthCustomer = $dbh->prepare("SELECT Invoice.InvoiceNo, Invoice.InvoiceDay, Invoice.InvoiceMonth, Invoice.InvoiceYear, CurrencyType, CurrencyRate, CustomerDetails.CompanyName, CustomerDetails.Address1, CustomerDetails.Address2, CustomerDetails.Address3, CustomerDetails.TownCity, CustomerDetails.County, CustomerDetails.Country, CustomerDetails.Postcode, CustomerDetails.PaymentTermsID, CustomerContacts.Name FROM Invoice,CustomerDetails,CustomerContacts WHERE Invoice.CoID = CustomerDetails.CoID AND Invoice.CustContactID = CustomerContacts.CustContactID AND InvoiceNo=$InvoiceNo");
$sthCustomer->execute();
my $refCustomer = $sthCustomer->fetchrow_hashref();

print <<"__END__";
<html>
<body>
<table align=center border=0 cellpadding=0 cellspacing=0 height=964 width=718>
<tr><td align=center colspan=2><img src="../images/title.gif"></td></tr>
__END__
if ($InvOrCred < 0)
{
        print "<tr><td align=center colspan=2><h1>Credit Note</h1></td></tr>";
} else {
        print "<tr><td align=center colspan=2><h1>Invoice</h1></td></tr>";
}
print <<"__END__";
<tr><td align=right colspan=2>
	<table border=0><tr><td align=left>InvoiceNo:</td><td align=right><b>$refCustomer->{InvoiceNo}</b></td></tr>
	<tr><td align=left>Invoice Date:</td><td align=right>$refCustomer->{InvoiceDay}/$refCustomer->{InvoiceMonth}/$refCustomer->{InvoiceYear}</td></tr>
</table></td></tr>
<tr><td><table>
<tr><td colspan=2>&nbsp;</td></tr>
<tr><td align=left colspan=2>Invoice To:</td></tr>
<tr><td align=left colspan=2>$refCustomer->{Name}</td></tr>
<tr><td align=left colspan=2>$refCustomer->{CoName}</td></tr>
<tr><td align=left colspan=2>$refCustomer->{Address1}</td></tr>
__END__

# Check if parts of address are empty and suppress
print "<tr><td align=left colspan=2>$refCustomer->{Address2}</td></tr>\n" if ( "$refCustomer->{Address2}" ne "" );
print "<tr><td align=left colspan=2>$refCustomer->{Address3}</td></tr>\n" if ( "$refCustomer->{Address3}" ne "" );
print "<tr><td align=left colspan=2>$refCustomer->{TownCity}</td></tr>\n" if ( "$refCustomer->{TownCity}" ne "" );
print "<tr><td align=left colspan=2>$refCustomer->{County}</td></tr>\n" if ( "$refCustomer->{County}" ne "" );
print "<tr><td align=left colspan=2>$refCustomer->{Country}</td></tr>\n" if ( "$refCustomer->{Country}" ne "" );
print "<tr><td colspan=2>&nbsp;</td></tr>\n";
print "</table></td></tr>";

# Now for each detail
print "<tr><td colspan=2>&nbsp;</td></tr>\n";
print "<tr><td colspan=2><table cellpadding=0 cellspacing=0 width='100%'>\n";
DrawLine("$refCustomer->{CurrencyType}");

print "<tr><th bgcolor=#000000 width=1></th><th width=250 align=center>Description</th><th width=20 align=center>Qty</th><th align=right width=100>Price GBP</th><th width=100 align=right>Total GBP</th><th bgcolor=#000000 width=1></th>";


print "<th width=100 align=right>Price $refCustomer->{CurrencyType}</th><th width=100 align=right>Total $refCustomer->{CurrencyType}</th><th bgcolor=#000000 width=1></th>" if ( "$refCustomer->{CurrencyType}" ne "GBP" );

print "</tr>\n";
DrawLine("$refCustomer->{CurrencyType}");
DrawLine2($refCustomer->{CurrencyType});

my $VATRate=0;
my $sthDetails = $dbh->prepare("SELECT *, (NetAmtUKP*Quantity) As UKPTotal,(AltCurrencyValue*Quantity) As AltTotal FROM InvoiceDetails WHERE InvoiceDetails.InvoiceNo = $refCustomer->{InvoiceNo}");
$sthDetails->execute();
while ( my $ref = $sthDetails->fetchrow_hashref() )
{
	my $descr = $ref->{Description};
	$descr =~ s/\n/<br>/g;
	print "<tr><td bgcolor=#000000></td><td width=250>$descr&nbsp;</td><td align=right width=20>$ref->{Quantity}&nbsp;</td><td align=right width=100>$ref->{NetAmtUKP}&nbsp;</td><td align=right width=100>$ref->{UKPTotal}&nbsp;</td><td bgcolor=#000000></td>";
	print "<td align=right width=100>$ref->{AltCurrencyValue}&nbsp;</td><td align=right width=100>$ref->{AltTotal}&nbsp;</td><td bgcolor=#000000></td>" if ( "$refCustomer->{CurrencyType}" ne "GBP" );
	print "</tr>\n";
	$VATRate=$ref->{VATRate};
}
$sthDetails->finish();

# Now do totals
$sthDetails = $dbh->prepare("SELECT sum(NetAmtUKP*Quantity) As UKPTotals, sum(GrossAmtUKP*Quantity) As GrossUKPTotals, sum(AltCurrencyValue*Quantity) As AltTotals, sum(AltGrossAmt*Quantity) As AltGrossTotals, sum(GrossAmtUKP*Quantity)-sum(NetAmtUKP*Quantity) As UKVAT, sum(AltGrossAmt*Quantity)-sum(AltCurrencyValue*Quantity) As AltVAT FROM InvoiceDetails WHERE InvoiceNo = $refCustomer->{InvoiceNo}");
$sthDetails->execute();
my $ref=$sthDetails->fetchrow_hashref();

DrawLine("$refCustomer->{CurrencyType}");
DrawLine2($refCustomer->{CurrencyType});

# Net Totals
print "<tr><td bgcolor=#000000></td><td colspan=3 align=right>Total before tax:</td><td align=right>$ref->{UKPTotals}&nbsp;</td><td bgcolor=#000000></td>";
print "<td></td><td align=right>$ref->{AltTotals}&nbsp;</td><td bgcolor=#000000></td>" if ( "$refCustomer->{CurrencyType}" ne "GBP" );

# Tax Amount
print "<tr><td bgcolor=#000000></td><td colspan=3 align=right>VAT:</td><td align=right>$ref->{UKVAT}&nbsp;</td><td bgcolor=#000000></td>";
print "<td></td><td align=right>$ref->{AltVAT}&nbsp;</td><td bgcolor=#000000></td>" if ( "$refCustomer->{CurrencyType}" ne "GBP" );

# Taxed Totals
print "<tr><td bgcolor=#000000></td><td colspan=3 align=right><b>Gross Total:</b></td><td align=right><b>$ref->{GrossUKPTotals}&nbsp;</b></td><td bgcolor=#000000></td>";
print "<td></td><td align=right><b>$ref->{AltGrossTotals}&nbsp;</b></td><td bgcolor=#000000></td>" if ( "$refCustomer->{CurrencyType}" ne "GBP" );

DrawLine("$refCustomer->{CurrencyType}");
print "</tr>\n";
$sthDetails->finish();
undef $ref;
print "</table></td></tr>\n";

# Display currency exchange rate
if ( "$refCustomer->{CurrencyType}" ne "GBP" )
{
	print "<tr><td colspan=2><table>\n";
	print "<tr><td align=left>Exchange Rate:</td><td align=right>$refCustomer->{CurrencyRate}</td></tr>\n";
	print "<tr><td>Currency:</td><td align=right>";
	my $sth = $dbh->prepare("SELECT CurrencyName FROM CurrencyType WHERE CurrencyType='$refCustomer->{CurrencyType}'");
	$sth->execute();
	my $ref = $sth->fetchrow_hashref();
	print "$ref->{CurrencyName}</td></tr></table></td></tr>\n";
	$sth->finish();
}

$sth=$dbh->prepare("SELECT PaymentTerms FROM PaymentTerms WHERE PaymentTermsID = $refCustomer->{PaymentTermsID}");
$sth->execute();
$ref=$sth->fetchrow_hashref();

print <<"__END__";
<tr><td colspan=2>&nbsp;</td></tr>
<tr><td colspan=2 align=center>Please make cheque(s) payable to $COMPANYNAME at the address below.<br>Payment requested within $ref->{PaymentTerms} of Invoice Date.<br>Any payments received after this time are subject to $INTERESTRATE% interest per day unpaid.<br>Days includes weekends and bank holidays<br></td></tr>
<tr><td colspan=2 align=center>&nbsp;<br>
$COMPANYNAME<br>
$COMPANYADDRESS<br>
Email: $ENV{'REMOTE_USER'}\@$COMPANYDOMAIN $tab Tel: $COMPANYPHONE<br>
Registered in England Number: $COMPANYREGNO $tab VAT Number: $COMPANYVATNO</td></tr>
</table>
</body>
</html>
__END__

$sth->finish();
undef $ref;
$sthCustomer->finish();
$dbh->disconnect();
