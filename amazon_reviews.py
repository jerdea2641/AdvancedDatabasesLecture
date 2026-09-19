#Jeremy Dean
#09-18-2026
#PA 3.5

from cassandra.cluster import Cluster
import json

cluster = Cluster()
session = cluster.connect()

#create keyspace
session.execute("CREATE KEYSPACE IF NOT EXISTS Amazon WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1}")

#use keypspace
session.set_keyspace("amazon")

#create Reviews table
session.execute("CREATE TABLE IF NOT EXISTS Reviews (review_id text PRIMARY KEY, product_id text, reviewer_id text, stars int, review_body text, review_title text, product_category text)")
#create product_cat table
session.execute("CREATE TABLE IF NOT EXISTS ProductCategories (product_id text PRIMARY KEY, stars int, language text, product_category text)")

print("Amazon database and tables created.")

#insert data from JSON
with open("dataset_en_dev.json", "r") as file:
    for line in file:
        dataSet = json.loads(line)

        #prepare insert data into Reviews
        insertReviewsPrep = """
            INSERT INTO Reviews
            (review_id, product_id, reviewer_id, stars, review_body, review_title, product_category)
            VALUES(%s, %s, %s, %s, %s, %s, %s);
            """
        
        #execute insert statement using JSON data
        session.execute(insertReviewsPrep, [
            dataSet["review_id"],
            dataSet["product_id"],
            dataSet["reviewer_id"],
            int(dataSet["stars"]),
            dataSet["review_body"],
            dataSet["review_title"],
            dataSet["product_category"]
        ])
        
        #prepare insert data into Product_cat
        insertCategoriesPrep = """
            INSERT INTO ProductCategories
            (product_id, stars, language, product_category)
            VALUES(%s, %s, %s, %s);
            """
        #execute statement using JSON data
        session.execute(insertCategoriesPrep, [
            dataSet["product_id"],
            int(dataSet["stars"]),
            dataSet["language"],
            dataSet["product_category"]
        ])

print("Data inserted into tables.")
        
        
    
while True:
    print("Type in a number and press enter to execute the menu option.")
    print("1. Display product category list")
    print("2. Diplay high (4+) star review count")
    print("3. Display low (1) star review count")
    print("4. Enter a query")
    print("5. Add/Remove table columns")
    print("6. Delete tables")
    print("7. Delete keyspace")
    print("8. Exit the program")

    choice = input("Enter your selection: ")

    if choice == "1":
        rows = session.execute("SELECT product_category FROM ProductCategories")
        for row in rows:
            print(row.product_category)

    elif choice == "2":
        category = input("Enter product category: ")
        rows = session.execute("SELECT stars FROM Reviews WHERE product_category = %s ALLOW FILTERING", [category])
        count = 0
        for row in rows:
            if row.stars >= 4:
                count += 1
        print("4+ star reviews: ", count)

    elif choice == "3":
        category = input("Enter product category: ")
        rows = session.execute("SELECT stars FROM Reviews WHERE product_category = %s ALLOW FILTERING", [category])
        count = 0
        for row in rows:
            if row.stars == 1:
                count +=1
        print ("1-star reviews:", count)

    elif choice == "4":
        query = input("Enter CQL SELECT query: ")
        rows = session.execute (query)
        for row in rows:
            print(row)

    elif choice == "5":
        table = input("Enter a table name: ")
        action = input("ADD or Remove column? ")

        column = input("Enter column name: ")
        if action.lower() == "add":
            session.execute ("ALTER TABLE " + table + " ADD " + column + " text")

        elif action.lower() == "remove":
            session.execute("ALTER TABLE " + table + " DROP " + column)
    
    elif choice == "6":
        table = input("ENTER table name: ")
        session.execute("DROP TABLE " + table)

    elif choice == "7":
        session.execute("DROP KEYSPACE amazon")
        print("Amazon keyspace deleted")

    elif choice == "8":
        print("Goodbye")
        break



