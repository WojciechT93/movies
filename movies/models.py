from django.db import models
import datetime

class Movie(models.Model):
    Title = models.CharField(max_length=50)
    Year = models.IntegerField(default='')
    Rated = models.CharField(max_length=50, blank=True)
    Released = models.CharField(max_length=20, blank=True)
    Runtime = models.CharField(max_length=20, blank=True)
    Genre = models.CharField(max_length=100, blank=True)
    Director = models.CharField(max_length=100, blank=True)
    Writer = models.CharField(max_length=10000, blank=True)
    Actors = models.CharField(max_length=1000, blank=True)
    Plot = models.CharField(max_length=10000, blank=True)
    Language = models.CharField(max_length=1000, blank=True)
    Country = models.CharField(max_length=50, blank=True)
    Awards = models.CharField(max_length=1000, blank=True)
    Poster = models.CharField(max_length=1000, blank=True)
    Metascore = models.CharField(max_length=50, blank=True)
    ImdbRating = models.CharField(max_length=50, blank=True)
    ImdbVotes = models.CharField(max_length=100, blank=True)
    ImdbID = models.CharField(max_length=100, blank=True)
    Type = models.CharField(max_length=100, blank=True)
    DVD = models.CharField(max_length=100, blank=True)
    BoxOffice = models.CharField(max_length=100, blank=True)
    Production = models.CharField(max_length=200, blank=True)
    Website = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.Title


class Rating(models.Model):
    Movie = models.ForeignKey(Movie, related_name = 'Ratings', on_delete=models.CASCADE)
    Source = models.CharField(max_length=50)
    Value = models.CharField(max_length=50)
    
    class Meta:
        unique_together = ('Movie','Source')

    def __str__(self):
        return '%s: %s' % (self.Source, self.Value)
    
class Comment(models.Model):
    Movie_id = models.ForeignKey(Movie, related_name = 'Comments',on_delete=models.CASCADE)
    Comment = models.CharField(max_length=10000)
    Date = models.DateField(default=datetime.date.today)

    def __str__(self):
        return '%s:%s' % (self.Movie_id, self.Comment)

