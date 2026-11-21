"""
TransitIQ Business Service & Transactional Layer (OLTP Workloads)
Executes ACID compliant operations for passenger ticketing, trip updates,
and real-time transit schedule management.
"""

from datetime import datetime
from typing import Dict, Any, Optional, List
from src.db.connection import get_raw_sqlite_connection, execute_query

class TransitService:
    @staticmethod
    def get_bookable_trips() -> List[Dict[str, Any]]:
        """
        Retrieves active trips open for seat/ticket booking.
        """
        query = """
        SELECT 
            t.trip_id,
            t.trip_code,
            r.route_code,
            r.route_name,
            r.route_type,
            r.base_fare,
            v.vehicle_code,
            v.capacity,
            (SELECT COUNT(*) FROM passenger_fares WHERE trip_id = t.trip_id AND transaction_status = 'Success') AS booked_passengers,
            t.scheduled_departure,
            t.trip_status
        FROM trips t
        JOIN routes r ON t.route_id = r.route_id
        JOIN vehicles v ON t.vehicle_id = v.vehicle_id
        WHERE t.trip_status IN ('Scheduled', 'In-Transit')
        ORDER BY t.scheduled_departure ASC
        LIMIT 25
        """
        return execute_query(query)

    @staticmethod
    def get_stops_for_trip(trip_id: int) -> List[Dict[str, Any]]:
        """
        Returns the ordered list of stops accessible on a specific trip's route.
        """
        query = """
        SELECT 
            s.stop_id,
            s.stop_code,
            s.stop_name,
            rs.stop_sequence,
            rs.distance_from_start_km,
            rs.est_travel_time_min
        FROM trips t
        JOIN route_segments rs ON t.route_id = rs.route_id
        JOIN stops s ON rs.stop_id = s.stop_id
        WHERE t.trip_id = :trip_id
        ORDER BY rs.stop_sequence ASC
        """
        return execute_query(query, {"trip_id": trip_id})

    @staticmethod
    def book_ticket(
        trip_id: int,
        origin_stop_id: int,
        destination_stop_id: int,
        passenger_type: str,
        payment_method: str
    ) -> Dict[str, Any]:
        """
        ACID Transaction: Atomically issues a ticket with validation.
        """
        conn = get_raw_sqlite_connection()
        cursor = conn.cursor()

        try:
            # 1. Fetch trip, route, and vehicle capacity
            cursor.execute("""
                SELECT t.trip_status, r.base_fare, v.capacity,
                       (SELECT COUNT(*) FROM passenger_fares WHERE trip_id = t.trip_id AND transaction_status = 'Success') as current_load
                FROM trips t
                JOIN routes r ON t.route_id = r.route_id
                JOIN vehicles v ON t.vehicle_id = v.vehicle_id
                WHERE t.trip_id = ?
            """, (trip_id,))
            trip_info = cursor.fetchone()

            if not trip_info:
                return {"success": False, "message": "Trip not found."}

            if trip_info["trip_status"] not in ("Scheduled", "In-Transit"):
                return {"success": False, "message": f"Cannot book ticket for trip with status '{trip_info['trip_status']}'."}

            if trip_info["current_load"] >= trip_info["capacity"]:
                return {"success": False, "message": "Trip is at full capacity. Booking rejected."}

            # 2. Compute discounted fare
            base_fare = trip_info["base_fare"]
            discount_map = {
                "Standard Adult": 1.0,
                "Student": 0.50,
                "Senior Citizen": 0.40,
                "Commuter Passholder": 0.70
            }
            fare_paid = round(base_fare * discount_map.get(passenger_type, 1.0), 2)

            # 3. Generate unique ticket reference
            now = datetime.now()
            cursor.execute("SELECT COUNT(*) FROM passenger_fares")
            seq = cursor.fetchone()[0] + 1
            ticket_ref = f"TKT-OLTP-{now.strftime('%y%m%d%H%M')}-{seq:04d}"

            # 4. Insert transactional record
            cursor.execute("""
                INSERT INTO passenger_fares (
                    ticket_reference, trip_id, origin_stop_id, destination_stop_id,
                    passenger_type, fare_paid, payment_method, transaction_status, boarding_timestamp
                ) VALUES (?, ?, ?, ?, ?, ?, ?, 'Success', ?)
            """, (
                ticket_ref, trip_id, origin_stop_id, destination_stop_id,
                passenger_type, fare_paid, payment_method, now.strftime("%Y-%m-%d %H:%M:%S")
            ))

            conn.commit()
            return {
                "success": True,
                "ticket_reference": ticket_ref,
                "fare_paid": fare_paid,
                "passenger_type": passenger_type,
                "payment_method": payment_method,
                "message": "Ticket successfully issued under ACID transaction."
            }

        except Exception as e:
            conn.rollback()
            return {"success": False, "message": f"Transaction rolled back due to error: {str(e)}"}
        finally:
            conn.close()

    @staticmethod
    def update_trip_status(trip_id: int, new_status: str, delay_minutes: int = 0) -> Dict[str, Any]:
        """
        Updates trip operational lifecycle status and delay metrics.
        """
        conn = get_raw_sqlite_connection()
        cursor = conn.cursor()

        try:
            now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            if new_status == "In-Transit":
                cursor.execute("""
                    UPDATE trips 
                    SET trip_status = ?, actual_departure = ?, delay_minutes = ?
                    WHERE trip_id = ?
                """, (new_status, now_str, delay_minutes, trip_id))
            elif new_status == "Completed":
                cursor.execute("""
                    UPDATE trips 
                    SET trip_status = ?, actual_arrival = ?, delay_minutes = ?
                    WHERE trip_id = ?
                """, (new_status, now_str, delay_minutes, trip_id))
            else:
                cursor.execute("""
                    UPDATE trips 
                    SET trip_status = ?, delay_minutes = ?
                    WHERE trip_id = ?
                """, (new_status, delay_minutes, trip_id))

            conn.commit()
            return {"success": True, "message": f"Trip {trip_id} updated to '{new_status}' with {delay_minutes}m delay."}
        except Exception as e:
            conn.rollback()
            return {"success": False, "message": f"Failed to update trip status: {str(e)}"}
        finally:
            conn.close()
