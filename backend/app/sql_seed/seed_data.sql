INSERT INTO app_bus (number, route, capacity, active) VALUES
('UAP-01','Gate A -> North Campus',50,1),
('UAP-02','Gate B -> South Campus',45,1);

-- Add timeslots (adjust bus_id if needed)
INSERT INTO app_timeslot (bus_id, departure_time, arrival_time) VALUES
(1,'08:00:00','08:30:00'),
(2,'09:00:00','09:30:00');
