SET foreign_key_checks = 0;

-- Set the invoice number
INSERT INTO Invoice (InvoiceNo,CoID,CustContactID,InvoiceDay,InvoiceMonth,InvoiceYear,AlternateCurrency) VALUES(101001,0,0,0,0,0,0);

-- Populate currency types
INSERT INTO CurrencyType (CurrencyType,CurrencyName) VALUES("EURO","Euro");
INSERT INTO CurrencyType (CurrencyType,CurrencyName) VALUES("USD","US Dollar");
INSERT INTO CurrencyType (CurrencyType,CurrencyName) VALUES("GBP","UK Sterling");

-- Populate Categories
INSERT INTO Category (CatName) VALUES ("IT Training");
INSERT INTO Category (CatName) VALUES ("Other Training");
INSERT INTO Category (CatName) VALUES ("Therapy");
INSERT INTO Category (CatName) VALUES ("CD Sales");
INSERT INTO Category (CatName) VALUES ("Web Site Sales");
INSERT INTO Category (CatName) VALUES ("Other Income");

-- Populate Payment Terms
INSERT INTO PaymentTerms (PaymentTerms) VALUES ("7 days (1 Week)");
INSERT INTO PaymentTerms (PaymentTerms) VALUES ("14 days (2 Weeks)");
INSERT INTO PaymentTerms (PaymentTerms) VALUES ("30 days (1 Month)");
INSERT INTO PaymentTerms (PaymentTerms) VALUES ("42 days (6 Weeks)");
INSERT INTO PaymentTerms (PaymentTerms) VALUES ("60 days (2 Months)");
INSERT INTO PaymentTerms (PaymentTerms) VALUES ("90 days (3 Months)");

-- Populate Countries
INSERT INTO Countries VALUES ("UK", "United Kingdom");
INSERT INTO Countries VALUEs ("USA", "United States of America");
INSERT INTO Countries VALUES ("IE", "Ireland");
INSERT INTO Countries VALUES ("NL", "Netherlands");
INSERT INTO Countries VALUES ("ESP", "Spain");
INSERT INTO Countries VALUES ("FR", "France");
INSERT INTO Countries VALUES ("G", "Germany");
INSERT INTO Countries VALUES ("BL", "Belgium");

-- Populate TAX Rates
INSERT INTO TAXRates VALUES ("HOME", "EC Home VAT", 17.5);
INSERT INTO TAXRates VALUES ("ZERO", "Zero Rate", 0.00);
INSERT INTO TAXRates VALUES ("EXPT", "VAT Exempt", 0.00);

SET foreign_key_checks = 1;
