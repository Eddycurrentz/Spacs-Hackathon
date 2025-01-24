from flask import Flask, render_template_string, request
import matplotlib.pyplot as plt
import os

app = Flask(__name__)

# HTML template as a string
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Academic Attendance and Grade Report</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 20px;
            background-color: #f4f4f4;
        }
        h1 {
            color: #333;
        }
        form {
            background: #fff;
            padding: 20px;
            border-radius: 5px;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
        }
        label {
            display: block;
            margin: 10px 0 5px;
        }
        input[type="text"] {
            width: 100%;
            padding: 10px;
            margin-bottom: 10px;
            border: 1px solid #ccc;
            border-radius: 4px;
        }
        input[type="submit"] {
            background-color: #28a745;
            color: white;
            border: none;
            padding: 10px 15px;
            border-radius: 4px;
            cursor: pointer;
        }
        input[type="submit"]:hover {
            background-color: #218838;
        }
        img {
            margin-top: 20px;
            max-width: 100%;
            height: auto;
            border: 1px solid #ccc;
            border-radius: 5px;
        }
    </style>
    <script>
        // Placeholder for future JavaScript functionality
        function showAlert() {
            alert("This is a placeholder for future interactivity!");
        }
    </script>
</head>
<body>
    <h1>Academic Attendance and Grade Report</h1>
    <form action="/generate" method="post">
        <label for="students">Students (comma-separated):</label>
        <input type="text" id="students" name="students" required>
        
        <label for="attendance">Attendance (comma-separated):</label>
        <input type="text" id="attendance" name="attendance" required>
        
        <label for="grades">Grades (comma-separated):</label>
        <input type="text" id="grades" name="grades" required>
        
        <input type="submit" value="Generate Graph" onclick="showAlert()">
    </form>
    <br>
    {% if graph_image %}
        <h2>Generated Graph:</h2>
        <img src="{{ url_for('static', filename=graph_image) }}" alt="Attendance and Grade Report">
    {% endif %}
</body>
</html>
"""

def create_graph(students, attendance, grades):
    # Create a figure and axis
    fig, ax1 = plt.subplots()

    # Create a bar chart for attendance
    color = 'tab:blue'
    ax1.set_xlabel('Students')
    ax1.set_ylabel('Attendance (%)', color=color)
    ax1.bar(students, attendance, color=color, alpha=0.6, label='Attendance')
    ax1.tick_params(axis='y', labelcolor=color)

    # Create a second y-axis for grades
    ax2 = ax1.twinx()  
    color = 'tab:orange'
    ax2.set_ylabel('Grades (%)', color=color)  
    ax2.plot(students, grades, color=color, marker='o', label='Grades')
    ax2.tick_params(axis='y', labelcolor=color)

    # Add title and grid
    plt.title('Academic Attendance and Grade Report')
    ax1.grid(axis='y', linestyle='--', alpha=0.7)

    # Save the plot as an image
    graph_image_path = 'static/attendance_grade_report.png'
    plt.savefig(graph_image_path)
    plt.close()
    return graph_image_path

@app.route('/', methods=['GET'])
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/generate', methods=['POST'])
def generate():
    students = request.form['students'].split(',')
    attendance = list(map(int, request.form['attendance'].split(',')))
    grades = list(map(int, request.form['grades'].split(',')))
    
    graph_image = create_graph(students, attendance, grades)  # Generate the graph
    return render_template_string(HTML_TEMPLATE, graph_image='attendance_grade_report.png')

if __name__ == '__main__':
    # Create static directory if it doesn't exist
    if not os.path.exists('static'):
        os.makedirs('static')
    
    app.run(debug=True)