from flask import Flask, render_template, request, jsonify, send_file
import pandas as pd
import io
import xlsxwriter
from datetime import datetime

app = Flask(__name__)

names = [
    "Raja Mama", "Chhora Mama", "Reena", "Aunty Ji", "Adarsh", "Majgva", "Arun", "Sarda", "Vikas", "Dukaan",
    "Jay Narayan", "Pushpraj", "JayLal", "vijay ji", "vijay kiraya", "Babbu Vish", "Sarji", "ravi kumar", "Indra Jeet",
    "Indra Pal", "Sen Ji", "Soni Ji", "Shailendra", "Ankush", "samay laal", "nirali", "Mori", "Arjun", "Roni Ji", "Om Ji",
    "Bindu", "Gopi", "Ram Kumar", "Bagiya", "Ram Saroj", "Gauri", "Gyanvi", "Ashu", "Dwivedi Ji", "Dwivedi Ji Bagal", "Dai",
    "Rakhi", "Dahiya", "Chandra Shekhar", "Mohan", "Chandra Bhan", "Shibbu", "ShreeKant", "Suraj", "Chhota", "Guddu Bagal",
    "Rajaniya", "Balmeek", "Upar Ladka", "Umesh", "Balkesh", "Kakur Ji", "Vipin", "Roni Samne", "Rubi", "Ram Deen",
    "Abhinash Bagal", "Pandey Ji", "Vishnu", "Mohan", "Gokul", "Bilake", "Guddu", "Rajiya", "Rajnish", "Nayagav 1",
    "Nayagav 2", "Vipin", "Indra Dev", "Vrindavan", "Akauna", "Sarda(Dai)", "Sudama", "Munna", "Badku Samne", "Badku",
    "Pradosh", "Gayatri", "Anuj", "Manish(Mahula)", "Shivraj", "Shivkumar", "Alu", "Pavan Bagal", "Pavan", "Ayoudhya",
    "Shivam(army)", "Shivam", "Seema", "Rakesh", "Ajuna Dwivedi", "Patle", "Seema 2", "chachi Bagal", "Abhinash…",
    "Desh pal", "Vokari", "Vinkiraya", "Mamta", 'Sangeet', 'Shyam Bhaiya', 'Durga Ji', 'Durga 2', 'Thakur', 'Rajjan', 'Satyam',
    'Vokari(Dai)', 'Galhu', 'Galhu2', 'Archana', 'Samdeen'
]

months_days = {
    "January": 31, "February": 28, "March": 31, "April": 30, "May": 31, "June": 30,
    "July": 31, "August": 31, "September": 30, "October": 31, "November": 30, "December": 31
}

@app.route('/', methods=['GET', 'POST'])
def index():
    selected_month = request.args.get('month', datetime.now().strftime('%B'))
    days_in_month = months_days.get(selected_month, 31)
    
    return render_template(
        'index.html',
        names_lst=names,
        months_days=months_days,
        selected_month=selected_month,
        days_in_month=days_in_month
    )

@app.route('/save-excel', methods=['POST'])
def save_excel():
    data = request.json
    month = data.get('month', 'Unknown')
    rows_data = data.get('data', [])
    
    # Create an in-memory Excel file
    output = io.BytesIO()
    workbook = xlsxwriter.Workbook(output)
    worksheet = workbook.add_worksheet(month)
    
    # Add headers
    worksheet.write(0, 0, 'Name')
    for i in range(months_days.get(month, 31)):
        worksheet.write(0, i+1, i+1)
    
    # Add data
    for row_idx, row_data in enumerate(rows_data):
        worksheet.write(row_idx+1, 0, row_data['name'])
        for col_idx, value in enumerate(row_data['values']):
            worksheet.write(row_idx+1, col_idx+1, value)
    
    workbook.close()
    output.seek(0)
    
    return send_file(
        output, 
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        as_attachment=True,
        download_name=f"{month}_data.xlsx"
    )

if __name__ == "__main__":
    app.run(debug=True)