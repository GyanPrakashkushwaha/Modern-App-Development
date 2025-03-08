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









<!-- ===================================================================== -->


<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Monthly Data Tracker</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH" crossorigin="anonymous">
    <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
    <style>
        /* Navbar height */
        .navbar {
            height: 50px;
            position: sticky;
            top: 0;
            z-index: 100;
        }
        
        /* Main container styling */
        .table-container {
            position: relative;
            height: calc(100vh - 60px);
            overflow: auto;
            margin-top: 10px;
        }
        
        /* Table styling */
        table {
            border-collapse: separate;
            border-spacing: 0;
        }
        
        /* Header row freeze */
        thead tr th {
            position: sticky;
            top: 0;
            background-color: #f8f9fa;
            z-index: 10;
            border-bottom: 2px solid #dee2e6;
        }
        
        /* First column freeze (checkbox) */
        .sticky-first-col {
            position: sticky;
            left: 0;
            background-color: #f8f9fa;
            z-index: 5;
            border-right: 1px solid #dee2e6;
        }
        
        /* Second column freeze (name) */
        .sticky-second-col {
            position: sticky;
            left: 42px; /* Adjust based on the width of the first column */
            background-color: #f8f9fa;
            z-index: 5;
            border-right: 2px solid #dee2e6;
        }
        
        /* Corner cells (header + sticky columns) get higher z-index */
        thead .sticky-first-col, thead .sticky-second-col {
            z-index: 15;
        }
        
        /* Cell value styling */
        .cell-value {
            min-width: 80px;
            text-align: center;
            padding: 0.25rem;
            border: 1px solid #dee2e6;
            border-radius: 4px;
            cursor: pointer;
            background-color: white;
        }
        
        /* Highlight selected values */
        .cell-value.selected-value {
            background-color: #e6f2ff;
            font-weight: bold;
        }
        
        /* Cell value dropdown */
        .cell-dropdown {
            position: absolute;
            background-color: white;
            border: 1px solid #dee2e6;
            border-radius: 4px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.2);
            z-index: 20;
            display: none;
        }
        
        .dropdown-option {
            padding: 0.5rem 1rem;
            cursor: pointer;
        }
        
        .dropdown-option:hover {
            background-color: #f0f7ff;
        }
        
        .dropdown-option.custom-option {
            border-top: 1px solid #dee2e6;
        }
        
        /* Custom input styling */
        .custom-input {
            padding: 0.25rem 0.5rem;
            width: 100%;
            border: 1px solid #0d6efd;
            border-radius: 4px;
            margin-top: 0.25rem;
            display: none;
        }
        
        /* Better table styling */
        .table th, .table td {
            vertical-align: middle;
            padding: 0.5rem;
        }
        
        /* Highlight row on hover */
        tbody tr:hover {
            background-color: rgba(0,0,0,0.05);
        }
        
        /* Day headers styling */
        .day-header {
            text-align: center;
            font-weight: bold;
        }
        
        /* Default value cell */
        .default-value-cell {
            background-color: #f8f9fa;
        }
    </style>
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
        <div class="container-fluid">
            <a class="navbar-brand" href="#">Monthly Tracker</a>
            <div class="d-flex">
                <select id="month-select" class="form-select me-2" onchange="updateDaysInMonth()">
                    {% for month, days in months_days.items() %}
                    <option value="{{ month }}" {% if selected_month == month %}selected{% endif %}>{{ month }}</option>
                    {% endfor %}
                </select>
                <button id="save-excel" class="btn btn-success">Save as Excel</button>
            </div>
        </div>
    </nav>

    <div class="container-fluid">
        <div class="table-container">
            <table class="table table-striped" id="data-table">
                <thead>
                    <tr>
                        <th class="sticky-first-col"><input type="checkbox" id="select-all" onclick="toggleAllCheckboxes()"></th>
                        <th class="sticky-second-col">Name</th>
                        <th>Default Value</th>
                        {% for i in range(days_in_month) %}
                        <th class="day-header">{{ i+1 }}</th>
                        {% endfor %}
                    </tr>
                </thead>
                <tbody>
                    {% for name in names_lst %}
                    <tr data-name="{{ name }}">
                        <td class="sticky-first-col"><input type="checkbox" class="row-checkbox" name="selected_row" value="{{ name }}"></td>
                        <th class="sticky-second-col">{{ name }}</th>
                        <td class="default-value-cell">
                            <div class="cell-value default-value" data-value="" onclick="showDropdown(this, true)">Select</div>
                            <input type="number" class="custom-input" onchange="updateCustomValue(this)" placeholder="Enter value">
                        </td>
                        {% for i in range(days_in_month) %}
                        <td>
                            <div class="cell-value day-value" data-value="0" onclick="showDropdown(this)">0</div>
                            <input type="number" class="custom-input" onchange="updateCustomValue(this)" placeholder="Enter value">
                        </td>
                        {% endfor %}
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
    </div>

    <!-- Dropdown template (will be cloned and positioned) -->
    <div id="dropdown-template" class="cell-dropdown">
        <div class="dropdown-option" data-value="0">0</div>
        <div class="dropdown-option" data-value="250">250</div>
        <div class="dropdown-option" data-value="500">500</div>
        <div class="dropdown-option" data-value="750">750</div>
        <div class="dropdown-option" data-value="1000">1000</div>
        <div class="dropdown-option" data-value="1500">1500</div>
        <div class="dropdown-option custom-option" data-value="custom">Custom...</div>
    </div>

    <script>
        // Global variable to track current active cell
        let activeCell = null;
        
        // Toggle all checkboxes
        function toggleAllCheckboxes() {
            const selectAll = document.getElementById('select-all');
            const checkboxes = document.getElementsByClassName('row-checkbox');
            
            for (let checkbox of checkboxes) {
                checkbox.checked = selectAll.checked;
            }
        }

        // Show dropdown for a cell
        function showDropdown(cell, isDefault = false) {
            // Close any open dropdown
            closeAllDropdowns();
            
            // Set active cell
            activeCell = cell;
            
            // Clone the dropdown template
            const dropdown = document.getElementById('dropdown-template').cloneNode(true);
            dropdown.id = '';
            
            // Position the dropdown
            const rect = cell.getBoundingClientRect();
            dropdown.style.top = (rect.bottom + window.scrollY) + 'px';
            dropdown.style.left = (rect.left + window.scrollX) + 'px';
            dropdown.style.minWidth = rect.width + 'px';
            
            // Add event listeners to options
            dropdown.querySelectorAll('.dropdown-option').forEach(option => {
                option.addEventListener('click', function() {
                    selectOption(this.dataset.value, isDefault);
                });
            });
            
            // Append to body and show
            document.body.appendChild(dropdown);
            dropdown.style.display = 'block';
            
            // Add click outside listener
            setTimeout(() => {
                document.addEventListener('click', closeDropdownOnClickOutside);
            }, 10);
        }
        
        // Close dropdown when clicking outside
        function closeDropdownOnClickOutside(e) {
            if (!e.target.closest('.cell-dropdown') && !e.target.closest('.cell-value')) {
                closeAllDropdowns();
            }
        }
        
        // Close all dropdowns
        function closeAllDropdowns() {
            document.querySelectorAll('.cell-dropdown:not(#dropdown-template)').forEach(dropdown => {
                dropdown.remove();
            });
            document.removeEventListener('click', closeDropdownOnClickOutside);
        }
        
        // Select an option from dropdown
        function selectOption(value, isDefault) {
            if (!activeCell) return;
            
            const cell = activeCell;
            const customInput = cell.nextElementSibling;
            
            if (value === 'custom') {
                // Show custom input
                customInput.style.display = 'block';
                customInput.focus();
            } else {
                // Update cell value
                cell.textContent = value;
                cell.dataset.value = value;
                customInput.style.display = 'none';
                
                // Update styling
                if (value && value !== '0') {
                    cell.classList.add('selected-value');
                } else {
                    cell.classList.remove('selected-value');
                }
                
                // If this is a default value, fill the row
                if (isDefault) {
                    fillRowWithValue(cell, value);
                }
            }
            
            closeAllDropdowns();
        }
        
        // Update custom value
        function updateCustomValue(input) {
            const value = input.value;
            const cell = input.previousElementSibling;
            
            if (value) {
                cell.textContent = value;
                cell.dataset.value = value;
                cell.classList.add('selected-value');
                
                // If this is a default value, fill the row
                if (cell.classList.contains('default-value')) {
                    fillRowWithValue(cell, value);
                }
            }
        }
        
        // Fill row with selected default value
        function fillRowWithValue(cell, value) {
            const row = cell.closest('tr');
            const dayCells = row.querySelectorAll('.day-value');
            
            dayCells.forEach(dayCell => {
                dayCell.textContent = value;
                dayCell.dataset.value = value;
                
                if (value && value !== '0') {
                    dayCell.classList.add('selected-value');
                } else {
                    dayCell.classList.remove('selected-value');
                }
            });
        }

        // Update days in month when month changes
        function updateDaysInMonth() {
            const month = document.getElementById('month-select').value;
            window.location.href = `/?month=${month}`;
        }

        // Save as Excel
        document.getElementById('save-excel').addEventListener('click', function() {
            const selectedRows = document.querySelectorAll('.row-checkbox:checked');
            if (selectedRows.length === 0) {
                alert('Please select at least one row to save');
                return;
            }

            const month = document.getElementById('month-select').value;
            const data = [];
            
            selectedRows.forEach(checkbox => {
                const row = checkbox.closest('tr');
                const name = row.querySelector('th').textContent;
                const dayValues = [];
                
                row.querySelectorAll('.day-value').forEach(cell => {
                    dayValues.push(cell.dataset.value);
                });
                
                data.push({
                    name: name,
                    values: dayValues
                });
            });
            
            // Send data to server to generate Excel file
            fetch('/save-excel', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    month: month,
                    data: data
                })
            })
            .then(response => response.blob())
            .then(blob => {
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = `${month}_data.xlsx`;
                document.body.appendChild(a);
                a.click();
                window.URL.revokeObjectURL(url);
            })
            .catch(error => {
                console.error('Error saving Excel file:', error);
                alert('Error saving Excel file');
            });
        });

        // Close dropdowns when scrolling
        document.querySelector('.table-container').addEventListener('scroll', function() {
            closeAllDropdowns();
        });
    </script>
</body>
</html>




















