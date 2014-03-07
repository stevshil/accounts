#!/usr/bin/perl

use lib "../include";
use personalise;
use CGI ':standard';
use DBI();

my $id = param('id');

my $rowcount=0;
my $bgcolour="#f3f0f9";

sub deletecos
{
	my $SQLstring = "UPDATE CustomerDetails set Deleted='Y' WHERE CoID=$id";
	my $dbh = DBI->connect("DBI:mysql:database=accounts;host=localhost","$DBUSER","$DBPASS") || die "Unable to connect to database";
	$dbh->do($SQLstring);
	$dbh->do("INSERT INTO History (TableName,ID,Action,ModifiedBy,ModifiedDate) VALUES(?,?,?,?,Now())",undef,"CustomerDetails","$id","Deleted","$ENV{'REMOTE_USER'}");
	$dbh->disconnect();
}

sub listcos
{
	print <<"__END__";
		<td align=left valign=top><h1>$COMPANYNAME Customers, Removal page</h1>
		<p>Click on the <b>ID</b> to remove the customer<br><br></p>
		<table width="100%" border=0 cellspacing=0 cellpadding=0>
		<tr><th align=left width=25>ID</th><th align=left width=250>Company Name</th><th align=left width=250>Address</th><th align=left width=100>Postcode</th><th align=left width=150>Phone</th></tr>
__END__

	my $dbh = DBI->connect("DBI:mysql:database=accounts;host=localhost","$DBUSER","$DBPASS") || die "Unable to connect to database";
	my $sth = $dbh->prepare("SELECT CoID, CompanyName, Address1, Postcode, Phone FROM CustomerDetails WHERE Deleted != 'Y'");
	$sth->execute();
	while ( my $ref = $sth->fetchrow_hashref() )
	{
		my $rowcolour="bgcolor='$bgcolour'" if ( ($rowcount % 2) != 0 );
        	$rowcount++;
		print "<tr $rowcolour><td><a href='remove.cgi?id=$ref->{'CoID'}'>$ref->{'CoID'}</a>&nbsp;</td>";
		print "<td>$ref->{'CompanyName'}&nbsp;</td><td>$ref->{'Address1'}&nbsp;</td>";
		print "<td>$ref->{'Postcode'}&nbsp;</td><td>$ref->{'Phone'}&nbsp;</td></tr>";
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

}

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

if ( defined param('id') )
{
	deletecos;
	listcos;
}
else
{
	listcos;
}
