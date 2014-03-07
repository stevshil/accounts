create table PaymentTerms ( PaymentTermsID SMALLINT NOT NULL AUTO_INCREMENT,
				PaymentTerms VARCHAR(100) NOT NULL,
				PRIMARY KEY (PaymentTermsID)
			) TYPE=INNODB; 

create table CustomerDetails ( CoID BIGINT NOT NULL AUTO_INCREMENT,
				CompanyName VARCHAR(150) NOT NULL,
				Address1 VARCHAR(150) NULL,
				Address2 VARCHAR(150) NULL,
				Address3 VARCHAR(150) NULL,
				TownCity VARCHAR(150) NULL,
				County VARCHAR(150) NULL,
				Country VARCHAR(4) NULL,
				Postcode VARCHAR(10) NULL,
				Phone VARCHAR(25) NULL,
				Fax VARCHAR(25) NULL,
				PaymentTermsID SMALLINT NULL,
				Deleted CHAR(1) NULL,
				PRIMARY KEY (CoID),
				INDEX payID (PaymentTermsID),
				FOREIGN KEY (PaymentTermsID) REFERENCES PaymentTerms(PaymentTermsID) ON DELETE CASCADE
			) TYPE=INNODB;

create table CustomerContacts ( CustContactID BIGINT NOT NULL AUTO_INCREMENT,
				CoID BIGINT NOT NULL,
				Name VARCHAR(150) NOT NULL,
				Address1 VARCHAR(150) NULL,
				Address2 VARCHAR(150) NULL,
				Address3 VARCHAR(150) NULL,
				TownCity VARCHAR(150) NULL,
				County VARCHAR(150) NULL,
				Country VARCHAR(4) NULL,
				Postcode VARCHAR(10) NULL,
				Phone VARCHAR(25) NULL,
				Mobile VARCHAR(25) NULL,
				Fax VARCHAR(25) NULL,
				email VARCHAR(200) NULL,
				Notes LONGTEXT NULL,
				PRIMARY KEY (CustContactID),
				INDEX CompID (CoID),
				FOREIGN KEY (CoID) REFERENCES CustomerDetails(CoID) ON DELETE CASCADE
			) TYPE=INNODB;

create table CurrencyType ( CurrencyType VARCHAR(4) NOT NULL UNIQUE,
				CurrencyName VARCHAR(15),
				PRIMARY KEY (CurrencyType)
			) TYPE=INNODB;

create table Category ( CategoryID INT NOT NULL AUTO_INCREMENT,
			CatName VARCHAR(50),
			PRIMARY KEY (CategoryID)
			) TYPE=INNODB;

create table Invoice ( InvoiceNo BIGINT NOT NULL AUTO_INCREMENT,
			CoID BIGINT NOT NULL,
			CustContactID BIGINT NOT NULL,
			InvoiceDay SMALLINT NOT NULL,
			InvoiceMonth SMALLINT NOT NULL,
			InvoiceYear MEDIUMINT NOT NULL,
			AlternateCurrency CHAR(1) NOT NULL,
			CurrencyType VARCHAR(4) NULL,
			CurrencyRate NUMERIC(5,2) NULL,
			Posted CHAR(1) NULL,
			CategoryID INT NULL,
			PrintedYear BIGINT NULL,
			PrintedMonth BIGINT NULL,
			PrintedDay BIGINT NULL,
			PRIMARY KEY (InvoiceNo),
			INDEX CompID2 (CoID),
			FOREIGN KEY (CoID) REFERENCES CustomerDetails(CoID) ON DELETE CASCADE,
			INDEX CustContID (CustContactID),
			FOREIGN KEY (CustContactID) REFERENCES CustomerContacts(CustContactID) ON DELETE CASCADE,
			INDEX CurType (CurrencyType),
			FOREIGN KEY (CurrencyType) REFERENCES CurrencyType(CurrencyType),
			INDEX CatID (CategoryID),
			FOREIGN KEY (CategoryID) REFERENCES Category(CategoryID)
			) TYPE=INNODB;

create table InvoiceDetails ( InvDetID BIGINT NOT NULL AUTO_INCREMENT,
				InvoiceNo BIGINT NOT NULL,
				Description VARCHAR(200) NOT NULL,
				Quantity MEDIUMINT NULL,
				NetAmtUKP NUMERIC(10,2) NULL,
				AltCurrencyValue NUMERIC(15,2) NULL,
				VATRate NUMERIC(6,2) NULL,
				GrossAmtUKP NUMERIC(15,2) NULL,
				AltGrossAmt NUMERIC(20,2) NULL,
				PRIMARY KEY (InvDetID),
				INDEX InvNo (InvoiceNo),
				FOREIGN KEY (InvoiceNo) REFERENCES Invoice(InvoiceNo) ON DELETE CASCADE
			) TYPE=INNODB;

create table Payments ( PaymentID BIGINT NOT NULL AUTO_INCREMENT,
			InvoiceNo BIGINT NOT NULL,
			PaymentDay SMALLINT NULL,
			PaymentMonth SMALLINT NULL,
			PaymentYear SMALLINT NULL,
			AmtPaidUKP NUMERIC(15,2) NULL,
			AmtPaidAltCur NUMERIC(20,2) NULL,
			PaymentMethod VARCHAR(100) NULL,
			PaymentRef VARCHAR(100) NULL,
			PRIMARY KEY (PaymentID),
			INDEX InvNo2 (InvoiceNo),
			FOREIGN KEY (InvoiceNo) REFERENCES Invoice(InvoiceNo) ON DELETE CASCADE
			) TYPE=INNODB;

create table PettyCash ( PettyCashID BIGINT NOT NULL AUTO_INCREMENT,
			Description VARCHAR(200) NULL,
			PaymentID BIGINT NULL REFERENCES Payments(PaymentID),
			AmtNet NUMERIC(20,2) NULL,
			AmtGross NUMERIC(20,2) NULL,
			PRIMARY KEY (PettyCashID)
			) TYPE=INNODB;

create table Countries ( CountryID VARCHAR(4) NOT NULL,
			 CountryText VARCHAR(100) NOT NULL,
			 PRIMARY KEY (CountryID)
			) TYPE=INNODB;

create table TAXRates ( TAXID VARCHAR(6) NOT NULL,
			TAXName VARCHAR(50) NOT NULL,
			TAXRate NUMERIC(6,2) NOT NULL,
			PRIMARY KEY (TAXID)
			) TYPE=INNODB;

create table History ( HistoryID BIGINT NOT NULL AUTO_INCREMENT,
			TableName VARCHAR(30) NOT NULL,
			ID VARCHAR(50) NOT NULL,
			Action VARCHAR(20) NOT NULL,
			ModifiedBy VARCHAR(30) NOT NULL,
			ModifiedDate DATETIME NOT NULL,
			PRIMARY KEY (HistoryID)
) TYPE=INNODB;
