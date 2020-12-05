import itertools

class Ticket:
    _row = None
    _column = None

    def __init__(self, code):
        self._code = code
    
    @property
    def seat_id(self):
        return self.row * 8  + self.column
    
    @property
    def row(self):
        if not self._row:
            self._row = int(self._code[:7].replace("F","0").replace("B","1"), base=2)
        return self._row

    @property
    def column(self):
        if not self._column:
            self._column = int(self._code[-3:].replace("L","0").replace("R", "1"), base=2)
        return self._column
    
with open('input.txt') as f:
    tickets = [Ticket(line.strip()) for line in f]
    max_id = max(ticket.seat_id for ticket in tickets)
    print("Max Seat ID for flight is :", max_id)

    sorted_tickets = sorted(tickets, key=lambda x : x.row)
    grouped_seats = itertools.groupby(sorted_tickets, lambda x: x.row)
    for row, tickets_grouper in grouped_seats:
        # have to turn tickets from a grouper object into an actual list to get len
        ticket_list = list(tickets_grouper)
        # rows should have 8 per row, so looking for the one with missing column
        if len(ticket_list) == 7:
            # columns should sum to 28 (0..7) so missing column is 28 - sum
            missing_column = 28 - sum(ticket.column for ticket in ticket_list)
            print("Missing ticket is", row, missing_column, " with ID", row * 8 + missing_column)
            break
