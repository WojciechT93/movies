
def pickTopComments(comments):
    movieCommCount = []
    for com in comments:
        if com['Date'] >= From and com['Date'] <= To:
            if com['Movie_id'] in movieCommCount:
                movieCommCount[com['Movie_id']] += 1
            else:
                movieCommCount.insert()
    return topComments