#!/usr/bin/perl

use lib "../include";
use personalise;
use CGI ':standard';
use DBI();

my $coname=param("coname");
my $CoID=param("id");
my $DoWhat = param("DoWhat");
my $next = param("DoNext");

print header();
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

sub AddContact
{
	my $coname=param("coname");
        my $name=param("custname");
	$name=~s/'/''/g;
        my $add1=param("add1");
        my $add2=param("add2");
        my $add3=param("add3");
        my $town=param("town");
        my $county=param("county");
        my $pcode=param("pcode");
        my $country=param("country");
        my $phone=param("phone");
        my $mobile=param("mobile");
        my $fax=param("fax");
        my $notes=param("notes");
	$notes=~s/'/''/g;

	my $dbh = DBI->connect("DBI:mysql:database=accounts;host=localhost","$DBUSER","$DBPASS") || die "Unable to connect to database";
        $dbh->do("INSERT INTO CustomerContacts (CoID,Name,Address1,Address2,Address3,TownCity,County,Country,Postcode,Phone,Mobile,Fax,Notes,email) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)",undef,$CoID,"$name","$add1","$add2","$add3","$town","$county","$country","$pcode","$phone","$mobile","$fax","$notes","$email");
	my $sth=$dbh->prepare("SELECT CustContactID FROM CustomerContacts WHERE CoID=$CoID AND Name='$name'");
	$sth->execute();
	my $ref=$sth->fetch_hashref();
	my $CCID=$ref->{CustContactID};
	$sth->finish();
	$dbh->do("INSERT INTO History (TableName,ID,Action,ModifiedBy,ModifiedDate) VALUES(?,?,?,?,Now())",undef,"CustomerContacts","$CCID","UPDATE","$ENV{'REMOTE_USER'}");
	$dbh->disconnect();

	print "<h3>Contact added to database</h3>";
}

sub drawForm
{
	print <<"__END__";
		<td align=left valign=top><h1>Add A Contact for $coname</h1>
		<form name=contactadd method=post action="AddContact.cgi">
		<input type=hidden name=DoWhat value=$next>
		<input type=hidden name=coname value="$coname">
		<input type=hidden name=id value=$CoID>
		<table>
		<tr><td>Name:</td><td><input type=text name=custname size=80></td></tr>
		<tr><td>&nbsp;</td></tr>
		<tr><td valign=top>Address:</td><td><input type=text name=add1 size=80><br>
					<input type=text name=add2 size=80><br>
					<input type=text name=add3 size=80></td></tr>
		<tr><td>Town/City:</td><td><input type=text name=town size=60></td></tr>
		<tr><td>County:</td><td><input type=text name=county size=60></td></tr>
		<tr><td>Post Code:</td><td><input type=text name=pcode size=20></td></tr>
__END__

	print "<tr><td>Country:</td><td><select name=country>";
	my $dbh = DBI->connect("DBI:mysql:database=accounts;host=localhost","$DBUSER","$DBPASS") || die "Unable to connect to database";
	my $sth = $dbh->prepare("SELECT * FROM Countries Order By CountryText");
	$sth->execute();
	while ( my $ref = $sth->fetchrow_hashref() )
	{
		if ( $ref->{'CountryID'} eq "UK" )
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
		<tr><td>Telephone:</td><td><input type=text name=phone size=30></td></tr>
		<tr><td>Mobile:</td><td><input type=text name=mobile size=30></td></tr>
		<tr><td>Fax:</td><td><input type=text name=fax size=30></td></tr>
		<tr><td>&nbsp;</td></tr>
		<tr><td>Notes:</td><td><textarea name=notes cols=60 rows=5></textarea></td></tr>
		<tr><td>&nbsp;</td></tr>
		<tr><td colspan=2 align=center><input type=submit value='Add Contact' name='Add'> &nbsp; <input type=reset value='Clear Fields'></td></tr>
		</table>
	</td></tr>
__END__
}

if ( "$DoWhat" eq "Add" )
{
	AddContact;
}
else
{
	drawForm;
}
print <<"__END__";
</table>
</body>
</html>
__END__
