from flask import Flask, render_template,request
#import pymongo
import sqlite3
from collections import OrderedDict
import itertools

#myclient = pymongo.MongoClient("mongodb://localhost:5000/")
#mydb = myclient["mydatabase"]
#rint(myclient.list_database_names())

conn = sqlite3.connect('employee.db')
c = conn.cursor()

#c.execute("DROP TABLE itemset")
#c.execute("""CREATE TABLE itemset(
#		id text,
#		prod_type text,
#		product_name text,
#        brand text,
# 		image_url text,
#		product_details text,
#		availability text,
#		price real
#	)""")

#c.execute("INSERT INTO itemset VALUES ('1','top','formalShirt','Myntra','formalShirt.jpg','white,collared,formal','In Stock',1000)")
#c.execute("INSERT INTO itemset VALUES ('2','top','floralTop','Myntra','floralTop.jpg','pink,long sleves,casual','In Stock',700)")
#c.execute("INSERT INTO itemset VALUES ('3','top','coldShoulderTop','Myntra','coldShoulderTop.jpg','red,long sleves,casuak','In Stock',800)")
#c.execute("INSERT INTO itemset VALUES ('4','top','kurti','Myntra','kurti.jpg','dark blue,long,ethnic','In Stock',800)")
#c.execute("INSERT INTO itemset VALUES ('5','bottom','leggings','Lyra','leggings.jpg','red,cotton,ethnic','In Stock',700)")
#c.execute("INSERT INTO itemset VALUES ('6','bottom','LongSkirt','Pantaloons','longSkirt.jpg','Pink,long,ethnic','In Stock',1000)")
#c.execute("INSERT INTO itemset VALUES ('7','bottom','Skirt','Forever21','skirt.jpg','DarkBlue,Knee-length','In Stock',1000)")
#c.execute("INSERT INTO itemset VALUES ('8','top','tankTop','H&M','tankTop.jpg','black,cotton,casual','In Stock',500)")
#c.execute("INSERT INTO itemset VALUES ('9','bottom','trackPant','H&M','trackPant.jpg','black,long,casual','In Stock',800)")
#c.execute("INSERT INTO itemset VALUES ('10','bottom','jeans','Forever21','jeans.jpg','denim,full-length,casual','In Stock',1000)")
#c.execute("INSERT INTO itemset VALUES ('11','bottom','formalPant','H&M','formalPant.jpg','black,long,formal','In Stock',1000)")
#c.execute("INSERT INTO itemset VALUES ('12','acc','watch','titan','watch.jpg','peachColored','In Stock',1500)")
#c.execute("INSERT INTO itemset VALUES ('13','acc','necklace','Forever21','necklace.jpg','silver,long,ethnic','In Stock',1000)")
#c.execute("INSERT INTO itemset VALUES ('14','acc','ring','Forever21','ring.jpg','platinum','In Stock',50000)")
#c.execute("INSERT INTO itemset VALUES ('15','acc','longEarings','Forever21','longEarings.jpg','Gold','In Stock',10000)")
#c.execute("INSERT INTO itemset VALUES ('16','acc','studs','Forever21','studs.jpg','silver','In Stock',5000)")

#c.execute("DELETE FROM itemset WHERE id = '7'")
c.execute("SELECT * FROM itemset")
prodDetails = c.fetchall()
print(prodDetails)
conn.commit()
conn.close()

def apriori(sItem):
	#selectedItem = []
	#selectedItem.append(sItem)
	items = []
	itemset = []
	freqItemSet = []
	freqSupCount = []
	strongAssociationRules = []
	Rulesconfidence = []
	minSupport = 2
	minConfidence = 0.6
	print("\nminSupport : ",minSupport)
	print("Confidence : ",minConfidence)

	with open("dataitems.txt","r") as data:
		i=0
		for line in data:
			if(i==0):
				i+=1
				continue
			line = line.strip()
			temp = line.split(" ")
			t = temp[1].split(",")
			items.append(t)
			for item in t:
				if item not in itemset:
					itemset.append(item)
	supCount = []
	l = len(itemset)
	index=0
	while(index<len(itemset)):
		supCount.append(0)
		for line in items:
			for i in line:
				if(i==itemset[index]):
					supCount[-1]+=1
		#print(itemset[index]," ",supCount," ",index)
		if(supCount[-1]<minSupport):
			supCount.pop()
			del itemset[index]
			index-=1
		index+=1

	singleItemset = [[x] for x in itemset]
	singleSupCount = supCount.copy()

	print("\nL1 :")
	print(itemset)
	print(supCount)

	#Generating C2
	itemset2 = []
	for i in range(len(itemset)):
		ele = itemset[i]
		for j in range(i+1,len(itemset)):
			temp = []
			temp.append(ele)
			temp.append(itemset[j])
			itemset2.append(temp)

	#Generating L2
	supCount2 = []
	index = 0
	while(index<len(itemset2)):
		supCount2.append(0)
		for line in items:
			if(set(itemset2[index]).issubset(set(line))):
				supCount2[-1]+=1
			#if(all(x in line for x in itemset2[index])):

		#print(itemset2[index]," ",supCount2," ",index)
		if(supCount2[-1]<minSupport):
			supCount2.pop()
			del itemset2[index]
			index-=1
		index+=1
	freqItemSet = freqItemSet + itemset2
	freqSupCount = freqSupCount + supCount2
	itemset = itemset2.copy()

	print("\nL2 :")
	print(itemset)
	print(supCount2)

	k=3
	while(itemset):
		common = k-2
		nextItemSet = []
		previousItemSet = itemset.copy()
		com = []
		for i in range(len(itemset)):
			ele = itemset[i]
			com = ele[0:common]
			for j in range(i+1,len(itemset)):
				if(set(com).issubset(set(itemset[j]))):
					temp = []
					temp = itemset[i]+itemset[j]
					#temp = list(set(itemset2[j]).union(set(itemset2[i])))
					temp = list(OrderedDict.fromkeys(temp))
					nextItemSet.append(temp)
		itemset = nextItemSet.copy()
		supCount = []
		index = 0
		while(index<len(itemset)):
			supCount.append(0)
			for line in items:
				if(set(itemset[index]).issubset(set(line))):
					supCount[-1]+=1
			if(supCount[-1]<minSupport):
				supCount.pop()
				del itemset[index]
				index-=1
			index+=1
		freqItemSet = freqItemSet + itemset
		freqSupCount = freqSupCount + supCount
		print("\nL",k," :")
		print(itemset)
		print(supCount)
		k+=1

	allItems = singleItemset + freqItemSet
	allItemSupCount = singleSupCount + freqSupCount 

	#Calculating Confidence
	print("\nThe Strong Association Rules are :")
	for item in freqItemSet:
		#rule = freqItemSet[i]
		subsets = []
		for i in range(1,len(item)):
			subsets += [list(x) for x in itertools.combinations(item, i)]
		for setItem in subsets:
			generation = [x for x in item if x not in setItem]
			confidence = allItemSupCount[allItems.index(item)]/allItemSupCount[allItems.index(setItem)]
			if(confidence>minConfidence and sItem in setItem): # and selectedItem == setItem
				print(setItem," --> ",generation," ",confidence*100,"%")
				temp = setItem + generation
				print(temp)
				strongAssociationRules.append(temp)
				#print(setItem," --> ",generation," ",confidence*100,"%")	
	print(strongAssociationRules)	
	#temp = set(tuple(x) for x in strongAssociationRules)
	#selectedRules = [ list(x) for x in strongAssociationRules]
	selectedRules = list(map(list, set(tuple(sorted(k)) for k in strongAssociationRules)))
	print(selectedRules)
	return selectedRules

def getImages(rules):
	print("In get Images")
	images = []
	print(rules)
	print(prodDetails)
	for rule in rules:
		temp = []
		for item in rule:
			for prod in prodDetails:
				if item in prod:
					temp.append(prod[4])
					break
		images.append(temp)
	print("IMAGES URL :")
	print(images)
	return images

def getPrice(rules):
	prices = []
	for rule in rules:
		price = 0
		for item in rule:
			for prod in prodDetails:
				if item in prod:
					price+=prod[7]
		prices.append(price)
	return prices
#xyz = apriori(selectedItem)
#xyz = apriori('formalShirt')
#print(xyz)
r = apriori('formalShirt')
i = getImages(r)

app = Flask(__name__)
@app.route('/')
def index():
	return render_template("index.html")


@app.route('/products')
def products():
	return render_template("items.html",productDetails = prodDetails)

@app.route('/products',methods = ['POST'])
def getvalue():
	name = request.form['prodName']
	rules = apriori(name)
	i = getImages(rules)
	p = getPrice(rules)
	#c.execute("SELECT * FROM itemset WHERE product_name = ",name)
	#sDetails = c.fetchall()
	for prod in prodDetails:
		if name in prod:
			sDetails = prod
			break
	print(rules)
	return render_template("product.html",images = i,selectedDetails = sDetails,prices = p)

if __name__ == "__main__":
	app.run()
