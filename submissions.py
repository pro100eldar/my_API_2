from operator import itemgetter

import requests
from plotly.graph_objs import Bar
from plotly import offline


url = 'https://hacker-news.firebaseio.com/v0/topstories.json'
r = requests.get(url)
print(f"Status code: {r.status_code}")

submission_ids = r.json()
submission_dicts = []

for submission_id in submission_ids[:15]:
    url = f'https://hacker-news.firebaseio.com/v0/item/{submission_id}.json'
    r = requests.get(url)
    response_dict = r.json()


    submission_dict = {
        'title': response_dict['title'],
        'hn_link': f"http://news.ycombinator.com/item?id={submission_id}",
        'comments': response_dict['descendants'],
        }
    submission_dicts.append(submission_dict)


submission_dicts = sorted(submission_dicts, key=itemgetter('comments'), reverse=True)

sub_links, comments = [], []
for submission_dict in submission_dicts:
    sub_title = submission_dict['title']
    sub_url = submission_dict['hn_link']
    sub_link = f"<a href='{sub_url}'>{sub_title}</a>"
    sub_links.append(sub_link)
    comments.append(submission_dict['comments'])


data = [{
    'type': 'bar',
    'x': sub_links,
    'y': comments,
    'marker': {
        'color': 'rgb(60, 100, 150)',
        'line': {'width': 1.5, 'color': 'rgb(25, 25, 25)'}
    },
    'opacity': 0.6,
}]

my_layout = {
    'title': f'Мost popular articles',
    'titlefont': {'size': 28},
    'xaxis': {
        'title': 'articles',
        'titlefont': {'size': 24},
        'tickfont': {'size': 14},
    },
    'yaxis': {
        'title': 'comments',
        'titlefont': {'size': 24},
        'tickfont': {'size': 14},
    },
}

fig = {'data': data, 'layout': my_layout}
offline.plot(fig, filename='submission.html')


