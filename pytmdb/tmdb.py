from typing import List, Iterator

import requests


class TMDBRequestError(Exception):
    def __init__(self, status_message: str, status_code: int, success: bool = None):
        self.status_message = status_message
        self.status_code = status_code
        self.success = success
        super().__init__(self.status_message)


class TVShowSearchResult:
    def __init__(self, data: dict):
        self.poster_path: str or None = data['poster_path']
        self.popularity: float = data['popularity']
        self.id: int = data['id']
        self.backdrop_path: str or None = data['backdrop_path']
        self.vote_average: float = data['vote_average']
        self.overview: str = data['overview']
        self.first_air_date: str = data['first_air_date']
        self.origin_country: List[str] = data['origin_country']
        self.genre_ids: List[int] = data['genre_ids']
        self.original_language: str = data['original_language']
        self.vote_count: int = data['vote_count']
        self.name: str = data['name']
        self.original_name: str = data['original_name']

    def __repr__(self) -> str:
        return F"<TVShowSearchResult id={self.id} name='{self.name}' original_name='{self.original_name}'>"


class MovieSearchResult:
    def __init__(self, data: dict):
        self.poster_path: str or None = data['poster_path']
        self.adult: bool = data['adult']
        self.overview: str = data['overview']
        self.release_date: str = data['release_date']
        self.genre_ids: List[int] = data['genre_ids']
        self.id: int = data['id']
        self.original_title: str = data['original_title']
        self.original_language: str = data['original_language']
        self.title: str = data['title']
        self.backdrop_path: str or None = data['backdrop_path']
        self.popularity: float = data['popularity']
        self.vote_count: int = data['vote_count']
        self.video: bool = data['video']
        self.vote_average: float = data['vote_average']

    def __repr__(self) -> str:
        return F"<MovieSearchResult id={self.id} title='{self.title}' original_title='{self.original_title}'>"


class TVShowSearchResults:
    def __init__(self, response: requests.Response):
        self._index = 0
        json_response = response.json()
        self.page: int = json_response['page']
        self.results: List[TVShowSearchResult] = [TVShowSearchResult(result) for result in json_response['results']]
        self.total_results: int = json_response['total_results']
        self.total_pages: int = json_response['total_pages']

    def __iter__(self) -> Iterator[TVShowSearchResult]:
        self._index = 0
        return self

    def __next__(self) -> TVShowSearchResult:
        if self._index < len(self.results):
            result: TVShowSearchResult = self.results[self._index]
            self._index += 1
            return result
        raise StopIteration

    def __len__(self) -> int:
        return len(self.results)

    def __getitem__(self, item) -> TVShowSearchResult:
        return self.results[item]

    def __repr__(self) -> str:
        return F"<TVShowSearchResults page={self.page} results_count={len(self.results)} " \
               F"total_results={self.total_results} total_pages={self.total_pages}>"


class TMDB:
    URL_ENDPOINT = 'https://api.themoviedb.org/3'

    def __init__(self, api_key: str):
        self.api_key = api_key

    def request(self, url: str, *, method: str = 'get', params: dict = None) -> requests.Response:
        if params is None:
            params = dict()
        if 'api_key' not in params:
            params['api_key'] = self.api_key
        return requests.request(method, url, params=params)

    def searchTVShow(self, query: str, *,
                     language: str = None,
                     page: int = None,
                     include_adult: bool = None,
                     first_air_date_year: int = None):
        params = {'query': query}
        if page is not None:
            params['page'] = page
        if language is not None:
            params['language'] = language
        if include_adult is not None:
            params['include_adult'] = include_adult
        if first_air_date_year is not None:
            params['first_air_date_year'] = first_air_date_year
        response = self.request(F'{TMDB.URL_ENDPOINT}/search/tv', params=params)
        if not response.ok:
            raise TMDBRequestError(**response.json())
        return TVShowSearchResults(response)

    def searchMovie(self, query: str, *,
                    language: str = None,
                    page: int = None,
                    include_adult: bool = None,
                    region: str = None,
                    year: int = None,
                    primary_release_year: int = None):
        params = {'query': query}
        if page is not None:
            params['page'] = page
        if language is not None:
            params['language'] = language
        if include_adult is not None:
            params['include_adult'] = include_adult
        if region is not None:
            params['region'] = region
        if year is not None:
            params['year'] = year
        if primary_release_year is not None:
            params['primary_release_year'] = primary_release_year
        response = self.request(F'{TMDB.URL_ENDPOINT}/search/tv', params=params)
        if not response.ok:
            raise TMDBRequestError(**response.json())
        return TVShowSearchResults(response)
