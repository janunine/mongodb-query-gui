#         pipline = [{"$match":{"name": "Xinrui"}}, {"$sort": {"age": -1}}]
# json_string = '[{"$lookup": {"from": "students", "localField": "studentId", "foreignField": "_id", "as": "student_info"}}]'
#    [{"$lookup": {"from": "students", "localField": "studentId", "foreignField": "_id", "as": "student_info"}}, {"$limit":1}]
# db.students.aggregate([{"$match":{"name": "Xinrui"}}, {"$sort": {"age": -1}}])
# db.movies.aggregate([{"$match": {"imdb.rating": {"$gt": 9.3}}},{"$sort":{"year": -1}}])
# db.movies.aggregate([{"$match": {"imdb.rating": {"$gt": 9.3}}},{"$sort":{"year": -1}},{"$project":{"_id":0,"title":1,"year":1,"type":1}}])
# db.movies.aggregate([{"$match": {"imdb.rating": {"$gt": 9.3}}},{"$sort":{"year": -1}},{"$project":{"_id":0,"title":1,"year":1,"imdb.rating":1}}])
import ast
import json
import tkinter as tk
from tkinter import ttk
from pymongo import MongoClient
import re
from urllib.parse import quote_plus

# Sample queries to choose from
# sample_queries = [
#     'db.collection_name.find()',
#     'db.collection_name.insert({ "field": "value" })',
#     'db.collection_name.update({ "field": "value" }, { "$set": { "field": "new_value" } })',
#     'db.collection_name.aggregate([ ... ])'
# ]


# Function to execute the MongoDB query
def run_query():
    query_text = query_entry.get()
    results.delete(0, tk.END)

    # Connect to MongoDB
    client = MongoClient('mongodb://localhost:27017/')
    #client = MongoClient('')

    db = client['sample_mflix']



    try:
        # Extract the collection name from the dropdown selection
        collection_name = collection_var.get()
        collection = db[collection_name]
        print(collection)

        # Extract the content inside the parentheses using regular expressions
        query_content = re.search(r'\((.*?)\)', query_text).group(1).strip()

        # Execute the query based on the extracted content
        if query_text.startswith(f"db.{collection_name}.find"):
            if not query_content.strip():
                cursor = collection.find()
            else:
                cursor = collection.find(json.loads(query_content.strip()))
                print(json.loads(query_content.strip()))
        elif query_text.startswith(f"db.{collection_name}.aggregate"):

            # stage_strings = query_content.strip('[]').split(',')
            # print(stage_strings)
            #aggregation_pipeline = [json.loads(stage_string) for stage_string in stage_strings]
            #print(aggregation_pipeline)
            #cursor = collection.aggregate(aggregation_pipeline)

            # for debug
            # json_string = '[{"$lookup": {"from": "students", "localField": "studentId", "foreignField": "_id", "as": "student_info"}}]'
            #
            # python_list = json.loads(json_string)
            # cursor = collection.aggregate(python_list)

            python_list = json.loads(query_content)
            cursor = collection.aggregate(python_list)




        #
        # if query_text.startswith(f"db.{collection_name}.insert"):
        #     # Insert document
        #     document = eval(query_content)
        #     collection.insert_one(document)
        #     results.insert(tk.END, "Document inserted successfully.")
        # elif query_text.startswith(f"db.{collection_name}.update"):
        #     # Update document
        #     update_query = eval(query_content)
        #     collection.update_one(update_query['filter'], {'$set': update_query['update']})
        #     results.insert(tk.END, "Document updated successfully.")
        # elif query_text.startswith(f"db.{collection_name}.aggregate"):
        #     # Aggregate documents
        #     pipeline = eval(query_content)
        #     cursor = collection.aggregate(pipeline)
        # else:
        #     # Execute a custom find query
        #     cursor = collection.find(eval(query_content))
        #
        # if cursor:
        #     # Display results
        #     if query_text.strip() == f"db.{collection_name}.find()":
        #         # Special case to extract the specified field
        #         for document in cursor:
        #             results.insert(tk.END, document)
        #     else:
        #         for document in cursor:
        #             results.insert(tk.END, document)

        for document in cursor:
            results.insert(tk.END, document)
    except Exception as e:
        results.insert(tk.END, "Error: " + str(e))




def fetch_collections():
    client = MongoClient('mongodb://localhost:27017/')
    db = client['sample_mflix']
    collection_names = db.list_collection_names()
    collection_dropdown['values'] = collection_names

# Function to update the sample query with the selected collection name
def update_sample_query(event):
    selected_collection = collection_var.get()
    query_entry.delete(0, tk.END)
    query_entry.insert(0, f'db.{selected_collection}.aggregate()')




# Function to set the query with the selected collection and operation
def set_query(operation):
    collection_name = collection_var.get()
    query_entry.delete(0, tk.END)
    query_entry.insert(0, f'db.{collection_name}.{operation}()')





# Create the main application window
root = tk.Tk()
root.title("MongoDB Query Tool")

# Create and place GUI elements
query_label = ttk.Label(root, text="Enter Query:")
query_label.pack()

query_entry = ttk.Entry(root, width=40)
query_entry.insert(0, 'db.collection_name.aggregate()')  # Initial query example
query_entry.pack()

# Create the dropdown for selecting collections
collection_var = tk.StringVar()
collection_dropdown = ttk.Combobox(root, textvariable=collection_var)
collection_dropdown.pack()


# Create buttons for different query operations
operations = ["find", "aggregate", "update", "delete"]
for operation in operations:
    operation_button = tk.Button(root, text=operation.capitalize(), command=lambda op=operation: set_query(op))
    # operation_button.pack()
    operation_button.pack()


# Create a button to execute the query
execute_button = ttk.Button(root, text="Execute Query", command=run_query)
execute_button.pack()


# Bind the update_sample_query function to the <<ComboboxSelected>> event
collection_dropdown.bind("<<ComboboxSelected>>", update_sample_query)

# Fetch and display the collection names
fetch_collections()



results_label = ttk.Label(root, text="Query Results:")
results_label.pack()

results = tk.Listbox(root, height=10, width=60)
results.pack()

root.mainloop()
