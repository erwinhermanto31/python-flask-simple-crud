from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from marshmallow import fields
from marshmallow_sqlalchemy import ModelSchema, auto_field
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost:3306/testing_db'
db = SQLAlchemy(app)

###Product###
###Models####
class Product(db.Model):
    __tablename__ = "products"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    description = db.Column(db.String(100))
    logo_id = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

    def create(self):
      db.session.add(self)
      db.session.commit()
      return self
    def __init__(self,name,description,logo_id):
        self.name = name
        self.description = description
        self.logo_id = logo_id
    def __repr__(self):
        return '' % self.id
db.create_all()
class ProductSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = Product
        sqla_session = db.session
    id = fields.Number(dump_only=True)
    name = fields.String(required=True)
    description = fields.String(required=True)
    variants = fields.Dict()
    logo_id = fields.Number(required=True)
    created_at = fields.DateTime(required=False)
    updated_at = fields.DateTime(required=False)

@app.route('/products', methods = ['GET'])
def index():
    get_products = Product.query.all()
    product_schema = ProductSchema(many=True)
    variants_schema = VariantSchema()
    products = product_schema.dump(get_products)
    for v in products:
        print (v["id"])
        get_variant = Variant.query.filter_by(product_id=v["id"]).first()
        variants = variants_schema.dump(get_variant)
        v["variants"] = variants
    return make_response(jsonify({"product": products}))
@app.route('/products/<id>', methods = ['GET'])
def get_product_by_id(id):
    get_product = Product.query.get(id)
    product_schema = ProductSchema()
    product = product_schema.dump(get_product)
    return make_response(jsonify({"product": product}))
@app.route('/products/<id>', methods = ['PUT'])
def update_product_by_id(id):
    data = request.get_json()
    get_product = Product.query.get(id)
    if data.get('name'):
        get_product.name = data['name']
    if data.get('description'):
        get_product.description = data['description']
    if data.get('logo_id'):
        get_product.logo_id = data['logo_id']
    if data.get('updated_at'):
        get_product.updated_at= data['updated_at']    
    get_product.updated_at = datetime.now()
    db.session.add(get_product)
    db.session.commit()
    product_schema = ProductSchema(only=['id', 'name', 'description','logo_id','updated_at'])
    product = product_schema.dump(get_product)
    return make_response(jsonify({"product": product}))
@app.route('/products/<id>', methods = ['DELETE'])
def delete_product_by_id(id):
    get_product = Product.query.get(id)
    db.session.delete(get_product)
    db.session.commit()
    return make_response("",204)
@app.route('/products', methods = ['POST'])
def create_product():
    data = request.get_json()
    product_schema = ProductSchema()
    product = product_schema.load(data)
    product.created_at = datetime.now()
    result = product_schema.dump(product.create())
    return make_response(jsonify({"product": result}),200)
###End part product###

###Variants###
###Models###
class Variant(db.Model):
    __tablename__ = "Variants"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    product_id = db.Column(db.Integer)
    size = db.Column(db.Integer)
    color = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

    def create(self):
      db.session.add(self)
      db.session.commit()
      return self
    def __init__(self,name,size,product_id,color):
        self.name = name
        self.size = size
        self.product_id = product_id
        self.color = color
    def __repr__(self):
        return '' % self.id
db.create_all()
class VariantSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = Variant
        sqla_session = db.session
    id = fields.Number(dump_only=True)
    name = fields.String(required=True)
    size = fields.Number(required=True)
    product_id = fields.Number(required=True)
    color = fields.String(required=True)
    created_at = fields.DateTime(required=False)
    updated_at = fields.DateTime(required=False)

@app.route('/variants', methods = ['GET'])
def index_variant():
    get_variants = Variant.query.all()
    variants_schema = VariantSchema(many=True)
    variants = variants_schema.dump(get_variants)
    return make_response(jsonify({"variant": variants}))
@app.route('/variants/<id>', methods = ['GET'])
def get_variant_by_id(id):
    get_variant = Variant.query.get(id)
    variants_schema = VariantSchema()
    variant = variants_schema.dump(get_variant)
    return make_response(jsonify({"variant": variant}))
@app.route('/variants/<id>', methods = ['PUT'])
def update_variant_by_id(id):
    data = request.get_json()
    get_variant = Variant.query.get(id)
    if data.get('name'):
        get_variant.name = data['name']
    if data.get('size'):
        get_variant.size = data['size']
    if data.get('product_id'):
        get_variant.product_id = data['product_id']
    if data.get('color'):
        get_variant.color = data['color']
    if data.get('updated_at'):
        get_variant.updated_at= data['updated_at']    
    get_variant.updated_at = datetime.now()
    db.session.add(get_variant)
    db.session.commit()
    variants_schema = VariantSchema(only=['id', 'name', 'size','product_id','color','updated_at'])
    variant = variants_schema.dump(get_variant)
    return make_response(jsonify({"variant": variant}))
@app.route('/variants/<id>', methods = ['DELETE'])
def delete_variant_by_id(id):
    get_variant = Variant.query.get(id)
    db.session.delete(get_variant)
    db.session.commit()
    return make_response("",204)
@app.route('/variants', methods = ['POST'])
def create_variant():
    data = request.get_json()
    variants_schema = VariantSchema()
    variant = variants_schema.load(data)
    variant.created_at = datetime.now()
    result = variants_schema.dump(variant.create())
    return make_response(jsonify({"variant": result}),200)

if __name__ == "__main__":
    app.run(debug=True)