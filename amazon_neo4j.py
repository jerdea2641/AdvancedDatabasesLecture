#Jeremy Dean
#Date: 09-25-20226
#Assignment: PA 4.5

from neo4j import GraphDatabase
import json


# Connect to Neo4j
driver = GraphDatabase.driver(
    "bolt://localhost:7687",
    auth=("neo4j", "password1")
)


# Import data from JSON file
def import_data():

    with open("dataset_en_dev.json", "r", encoding="utf-8") as file:

        with driver.session() as session:

            for line in file:

                item = json.loads(line)

                # Create Category
                session.run(
                    "MERGE (:Category {name: $category})",
                    category=item["product_category"]
                )

                # Create Product
                session.run(
                    "MERGE (:Product {name: $product})",
                    product=item["product_id"]
                )

                # Create Reviewer
                session.run(
                    "MERGE (:Reviewer {name: $reviewer})",
                    reviewer=item["reviewer_id"]
                )

                # Create Review
                session.run(
                    """
                    MERGE (r:Review {review_id: $review_id})
                    SET r.title = $title,
                        r.content = $content,
                        r.stars = $stars
                    """,
                    review_id=item["review_id"],
                    title=item["review_title"],
                    content=item["review_body"],
                    stars=item["stars"]
                )

                # Product belongs to Category
                session.run(
                    """
                    MATCH (p:Product {name: $product})
                    MATCH (c:Category {name: $category})
                    MERGE (p)-[:BELONGS_TO]->(c)
                    """,
                    product=item["product_id"],
                    category=item["product_category"]
                )

                # Product has Review
                session.run(
                    """
                    MATCH (p:Product {name: $product})
                    MATCH (r:Review {review_id: $review_id})
                    MERGE (p)-[:HAS_REVIEW]->(r)
                    """,
                    product=item["product_id"],
                    review_id=item["review_id"]
                )

                # Reviewer wrote Review
                session.run(
                    """
                    MATCH (u:Reviewer {name: $reviewer})
                    MATCH (r:Review {review_id: $review_id})
                    MERGE (u)-[:WROTE]->(r)
                    """,
                    reviewer=item["reviewer_id"],
                    review_id=item["review_id"]
                )

    print("\nData imported successfully.")


# Create a node
def create_node():

    print("\n1. Category")
    print("2. Product")
    print("3. Reviewer")
    print("4. Review")

    choice = input("Choose node type: ")

    with driver.session() as session:

        if choice == "1":

            name = input("Enter category name: ")

            session.run(
                "CREATE (:Category {name: $name})",
                name=name
            )

            print("Category created.")

        elif choice == "2":

            name = input("Enter product ID: ")

            session.run(
                "CREATE (:Product {name: $name})",
                name=name
            )

            print("Product created.")

        elif choice == "3":

            name = input("Enter reviewer ID: ")

            session.run(
                "CREATE (:Reviewer {name: $name})",
                name=name
            )

            print("Reviewer created.")

        elif choice == "4":

            review_id = input("Enter review ID: ")
            title = input("Enter review title: ")
            content = input("Enter review content: ")
            stars = input("Enter stars: ")

            session.run(
                """
                CREATE (:Review {
                    review_id: $review_id,
                    title: $title,
                    content: $content,
                    stars: $stars
                })
                """,
                review_id=review_id,
                title=title,
                content=content,
                stars=stars
            )

            print("Review created.")

        else:

            print("Invalid choice.")


# Create a relationship
def create_relationship():

    print("\n1. Product -> Category")
    print("2. Product -> Review")
    print("3. Reviewer -> Review")

    choice = input("Choose relationship: ")

    with driver.session() as session:

        if choice == "1":

            product = input("Enter product ID: ")
            category = input("Enter category name: ")

            session.run(
                """
                MATCH (p:Product {name: $product})
                MATCH (c:Category {name: $category})
                MERGE (p)-[:BELONGS_TO]->(c)
                """,
                product=product,
                category=category
            )

            print("Relationship created.")

        elif choice == "2":

            product = input("Enter product ID: ")
            review_id = input("Enter review ID: ")

            session.run(
                """
                MATCH (p:Product {name: $product})
                MATCH (r:Review {review_id: $review_id})
                MERGE (p)-[:HAS_REVIEW]->(r)
                """,
                product=product,
                review_id=review_id
            )

            print("Relationship created.")

        elif choice == "3":

            reviewer = input("Enter reviewer ID: ")
            review_id = input("Enter review ID: ")

            session.run(
                """
                MATCH (u:Reviewer {name: $reviewer})
                MATCH (r:Review {review_id: $review_id})
                MERGE (u)-[:WROTE]->(r)
                """,
                reviewer=reviewer,
                review_id=review_id
            )

            print("Relationship created.")

        else:

            print("Invalid choice.")


# Count products associated with a category
def count_products():

    category = input("Enter category name: ")

    with driver.session() as session:

        result = session.run(
            """
            MATCH (c:Category {name: $category})
            MATCH (p:Product)-[:BELONGS_TO]->(c)
            RETURN count(p) AS total
            """,
            category=category
        )

        record = result.single()

        print("Product count:", record["total"])


# Count reviews associated with a reviewer
def count_reviews():

    reviewer = input("Enter reviewer ID: ")

    with driver.session() as session:

        result = session.run(
            """
            MATCH (u:Reviewer {name: $reviewer})
            MATCH (u)-[:WROTE]->(r:Review)
            RETURN count(r) AS total
            """,
            reviewer=reviewer
        )

        record = result.single()

        print("Review count:", record["total"])


# Delete a category
def delete_category():

    category = input("Enter category name: ")

    with driver.session() as session:

        session.run(
            """
            MATCH (c:Category {name: $category})
            DETACH DELETE c
            """,
            category=category
        )

    print("Category deleted.")


# Delete all relationships
def delete_relationships():

    with driver.session() as session:

        session.run(
            "MATCH ()-[r]-() DELETE r"
        )

    print("All relationships deleted.")


# Delete all nodes
def delete_nodes():

    with driver.session() as session:

        session.run(
            "MATCH (n) DETACH DELETE n"
        )

    print("All nodes deleted.")


# Import the JSON data automatically
try:

    import_data()

except Exception as e:

    print("\nJSON import could not be completed.")
    print("Error:", e)


# Main menu
while True:

    print("\n======================")
    print("      NEO4J MENU")
    print("======================")
    print("1. Create node")
    print("2. Create relationship")
    print("3. Count products in category")
    print("4. Count reviews by reviewer")
    print("5. Delete category")
    print("6. Delete all relationships")
    print("7. Delete all nodes")
    print("8. Exit")

    choice = input("Enter choice: ")

    if choice == "1":

        create_node()

    elif choice == "2":

        create_relationship()

    elif choice == "3":

        count_products()

    elif choice == "4":

        count_reviews()

    elif choice == "5":

        delete_category()

    elif choice == "6":

        delete_relationships()

    elif choice == "7":

        delete_nodes()

    elif choice == "8":

        print("Goodbye.")
        break

    else:

        print("Invalid choice.")


# Close Neo4j connection
driver.close()
