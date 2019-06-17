from rest_framework import serializers
from .models import Rating, Movie, Comment

class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ('Source', 'Value')

class MovieSerializer(serializers.ModelSerializer):
    Ratings = RatingSerializer(many=True, read_only=True)
    
    class Meta:
        model = Movie
        fields = '__all__'
        # fields = ('Title', 'Year', 'Rated', 'Released', 'Runtime', 'Genre', 
        #         'Director', 'Writer', 'Actors', 'Plot', 'Language', 'Country', 
        #         'Awards', 'Poster', 'Ratings', 'Metascore', 'ImdbRating', 'ImdbVotes', 
        #         'ImdbID', 'Type', 'DVD', 'BoxOffice', 'Production', 'Website')

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('Comment', 'Movie_id', 'Date')

class TopSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    place = serializers.CharField()
    total_comments = serializers.CharField()
