# White API

White API is a Flask application that provides an API for fetching news articles and images based on search terms and filters.

## Installation

1. Clone this repository to your local machine:

```
git clone https://github.com/KunalG932/WhiteAPI
```

2. Navigate to the project directory:

```
cd WhiteAPI
```

3. Install the required dependencies:

```
pip install -r requirements.txt
```

## Usage

1. Run the Flask application:

```
python3 app.py
```

2. Open your web browser and go to [http://127.0.0.1:5000/](http://127.0.0.1:5000/) to access the landing page.

3. Use the following endpoints to fetch news articles and images:

- To fetch news articles:
  - Endpoint: `/news`
  - Parameters:
    - `q` (required): Search term
    - `filter` (optional): Data filter (e.g., today, this_week, this_year, or a specific number of days)
  - Example: `GET /news?q=technology&filter=today`

- To search for images:
  - Endpoint: `/images/<query>`
  - Example: `GET /images/cats`

## Contributors

- [KUnal Gaikwad](https://github.com/KunalG932)

## License

This project is licensed under the GPL-3.0 license - see the [GPL-3.0 license](https://github.com/KunalG932/WhiteAPI/blob/main/LICENSE) file for details.
