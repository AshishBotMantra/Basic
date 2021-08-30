from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask('__name__')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.employee'
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False

db = SQLAlchemy(app)

ma = Marshmallow(app)

class EmployeeSchema(ma.Schema):
    class Meta():
        fields = ('id','name','emp_id','role')

employee_schema = EmployeeSchema()
employees_schema = EmployeeSchema(many=True)

#create database
@app.before_first_request
def create():
    db.create_all()


#Create Employee
@app.route('/employee',methods=['POST'])
def create_employee():
    name = request.json['name']
    emp_id = request.json['emp_id']
    role = request.json['role']

    new_employee = Employee(name, emp_id, role)
    db.session.add(new_employee)
    db.session.commit()
    return employee_schema.jsonify(new_employee)

#get all employee
@app.route('/employee',methods=['GET'])
def get_employee():
    all_employee =  Employee.query.all()
    result = employees_schema.dump(all_employee)
    return jsonify(result)

#get single employee
@app.route('/employee/<id>',methods=['GET'])
def employee(id):
    employee =  Employee.query.get(id)
    return employee_schema.jsonify(employee)

#update employee
@app.route('/employee/<id>',methods=['PUT'])
def update_employee(id):
    update = Employee.query.get(id)
    name = request.json['name']
    emp_id = request.json['emp_id']
    role = request.json['role']

    update.name = name
    update.emp_id = emp_id
    update.role = role

    db.session.commit()
    return employee_schema.jsonify(update)

#delete employee
@app.route('/employee/<id>', methods=['DELETE'])
def delete_employee(id):

    emp = Employee.query.get(id)
    db.session.delete(emp)
    db.session.commit()
    return employee_schema.jsonify(emp)

if __name__ == "__main__":
    app.run(debug=True)