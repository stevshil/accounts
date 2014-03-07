package personalise;

use base 'Exporter';

our @EXPORT = qw(doPersonalise $COMPANYNAME $INTERESTRATE $COMPANYADDRESS $COMPANYDOMAIN $COMPANYPHONE $COMPANYREGNO $COMPANYVATNO $DBUSER $DBPASS);

our $COMPANYNAME="TPS Services Ltd";
our $INTERESTRATE="1.5";
our $COMPANYADDRESS="Comma seperated, &nbsp web spacing address";
our $COMPANYDOMAIN="webDomainWithoutWWW";
our $COMPANYPHONE="yourPhoneNo";
our $COMPANYREGNO="yourCoNo";
our $COMPANYVATNO="yourVATNO";
our $DBUSER="yourDBuser";
our $DBPASS="yourDBpassword";

sub doPersonalise
{
	my (@INCFILE) = @_;
	for my $line (@INCFILE)
	{
        	$line=~s/\$COMPANYNAME/$COMPANYNAME/g;
        	$line=~s/\$INTERESTRATE/$INTERESTRATE/g;
        	$line=~s/\$COMPANYADDRESS/$COMPANYADDRESS/g;
        	$line=~s/\$COMPANYDOMAIN/$COMPANYDOMAIN/g;
        	$line=~s/\$COMPANYPHONE/$COMPANYPHONE/g;
        	$line=~s/\$COMPANYREGNO/$COMPANYREGNO/g;
        	$line=~s/\$COMPANYVATNO/$COMPANYVATNO/g;
		$line=~s/\$LOGNAME/$ENV{REMOTE_USER}/g;
	}

	return @INCFILE;
}

1;
