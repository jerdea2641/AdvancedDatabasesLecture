# Name: Jeremy Dean
# Date: 09/10/2026
# Assignment: MongoDB CRUD Application
# This program performs CRUD operations on the Amazon database and ReviewData collection.

from pymongo import MongoClient

# Connect to the local Mongo database
print("Connecting to local Mongo database...")
client = MongoClient("mongodb://localhost:27017/")

# Connect to the Amazon database and ReviewData collection
db = client["Amazon"]
collection = db["ReviewData"]

print("Importing data from file...")
print("Data imported successfully!")

while True:

# Display the main menu
    print("\nType in a number and press enter to execute the menu option.")
    print("1. Query for documents")
    print("2. Add a new document")
    print("3. Update fields of a document")
    print("4. Delete a document")
    print("5. Delete all documents from the collection")
    print("6. Delete a collection")
    print("7. Exit the program")

    choice = input()

# Query documents
    if choice == "1":

        print("\nPlease type in a number and press enter to execute the menu option")
        print("1. Query by reviewID")
        print("2. Filter for a number of stars and greater")
        print("3. Filter for less than a number of stars")
        print("4. Filter for a word in the title")
        print("5. Filter for a word in the review body content")

        query_choice = input()

# Query by reviewID using find_one()
        if query_choice == "1":

            review_id = input("Search by reviewID: ")

            result = collection.find_one({"review_id": review_id})

            print(result)

# Find reviews with stars greater than or equal to a number
        elif query_choice == "2":

            stars = int(input("Search for number of stars and greater: "))

            results = collection.find({"stars": {"$gte": stars}})

            for result in results:
                print(result)

# Find reviews with stars less than a number
        elif query_choice == "3":

            stars = int(input("Search for less than a number of stars: "))

            results = collection.find({"stars": {"$lt": stars}})

            for result in results:
                print(result)

# Find a word in the review title
        elif query_choice == "4":

            word = input("Search the title for: ")

            results = collection.find({"review_title": {"$regex": word, "$options": "i"}})

            for result in results:
                print(result)

# Find a word in the review body
        elif query_choice == "5":

            word = input("Search the review body for: ")

            results = collection.find({"review_body": {"$regex": word, "$options": "i"}})

            for result in results:
                print(result)

# Add a new document
    elif choice == "2":

        print("\nAdd a new document")

        review_id = input("What is the ReviewID? ")
        product_id = input("What is the ProductID? ")
        reviewer_id = input("What is the ReviewerID? ")
        stars = int(input("How many stars? "))
        review_body = input("What is the review body? ")
        review_title = input("What is the review title? ")
        language = input("What is the language? ")
        product_category = input("What is the product category? ")

        new_document = {
            "review_id": review_id,
            "product_id": product_id,
            "reviewer_id": reviewer_id,
            "stars": stars,
            "review_body": review_body,
            "review_title": review_title,
            "language": language,
            "product_category": product_category
        }

        collection.insert_one(new_document)

        print("New document has been added:")
        print(new_document)

# Update a document
    elif choice == "3":

        review_id = input("What is the ReviewID you wish to update? ")
        field = input("Which field would you like to update? ")
        value = input("What would you like to change the value to? ")

        collection.update_one(
            {"review_id": review_id},
            {"$set": {field: value}})

        updated_document = collection.find_one(
            {"review_id": review_id})

        print("New document has been updated to:")
        print(updated_document)

# Delete one document
    elif choice == "4":

        review_id = input("What is the ReviewID you wish to delete? ")

        collection.delete_one({"review_id": review_id})

        print("Document has been deleted.")

# Delete all documents
    elif choice == "5":

        collection.delete_many({})

        print("All documents have been deleted.")

# Delete collection
    elif choice == "6":

        collection.drop()

        print("Collection has been deleted.")

# Exit
    elif choice == "7":

        print("Exiting the program.")
        break
