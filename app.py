from flask import Flask, render_template, request
import mysql.connector
import yaml

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    html_result = ""
    query = ""
    with_br_query = ""
    num_rows = 1

    if request.method == 'POST':
        # get the query from the form on the web page
        with_br_query = request.form['query'].strip()
        with_br_query = with_br_query.replace('<br>', '\n')
        query = with_br_query.replace('\n', ' ')

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
            html_result += '<table>'
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

        except Exception as e:
            html_result = "Error executing query: " + str(e)
            return render_template('index.html', error=html_result, last_query = with_br_query)

    return render_template('index.html', result=html_result, last_query = with_br_query)


@app.route('/sample_queries.html', methods=['GET', 'POST'])
def sample_queries():
    queries = None
    with open('./sql/sample_queries.sql', 'r') as f:
        sql = f.read().strip()
        queries = sql.split(';')
        queries = [q.strip() + ';' for q in queries]
        queries = [q.replace('\n', '<br>') for q in queries]
        queries = [q for q in queries if q != ';']
    return render_template('sample_queries.html', queries=queries)

if __name__ == '__main__':
    app.run(debug=True)
@app.errorhandler(404)
def page_not_found(e):
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
