#from authkey import user_insta
from modulos.InstaloaderDownloader import InstaloaderDownloader
import modulos.LocalDataBase as localdatabase
from datetime import datetime


#####################################################################################

UNTIL = datetime(2021,8,1) # Data de fim da coleta
SINCE = datetime(2021,7,1) # Data de inicio da coleta

HASHTAG = 'vegano' 

MAX_PUBLIC = 3000 #Numero máximo de publicacoes coletadas

############################## Dados importantes #####################################



def main():
    instaloader_downloader = InstaloaderDownloader()
    #post_iterator = get_iterator_hashtag(session=session,hashtag=HASHTAG)
    db = localdatabase.StartDataBase('posts_instagram')
    post_iterator = instaloader_downloader.get_iterator_hashtag(hashtag=HASHTAG)  
    itr = 0
    print("!!!...Programa iniciado...!!!")
    for post in post_iterator:
        if(itr < MAX_PUBLIC):
            if((post.date >= SINCE) and (post.date < UNTIL)):
                if(db.exist_postagem(post.shortcode)):
                    print(f"{post.shortcode} ja existe no banco")
                    continue

                print(f'Shortcode: {post.shortcode}')
                
                db.add_postagem({
                                'ShortCode' : post.shortcode,
                                'Hashtag': HASHTAG,
                                'Proprietario' : post.owner_username,
                                'LegendaPerfil' : 'sem_legenda' if post.pcaption is None else 'sem_legenda' if str(post.pcaption) == '' else str(post.pcaption),
                                'LegendaPostagem' : 'sem_legenda' if post.caption is None else 'sem_legenda' if str(post.caption) == '' else str(post.caption),
                                'QtdCurtidas' : post.likes,
                                'QtdComentarios' : post.comments,
                                'DataIso' : post.date.strftime("%Y-%m-%d"),
                                'QtdImagens' : post.mediacount,
                                'IsVideo' : post.is_video,
                                'VideoVisualizacao' : int(post.video_view_count) if post.is_video else 0,
                                'VideoDuracao' : int(post.video_duration) if post.is_video else 0,
                                'Localizacao' : 'sem_localizacao' if post.location is None else post.location.name
                            })
                if(post.comments > 0):
                    for comment in post.get_comments():
                        db.add_comentario({
                                        'Proprietario' : comment.owner.username,
                                        'Comentario' : str(comment.text),
                                        'QtdCurtidas' : comment.likes_count,
                                        'DataIso' : comment.created_at_utc.strftime("%Y-%m-%d"),
                                        'Postagem' : post.shortcode
                                    })
                print(f"Usuario [{itr+1}] coletado de [{MAX_PUBLIC}]")
                itr += 1
        else:
            break


main()
