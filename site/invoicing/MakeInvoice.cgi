#!/usr/bin/perl
# Invoice rate changed as of December 1st 2008 to 15%

use lib "../include";
use personalise;
use CGI ':standard';
use DBI();
use CGI::Carp 'fatalsToBrowser';

print header();
print <<"__END__";

<html>
<head>
<title>$COMPANYNAME, Accounting System for Invoicing, Create Invoice</title>
<link rel="stylesheet" href="../main.css" type="text/css">
<link rel="stylesheet" href="../style.css" type="text/css">
__END__

# include header file
open (INCFILE, "<../include/invoicing.inc") || die "No such file";
my @INCFILE = <INCFILE>;
close INCFILE;
@INCFILE=doPersonalise(@INCFILE);
print "@INCFILE";

# Get main invoice details for Invoice
my $CoID = param(coname);
my $CustContactID = param(CustContactID);
my $InvoiceDay = param(InvoiceDay);
my $InvoiceMonth = param(InvoiceMonth);
my $InvoiceYear = param(InvoiceYear);
my $CurrencyType = param(CurrencyType);
my $CurrencyRate = param(CurrencyRate);
my $CategoryID = param(CategoryID);

$AlternateCurrency = "Y" if ( $CurrencyType ne "GBP" );

# Add Invoice Detail to Invoice Table
my $dbh = DBI->connect("DBI:mysql:database=accounts;host=localhost","$DBUSER","$DBPASS") || die "Unable to connect to database";

my $insertString="";

if ( $CustContactID != 0 )
{
	$insertString = "INSERT INTO Invoice (CoID, CustContactID, InvoiceDay, InvoiceMonth, InvoiceYear, AlternateCurrency, CurrencyType, CurrencyRate, Posted, CategoryID) VALUES ($CoID, $CustContactID, $InvoiceDay, $InvoiceMonth, $InvoiceYear, '$AlternateCurrency', '$CurrencyType', $CurrencyRate, 'N', $CategoryID)";
}
else
{
	$insertString = "INSERT INTO Invoice (CoID, InvoiceDay, InvoiceMonth, InvoiceYear, AlternateCurrency, CurrencyType, CurrencyRate, Posted, CategoryID) VALUES ($CoID, $InvoiceDay, $InvoiceMonth, $InvoiceYear, '$AlternateCurrency', '$CurrencyType', $CurrencyRate, 'N', $CategoryID)";
}

$dbh->do("$insertString");

my $sth = $dbh->prepare("SELECT LAST_INSERT_ID() AS LastID");
$sth->execute();
my $ref=$sth->fetchrow_hashref();
my $invNo = $ref->{LastID};

$dbh->do("INSERT INTO History (TableName,ID,Action,ModifiedBy,ModifiedDate) VALUES(?,?,?,?,Now())",undef,"Invoice","$invNo","INSERT","$ENV{'REMOTE_USER'}");

$sth->finish();
$sth = undef;

my $sth = $dbh->prepare("SELECT CompanyName FROM CustomerDetails WHERE CoID = $CoID");
$sth->execute();
$ref = $sth->fetchrow_hashref();
my $CoName = $ref->{"CompanyName"};
$sth->finish();
$sth = undef;

print <<"__END__";
	<td align=left valign=top><h1>Invoice number $invNo created</h1>
	<table><tr><td>Company:</td><td>$CoName</td></tr>
	<tr><td>Date:</td><td>$InvoiceDay - $InvoiceMonth - $InvoiceYear</td></tr>
__END__

# Now add the invoice details
my @params = param();
my $counter=0;
foreach $detail (@params)
{
	if ( $detail =~ /^detail/ || $detail =~ /^qty/ || $detail =~ /baseamt/ || $detail || $detail =~ /^VAT/ )
	{
		$details{$detail}=param($detail);
	}
	if ( $detail =~ /^detail/ )
	{
		$counter++;
	}
}
for ( $x = 1; $x <= $counter; $x++ )
{
	my $description="detail$x";
	my $quantity="qty$x";
	my $baseamt="baseamt$x";
	my $VAT="VAT$x";
	my $incVAT="incVAT$x";
	my $sth = $dbh->prepare("SELECT * FROM TAXRates WHERE TAXID='$details{$VAT}'");
	$sth->execute();
	my $thisref = $sth->fetchrow_hashref();
	$thisVAT=$thisref->{"TAXRate"};
	$sth->finish();

	if ( $CurrencyRate == 1 )
	{
		my $tmpVal = $details{$baseamt}*(1+($thisVAT/100));
		$details{$description}=~s/'/''/g;

		# Deal with VAT total amounts, instead of net
		if ( $details{$incVAT} eq "on" )
		{
			my $mybase=$details{$baseamt};	# Now includes VAT
			#$mybase /= 1.175;
			#$mybase /= 1.15;
			$mybase /= (($thisVAT/100)+1);
			my $myVATamt = $details{$baseamt} - $mybase;
			#my $tmpVal = $mybase*(1+($myVATamt/100));
			my $tmpVal = $details{$baseamt};

			$insertString = "INSERT INTO InvoiceDetails (InvoiceNo, Description, Quantity, NetAmtUKP, AltCurrencyValue, VATRate, GrossAmtUKP, AltGrossAmt) VALUES ($invNo, '$details{$description}', $details{$quantity}, $mybase, $mybase, $myVATamt, $tmpVal, $tmpVal )";
		}
		else
		{
			$insertString = "INSERT INTO InvoiceDetails (InvoiceNo, Description, Quantity, NetAmtUKP, AltCurrencyValue, VATRate, GrossAmtUKP, AltGrossAmt) VALUES ($invNo, '$details{$description}', $details{$quantity}, $details{$baseamt}, $details{$baseamt}, $thisVAT, $tmpVal, $tmpVal )";
		}
		$dbh->do("$insertString");
	}
	else
	{
		my $tmpVal = $details{$baseamt}*(1+($thisVAT/100));
		$details{$description}=~s/'/''/g;

		# Deal with VAT total amounts, instead of net
		if ( $details{$incVAT} eq "on" )
		{
			my $mybase=$details{$baseamt};	# Now includes VAT
			#$mybase /= 1.175;
			#$mybase /= 1.15;
			$mybase /= (($thisVAT/100)+1);
			my $myVATamt = $details{$baseamt} - $mybase;
			my $tmpVal = $mybase*(1+($myVATamt/100));

			$insertString= "INSERT INTO InvoiceDetails (InvoiceNo, Description, Quantity, AltCurrencyValue, VATRate, AltGrossAmt) VALUES ($invNo, '$details{$description}', $details{$quantity}, $mybase, $myVATamt, $tmpVal )";
		}
		else
		{
			$insertString= "INSERT INTO InvoiceDetails (InvoiceNo, Description, Quantity, AltCurrencyValue, VATRate, AltGrossAmt) VALUES ($invNo, '$details{$description}', $details{$quantity}, $details{$baseamt}, $thisVAT, $tmpVal )";
		}
		$dbh->do("$insertString");
	}
}

my $sth=$dbh->prepare("SELECT InvDetID FROM InvoiceDetails WHERE InvoiceNo=$invNo");
$sth->execute();
while ( my $refHID=$sth->fetchrow_hashref() )
{
	my $HID=$refHID->{InvDetID};
	$dbh->do("INSERT INTO History (TableName,ID,Action,ModifiedBy,ModifiedDate) VALUES(?,?,?,?,Now())",undef,"InvoiceDetails","$HID","INSERT","$ENV{'REMOTE_USER'}");
}
$sth->finish();
$sth=undef();

$dbh->disconnect();
print end_html();
