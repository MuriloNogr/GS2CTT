LOAD DATA
INFILE './Matrizes.csv'
APPEND
INTO TABLE Matrizes
FIELDS TERMINATED BY ',' optionally enclosed by '"'
TRAILING NULLCOLS
(
    Node_ID CHAR(255),
    Centroide CHAR(255),
    UF CHAR(2)
)