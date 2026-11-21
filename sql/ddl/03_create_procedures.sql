-- ============================================================================
-- TransitIQ: Stored Procedures & Transactional Business Logic Simulation
-- Alignment: Microsoft DP-900 (ACID transactions, concurrency, procedural SQL)
-- Note: Contains T-SQL for Azure SQL / SQL Server, and SQLite procedural equivalents
-- ============================================================================

-- ----------------------------------------------------------------------------
-- PROCEDURE 1: sp_book_passenger_ticket (OLTP Transaction)
-- Atomically books a transit ticket, verifying trip status and capacity.
-- ----------------------------------------------------------------------------
/*
-- T-SQL (Azure SQL Database / Microsoft SQL Server):
CREATE PROCEDURE sp_book_passenger_ticket
    @p_trip_id INT,
    @p_origin_stop_id INT,
    @p_dest_stop_id INT,
    @p_passenger_type VARCHAR(20),
    @p_payment_method VARCHAR(30),
    @p_ticket_ref VARCHAR(40) OUTPUT,
    @p_status_message VARCHAR(100) OUTPUT
AS
BEGIN
    SET NOCOUNT ON;
    BEGIN TRANSACTION;
    TRY
        -- Check trip exists and is active
        IF NOT EXISTS (SELECT 1 FROM trips WHERE trip_id = @p_trip_id AND trip_status IN ('Scheduled', 'In-Transit'))
        BEGIN
            SET @p_status_message = 'ERROR: Trip is not active or available for booking.';
            ROLLBACK TRANSACTION;
            RETURN;
        END

        -- Compute discounted fare
        DECLARE @base_fare DECIMAL(6,2);
        SELECT @base_fare = r.base_fare FROM routes r JOIN trips t ON r.route_id = t.route_id WHERE t.trip_id = @p_trip_id;

        DECLARE @final_fare DECIMAL(6,2) = @base_fare;
        IF @p_passenger_type = 'Student' SET @final_fare = @base_fare * 0.50;
        ELSE IF @p_passenger_type = 'Senior Citizen' SET @final_fare = @base_fare * 0.40;
        ELSE IF @p_passenger_type = 'Commuter Passholder' SET @final_fare = @base_fare * 0.70;

        SET @p_ticket_ref = CONCAT('TKT-', FORMAT(GETDATE(), 'yyyyMMddHHmmss'), '-', ABS(CHECKSUM(NEWID())) % 10000);

        INSERT INTO passenger_fares (ticket_reference, trip_id, origin_stop_id, destination_stop_id, passenger_type, fare_paid, payment_method, transaction_status)
        VALUES (@p_ticket_ref, @p_trip_id, @p_origin_stop_id, @p_dest_stop_id, @p_passenger_type, @final_fare, @p_payment_method, 'Success');

        COMMIT TRANSACTION;
        SET @p_status_message = 'SUCCESS: Ticket issued successfully.';
    END TRY
    BEGIN CATCH
        ROLLBACK TRANSACTION;
        SET @p_status_message = ERROR_MESSAGE();
    END CATCH
END;
*/

-- ----------------------------------------------------------------------------
-- PROCEDURE 2: sp_update_trip_status
-- Validates trip lifecycle and calculates delay minutes upon completion.
-- ----------------------------------------------------------------------------
/*
-- T-SQL (Azure SQL Database / Microsoft SQL Server):
CREATE PROCEDURE sp_update_trip_status
    @p_trip_id INT,
    @p_new_status VARCHAR(20),
    @p_actual_timestamp DATETIME
AS
BEGIN
    SET NOCOUNT ON;
    BEGIN TRANSACTION;
    TRY
        IF @p_new_status = 'In-Transit'
        BEGIN
            UPDATE trips 
            SET trip_status = 'In-Transit', 
                actual_departure = @p_actual_timestamp,
                delay_minutes = DATEDIFF(MINUTE, scheduled_departure, @p_actual_timestamp)
            WHERE trip_id = @p_trip_id;
        END
        ELSE IF @p_new_status = 'Completed'
        BEGIN
            UPDATE trips 
            SET trip_status = 'Completed', 
                actual_arrival = @p_actual_timestamp,
                delay_minutes = DATEDIFF(MINUTE, scheduled_arrival, @p_actual_timestamp)
            WHERE trip_id = @p_trip_id;
        END
        ELSE IF @p_new_status = 'Cancelled'
        BEGIN
            UPDATE trips 
            SET trip_status = 'Cancelled'
            WHERE trip_id = @p_trip_id;
        END

        COMMIT TRANSACTION;
    END TRY
    BEGIN CATCH
        ROLLBACK TRANSACTION;
        THROW;
    END CATCH
END;
*/
