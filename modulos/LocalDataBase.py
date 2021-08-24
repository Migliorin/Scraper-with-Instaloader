from pony.orm import Required
from pony import orm
import os


db = orm.Database()




class PostagemInstagram(db.Entity):
    ShortCode = Required(str,unique=True)
    Hashtag = Required(str)
    Proprietario = Required(str)
    LegendaPerfil = Required(str)
    LegendaPostagem = Required(str)
    QtdCurtidas = Required(int)
    QtdComentarios = Required(int)
    DataIso = Required(str)
    QtdImagens = Required(int)
    IsVideo = Required(bool)
    VideoVisualizacao = Required(int)
    VideoDuracao = Required(int)
    Localizacao = Required(str)
    TbComentarios = orm.Set('ComentariosInstagram')

class ComentariosInstagram(db.Entity):
    #ShortCode = Required(str)
    Proprietario = Required(str)
    Comentario = Required(str)
    QtdCurtidas = Required(int)
    DataIso = Required(str)
    Postagem = Required(PostagemInstagram,column='ShortCode')


class StartDataBase():
    def __init__(self,name_file):
        self.name_file = name_file
        self.generate_database()

    def generate_database(self):
        save_path = f'{os.getcwd()}/SQLite Data'

        if(not os.path.exists(save_path)):
            os.mkdir(save_path)
            print(f"!!! Criando a pasta {save_path} !!!")

        db.bind('sqlite', f'{save_path}/{self.name_file}.sqlite', create_db=True)
        db.generate_mapping(create_tables=True)
        print(f'!!! Gerando o banco {self.name_file} !!!')


    @orm.db_session
    def add_postagem(self,postagem):
        postagem = PostagemInstagram(**postagem)
        orm.commit()
        
    @orm.db_session
    def add_comentario(self,comentario):
        comentario['Postagem'] = PostagemInstagram.get(ShortCode=comentario['Postagem']).id
        comentario = ComentariosInstagram(**comentario)
        orm.commit()

    @orm.db_session
    def get_postagem(self):
        return orm.select(t for t in PostagemInstagram)[:].show()


    @orm.db_session
    def exist_postagem(self,shortcode):
        return PostagemInstagram.get(ShortCode=shortcode) is not None