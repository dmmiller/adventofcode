import itertools

class Ticket:

    def __init__(self, row, column):
        self.row = row
        self.column = column
    
    @property
    def seat_id(self):
        return self.row * 8  + self.column
    
    @classmethod
    def from_code(cls, code):
        row, column = code[:7], code [-3:]
        return Ticket(int(row.replace("F","0").replace("B","1"), base=2), int(column.replace("L","0").replace("R", "1"), base=2))

with open('input.txt') as f:
    tickets = [Ticket.from_code(line.strip()) for line in f]
    max_id = max(ticket.seat_id for ticket in tickets)
    print(f"Max Seat ID for flight is : {max_id}")

    sorted_tickets = sorted(tickets, key=lambda x : x.row)
    grouped_seats = itertools.groupby(sorted_tickets, lambda x: x.row)
    for row, tickets_grouper in grouped_seats:
        # have to turn tickets from a grouper object into an actual list to get len
        ticket_list = list(tickets_grouper)
        # rows should have 8 per row, so looking for the one with missing column
        if len(ticket_list) == 7:
            # columns should sum to 28 (0..7) so missing column is 28 - sum
            missing_column = 28 - sum(ticket.column for ticket in ticket_list)
            print(f"Missing ticket is ({row}, {missing_column}) with ID : {Ticket(row, missing_column).seat_id}")
            break
