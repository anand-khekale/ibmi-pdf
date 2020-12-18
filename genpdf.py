from fpdf import FPDF
import ibm_db_dbi as db2 #Import the package

# Fetch data from the database 
conn= db2.connect() # Make a connection 
cur = conn.cursor()
cur.execute("SELECT CUSNUM, LSTNAM, BALDUE, CDTLMT FROM QIWS.QCUSTCDT")

# CursorByName will provide data in Key:Value pair, which we will use while generating
# the PDF
class CursorByName():
    def __init__(self, cursor):
        self._cursor = cursor

    def __iter__(self):
        return self

    def __next__(self):
        row = self._cursor.__next__()

        return {description[0]: row[col] for col, description in enumerate(self._cursor.description)}

data=[]
for row in CursorByName(cur):
    data.append(row)

## PDF Processing

## Add Header and Footer to the page
class PDF(FPDF):
    def header(self):
        # Logo
        self.image('ibmi.png', 10, 8, 20)
        # Arial bold 15
        self.set_font('Arial', 'B', 15)
        # Move to the right
        self.cell(80)
        # Title
        self.cell(30, 10, 'Customer balance due report  ', 0, 0, 'C')
        # Line break
        self.ln(40)
        # Add dashed line
        self.dashed_line(10, 50, 200, 50, 1, 1)
        # Add line break after the dashed line
        self.ln(20)

    # Page footer
    def footer(self):
        # Position at 1.5 cm from bottom
        self.set_y(-15)
        # Arial italic 8
        self.set_font('Arial', 'I', 8)
        # Page number
        self.cell(0, 10, 'Page ' + str(self.page_no()), 0, 0, 'C')

# Instatiate the PDF class and add page with attributes
pdf = PDF()
pdf.add_page()
pdf.set_left_margin(margin=40)
pdf.set_font('Arial', 'B', 12)
pdf.set_fill_color(193,229,252)

#Set the table headers, with background fill color 
fill_color = 1
pdf.cell(w=40, h=10, txt='Customer Number', border=1, ln=0, align='L', fill=fill_color)
pdf.cell(w=30, h=10, txt='Last Name', border=1, ln=0, align='L', fill=fill_color)
pdf.cell(w=30, h=10, txt='Balance Due', border=1, ln=0, align='L', fill=fill_color)
pdf.cell(w=30, h=10, txt='Credit Limit', border=1, ln=1, align='L', fill=fill_color)

# Style set up for rows
pdf.set_font('Arial', '', 12)
pdf.set_fill_color(235,236,236)

# Process the database rows to print to the PDF
fill_color = 0
for row in data:
    # Get data from each row of the table
    cus_num = str(row['CUSNUM'])
    lst_nam = row['LSTNAM']
    bal_due = str(row['BALDUE'])
    cdt_lmt = str(row['CDTLMT'])

    # Create cells with the data and print it on PDF
    pdf.cell(w=40, h=8, txt=cus_num, border=1, ln=0, align='L', fill=fill_color)
    pdf.cell(w=30, h=8, txt=lst_nam, border=1, ln=0, align='L', fill=fill_color)
    pdf.cell(w=30, h=8, txt=bal_due, border=1, ln=0, align='R', fill=fill_color)
    pdf.cell(w=30, h=8, txt=cdt_lmt, border=1, ln=1, align='R', fill=fill_color)

    # Flip the fill color for alternate row.
    if (fill_color==0):
        fill_color=1
    else:
        fill_color=0

# Output the PDF file        
pdf.output('customer.pdf','F')