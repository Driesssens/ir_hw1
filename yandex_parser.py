def parse_yandex_file(file_name):
    queries = []

    with open(file_name) as f:
        for line in f.read().splitlines():
            if 'Q' in line:
                session_id, query_id, ranking = parse_query(line)
                query = next((q for q in queries if q.session_id == session_id and q.id == query_id), None)

                if query is None:
                    queries.append(Query(session_id, query_id, ranking))
                else:
                    query.ranking += ranking

            else:
                session_id, url_id = parse_click(line)
                query = next(q for q in reversed(queries) if url_id in q.ranking and session_id == q.session_id)
                query.clicks.append(query.ranking.index(url_id))

    return queries


def parse_query(string):
    split = string.split()
    session_id = split[0]
    query_id = split[3]
    ranking = split[5:]
    return session_id, query_id, ranking


def parse_click(string):
    split = string.split()
    session_id = split[0]
    url_id = split[3]
    return session_id, url_id


class Query:
    def __init__(self, session_id, query_id, ranking):
        self.session_id = session_id
        self.id = query_id
        self.ranking = ranking
        self.clicks = []
