#!/usr/bin/perl

use lib "../include";
use personalise;
use CGI ':standard';
use CGI::Carp 'fatalsToBrowser';
use DBI();

my $rowcount=0;
my $bgcolour="#f3f0f9";

my $coname = param("coname");
my $contactname = param("contactname");
my $add1 = param("add1");
my $add2 = param("add2");
my $add3 = param("add3");
my $town = param("town");
my $county = param("county");
my $country = param("country");
my $pcode = param("pcode");
my $phone = param("phone");
my $fax = param("fax");
my $payterm = param("payterm");
my $notused="";

print header();
if ( (!defined $coname) || $coname =~ /^ *$/ )
{
	print start_html();
	print "<script language=JavaScript>history.go(-1)</script>";
	print end_html;
}
print <<"__END__";

<html>
<head>
<title>$COMPANYNAME, Accounting System for Invoicing, Add Company</title>
<link rel="stylesheet" href="../main.css" type="text/css">
<link rel="stylesheet" href="../style.css" type="text/css">
__END__

# include header file
open (INCFILE, "<../include/companies.inc") || die "No such file";
my @INCFILE = <INCFILE>;
close INCFILE;
@INCFILE=doPersonalise(@INCFILE);
print "@INCFILE";

print <<"__END__";
	<td align=left valign=top><h1>Add A Company</h1>
	<p>Click on <b>YES</b> to re-enable the company<br>Click on the <b>ID</b> to edit the company details<br><br></p>
	<table border=0 cellspacing=0 cellpadding=0>
	<tr><td>&nbsp;</td></tr>
__END__

# Check if company name already exists
my $dbh = DBI->connect("DBI:mysql:database=accounts;host=localhost","$DBUSER","$DBPASS") || die "Unable to connect to database";
my $sth = $dbh->prepare("SELECT count(CoID) As Companies FROM CustomerDetails WHERE Postcode = '$pcode'");

$sth->execute();
my $counter = $sth->fetchrow_hashref();
if ( $counter->{'Companies'} > 0 )
{
	# Company exists display details
	print "<tr><td colspan=5>Company exists in database, or has same postcode as another company.  Found ", $counter->{'Companies'}, " companies.</td></tr>";
	print "<tr><td colspan=5>&nbsp;</td></tr>";

	$sth->finish();
	$sth = $dbh->prepare("SELECT CoID, CompanyName, Address1, Postcode, Phone, Deleted FROM CustomerDetails WHERE Postcode = '$pcode'");
	$sth->execute();

	print "<tr><th width=25 align=left>ID</td><th width=250 align=left>Company Name</td><th width=250 align=left>Address</td><th width=100 align=left>Postcode</td><th width=150 align=left>Phone</td><th align=center>Undelete?</td></tr>\n";
	while ( my $ref = $sth->fetchrow_hashref() )
	{
		my $rowcolour="bgcolor=$bgcolour" if ( ($rowcount % 2) != 0 );
		$rowcount++;
		print "<tr $rowcolour><td><a href='CoDetails.cgi?id=$ref->{'CoID'}'>$ref->{'CoID'}</a></td>";
		print "<td>$ref->{'CompanyName'}</td><td>$ref->{'Address1'}</td>";
		print "<td>$ref->{'Postcode'}</td><td>$ref->{'Phone'}</td>";
		if ( $ref->{'Deleted'} eq 'Y' )
		{
			print "<td align=center><a href='undelete.cgi?id=$ref->{'CoID'}'>YES</a></td></tr>\n";
		}
		else
		{
			print "<td>&nbsp;</td>";
		}
	}
print <<"__END__";
	<form name=stilladd action='pleaseadd.cgi' method=post>
	<input type=hidden name=coname value="$coname">
        <input type=hidden name=contactname value="$contactname">
	<input type=hidden name=add1 value="$add1">
	<input type=hidden name=add2 value="$add2">
	<input type=hidden name=add3 value="$add3">
	<input type=hidden name=town value="$town">
	<input type=hidden name=county value="$county">
	<input type=hidden name=country value="$country">
	<input type=hidden name=pcode value="$pcode">
	<input type=hidden name=phone value="$phone">
	<input type=hidden name=fax value="$fax">
	<input type=hidden name=payterm value="$payterm">
	<input type=hidden name=notused value="$notused">
	<tr><td colspan=5 align=center><input type=submit value="YES Add Company"> &nbsp; &nbsp; <input type=button onClick="javascript:history.go(-1)" value='Cancel'></td></tr>
	</form>
__END__
}
else
{
	$coname=~s/'/''/g;
        $contactname=~s/'/''/g;
	# Add company
	$dbh->do("INSERT INTO CustomerDetails (CompanyName,Address1,Address2,Address3,TownCity,County,Country,Postcode,Phone,Fax,PaymentTermsID,Deleted) VALUES(?,?,?,?,?,?,?,?,?,?,?,?)",undef,"$coname","$add1","$add2","$add3","$town","$county","$country","$pcode","$phone","$fax","$payterm","$notused");
	my $sth = $dbh->prepare("SELECT CoID FROM CustomerDetails WHERE CompanyName = '$coname' AND Postcode = '$pcode'");
        $sth->execute();
        my $ref=$sth->fetchrow_hashref();
        my $COID = $ref->{CoID};
	$sth->finish();

        $dbh->do("INSERT INTO CustomerContacts (CoID,Name,Address1,Address2,Address3,TownCity,County,Country,PostCode,Phone,Fax) VALUES(?,?,?,?,?,?,?,?,?,?,?)",undef,$COID,"$contactname","$add1","$add2","$add3","$town","$county","$country","$pcode","$phone","$fax");
	$sth = $dbh->prepare("SELECT CustContactID FROM CustomerContacts WHERE CoID=$COID");
	$sth->execute();
	$ref=$sth->fetchrow_hashref();
	my $CCID=$ref->{CustContactID};
	$sth->finish();
	$dbh->do("INSERT INTO History (TableName,ID,Action,ModifiedBy,ModifiedDate) VALUES(?,?,?,?,Now())",undef,"CustomerDetails","$COID","ADD","$ENV{'REMOTE_USER'}");
	$dbh->do("INSERT INTO History (TableName,ID,Action,ModifiedBy,ModifiedDate) VALUES(?,?,?,?,Now())",undef,"CustomerContacts","$CCID","ADD","$ENV{'REMOTE_USER'}");
	print "<h3>Company added to database</h3>";
}
#$sth->finish();
$dbh->disconnect();

print <<"__END__";
	</td></tr>
	</table>
</table>
</body>
</html>
__END__
