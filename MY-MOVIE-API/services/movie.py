from models.movie import Movie as MovieModel
from schema.movie import Movie

class MovieService:

    def __init__(self, db) -> None:
        self.db = db
    
    def get_movies(self):
        result = self.db.query(MovieModel).all()
        return result
    
    def get_movie(self, id):
        result = self.db.query(MovieModel).filter(MovieModel.id == id).first()
        return result
    
    def get_movie_category(self, category):
        result = self.db.query(MovieModel).filter(MovieModel.category == category).all()
        return result
    
    def create_movie(self, movie: Movie):
        new_movie = MovieModel(**movie.dict())
        self.db.add(new_movie)
        self.db.commit()
        self.db.refresh(new_movie)  # Refresca la instancia para obtener el ID
        return new_movie  # Retorna la instancia creada
    
    def update_movie(self, id: int, movie: Movie):
        existing_movie = self.db.query(MovieModel).filter(MovieModel.id == id).first()
        if not existing_movie:
            return None
        
        existing_movie.title = movie.title
        existing_movie.overview = movie.overview
        existing_movie.year = movie.year
        existing_movie.rating = movie.rating
        existing_movie.category = movie.category

        self.db.commit()
        self.db.refresh(existing_movie)
        
        return existing_movie
    
    def delete_movie(self, id: int):
        existing_movie = self.db.query(MovieModel).filter(MovieModel.id == id).first()
        if not existing_movie:
            return None
        
        self.db.delete(existing_movie)
        self.db.commit()
        
        return existing_movie
