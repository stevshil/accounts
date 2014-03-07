#!/usr/bin/perl

use lib "../include";
use personalise;
use CGI ':standard';
use DBI();

my $rowcount=0;
my $bgcolour="#f3f0f9";
my $selectedChar = param("start");

my $DoWhat = param("DoWhat");
my $ID=param("id");

print header();

print <<"__END__";
<html>
<head>
<title>$COMPANYNAME, Accounting System for VAT Rates</title>
<link rel="stylesheet" href="../main.css" type="text/css">
<link rel="stylesheet" href="../style.css" type="text/css">
__END__

open (INCFILE, "<../include/management.inc") || die "No such file";
my @INCFILE = <INCFILE>;
close INCFILE;
@INCFILE=doPersonalise(@INCFILE);
print "@INCFILE";

sub displayRates
{
	print <<"__END__";
	<td align=left valign=top><h1>VAT Rates </h1>
	<p>Click on the ID column number to view/edit VAT details.<br><br>
	<table width="100%" border=0 cellspacing=0 cellpadding=0>
	<tr><th align=left width=25>ID</th><th align=left width=250>Name</th><th align=left width=250>Rate</th></tr>
__END__

	# Table generation for company list
	# Format of table:	CompanyID as link, Company Name, Telephone, Postcode, 1st Address Line, Contact
	
	my $dbh = DBI->connect("DBI:mysql:database=accounts;host=localhost","$DBUSER","$DBPASS") || die "Unable to connect to database";
	$sth = $dbh->prepare("SELECT * FROM TAXRates");
	$sth->execute();
	while ( my $ref = $sth->fetchrow_hashref() )
	{
		
		my $rowcolour="bgcolor='$bgcolour'" if ( ($rowcount % 2) != 0 );
		$rowcount++;
		print "<tr $rowcolour><td><a href='VAT.cgi?id=$ref->{'TAXID'}&DoWhat=Edit'>$ref->{'TAXID'}</a></td>";
		print "<td>$ref->{'TAXName'}</td><td>$ref->{'TAXRate'}</tr>\n";
		$rowcolour=undef;
	}
	$sth->finish();
	$dbh->disconnect();

	print <<"__END__";
		</table>
__END__
}

sub EditRate
{
	print <<"__END__";
	<td align=left valign=top><h1>VAT Rates </h1>
	<p>Click on the ID column number to view/edit VAT details.<br><br>
	<table width="100%" border=0 cellspacing=0 cellpadding=0>
	<tr><th align=left width=25>ID</th><th align=left width=250>Name</th><th align=left width=250>Rate</th></tr>
__END__

	# Table generation for company list
	# Format of table:	CompanyID as link, Company Name, Telephone, Postcode, 1st Address Line, Contact
	
	print "<form name=Edit action='VAT.cgi'>";
	my $dbh = DBI->connect("DBI:mysql:database=accounts;host=localhost","$DBUSER","$DBPASS") || die "Unable to connect to database";
	$sth = $dbh->prepare("SELECT * FROM TAXRates");
	$sth->execute();
	print "<input type=hidden name=DoWhat value=Update>";
	while ( my $ref = $sth->fetchrow_hashref() )
	{
		my $rowcolour="bgcolor='$bgcolour'" if ( ($rowcount % 2) != 0 );
		$rowcount++;
		
		
		if ( $ref->{'TAXID'} eq $ID )
		{
			print "<tr $rowcolour><td>$ref->{'TAXID'}";
			print "<input type=hidden name=id value='$ref->{TAXID}'></td>";
			print "<td><input type=text name=TAXName value='$ref->{TAXName}'></td><td><input type=text name=TAXRate value='$ref->{TAXRate}'></td></tr>\n";
		}
		else
		{
			print "<tr $rowcolour><td><a href='VAT.cgi?id=$ref->{'TAXID'}&DoWhat=Edit'>$ref->{'TAXID'}</a></td>";
			print "<td>$ref->{'TAXName'}</td><td>$ref->{'TAXRate'}</tr>\n";
		}
		$rowcolour=undef;
	}
	$sth->finish();
	$dbh->disconnect();

	print <<"__END__";
	<tr><td colspan=3><input type=submit value=Update> <input type=button value=Back onClick='history(-1)'></td></tr>
		</table>
__END__

}

sub Updating
{
	my ($TAXName,$TAXRate) = @_;
	# Update values
	my $dbh = DBI->connect("DBI:mysql:database=accounts;host=localhost","$DBUSER","$DBPASS") || die "Unable to connect to database";
	my $SQLstring="UPDATE TAXRates SET TAXName='$TAXName', TAXRate=$TAXRate WHERE TAXID='$ID'";
	$dbh->do($SQLstring);
	$dbh->do("INSERT INTO History (TableName,ID,Action,ModifiedBy,ModifiedDate) VALUES(?,?,?,?,Now())",undef,"TAXRates","$ID","UPDATE","$ENV{'REMOTE_USER'}");
	$dbh->disconnect();
	displayRates();
}

sub general
{
	print <<"__END__";
	</td></tr>
</table>
</body>
</html>
__END__
}

if ( $DoWhat eq "Edit" )
{
	EditRate();
	general();
}
elsif ( $DoWhat eq "Update" )
{
	my $TAXRate = param("TAXRate");
	my $TAXName = param("TAXName");
	Updating($TAXName,$TAXRate);
	general();
}
else
{
	displayRates();
	general();
}
