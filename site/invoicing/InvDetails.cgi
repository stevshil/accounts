#!/usr/bin/perl

use lib "../include";
use personalise;
use CGI ':standard';
use CGI::Carp 'fatalsToBrowser';
use DBI();

my $InvoiceNo = param("id");
my $DoWhat = param("DoWhat");

print header();
print <<"__END__";
<html>
<head>
<title>$COMPANYNAME, Accounting System for Invoicing, Invoicing Options</title>
<link rel="stylesheet" href="../main.css" type="text/css">
<link rel="stylesheet" href="../style.css" type="text/css">
<script language=JavaScript>
	function printInvoice()
	{
		location.href='print.cgi?ID=$InvoiceNo&DoWhat=Print&Print=$InvoiceNo';
	}
</script>
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

my $dbh = DBI->connect("DBI:mysql:database=accounts;host=localhost","$DBUSER","$DBPASS") || die "Unable to connect to database";
my $sth = $dbh->prepare("SELECT CompanyName FROM Invoice,CustomerDetails WHERE Invoice.CoID = CustomerDetails.CoID AND InvoiceNo = $InvoiceNo");
$sth->execute();
my $ref=$sth->fetchrow_hashref();
my $CoName = $ref->{CompanyName};
$sth->finish();
my $sth = $dbh->prepare("SELECT CurrencyRate,CurrencyType, Posted FROM Invoice WHERE InvoiceNo = $InvoiceNo");
$sth->execute();
$ref=$sth->fetchrow_hashref();
my $tmpCurrencyType = $ref->{CurrencyType};
my $CurrencyRate = $ref->{CurrencyRate};
my $Posted = $ref->{Posted};
$sth->finish();
my $sth = $dbh->prepare("SELECT * FROM CurrencyType WHERE CurrencyType = '$tmpCurrencyType'");
$sth->execute();
$ref=$sth->fetchrow_hashref();
my $CurrencyType = $ref->{CurrencyName};
$sth->finish();
$dbh->disconnect();
undef $sth;
undef $dbh;
undef $ref;

print <<"__END__";
       	<td align=left valign=top><h1>Invoice Number:<b> $InvoiceNo</b></h1>
	<table><tr><td><h3>Currency:</h3></td><td><h3>$CurrencyType</h3></td></tr>
	<tr><td><h3>Rate:</h3></td><td><h3>$CurrencyRate</h3></td></tr>
	</table>
__END__

sub ShowDetail
{
	my $dbh = DBI->connect("DBI:mysql:database=accounts;host=localhost","$DBUSER","$DBPASS") || die "Unable to connect to database";
	my $sth = $dbh->prepare("SELECT Address1,Address2,Address3,TownCity,County,Country,Postcode FROM Invoice,CustomerDetails WHERE Invoice.CoID = CustomerDetails.CoID AND InvoiceNo = $InvoiceNo");
	$sth->execute();
	my $ref=$sth->fetchrow_hashref();
	my $Add1 = $ref->{Address1};
	my $Add2 = $ref->{Address2};
	my $Add3 = $ref->{Address3};
	my $Town = $ref->{TownCity};
	my $County = $ref->{County};
	my $Country = $ref->{Country};
	my $PCode = $ref->{Postcode};
	$sth->finish();
	print "<table><tr><td valign=top><h3>Address:</h3></td><td><h2>$CoName<br>$Add1<br>";
	print "$Add2<br>" if ( "$Add2" ne "");
	print "$Add3<br>" if ("$Add3" ne "");
	print "$Town<br>" if ("$Town" ne "");
	print "$County<br>" if ("$County" ne "");
	print "$PCode<br>" if ("$PCode" ne "");
	print "$Country" if ("$Country" ne "");
	print "</h2></td></tr></table>\n";

print <<"__END__";
       	<p>Click ID to edit details<br><br>
	<form name=details action='InvDetails.cgi' method=post>
       	<table width="100%" border=0 cellspacing=0 cellpadding=0>
	<tr><th width=40 align=left>ID</th><th width=450 align=left>Detail</th><th width=40 align=right>Qty</th><th align=right>Net Amt. (&pound)</th><th align=right>Currency Amt</th></tr>
__END__

	my $VATRate=0;
	$sth = $dbh->prepare("SELECT InvDetID,Description,Quantity,NetAmtUKP,AltCurrencyValue,VATRate,CurrencyRate,CurrencyType,Posted FROM Invoice,InvoiceDetails WHERE Invoice.InvoiceNo = InvoiceDetails.InvoiceNo AND InvoiceDetails.InvoiceNo = $InvoiceNo");
	$sth->execute();
	while ( my $ref = $sth->fetchrow_hashref() )
	{
		if ( $ref->{Posted} ne 'Y' )
		{
			print "<tr><td><a href='InvDetails.cgi?id=$InvoiceNo&DetID=$ref->{InvDetID}&DoWhat=Edit'>$ref->{InvDetID}</a></td>";
		}
		else
		{
			print "<tr><td>$ref->{InvDetID}</td>";
		}
		my $descr = $ref->{Description};
		$descr =~ s/\n/<br>/g;
		print "<td>$descr</td><td align=right>$ref->{Quantity}</td><td align=right>$ref->{NetAmtUKP}</td><td align=right>$ref->{AltCurrencyValue}</td></tr>\n";
		$VATRate=$ref->{VATRate};
	}
	$sth->finish();

	$sth = $dbh->prepare("SELECT round(sum(NetAmtUKP*Quantity),2) AS NetAmt, round(sum(AltCurrencyValue*Quantity),2) As AltCurVal, round((sum(GrossAmtUKP*Quantity)),2) As GrossAmt, round(sum(AltGrossAmt*Quantity),2) As AltGrossAmt From InvoiceDetails Where InvoiceNo=$InvoiceNo");
	$sth->execute();
	$ref = $sth->fetchrow_hashref();
	print "<tr><td colspan=5><hr></td></tr>";
	print "<tr><td>&nbsp;</td><td>&nbsp;</td><td align=right><b>&nbsp;Sub Total:</b></td><td align=right><b>$ref->{NetAmt}</b></td><td align=right><b>$ref->{AltCurVal}</b></td><td>&nbsp;</td><td>&nbsp;</td></tr>\n";

	#my $VATCharge=($ref->{NetAmt}) * ($VATRate/100);
	$VATCharge=$ref->{GrossAmt} - $ref->{NetAmt};
	my $AltVATCharge=$ref->{AltGrossAmt} - $ref->{AltCurVal};
	if ( index($VATCharge,".") < 0 )
	{
		$VATCharge.=".00";
	}
	else
	{
		my $tmpString = substr($VATCharge,index($VATCharge,"."));
		$VATCharge .= "0" if ( length($tmpString) == 2 );
		$VATCharge = substr($VATCharge,0,index($VATCharge,".")+3) if ( length($tmpString) > 2);
	}
	if ( index($AltVATCharge,".") < 0 )
	{
		$AltVATCharge.=".00";
	}
	else
	{
		my $tmpString = substr($AltVATCharge,index($AltVATCharge,"."));
		$AltVATCharge .= "0" if ( length($tmpString) == 2 );
		$AltVATCharge = substr($AltVATCharge,0,index($AltVATCharge,".")+3) if ( length($tmpString) > 2);
	}
	
	print "<tr><td>&nbsp;</td><td>&nbsp;</td><td align=right><b>&nbsp;VAT:</b></td><td align=right><b>$VATCharge</b></td><td align=right><b>";

	print "$AltVATCharge</b></td><td>&nbsp;</td><td>&nbsp;</td></tr>\n";

	print "<tr><td colspan=5><hr></td></tr>";

	print "<tr><td>&nbsp;</td><td>&nbsp;</td><td align=right><b>&nbsp;Total:</b></td><td align=right><b>$ref->{GrossAmt}</b></td><td align=right><b>";

	print "$ref->{AltGrossAmt}</b></td><td>&nbsp;</td><td>&nbsp;</td></tr>\n";
	$sth->finish();
	$dbh->disconnect();

	print "<tr><td colspan=5>&nbsp;</td></tr>\n";
	if ( "$tmpCurrencyType" ne "GBP" && "$Posted" ne "Y")
	{
		print "<tr><td>UK Total:<input type=text name=UKPAmt value='Enter UKP Total' onFocus='javascript:this.value.clear()'></td>";
		print "<td><input type=submit name=altCurData value='Enter GBP Amount' onClick='enterGBP()'></td><td colspan=2>&nbsp;</td></tr>\n";
	print "<input type=hidden name=DoWhat value=AddGBP>";
	print "<input type=hidden name=id value=$InvoiceNo>";
	}
	print "<tr><td colspan=5 align=center><input type=button name=print value='     Print     ' onClick='printInvoice()'></td></tr>";
	print "</table></form>\n";
}

sub EditDetail
{
	my $DetID = param("DetID");

	my $dbh = DBI->connect("DBI:mysql:database=accounts;host=localhost","$DBUSER","$DBPASS") || die "Unable to connect to database";
	my $sth = $dbh->prepare("SELECT Address1,Address2,Address3,TownCity,County,Country,Postcode FROM Invoice,CustomerDetails WHERE Invoice.CoID = CustomerDetails.CoID AND InvoiceNo = $InvoiceNo");
	$sth->execute();
	my $ref=$sth->fetchrow_hashref();
	my $Add1 = $ref->{Address1};
	my $Add2 = $ref->{Address2};
	my $Add3 = $ref->{Address3};
	my $Town = $ref->{TownCity};
	my $County = $ref->{County};
	my $Country = $ref->{Country};
	my $PCode = $ref->{Postcode};
	$sth->finish();
	print "<table><tr><td valign=top><h3>Address:</h3></td><td><h2>$CoName<br>$Add1<br>";
	print "$Add2<br>" if ( "$Add2" ne "");
	print "$Add3<br>" if ("$Add3" ne "");
	print "$Town<br>" if ("$Town" ne "");
	print "$County<br>" if ("$County" ne "");
	print "$PCode<br>" if ("$PCode" ne "");
	print "$Country" if ("$Country" ne "");
	print "</h2></td></tr></table>\n";

print <<"__END__";
       	<p>Modify Details and click UPDATE<br><br>
	<form name=details action='InvDetails.cgi' method=post>
	<input type=hidden name=DoWhat value="AlterDetail">
	<input type=hidden name=id value=$InvoiceNo>
	<input type=hidden name=DetID value=$DetID>
       	<table width="100%" border=0 cellspacing=0 cellpadding=0>
	<tr><th width=40 align=left>ID</th><th width=450 align=left>Detail</th><th width=40 align=right>Qty</th><th align=right>Net Amt. (&pound)</th><th align=right>Currency Amt</th></tr>
__END__

	my $VATRate=0;
	$sth = $dbh->prepare("SELECT InvDetID,Description,Quantity,NetAmtUKP,AltCurrencyValue,VATRate,CurrencyRate,CurrencyType FROM Invoice,InvoiceDetails WHERE Invoice.InvoiceNo = InvoiceDetails.InvoiceNo AND InvoiceDetails.InvoiceNo = $InvoiceNo");
	$sth->execute();
	while ( my $ref = $sth->fetchrow_hashref() )
	{
		if ( $ref->{InvDetID} == $DetID )
		{
			print "<tr><td><b>$DetID</b></td><td><textarea name=Description cols=50>$ref->{Description}</textarea></td><td align=right><input type=text name=Quantity";
			print " value='$ref->{Quantity}'" if ("$ref->{Quantity}" !~ /^ *$/);
			print " align=right></td><td align=right><input type=text name=NetAmtUKP";
			print " value='$ref->{NetAmtUKP}'" if ("$ref->{NetAmtUKP}" !~ /^ *$/);
			print " align=right></td><td align=right><input type=text name=AltCurrencyValue";
			print " value='$ref->{AltCurrencyValue}'" if ("$ref->{AltCurrencyValue}" !~ /^ *$/);
			print " align=right></td></tr>\n";
		}
		else
		{
			my $descr = $ref->{Description};
			$descr =~ s/\n/<br>/g;
			print "<tr><td><a href='InvDetails.cgi?id=$InvoiceNo&DetID=$ref->{InvDetID}&DoWhat=Edit'>$ref->{InvDetID}</a></td><td>$descr</td><td align=right>$ref->{Quantity}</td><td align=right>$ref->{NetAmtUKP}</td><td align=right>$ref->{AltCurrencyValue}</td></tr>\n";
		}
		$VATRate=$ref->{VATRate};
	}
	$sth->finish();

	$sth = $dbh->prepare("SELECT round(sum(NetAmtUKP*Quantity),2) AS NetAmt, round(sum(AltCurrencyValue*Quantity),2) As AltCurVal, round((sum(GrossAmtUKP*Quantity)),2) As GrossAmt, round(sum(AltGrossAmt*Quantity),2) As AltGrossAmt From InvoiceDetails Where InvoiceNo=$InvoiceNo");
	$sth->execute();
	$ref = $sth->fetchrow_hashref();
	print "<tr><td colspan=5><hr></td></tr>";
	print "<tr><td>&nbsp;</td><td>&nbsp;</td><td align=right><b>&nbsp;Sub Total:</b></td><td align=right><b>$ref->{NetAmt}</b></td><td align=right><b>$ref->{AltCurVal}</b></td><td>&nbsp;</td><td>&nbsp;</td></tr>\n";

	#my $VATCharge=($ref->{NetAmt}) * ($VATRate/100);
	$VATCharge=$ref->{GrossAmt} - $ref->{NetAmt};
	my $AltVATCharge=$ref->{AltGrossAmt} - $ref->{AltCurVal};
	if ( index($VATCharge,".") < 0 )
	{
		$VATCharge.=".00";
	}
	else
	{
		my $tmpString = substr($VATCharge,index($VATCharge,"."));
		$VATCharge .= "0" if ( length($tmpString) == 2 );
		$VATCharge = substr($VATCharge,0,index($VATCharge,".")+3) if ( length($tmpString) > 2);
	}
	if ( index($AltVATCharge,".") < 0 )
	{
		$AltVATCharge.=".00";
	}
	else
	{
		my $tmpString = substr($AltVATCharge,index($AltVATCharge,"."));
		$AltVATCharge .= "0" if ( length($tmpString) == 2 );
		$AltVATCharge = substr($AltVATCharge,0,index($AltVATCharge,".")+3) if ( length($tmpString) > 2);
	}
	
	print "<tr><td>&nbsp;</td><td>&nbsp;</td><td align=right><b>&nbsp;VAT:</b></td><td align=right><b>$VATCharge</b></td><td align=right><b>";

	print "$AltVATCharge</b></td><td>&nbsp;</td><td>&nbsp;</td></tr>\n";

	print "<tr><td colspan=5><hr></td></tr>";

	print "<tr><td>&nbsp;</td><td>&nbsp;</td><td align=right><b>&nbsp;Total:</b></td><td align=right><b>$ref->{GrossAmt}</b></td><td align=right><b>";

	print "$ref->{AltGrossAmt}</b></td><td>&nbsp;</td><td>&nbsp;</td></tr>\n";
	$sth->finish();
	$dbh->disconnect();

	print "<tr><td colspan=5>&nbsp;</td></tr>\n";
	print "<tr><td colspan=5 align=center><div id=hideme><input type=submit name=doit value=UPDATE onclick='hideme()'></div></td></tr>";
	print "</table></form>\n";
}

sub AddUKPAmt
{
	my $UKPAmt = param(UKPAmt);
	my $totalUKP=0;

	my $dbh = DBI->connect("DBI:mysql:database=accounts;host=localhost","$DBUSER","$DBPASS") || die "Unable to connect to database";
	my $sth = $dbh->prepare("SELECT sum(NetAmtUKP*Quantity) AS NetAmt, sum(AltCurrencyValue*Quantity) As AltCurVal, round((sum(GrossAmtUKP*Quantity)),2) As GrossAmt, round((sum(AltGrossAmt*Quantity)),2) As AltGrossAmt From InvoiceDetails Where InvoiceNo=$InvoiceNo");
	$sth->execute();
	my $ref = $sth->fetchrow_hashref();

	my $exRate = $ref->{AltGrossAmt}/$UKPAmt;

	# Update invoice currency rate
	my $updateStr="UPDATE Invoice Set CurrencyRate = $ref->{AltCurVal}/$UKPAmt WHERE InvoiceNo=$InvoiceNo";
	$dbh->do("$updateStr");
	$dbh->do("INSERT INTO History (TableName,ID,Action,ModifiedBy,ModifiedDate) VALUES(?,?,?,?,Now())",undef,"Invoice","$InvoiceNo","UPDATEUKPAmt","$ENV{'REMOTE_USER'}");
	$sth->finish();

	# Now divide into details
	$sth = $dbh->prepare("SELECT InvDetID,Description,Quantity,NetAmtUKP,AltCurrencyValue,VATRate,CurrencyRate,CurrencyType FROM Invoice,InvoiceDetails WHERE Invoice.InvoiceNo = InvoiceDetails.InvoiceNo AND InvoiceDetails.InvoiceNo = $InvoiceNo");
	$sth->execute();
	while ( my $refDetail = $sth->fetchrow_hashref() )
	{
		# Update InvoiceDetails
		my $updateStr="";
		if ( $refDetail->{VATRate} > 0.00 )
		{
			my $tmpGross = ($refDetail->{AltCurrencyValue}/$exRate)*(1+($refDetail->{VATRate}/100));
			my $tmpNET = $refDetail->{AltCurrencyValue}/$exRate;
			$updateStr = "UPDATE InvoiceDetails Set NetAmtUKP = Round($tmpNET,2)";
			$updateStr .= ", GrossAmtUKP = Round($tmpGross,2) WHERE InvDetID = $refDetail->{InvDetID}";
		}
		else
		{
			my $tmpNET = $refDetail->{AltCurrencyValue}/$exRate;
			$updateStr = "UPDATE InvoiceDetails Set NetAmtUKP = Round($tmpNET,2)";
			$updateStr .= ", GrossAmtUKP = Round($tmpNET,2) WHERE InvDetID=$refDetail->{InvDetID}";
		}
		$dbh->do($updateStr);
		$dbh->do("INSERT INTO History (TableName,ID,Action,ModifiedBy,ModifiedDate) VALUES(?,?,?,?,Now())",undef,"InvoiceDetails","$refDetail->{InvDetID}","UPDATEUKPAmt","$ENV{'REMOTE_USER'}");
		
	}
	$sth->finish();
	$dbh->disconnect();

	print "<script language=JavaScript>location.href='InvDetails.cgi?id=$InvoiceNo&DoWhat=Display'</script>";
}

sub AlterDetail
{
	my $DetID = param("DetID");
	my $Description = param("Description");
	my $Quantity = param("Quantity");
	my $NetAmtUKP = param("NetAmtUKP");
	my $AltCurrencyValue = param("AltCurrencyValue");

	# Allow appostrophes
	$Description=~s/'/''/g;

	my $dbh = DBI->connect("DBI:mysql:database=accounts;host=localhost","$DBUSER","$DBPASS") || die "Unable to connect to database";
	my $sth_GBP = $dbh->prepare("SELECT CurrencyType FROM Invoice Where InvoiceNo = $InvoiceNo");
	$sth_GBP->execute();
	my $ref_GBP = $sth_GBP->fetchrow_hashref();
	my $curType = $ref_GBP->{CurrencyType};
	$sth_GBP->finish();

	my $sth = $dbh->prepare("SELECT * FROM InvoiceDetails WHERE InvDetID=$DetID");
	$sth->execute();
	my $ref = $sth->fetchrow_hashref();

	my $updateStr="";
	if ( $ref->{VATRate} > 0.00 )
	{
		$AltCurrencyValue = $NetAmtUKP if ( "$curType" eq "GBP" );

		$updateStr = "UPDATE InvoiceDetails SET Description='$Description', Quantity=$Quantity, AltCurrencyValue = Round($AltCurrencyValue,2), AltGrossAmt=Round(($AltCurrencyValue*(1+($ref->{VATRate}/100))),2)";
		if ( $NetAmtUKP !~ /^ *$/ )
		{
			$updateStr .= ", NetAmtUKP = Round($NetAmtUKP,2), GrossAmtUKP=Round(($NetAmtUKP*(1+($ref->{VATRate}/100))),2)";
		}
		$updateStr .= " WHERE InvDetID=$DetID"; 
	}
	else
	{
		$AltCurrencyValue = $NetAmtUKP if ( "$curType" eq "GBP" );

		$updateStr = "UPDATE InvoiceDetails SET Description='$Description', Quantity=$Quantity, AltCurrencyValue = Round($AltCurrencyValue,2), AltGrossAmt=Round($AltCurrencyValue,2)";
		if ( $NetAmtUKP !~ /^ *$/ )
		{
			$updateStr .= ", NetAmtUKP = Round($NetAmtUKP,2), GrossAmtUKP=Round($NetAmtUKP,2)";
		}
		$updateStr .= " WHERE InvDetID=$DetID"; 
	}
	#print "$updateStr";
	$sth->finish();
	$dbh->do($updateStr);
	$dbh->do("INSERT INTO History (TableName,ID,Action,ModifiedBy,ModifiedDate) VALUES(?,?,?,?,Now())",undef,"InvoiceDetails","$DetID","UPDATEDetail","$ENV{'REMOTE_USER'}");
	$dbh->disconnect();

	#print "<script language=JavaScript>location.href='InvDetails.cgi?id=$InvoiceNo&DoWhat=Display'</script>";
} 

if ( "$DoWhat" eq "Edit" )
{
	EditDetail();
}
elsif ( "$DoWhat" eq "AddGBP" )
{
	AddUKPAmt();
}
elsif ( "$DoWhat" eq "AlterDetail" )
{
	AlterDetail();
}
else
{
	ShowDetail();
}

print "</table>";
print end_html();
