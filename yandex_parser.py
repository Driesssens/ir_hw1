def parse_yandex_file(file_name):
    """"Parses the Yandex log file.

    Makes the following assumptions:
    - Within a session, a click on a url_id was on the most recent query that returned that url_id.
    - Within a session, if a query_id appears a second time with different results, this is
        interpreted as page 2, and the results get appended to the query
    - Within a session, if a query_id appears a second time with overlapping results,
        this is interpreted as a new query
    """
    queries = []

    with open(file_name) as f:
        for line in f.read().splitlines():
            if 'Q' in line:
                parsed_session_id, parsed_query_id, parsed_ranking = parse_query(line)
                query = next(
                    (
                        q for q in reversed(queries) if
                        (
                            q.session_id == parsed_session_id
                            and q.id == parsed_query_id
                            and not any(url_id in q.ranking for url_id in parsed_ranking)
                        )
                    ), None)

                if query is None:
                    queries.append(Query(parsed_session_id, parsed_query_id, parsed_ranking))
                else:
                    query.ranking += parsed_ranking

            else:
                parsed_session_id, parsed_url_id = parse_click(line)
                query = next((q for q in reversed(queries) if parsed_url_id in q.ranking and parsed_session_id == q.session_id), None)
                query.clicks.append(query.ranking.index(parsed_url_id) + 1)

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

    def __repr__(self):
        return "Query[{0}:{1:4} ranking={2} clicks={3}]".format(self.session_id, self.id, self.ranking, self.clicks)
