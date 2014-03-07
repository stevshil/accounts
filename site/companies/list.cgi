#!/usr/bin/perl

use lib "../include";
use personalise;
use CGI ':standard';
use DBI();

my $rowcount=0;
my $bgcolour="#f3f0f9";
my $selectedChar = param("start");

print header();

print <<"__END__";
<html>
<head>
<title>$COMPANYNAME, Accounting System for Invoicing, Company Options</title>
<link rel="stylesheet" href="../main.css" type="text/css">
<link rel="stylesheet" href="../style.css" type="text/css">
__END__

open (INCFILE, "<../include/companies.inc") || die "No such file";
my @INCFILE = <INCFILE>;
close INCFILE;
@INCFILE=doPersonalise(@INCFILE);
print "@INCFILE";

print <<"__END__";
	<td align=left valign=top><h1>$COMPANYNAME Customers </h1>
	<p>Click on the ID column number to view/edit company details.<br><br>
__END__

print "<table cellpadding=10><tr>";
print "<td><a href='list.cgi?start='>ALL</a></td>";
for $char ('A' .. 'Z')
{
	print "<td><a href='list.cgi?start=$char'>$char</a></td>";
}
print "</tr></table>";

print <<"__END__";
	<table width="100%" border=0 cellspacing=0 cellpadding=0>
	<tr><th align=left width=25>ID</th><th align=left width=250>Company Name</th><th align=left width=250>Address</th><th align=left width=100>Postcode</th><th align=left width=150>Phone</th><th align=center>Add/Edit Contacts</th></tr>
__END__

# Table generation for company list
# Format of table:	CompanyID as link, Company Name, Telephone, Postcode, 1st Address Line, Contact

my $dbh = DBI->connect("DBI:mysql:database=accounts;host=localhost","$DBUSER","$DBPASS") || die "Unable to connect to database";
my $sth="";
if ( $selectedChar ne "" )
{
	$sth = $dbh->prepare("SELECT CoID, CompanyName, Address1, Postcode, Phone FROM CustomerDetails WHERE Deleted != 'Y' AND CompanyName like '$selectedChar%' Order by 'CompanyName'");
}
else
{
	$sth = $dbh->prepare("SELECT CoID, CompanyName, Address1, Postcode, Phone FROM CustomerDetails WHERE Deleted != 'Y' Order by 'CompanyName'");
}
$sth->execute();
while ( my $ref = $sth->fetchrow_hashref() )
{
	
	my $rowcolour="bgcolor='$bgcolour'" if ( ($rowcount % 2) != 0 );
	$rowcount++;
	print "<tr $rowcolour><td><a href='CoDetails.cgi?id=$ref->{'CoID'}&DoWhat=Display'>$ref->{'CoID'}</a></td>";
	print "<td>$ref->{'CompanyName'}</td><td>$ref->{'Address1'}&nbsp;</td>";
	print "<td>$ref->{'Postcode'}&nbsp;</td><td>$ref->{'Phone'}&nbsp;</td>";
	print "<td align=center><a href='CoContacts.cgi?id=$ref->{'CoID'}&DoWhat=list'>Add/Edit/View Contacts</a>&nbsp;</td></tr>\n";
	$rowcolour=undef;
}
$sth->finish();
$dbh->disconnect();

print <<"__END__";
	</table>
	</td></tr>
</table>
</body>
</html>
__END__
