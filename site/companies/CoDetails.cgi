#!/usr/bin/perl

use lib "../include";
use personalise;
use CGI ':standard';
use DBI();

$CoID=param("id");

sub updateDetails
{
	my $CoID=param("id");
	my $coname=param("coname");
	$coname=~s/'/''/g;
	my $add1=param("add1");
	my $add2=param("add2");
	my $add3=param("add3");
	my $town=param("town");
	my $county=param("county");
	my $pcode=param("pcode");
	my $country=param("country");
	my $phone=param("phone");
	my $fax=param("fax");
	my $payterm=param("payterm");
	my $deleted=param("notused");

	my $dbh = DBI->connect("DBI:mysql:database=accounts;host=localhost","$DBUSER","$DBPASS") || die "Unable to connect to database";
	$dbh->do("UPDATE CustomerDetails SET CompanyName='$coname', Address1='$add1', Address2='$add2', Address3='$add3', TownCity='$town', County='$county', Postcode='$pcode', Country='$country', Phone='$phone', Fax='$fax', PaymentTermsID=$payterm, Deleted='$deleted' WHERE CoID=$CoID");

	$dbh->do("INSERT INTO History (TableName,ID,Action,ModifiedBy,ModifiedDate) VALUES(?,?,?,?,Now())",undef,"CustomerDetails","$CoID","UPDATE","$ENV{'REMOTE_USER'}");

	$dbh->disconnect();
	print "<td valign=top align=left><h1>Company updated successfully</h1><br>";
	print "<form><input type=button name=here value='Back to list' onClick='location.href=\"list.cgi\"'></form></td></tr>";
}

sub displayDetails
{
	print <<"__END__";
		<td align=left valign=top><h1>View Company $coname</h1>
		<table>
		<tr><td>Company Name:</td><td>$coname</td></tr>
		<tr><td>&nbsp;</td></tr>
		<tr><td valign=top>Address:</td><td>$add1<br>
					$add2<br>
					$add3</td></tr>
		<tr><td>Town/City:</td><td>$town</td></tr>
		<tr><td>County:</td><td>$county</td></tr>
		<tr><td>Post Code:</td><td>$pcode</td></tr>
__END__

	print "<tr><td>Country:</td><td>";
	my $dbh = DBI->connect("DBI:mysql:database=accounts;host=localhost","$DBUSER","$DBPASS") || die "Unable to connect to database";
	my $sth = $dbh->prepare("SELECT * FROM Countries WHERE CountryID='$country'");
	$sth->execute();
	my $ref = $sth->fetchrow_hashref();
	print "$ref->{'CountryText'}";
	$sth->finish();
	$dbh->disconnect();
	print "</td></tr>";

	print <<"__END__";
		<tr><td>&nbsp;</td></tr>
		<tr><td>Telephone:</td><td>$phone</td></tr>
		<tr><td>Fax:</td><td>$fax</td></tr>
		<tr><td>&nbsp;</td></tr>
		<tr><td>Payment Terms:</td><td>
__END__
	
	$dbh = DBI->connect("DBI:mysql:database=accounts;host=localhost","$DBUSER","$DBPASS") || die "Unable to connect to database";
	$sth = $dbh->prepare("SELECT * FROM PaymentTerms WHERE PaymentTermsID=$payterm");
	$sth->execute();
	while ( my $ref = $sth->fetchrow_hashref() )
	{
			print "$ref->{'PaymentTerms'}";
	}
	$sth->finish();
	$dbh->disconnect();
	print "</td></tr>";
	
	print <<"__END__";
		<tr><td>&nbsp;</td></tr>
		<tr><td>No Longer Used?:</td><td>$Deleted</td></tr>
		<tr><td>&nbsp;</td></tr>
		<tr><td colspan=2 align=center><input type=button name=edit onClick="location.href='CoDetails.cgi?id=$CoID&DoWhat=Edit'" value="Edit"> &nbsp; <input type=button name=back onClick="history.go(-1)" value="Back"></td></tr>
		</table>
		</td></tr>
	</table>
__END__
}

sub editDetails
{
	print <<"__END__";
		<td align=left valign=top><h1>Edit Company $coname</h1>
		<form name=companyedit method=post action="CoDetails.cgi">
		<input type=hidden name=id value="$CoID"><input type=hidden name=DoWhat value=Update>
		<table>
		<tr><td>Company Name:</td><td><input type=text name=coname value="$coname" size=80></td></tr>
		<tr><td>&nbsp;</td></tr>
		<tr><td valign=top>Address:</td><td><input type=text name=add1 value="$add1" size=80><br>
					<input type=text name=add2 value="$add2" size=80><br>
					<input type=text name=add3 value="$add3" size=80></td></tr>
		<tr><td>Town/City:</td><td><input type=text name=town value="$town" size=60></td></tr>
		<tr><td>County:</td><td><input type=text name=county value="$county" size=60></td></tr>
		<tr><td>Post Code:</td><td><input type=text name=pcode value="$pcode" size=20></td></tr>
__END__

	print "<tr><td>Country:</td><td><select name=country>";
	my $dbh = DBI->connect("DBI:mysql:database=accounts;host=localhost","$DBUSER","$DBPASS") || die "Unable to connect to database";
	my $sth = $dbh->prepare("SELECT * FROM Countries Order By CountryText");
	$sth->execute();
	while ( my $ref = $sth->fetchrow_hashref() )
	{
		if ( $ref->{'CountryID'} eq "$country" )
		{
			print "<option value=$ref->{'CountryID'} selected>$ref->{'CountryText'}</option>";
		}
		else
		{
			print "<option value=$ref->{'CountryID'}>$ref->{'CountryText'}</option>";
		}
	}
	$sth->finish();
	$dbh->disconnect();
	print "</select></td></tr>";

	print <<"__END__";
		<tr><td>&nbsp;</td></tr>
		<tr><td>Telephone:</td><td><input type=text name=phone value="$phone" size=30></td></tr>
		<tr><td>Fax:</td><td><input type=text name=fax value="$fax" size=30></td></tr>
		<tr><td>&nbsp;</td></tr>
		<tr><td>Payment Terms:</td><td><select name=payterm>
__END__
	
	$dbh = DBI->connect("DBI:mysql:database=accounts;host=localhost","$DBUSER","$DBPASS") || die "Unable to connect to database";
	$sth = $dbh->prepare("SELECT * FROM PaymentTerms");
	$sth->execute();
	while ( my $ref = $sth->fetchrow_hashref() )
	{
		if ( $ref->{'PaymentTermsID'} == $payterm )
		{
			print "<option value=$ref->{'PaymentTermsID'} selected>$ref->{'PaymentTerms'}</option>";
		}
		else
		{
			print "<option value=$ref->{'PaymentTermsID'}>$ref->{'PaymentTerms'}</option>";
		}
	}
	$sth->finish();
	$dbh->disconnect();
	print "</select></td></tr>";
	
	print <<"__END__";
		<tr><td>&nbsp;</td></tr>
		<tr><td>No Longer Used?:</td><td><input type=checkbox name=notused></td></tr>
		<tr><td colspan=2 align=center><div id=hideme><input type=submit value='Update Customer' name='Update' onClick='hidebtn()'> &nbsp; <input type=button value='Back' onClick='history.go(-1)'></div></td></tr>
		</table>
		</td></tr>
	</table>
__END__
}

sub general
{
	# Select company detail from database
	my $dbh = DBI->connect("DBI:mysql:database=accounts;host=localhost","$DBUSER","$DBPASS") || die "Unable to connect to database";
	my $sth = $dbh->prepare("SELECT * FROM CustomerDetails WHERE CoID=$CoID");
	$sth->execute();
	while ( my $ref = $sth->fetchrow_hashref() )
	{
		$coname=$ref->{'CompanyName'};
		$add1=$ref->{'Address1'};
		$add2=$ref->{'Address2'};
		$add3=$ref->{'Address3'};
		$town=$ref->{'TownCity'};
		$county=$ref->{'County'};
		$pcode=$ref->{'Postcode'};
		$country=$ref->{'Country'};
		$phone=$ref->{'Phone'};
		$fax=$ref->{'Fax'};
		$payterm=$ref->{'PaymentTermsID'};
		$notused=$ref->{'Deleted'};
	}
	$sth->finish();
	$dbh->disconnect();
}

print header();
print <<"__END__";

<html>
<head>
<title>$COMPANYNAME, Accounting System for Invoicing, Company Details</title>
<link rel="stylesheet" href="../main.css" type="text/css">
<link rel="stylesheet" href="../style.css" type="text/css">
__END__

# include header file
open(INCFILE, "<../include/hidebtns.inc") || die "No such file";
my @INCFILE=<INCFILE>;
print "@INCFILE";
close INCFILE;

open (INCFILE, "<../include/companies.inc") || die "No such file";
my @INCFILE = <INCFILE>;
close INCFILE;
@INCFILE=doPersonalise(@INCFILE);
print "@INCFILE";

if (param("DoWhat") eq "Edit")
{
	general;
	editDetails;
}
elsif ( param("DoWhat") eq "Update" )
{
	updateDetails;
}
else
{
	general;
	displayDetails;
}

print <<"__END__";
</body>
</html>
__END__
