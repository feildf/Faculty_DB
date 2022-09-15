from scholarly import scholarly

def google_scholar(name):
    search_query = scholarly.search_author(name)
    try:
        first_author_result = next(search_query)
    except StopIteration:
        return -1
    author = scholarly.fill(first_author_result)
    data = []
    for paper in author['publications']:
        try:
            paper_info = {'title':paper['bib']['title'], 'year':paper['bib']['pub_year'], 'num_citations':paper['num_citations']}
        except:
            pass
        else:
            if paper_info['year'] == '2022':
                #search_query = scholarly.search_pubs(paper_info['title'])
                #first_pub_result = next(search_query)
                #pub = scholarly.fill(first_pub_result)
                paper_info['venue'] = ''
                data.append(paper_info)
    return data
