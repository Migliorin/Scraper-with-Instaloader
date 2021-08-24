from .authkey import user_insta
import instaloader


class InstaloaderDownloader():
    def __init__(self):
        self.init_session()

    def init_session(self):
        # Get instance
        L = instaloader.Instaloader()
        dados = user_insta() # Login e senha para acessar o perfil 
        L.login(**dados)

        self.session = L

    # Iterador inicial para as proximas requisicoes de publicacoes
    def get_iterator_hashtag(self,hashtag):

        post_iterator = instaloader.NodeIterator(
            self.session.context, "9b498c08113f1e09617a1703c22b2f32",
            lambda d: d['data']['hashtag']['edge_hashtag_to_media'],
            lambda n: instaloader.Post(self.session.context, n),
            {'tag_name': hashtag},
            f"https://www.instagram.com/explore/tags/{hashtag}/"
        )
        return post_iterator