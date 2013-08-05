import sqlalchemy as sqla
import sqlalchemy.orm as sqlorm
from sqlalchemy.ext.declarative import declarative_base as sqla_declarative_base

Base = sqla_declarative_base()
engine = sqla.create_engine('postgresql://vypsacoerijvxq:8ZcsasplA5yi7CsA-4PwDe0hBs@ec2-54-225-89-169.compute-1.amazonaws.com:5432/datc4qcfbqcni', echo=True)

    
class Blog(Base):
    __tablename__ = 'blog'
    id = sqla.Column('id', sqla.Integer, primary_key=True)
    title = sqla.Column('title', sqla.String)
    content = sqla.Column('content', sqla.String)
    tags = sqla.Column('tags', sqla.String)

Base.metadata.bind = engine
Base.metadata.create_all()

Session = sqlorm.scoped_session(sqlorm.sessionmaker(bind=engine))

def show_entry():
    session = Session()
    try:
    	entry = session.query(Blog).order_by(Blog.id.desc()).all()
    finally:
    	session.close()
    return entry

    		
def add_entry(title, content, tags):
    session = Session()
    entry = Blog(title=title, content=content, tags=tags)
    try:
	session.add(entry)
	session.flush()
	session.commit()
    finally:
	session.close()
    return True

def view_post(id):
    session = Session()
    try:
    	post = session.query(Blog).filter_by(id=id).all()
    finally:
	session.close()
    return post

def delete_post(id):
    session = Session()
    try:
	posts = session.query(Blog).filter_by(id=id).all()
	for post in posts:
		session.delete(post)
		session.commit()
    finally:
	session.close()
    return True

def edit_entry(id, title, content, tags):
    session = Session()
    try:
	post = session.query(Blog).filter_by(id=id).first()
	post.title = title
	post.content = content
	post.tags = tags
	session.commit()
    finally:
	session.close()
    return True

def search_post(key):
    session = Session()
    try:
	result = session.query(Blog).filter(Blog.content.like('%'+key+'%')).all()
    finally:
	session.close()
    return result
