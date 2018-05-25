from neo4jrestclient.client import GraphDatabase
import os
import time

os.system("./neo4j-community-3.4.0/bin/neo4j stop")
os.system("rm -r ./neo4j-community-3.4.0/data/databases/graph.db")
os.system("./neo4j-community-3.4.0/bin/neo4j start")
time.sleep(20) 

db = GraphDatabase("http://localhost:7474", username="neo4j", password="2178026")

archivo = open("./output/finalOutput.csv","r")
lineas = archivo.readlines()
rating = []
prediction = []
conclusion = []

for i in lineas:
	linea = i.split(",")
	rating.append(linea[0])
	prediction.append(linea[1])
	conclusion.append(linea[2].rstrip())


# Create some nodes with labels
ratingL = db.labels.create("Rating")
predictionL = db.labels.create("Prediction")
conclusionL = db.labels.create("Conclusion")
for i,j,z in zip(rating,prediction,conclusion):
	r1 = db.nodes.create(name=str(i))
	ratingL.add(r1)
	p1 = db.nodes.create(name=str(j))
	predictionL.add(p1)
	c1 = db.nodes.create(name=str(z))
	conclusionL.add(c1)
	r1.relationships.create("-",p1)
	p1.relationships.create("-",c1)

 
# beer = db.labels.create("Materia")
# b1 = db.nodes.create(name="Telematica")
# b2 = db.nodes.create(name="SO")
# # You can associate a label with many nodes in one go
# beer.add(b1, b2)

# # User-likes->Beer relationships
# u1.relationships.create("likes", b1)
# u1.relationships.create("likes", b2)
# u2.relationships.create("likes", b1)
# # Bi-directional relationship?
# u1.relationships.create("friends", u2)


#MATCH (n)-[r]->(m) RETURN n, r, m;
#MATCH (conclusion:Conclusion { name: 'Mal' })--(prediction:Prediction) RETURN prediction.name
#MATCH (conclusion:Conclusion), (rating:Rating) , (prediction:Prediction) RETURN conclusion.name,prediction.name,rating.name
#MATCH (conclusion:Conclusion {name:'Bueno'}), (rating:Rating) , (prediction:Prediction) RETURN rating.name,prediction.name,conclusion.name
#MATCH (conclusion:Conclusion {name:'Bueno'}), (rating:Rating) , (prediction:Prediction {name:'Bueno'}) RETURN rating.name,prediction.name,conclusion.name LIMIT 10
#MATCH(n) RETURN labels(n), keys(n),size(keys(n)), count(*) ORDER BY size(keys(n)) DESC
#MATCH (n)-[r]->(m)-[q]->(f) RETURN n.name, m.name, f.name;
#MATCH (n)-[r]->(m)-[q]->(f) where m.name in ['bueno'] RETURN n.name, m.name, f.name;