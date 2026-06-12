CREATE TABLE Medicines (
    medicineid Int Identity(0,1),
    MedicineName VARCHAR(150) Unique not null,
    Price DECIMAL(10,2) not null,
    StockQuantity INT default 1
);
CREATE TABLE Doctor
(
doctorid int Identity(0,1),
Name varchar(50) not null,
fee int not null

);
