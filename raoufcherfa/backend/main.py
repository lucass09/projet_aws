from flask import Flask, jsonify, request
import mysql.connector
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Connexion à la base de données
db = mysql.connector.connect(
    host="db",
    port=3306,
    user="root",
    password="example",
    database="employees",
    auth_plugin="mysql_native_password"
)

cursor = db.cursor()
# Routes

@ app.route('/', methods=['GET'])
def  get_raouf():       
    return 'hello Raouf'


# Afficher tous les employés de la bdd
@app.route('/api/v1/employees', methods=['GET']) 
def get_employees():     
    # Exécuter une requête SELECT pour récupérer tous les employés     
    cursor.execute("SELECT * FROM employees")     
    result = cursor.fetchall()     
    # Convertir le résultat en une liste de dictionnaires     
    employees = []     
    for row in result:         
        employee = {"id": row[0], "firstName": row[1], "lastName": row[2], "emailId": row[3]}         
        employees.append(employee)     
    return jsonify(employees)
 
# Afficher un employé de la bdd
@app.route('/api/v1/employees/<int:employee_id>', methods=['GET'])
def get_employee(employee_id):
    # Exécuter une requête SELECT pour récupérer tous les employés     
    cursor.execute("SELECT * FROM employees WHERE id = %s", (employee_id))     
    result = cursor.fetchone()     
    # Convertir le résultat en une liste de dictionnaires     
    employees = []     
    for row in result:         
        employee = {"id": row[0], "firstName": row[1], "lastName": row[2], "emailId": row[3]}         
        employees.append(employee)     
    return jsonify(employees)


# Ajouter un employé dans la bdd
@app.route('/api/v1/employees', methods=['POST'])
def add_employee():
    employee = request.get_json()
    # Récupération des données de la requête POST
    firstname = employee['firstName']
    lastname = employee['lastName']
    email = employee['emailId']

    # Insérer les données dans la table 'employees'
    sql = "INSERT INTO employees (firstName, lastName, emailId) VALUES (%s, %s, %s)"
    val = (firstname, lastname, email)
    cursor.execute(sql, val)

        # Sauvegarder les modifications
    db.commit()

    # Retourner une réponse JSON pour indiquer que l'employé a été ajouté
    response = {
        "status": "success",
        "message": "Employee added successfully."
    }
    return jsonify(response)

#Mettre à jour un employé de la bdd
@app.route('/api/v1/employees/<int:employee_id>', methods=['PUT'])
def update_employee(employee_id):
    employee = request.get_json()
    # Récupérer les données du formulaire
    firstname = employee['firstName']
    lastname = employee['lastName']
    email = employee['emailId']

    # Mettre à jour les données de l'employé dans la table 'employees'
    sql = "UPDATE employees SET firstName = %s, lastName = %s, emailId = %s WHERE id = %s"
    val = (firstname, lastname, email, employee_id)
    cursor.execute(sql, val)
    
    # Sauvegarder les modifications
    db.commit()

    # Retourner une réponse JSON pour indiquer que l'employé a été mis à jour
    response = {
        "status": "success",
        "message": "Employee updated successfully."
    }
    return jsonify(response)

# Supprimer un employé de la bdd
@app.route('/api/v1/employees/<int:employee_id>', methods=['DELETE'])
def delete_employee(employee_id):
    # Supprimer les données de l'employé dans la table 'employees'
    sql = "DELETE FROM employees WHERE id = %s"
    val = (employee_id,)
    cursor.execute(sql, val)

    # Sauvegarder les modifications
    db.commit()

    # Retourner une réponse JSON pour indiquer que l'employé a été supprimé
    response = {
        "status": "success",
        "message": "Employee deleted successfully."
    }
    return jsonify(response)


if __name__ == '__main__':
    cursor.execute("CREATE TABLE IF NOT EXISTS employees (ID INT AUTO_INCREMENT PRIMARY KEY, firstName VARCHAR(255), lastName VARCHAR(255), emailId VARCHAR(255))")
    app.run(host='0.0.0.0', port=8081, debug=True)
