from flask import Flask, request, render_template
#### Importing SQLAlchemy ###############
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

######Database Configurations #############
# app.config is the dictionary through which we can update the settings for
#whole project.

app.config.update(

SECRET_KEY = 'topsecret',
#SQLALCHEMY_DATABASE_URI = '<database>://<user_id>:<password>@<server>/<database_name>',
SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:pepper80@localhost/catalog_db',
SQLALCHEMY_TRACK_MODIFICATIONS = False
)

db = SQLAlchemy(app)

##########################################
@app.route('/table')
def movies_2017():
    movies_dict = { 'Star Wars: The Last Jedi': 2.14,
                    'Beauty and the Beast': 1.2,
                    'The Fate of the Furious': 3.5,
                    'Despicable Me 3': 2.5,
                    'Jumanji: Welcome to the Jungle': 2.6,
                    'Spider-Man: Homecoming': 1.7,
                    'Wolf Warrior 2': 5.4}

    return render_template('table_data.html',
                            movies = movies_dict,
                            name = 'Sally')
################## Publication class ##############################
class Publication(db.Model):
    __tablename__ = 'publication'

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(80), nullable = False)

    def __init__(self, name):
        # self.id = id   # it will be generated automatically
        self.name = name

    def __repr__(self):
        return 'Publisher is {}'.format(self.name)

##############Book ###########################
class Book(db.Model):
    __tablename__ = 'book'

    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(500), nullable = False, index = True)
    author = db.Column(db.String(350))
    avg_rating = db.Column(db.Float)
    format = db.Column(db.String(50))
    image = db.Column(db.String(100), unique = True)
    num_pages = db.Column(db.Integer)
    #for the following, first import => from datetime import datetime
    pub_date = db.Column(db.DateTime, default = datetime.utcnow())

    #relationship
    pub_id = db.Column(db.Integer, db.ForeignKey('publication.id'))

    def __init__(self, title, author, avg_rating, book_format, image, num_pages, pub_id):

        self.title = title
        self.author = author
        self.avg_rating = avg_rating
        self.format = book_format
        self.image = image
        self.num_pages = num_pages
        self.pub_id = pub_id

    def __repr__(self):
        return '{} by {}'.format(self.title, self.author)


###################################################
#
#               Creating a Table in database_name
###################################################

# (step 1) from run import db, Publication where 'Publication' is the Table name
# you can run this in CMD
# (Step 2) pub = Publication(100, 'Oxford Publications') create an instance

# (step 3) db.session.add(pub)  create a session
# you can add many instances of table using:

#db.session.add_all([para, oracle])

# (step 4) db.session.commit()  call a commit method to save it to db, it is similar to
# temporary memory where all un-commited actions exist

#important info
#---------------
# use dir(pub) to get all the properties of an instance

#--------------------------END ---------------------


###########################################################
#
#         1. populating tables through Excel
#         2. Querying tables/Data
#
###########################################################

# Steps
# (1) from run import db, Publication , book

# (2) copy and past all commands from excel sheet into console
#---------------------------------------------------------
#Book.query.all()  this will retrieve all the data in the list format
#EXAMPLE:
#>>> all = Book.query.all()
#>>> type(all)
#<type 'list'>
#-------------------------
# To get the first record

#>>> first = Book.query.first()
#>>> first
#Miky's Delivery Service by William Dobelli

#Note: the output is based on the repr method defined earlier
#-----------------------------------
# using filters
# in this example, I filter the data based on 'ePub', it is similar to 'where' in
#traditional SQL (where format = 'ePub')
#>>>filter_data = Book.query.filter_by(format = 'ePub').all()
#>>> filter_data
#[Miky's Delivery Service by William Dobelli, The Sacred Book of Kairo by Heidi Zimmerman]
#-----------------------------------------------------

#Getting the data based on the primaryKey
#>>> pk = Book.query.get(1)
#---------------------------------------------------

#for getting first 5 records from the tables
#Book.query.limit(5).all()
#---------------------------------------------------

#order_by method
#this method will order the book data based on title
#>>> order_records = Book.query.order_by(Book.title).all()
#>>> order_records
#-----------------------------------------------------------

# we can chain all methods together
#>> we first filter the database
#>> then we used resultant data and ordered it based on the title
#Book.query.filter_by(format = 'Paperback').order_by(Book.title).all()
#-----------------------------------------------------------------------

#query data from two tables (takiong advantage of foregn keys)

#lets say, we want to query the publication table first and fetch the first records
#result = Publication.query.filter_by(name = 'Broadway Press').first()

#next, we will use the ID from this publisher to query into the Book tables
#broadway = Book.query.filter_by(pub_id = result.id).all()
#remember that result is an instance of publication, so we can access the attribute using
#result.id

#-------------------------------------------------------------

######################################################################
#
#                 Updating and Deleting records
#
#######################################################################

#Steps for updating record

# (1) first you need to access the record which you want to update
# u = Book.query.get(16)
#
# (2) then you need to use attribute of an instance 'u' to update values
# u.format = 'Hardcover'
#
# (3) do not forget to commit changes
# db.session.commit()
#-----------------------------------------------------

#deleting the records

# Steps
# 1) first access the record which you want to delete
# x = Book.query.get(10)
#
# 2) then delete it using session, do not forget to pass instance 'x'
# db.session.delete(x)
#
# 3) commit changes
# db.session.commit()
#--------------------------------------------------------

#deleting record from the parent table

# first you need to delete records from the child tables

# note: use db.session.close() to avoid any conficts with previous operations

# Steps
# step # 1:
# >>> Book.query.filter_by(pub_id=6).delete()
# 3
# this will delete 3 record

#step # 2:
# db.session.commit()

# step # 3:
# >>> Publication.query.filter_by(id=6).delete()
# 1
# >>> db.session.commit()











if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
