import SQLAlchemy
from sqlalchemy import create_engine, Table, Column, Integer, String, ForeignKey, Select

from sqlalchemy.orm import Session, declarative_base, relationship

Base = delcarative_base()

class User(Base):
    __tablename__ = 'users' # This should be same as table name in database
    user_id = Column(Integer, autoincrement=True, primary_key=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    
class Article(Base):
    __tablename__ = 'article'
    article_id = Column(Integer, autoincrement=True, primary_key=True)
    title = Column(String, unique=True)
    content = Column(String)


class ArticleAuthors(Base):
    __tablename__ = 'article_authors'
    user_id = Column(Integer, ForeignKey('users.user_id'), primary_key=True)
    article_id = Column(Integer,ForeignKey('article.article_id'), primary_key=True)



@app.route('/', methods=['GET', 'POST'])
def home():
    articles = Article.query.all()
    return render_template('index.html')


@app.route('/projects', methods=['GET', 'POST'])
def projects():
    articles = Article.query.all()
    return render_template('projects.html')

@app.route('/about_me', methods=['GET', 'POST'])
def about_me():
    articles = Article.query.all()
    return render_template('about_me.html')





if __name__ == '__main__':
    app.run(debug=True)
    








