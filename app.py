from flask import Flask, render_template, request
import mysql.connector
import yaml

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/query', methods=['POST'])
def query():
    # get the query from the form on the web page
    query = request.form['query']
    
    try:
        # connect to the database
        with open("./config.yaml", mode="r") as file:
            config = yaml.safe_load(file)
        
        mydb = mysql.connector.connect(**config["lms"])

        # execute the query
        cursor = mydb.cursor()
        cursor.execute(query)
        result = cursor.fetchall()

        # close the database connection
        mydb.close()

        # Get the column names
        column_names = [i[0] for i in cursor.description]

        # Format the result as HTML
        html_result = '<table>'
        html_result += '<tr>'
        for name in column_names:
            html_result += '<th>' + name + '</th>'
        html_result += '</tr>'

        for row in result:
            html_result += '<tr>'
            for col in row:
                html_result += '<td>' + str(col) + '</td>'
            html_result += '</tr>'

        html_result += '</table>'

        # send the result back to the web page for display
        return render_template('result.html', result=html_result)

    except Exception as e:
        error_message = "Error executing query: " + str(e)
        return render_template('result.html', result=error_message)

@app.route('/results')
def results_page():
    referrer = request.referrer
    if referrer and referrer != request.url_root:
        return redirect(url_for('index'))
    else:
        return render_template('results.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('index.html')

if __name__ == '__main__':
    app.run()