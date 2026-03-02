# coding: utf-8
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import INTEGER, TEXT, TSVECTOR
from sqlalchemy import Integer
from ..extensions import db


class Actor(db.Model):
    __tablename__ = 'actor'

    actor_id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    first_name = db.Column(db.Text, nullable=False)
    last_name = db.Column(db.Text, nullable=False, index=True)
    last_update = db.Column(db.DateTime(True), nullable=False, server_default=db.FetchedValue())



t_actor_info = db.Table(
    'actor_info',
    db.Column('actor_id', db.Integer),
    db.Column('first_name', db.Text),
    db.Column('last_name', db.Text),
    db.Column('film_info', db.Text)
)



class Addres(db.Model):
    __tablename__ = 'address'

    address_id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    address = db.Column(db.Text, nullable=False)
    address2 = db.Column(db.Text)
    district = db.Column(db.Text, nullable=False)
    city_id = db.Column(db.ForeignKey('city.city_id', ondelete='RESTRICT', onupdate='CASCADE'), nullable=False, index=True)
    postal_code = db.Column(db.Text)
    phone = db.Column(db.Text, nullable=False)
    last_update = db.Column(db.DateTime(True), nullable=False, server_default=db.FetchedValue())

    city = db.relationship('City', primaryjoin='Addres.city_id == City.city_id', backref='address')



class Category(db.Model):
    __tablename__ = 'category'

    category_id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    name = db.Column(db.Text, nullable=False)
    last_update = db.Column(db.DateTime(True), nullable=False, server_default=db.FetchedValue())



class City(db.Model):
    __tablename__ = 'city'

    city_id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    city = db.Column(db.Text, nullable=False)
    country_id = db.Column(db.ForeignKey('country.country_id', ondelete='RESTRICT', onupdate='CASCADE'), nullable=False, index=True)
    last_update = db.Column(db.DateTime(True), nullable=False, server_default=db.FetchedValue())

    country = db.relationship('Country', primaryjoin='City.country_id == Country.country_id', backref='cities')



class Country(db.Model):
    __tablename__ = 'country'

    country_id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    country = db.Column(db.Text, nullable=False)
    last_update = db.Column(db.DateTime(True), nullable=False, server_default=db.FetchedValue())



class Customer(db.Model):
    __tablename__ = 'customer'

    customer_id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    store_id = db.Column(db.ForeignKey('store.store_id', ondelete='RESTRICT', onupdate='CASCADE'), nullable=False, index=True)
    first_name = db.Column(db.Text, nullable=False)
    last_name = db.Column(db.Text, nullable=False, index=True)
    email = db.Column(db.Text)
    address_id = db.Column(db.ForeignKey('address.address_id', ondelete='RESTRICT', onupdate='CASCADE'), nullable=False, index=True)
    activebool = db.Column(db.Boolean, nullable=False, server_default=db.FetchedValue())
    create_date = db.Column(db.Date, nullable=False, server_default=db.FetchedValue())
    last_update = db.Column(db.DateTime(True), server_default=db.FetchedValue())
    active = db.Column(db.Integer)

    address = db.relationship('Addres', primaryjoin='Customer.address_id == Addres.address_id', backref='customers')
    store = db.relationship('Store', primaryjoin='Customer.store_id == Store.store_id', backref='customers')



t_customer_list = db.Table(
    'customer_list',
    db.Column('id', db.Integer),
    db.Column('name', db.Text),
    db.Column('address', db.Text),
    db.Column('zip code', db.Text),
    db.Column('phone', db.Text),
    db.Column('city', db.Text),
    db.Column('country', db.Text),
    db.Column('notes', db.Text),
    db.Column('sid', db.Integer)
)



class Film(db.Model):
    __tablename__ = 'film'

    film_id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    title = db.Column(db.Text, nullable=False, index=True)
    description = db.Column(db.Text)
    release_year = db.Column(db.Integer)
    language_id = db.Column(db.ForeignKey('language.language_id', ondelete='RESTRICT', onupdate='CASCADE'), nullable=False, index=True)
    original_language_id = db.Column(db.ForeignKey('language.language_id', ondelete='RESTRICT', onupdate='CASCADE'), index=True)
    rental_duration = db.Column(db.SmallInteger, nullable=False, server_default=db.FetchedValue())
    rental_rate = db.Column(db.Numeric(4, 2), nullable=False, server_default=db.FetchedValue())
    length = db.Column(db.SmallInteger)
    replacement_cost = db.Column(db.Numeric(5, 2), nullable=False, server_default=db.FetchedValue())
    rating = db.Column(db.Enum('G', 'PG', 'PG-13', 'R', 'NC-17', name='mpaa_rating'), server_default=db.FetchedValue())
    last_update = db.Column(db.DateTime(True), nullable=False, server_default=db.FetchedValue())
    special_features = db.Column(db.ARRAY(TEXT()))
    fulltext = db.Column(TSVECTOR, nullable=False)
    language = db.relationship('Language', primaryjoin='Film.language_id == Language.language_id', backref='language_films')
    original_language = db.relationship('Language', primaryjoin='Film.original_language_id == Language.language_id', backref='language_films_0')



class FilmActor(db.Model):
    __tablename__ = 'film_actor'

    actor_id = db.Column(db.ForeignKey('actor.actor_id', ondelete='RESTRICT', onupdate='CASCADE'), primary_key=True, nullable=False)
    film_id = db.Column(db.ForeignKey('film.film_id', ondelete='RESTRICT', onupdate='CASCADE'), primary_key=True, nullable=False, index=True)
    last_update = db.Column(db.DateTime(True), nullable=False, server_default=db.FetchedValue())

    actor = db.relationship('Actor', primaryjoin='FilmActor.actor_id == Actor.actor_id', backref='film_actors')
    film = db.relationship('Film', primaryjoin='FilmActor.film_id == Film.film_id', backref='film_actors')



class FilmCategory(db.Model):
    __tablename__ = 'film_category'

    film_id = db.Column(db.ForeignKey('film.film_id', ondelete='RESTRICT', onupdate='CASCADE'), primary_key=True, nullable=False)
    category_id = db.Column(db.ForeignKey('category.category_id', ondelete='RESTRICT', onupdate='CASCADE'), primary_key=True, nullable=False)
    last_update = db.Column(db.DateTime(True), nullable=False, server_default=db.FetchedValue())

    category = db.relationship('Category', primaryjoin='FilmCategory.category_id == Category.category_id', backref='film_categories')
    film = db.relationship('Film', primaryjoin='FilmCategory.film_id == Film.film_id', backref='film_categories')



t_film_list = db.Table(
    'film_list',
    db.Column('fid', db.Integer),
    db.Column('title', db.Text),
    db.Column('description', db.Text),
    db.Column('category', db.Text),
    db.Column('price', db.Numeric(4, 2)),
    db.Column('length', db.SmallInteger),
    db.Column('rating', db.Enum('G', 'PG', 'PG-13', 'R', 'NC-17', name='mpaa_rating')),
    db.Column('actors', db.Text)
)



class Inventory(db.Model):
    __tablename__ = 'inventory'
    __table_args__ = (
        db.Index('idx_store_id_film_id', 'store_id', 'film_id'),
    )

    inventory_id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    film_id = db.Column(db.ForeignKey('film.film_id', ondelete='RESTRICT', onupdate='CASCADE'), nullable=False)
    store_id = db.Column(db.ForeignKey('store.store_id', ondelete='RESTRICT', onupdate='CASCADE'), nullable=False)
    last_update = db.Column(db.DateTime(True), nullable=False, server_default=db.FetchedValue())

    film = db.relationship('Film', primaryjoin='Inventory.film_id == Film.film_id', backref='inventories')
    store = db.relationship('Store', primaryjoin='Inventory.store_id == Store.store_id', backref='inventories')



class Language(db.Model):
    __tablename__ = 'language'

    language_id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    name = db.Column(db.String(20), nullable=False)
    last_update = db.Column(db.DateTime(True), nullable=False, server_default=db.FetchedValue())



t_nicer_but_slower_film_list = db.Table(
    'nicer_but_slower_film_list',
    db.Column('fid', db.Integer),
    db.Column('title', db.Text),
    db.Column('description', db.Text),
    db.Column('category', db.Text),
    db.Column('price', db.Numeric(4, 2)),
    db.Column('length', db.SmallInteger),
    db.Column('rating', db.Enum('G', 'PG', 'PG-13', 'R', 'NC-17', name='mpaa_rating')),
    db.Column('actors', db.Text)
)



class Payment(db.Model):
    __tablename__ = 'payment'

    payment_id = db.Column(db.Integer, primary_key=True, nullable=False, server_default=db.FetchedValue())
    customer_id = db.Column(db.Integer, nullable=False)
    staff_id = db.Column(db.Integer, nullable=False)
    rental_id = db.Column(db.Integer, nullable=False)
    amount = db.Column(db.Numeric(5, 2), nullable=False)
    payment_date = db.Column(db.DateTime(True), primary_key=True, nullable=False)



class PaymentP202201(db.Model):
    __tablename__ = 'payment_p2022_01'

    payment_id = db.Column(db.Integer, primary_key=True, nullable=False, server_default=db.FetchedValue())
    customer_id = db.Column(db.ForeignKey('customer.customer_id'), nullable=False, index=True)
    staff_id = db.Column(db.ForeignKey('staff.staff_id'), nullable=False, index=True)
    rental_id = db.Column(db.ForeignKey('rental.rental_id'), nullable=False)
    amount = db.Column(db.Numeric(5, 2), nullable=False)
    payment_date = db.Column(db.DateTime(True), primary_key=True, nullable=False)

    customer = db.relationship('Customer', primaryjoin='PaymentP202201.customer_id == Customer.customer_id', backref='payment_p202201s')
    rental = db.relationship('Rental', primaryjoin='PaymentP202201.rental_id == Rental.rental_id', backref='payment_p202201s')
    staff = db.relationship('Staff', primaryjoin='PaymentP202201.staff_id == Staff.staff_id', backref='payment_p202201s')



class PaymentP202202(db.Model):
    __tablename__ = 'payment_p2022_02'

    payment_id = db.Column(db.Integer, primary_key=True, nullable=False, server_default=db.FetchedValue())
    customer_id = db.Column(db.ForeignKey('customer.customer_id'), nullable=False, index=True)
    staff_id = db.Column(db.ForeignKey('staff.staff_id'), nullable=False, index=True)
    rental_id = db.Column(db.ForeignKey('rental.rental_id'), nullable=False)
    amount = db.Column(db.Numeric(5, 2), nullable=False)
    payment_date = db.Column(db.DateTime(True), primary_key=True, nullable=False)

    customer = db.relationship('Customer', primaryjoin='PaymentP202202.customer_id == Customer.customer_id', backref='payment_p202202s')
    rental = db.relationship('Rental', primaryjoin='PaymentP202202.rental_id == Rental.rental_id', backref='payment_p202202s')
    staff = db.relationship('Staff', primaryjoin='PaymentP202202.staff_id == Staff.staff_id', backref='payment_p202202s')



class PaymentP202203(db.Model):
    __tablename__ = 'payment_p2022_03'

    payment_id = db.Column(db.Integer, primary_key=True, nullable=False, server_default=db.FetchedValue())
    customer_id = db.Column(db.ForeignKey('customer.customer_id'), nullable=False, index=True)
    staff_id = db.Column(db.ForeignKey('staff.staff_id'), nullable=False, index=True)
    rental_id = db.Column(db.ForeignKey('rental.rental_id'), nullable=False)
    amount = db.Column(db.Numeric(5, 2), nullable=False)
    payment_date = db.Column(db.DateTime(True), primary_key=True, nullable=False)

    customer = db.relationship('Customer', primaryjoin='PaymentP202203.customer_id == Customer.customer_id', backref='payment_p202203s')
    rental = db.relationship('Rental', primaryjoin='PaymentP202203.rental_id == Rental.rental_id', backref='payment_p202203s')
    staff = db.relationship('Staff', primaryjoin='PaymentP202203.staff_id == Staff.staff_id', backref='payment_p202203s')



class PaymentP202204(db.Model):
    __tablename__ = 'payment_p2022_04'

    payment_id = db.Column(db.Integer, primary_key=True, nullable=False, server_default=db.FetchedValue())
    customer_id = db.Column(db.ForeignKey('customer.customer_id'), nullable=False, index=True)
    staff_id = db.Column(db.ForeignKey('staff.staff_id'), nullable=False, index=True)
    rental_id = db.Column(db.ForeignKey('rental.rental_id'), nullable=False)
    amount = db.Column(db.Numeric(5, 2), nullable=False)
    payment_date = db.Column(db.DateTime(True), primary_key=True, nullable=False)

    customer = db.relationship('Customer', primaryjoin='PaymentP202204.customer_id == Customer.customer_id', backref='payment_p202204s')
    rental = db.relationship('Rental', primaryjoin='PaymentP202204.rental_id == Rental.rental_id', backref='payment_p202204s')
    staff = db.relationship('Staff', primaryjoin='PaymentP202204.staff_id == Staff.staff_id', backref='payment_p202204s')



class PaymentP202205(db.Model):
    __tablename__ = 'payment_p2022_05'

    payment_id = db.Column(db.Integer, primary_key=True, nullable=False, server_default=db.FetchedValue())
    customer_id = db.Column(db.ForeignKey('customer.customer_id'), nullable=False, index=True)
    staff_id = db.Column(db.ForeignKey('staff.staff_id'), nullable=False, index=True)
    rental_id = db.Column(db.ForeignKey('rental.rental_id'), nullable=False)
    amount = db.Column(db.Numeric(5, 2), nullable=False)
    payment_date = db.Column(db.DateTime(True), primary_key=True, nullable=False)

    customer = db.relationship('Customer', primaryjoin='PaymentP202205.customer_id == Customer.customer_id', backref='payment_p202205s')
    rental = db.relationship('Rental', primaryjoin='PaymentP202205.rental_id == Rental.rental_id', backref='payment_p202205s')
    staff = db.relationship('Staff', primaryjoin='PaymentP202205.staff_id == Staff.staff_id', backref='payment_p202205s')



class PaymentP202206(db.Model):
    __tablename__ = 'payment_p2022_06'

    payment_id = db.Column(db.Integer, primary_key=True, nullable=False, server_default=db.FetchedValue())
    customer_id = db.Column(db.ForeignKey('customer.customer_id'), nullable=False, index=True)
    staff_id = db.Column(db.ForeignKey('staff.staff_id'), nullable=False, index=True)
    rental_id = db.Column(db.ForeignKey('rental.rental_id'), nullable=False)
    amount = db.Column(db.Numeric(5, 2), nullable=False)
    payment_date = db.Column(db.DateTime(True), primary_key=True, nullable=False)

    customer = db.relationship('Customer', primaryjoin='PaymentP202206.customer_id == Customer.customer_id', backref='payment_p202206s')
    rental = db.relationship('Rental', primaryjoin='PaymentP202206.rental_id == Rental.rental_id', backref='payment_p202206s')
    staff = db.relationship('Staff', primaryjoin='PaymentP202206.staff_id == Staff.staff_id', backref='payment_p202206s')



class PaymentP202207(db.Model):
    __tablename__ = 'payment_p2022_07'

    payment_id = db.Column(db.Integer, primary_key=True, nullable=False, server_default=db.FetchedValue())
    customer_id = db.Column(db.Integer, nullable=False)
    staff_id = db.Column(db.Integer, nullable=False)
    rental_id = db.Column(db.Integer, nullable=False)
    amount = db.Column(db.Numeric(5, 2), nullable=False)
    payment_date = db.Column(db.DateTime(True), primary_key=True, nullable=False)



class Rental(db.Model):
    __tablename__ = 'rental'
    __table_args__ = (
        db.Index('idx_unq_rental_rental_date_inventory_id_customer_id', 'rental_date', 'inventory_id', 'customer_id'),
    )

    rental_id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    rental_date = db.Column(db.DateTime(True), nullable=False)
    inventory_id = db.Column(db.ForeignKey('inventory.inventory_id', ondelete='RESTRICT', onupdate='CASCADE'), nullable=False, index=True)
    customer_id = db.Column(db.ForeignKey('customer.customer_id', ondelete='RESTRICT', onupdate='CASCADE'), nullable=False)
    return_date = db.Column(db.DateTime(True))
    staff_id = db.Column(db.ForeignKey('staff.staff_id', ondelete='RESTRICT', onupdate='CASCADE'), nullable=False)
    last_update = db.Column(db.DateTime(True), nullable=False, server_default=db.FetchedValue())

    customer = db.relationship('Customer', primaryjoin='Rental.customer_id == Customer.customer_id', backref='rentals')
    inventory = db.relationship('Inventory', primaryjoin='Rental.inventory_id == Inventory.inventory_id', backref='rentals')
    staff = db.relationship('Staff', primaryjoin='Rental.staff_id == Staff.staff_id', backref='rentals')



t_rental_by_category = db.Table(
    'rental_by_category',
    db.Column('category', db.Text, unique=True),
    db.Column('total_sales', db.Numeric)
)



t_sales_by_film_category = db.Table(
    'sales_by_film_category',
    db.Column('category', db.Text),
    db.Column('total_sales', db.Numeric)
)



t_sales_by_store = db.Table(
    'sales_by_store',
    db.Column('store', db.Text),
    db.Column('manager', db.Text),
    db.Column('total_sales', db.Numeric)
)



class Staff(db.Model):
    __tablename__ = 'staff'

    staff_id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    first_name = db.Column(db.Text, nullable=False)
    last_name = db.Column(db.Text, nullable=False)
    address_id = db.Column(db.ForeignKey('address.address_id', ondelete='RESTRICT', onupdate='CASCADE'), nullable=False)
    email = db.Column(db.Text)
    store_id = db.Column(db.ForeignKey('store.store_id'), nullable=False)
    active = db.Column(db.Boolean, nullable=False, server_default=db.FetchedValue())
    username = db.Column(db.Text, nullable=False)
    password = db.Column(db.Text)
    last_update = db.Column(db.DateTime(True), nullable=False, server_default=db.FetchedValue())
    picture = db.Column(db.LargeBinary)

    address = db.relationship('Addres', primaryjoin='Staff.address_id == Addres.address_id', backref='staffs')
    store = db.relationship('Store', primaryjoin='Staff.store_id == Store.store_id', backref='staffs')



t_staff_list = db.Table(
    'staff_list',
    db.Column('id', db.Integer),
    db.Column('name', db.Text),
    db.Column('address', db.Text),
    db.Column('zip code', db.Text),
    db.Column('phone', db.Text),
    db.Column('city', db.Text),
    db.Column('country', db.Text),
    db.Column('sid', db.Integer)
)

class Store(db.Model):
    __tablename__ = 'store'

    store_id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    manager_staff_id = db.Column(db.Integer, nullable=False, unique=True)
    address_id = db.Column(db.ForeignKey('address.address_id', ondelete='RESTRICT', onupdate='CASCADE'), nullable=False)
    last_update = db.Column(db.DateTime(True), nullable=False, server_default=db.FetchedValue())

    address = db.relationship('Addres', primaryjoin='Store.address_id == Addres.address_id', backref='stores')
