#!/usr/bin/perl

use lib "../include";
use personalise;
use CGI ':standard';
use DBI();

print header();
print <<"__END__";

<html>
<head>
<title>$COMPANYNAME, Accounting System for Invoicing, Add Company</title>
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

print <<"__END__";
	<td align=left valign=top><h1>Add A Company</h1>
	<form name=companyadd method=post action="addco.cgi">
	<table>
	<tr><td>Company Name:</td><td><input type=text name=coname size=80></td></tr>
	<tr><td>Contact Name:</td><td><input type=text name=contactname size=80></td></tr>
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
	<tr><td>Fax:</td><td><input type=text name=fax size=30></td></tr>
	<tr><td>&nbsp;</td></tr>
	<tr><td>Payment Terms:</td><td><select name=payterm>
__END__

$dbh = DBI->connect("DBI:mysql:database=accounts;host=localhost","$DBUSER","$DBPASS") || die "Unable to connect to database";
$sth = $dbh->prepare("SELECT * FROM PaymentTerms");
$sth->execute();
while ( my $ref = $sth->fetchrow_hashref() )
{
	print "<option value=$ref->{'PaymentTermsID'}>$ref->{'PaymentTerms'}</option>";
}
$sth->finish();
$dbh->disconnect();
print "</select></td></tr>";
	
print <<"__END__";
	<tr><td>&nbsp;</td></tr>
	<tr><td>No Longer Used?:</td><td><input type=checkbox name=notused></td></tr>
	<tr><td colspan=2 align=center><div id=hideme><input type=submit value='Add Customer' name='Add' onclick='hidebtn()'> &nbsp; <input type=reset value='Clear Fields'></div></td></tr>
	</table>
	</td></tr>
</table>
</body>
</html>
__END__
