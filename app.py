from flask import Flask, render_template, request
import config
from elasticsearch import Elasticsearch
import search, detail

app = Flask(__name__)
app.config.from_object(config)
results = {}

#connect to our cluster
es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
body = {
    "size":"0",
    "aggs": {
        "uniq_depart": {
            "terms": {
                "field": "department.keyword",
                "size" : 500
            }
        }
    }
}
# msmu_depart = es.search(index="msmu-program", body=body)['aggregations']['uniq_depart']['buckets']
smc_depart = es.search(index="smc-program", body=body)['aggregations']['uniq_depart']['buckets']
scu_depart = es.search(index="scu-program", body=body)['aggregations']['uniq_depart']['buckets']

@app.route('/')
def index():
    # return render_template('index.html', smc_depart=smc_depart, scu_depart=scu_depart, msmu_depart=msmu_depart)
    return render_template('index.html', smc_depart=smc_depart, scu_depart=scu_depart)

@app.route('/search', methods=['Get', 'POST'])
def search_programs():
    global results
    if request.method == "POST":
        results = search.getPrograms(es)

    # Pagination
    results_for_render, pagination = search.paginate(results)
    # return render_template('search.html', smc_depart=smc_depart, scu_depart=scu_depart, msmu_depart=msmu_depart, results=results_for_render, pagination=pagination, type="program")
    return render_template('search.html', smc_depart=smc_depart, scu_depart=scu_depart, results=results_for_render, pagination=pagination, type="program")

@app.route('/details')
def show_details():
    details = detail.getDetails(es)
    return render_template('details.html', details=details)

@app.route('/feature')
def feature():
    return render_template('subsection.html')

if __name__ == '__main__':
    app.run()
