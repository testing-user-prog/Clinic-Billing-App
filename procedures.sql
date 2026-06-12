DROP VIEW IF EXISTS getdoctornames
GO
CREATE VIEW getdoctornames
AS
SELECT Name FROM Doctor
GO

-- Update doctor fee
DROP PROCEDURE IF EXISTS updatedoctorfee
GO
CREATE PROCEDURE updatedoctorfee
    @doc_name varchar(50),
    @new_fee int
AS
BEGIN
    UPDATE Doctor
    SET fee = @new_fee
    WHERE Name = @doc_name
END
GO

-- Search medicines by name (for the search box in UI)
DROP PROCEDURE IF EXISTS searchmedicines
GO
CREATE PROCEDURE searchmedicines
    @medicine_name varchar(150)
AS
BEGIN
    SELECT medicineid, MedicineName, Price, StockQuantity
    FROM Medicines
    WHERE MedicineName LIKE '%' + @medicine_name + '%'
END
GO

-- Increase medicine price
DROP PROCEDURE IF EXISTS increasemedicineprice
GO
CREATE PROCEDURE increasemedicineprice
    @medicineid int,
    @new_price decimal(10,2)
AS
BEGIN
    IF NOT EXISTS (SELECT 1 FROM Medicines WHERE medicineid = @medicineid)
    BEGIN
        RAISERROR('Medicine not found.', 16, 1)
        RETURN
    END
    UPDATE Medicines
    SET Price = @new_price
    WHERE medicineid = @medicineid
END
GO

-- Increase stock quantity
DROP PROCEDURE IF EXISTS increasestockquantity
GO
CREATE PROCEDURE increasestockquantity
    @medicineid int,
    @quantity int
AS
BEGIN
    IF NOT EXISTS (SELECT 1 FROM Medicines WHERE medicineid = @medicineid)
    BEGIN
        RAISERROR('Medicine not found.', 16, 1)
        RETURN
    END
    UPDATE Medicines
    SET StockQuantity = StockQuantity + @quantity
    WHERE medicineid = @medicineid
END
GO

-- Decrease stock quantity (when patient purchases a medicine)
DROP PROCEDURE IF EXISTS decreasestockquantity
GO
CREATE PROCEDURE decreasestockquantity
    @medicineid int,
    @quantity int
AS
BEGIN
    IF NOT EXISTS (SELECT 1 FROM Medicines WHERE medicineid = @medicineid)
    BEGIN
        RAISERROR('Medicine not found.', 16, 1)
        RETURN
    END

    DECLARE @current_stock int
    SELECT @current_stock = StockQuantity FROM Medicines WHERE medicineid = @medicineid

    IF @current_stock < @quantity
    BEGIN
        RAISERROR('Insufficient stock.', 16, 1)
        RETURN
    END

    UPDATE Medicines
    SET StockQuantity = StockQuantity - @quantity
    WHERE medicineid = @medicineid
END
GO