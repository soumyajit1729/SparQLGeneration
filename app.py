from flask import Flask, render_template, request
# from generate_sparql import get_query

app = Flask(__name__)

dict = {}

def make(entity):
  a = 'b'
  i=0
  for x in entity:
    dict[x] = a
    a = chr(ord(a)+1)

def get_var(s):
  return '?'+dict[s]

def get_query(query):
  answer = "SELECT " 
  make(query["entity"])
  for show in query["show"]:
    answer = answer + "?" + show + " "
  answer += '\nWHERE {\n'

  # only for one entity
  if query["num_ent"]==1:
    answer += ("\t?x type " + query["entity"][0] + ".\n")
    for show in query["show"]:
      answer += ("\t?x " + show + " ?" + show + ".\n")
    for con in query["condition"]:
      answer += ("\t?x " + con[1] + " " + con[2] + ".\n")
    

  # for two entity
  elif query["num_ent"]==2:
    answer += ("\t" + get_var(query["entity"][0]) + " type " + query["entity"][0] + ".\n")
    answer += ("\t" + get_var(query["entity"][1]) + " type " + query["entity"][1] + ".\n")
    answer += ("\t" + get_var(query["entity"][0]) + " " + query["relation"] + " " + get_var(query["entity"][1]) + ".\n")

    i=0
    for show in query["show"]:
      answer += ("\t" + get_var(query["about"][i]) + " " + show + " ?" + show + ".\n")
      i = i+1

    for con in query["condition"]:
      answer += ("\t" + get_var(con[0]) + " " + con[1] + " " + con[2] + ".\n")
  
  answer += "}\n"
  if(query["limit"]!=-1):
    answer += "Limit "+str(query["limit"])+"\n"
  if(query["order"]!=""):
    answer += "Order By ?"+str(query["order"])+"\n"

  return answer

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/query1', methods=['POST'])
def query1():
    query = {}
    query["num_ent"] = int(request.form['entity_count'])
    entities = []
    entities.append(request.form['entity1'])
    if(query["num_ent"]==2):
        entities.append(request.form['entity2'])
    query["entity"] = entities
    query["relation"] = request.form['relation']  
    properties =  request.form['properties']
    properties = properties.replace(" ","")
    properties = properties.split(",")
    query["show"] = properties

    pen =  request.form['property_entity']
    pen = pen.replace(" ","")
    pen = pen.split(",")
    query["about"] = pen

    query["limit"] = request.form['limit']
    query["order"] = request.form['order']

    num_con = int(request.form['condition_count'])
    cond = []
    for i in range(num_con):
        ent = "ent"+str(i+1)
        prop = "prop"+str(i+1)
        val = "val"+str(i+1)
        print("/////////////////////////")
        print(ent)
        con = [request.form[ent], request.form[prop], request.form[val]]
        cond.append(con)

    query["condition"] = cond
    
    print(query)

    sparql_query = get_query(query)
    print(sparql_query)
    return render_template('home.html', sparql_query=sparql_query)

if __name__ == '__main__':
    app.run(debug=True)
