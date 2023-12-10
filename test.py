import openpyxl

book = openpyxl.open("example.xlsx", read_only=True)
sheet = book.active
for row in range(1, 1000):
    if not (sheet.cell(row=row, column=1).value is None):
        print('TRUE')
book.close()