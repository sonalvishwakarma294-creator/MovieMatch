# MovieMatch

MovieMatch is a content-based movie recommendation system that helps users discover movies similar to their favorites using NLP, cosine similarity, and movie metadata. The application combines movie descriptions, genres, cast, director, and ratings to generate personalized recommendations in an interactive Streamlit web app.

## Demo

A live version of the app can be launched locally with Streamlit, and the project is also prepared for deployment to services like Render or Heroku using the included Procfile and setup script.

## Features

- Personalized movie recommendations based on a selected movie
- Content-based filtering using textual metadata and similarity scoring
- Genre filtering and minimum rating controls
- Dynamic recommendation cards with posters and trailer links
- Interactive Streamlit UI for easy browsing
- Support for TMDb and OMDb poster retrieval
- Deployed app-ready configuration for hosting platforms

## Tech Stack

- Python
- Streamlit
- Pandas
- NumPy
- scikit-learn (used in the recommendation logic in the notebook pipeline)
- Requests
- Python-dotenv
- TMDb API / OMDb API

## Project Structure

```text
MovieMatch/
├── app.py                     # Streamlit web application
├── movie-recommender-system.ipynb  # Notebook used for building the recommendation model
├── movies.pkl                # Movie metadata dataset used by the app
├── similarity.pkl            # Cosine similarity matrix
├── movie_dict.pkl            # Additional movie dictionary data
├── movies_dict.pkl           # Alternative movie dictionary structure
├── requirements.txt          # Python dependencies
├── .env.example              # Sample environment file
├── Procfile                  # Deployment config for web servers
├── setup.sh                 # Streamlit setup script for deployment
├── README.md                # Project documentation
├── .gitignore               # Git ignore rules
└── .streamlit/              # Generated configuration (created at runtime)
```

## How It Works

The recommendation engine uses a content-based approach:

1. Movie metadata such as title, overview, genres, cast, and director are processed.
2. Textual features are transformed into a vector representation.
3. Cosine similarity is computed between movies.
4. When a user selects a movie, the app ranks the most similar titles and displays them as recommendations.

## Getting Started

### Prerequisites

- Python 3.9+
- pip
- A TMDb API key (optional for image fetching but recommended)
- An OMDb API key (optional fallback for posters)

### Clone the Repository

```bash
git clone https://github.com/sonalvishwakarma294-creator/MovieMatch.git
cd MovieMatch
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Configure Environment Variables

Create a `.env` file in the project root based on `.env.example`:

```env
TMDB_API_KEY=your_tmdb_api_key_here
OMDB_API_KEY=your_omdb_api_key_here
```

You can copy the sample file:

```bash
cp .env.example .env
```

### Run the App

```bash
streamlit run app.py
```

The app will open in your default browser, usually at:

```text
http://localhost:8501
```

## Deployment

This project includes deployment support for web hosting platforms:

- `Procfile` for app startup commands
- `setup.sh` to configure Streamlit server settings

Example deployment flow for a Python hosting service:

```bash
pip install -r requirements.txt
streamlit run app.py --server.port $PORT
```

## Usage

1. Select a movie from the dropdown.
2. Adjust the genre filter, number of recommendations, and minimum rating.
3. Click "Get Recommendations" to view similar movies.
4. Explore movie details, genre tags, and trailer links.

## Dataset Notes

The application relies on movie metadata and similarity data generated from a movie recommendation dataset. Poster images are fetched from TMDb and OMDb when available.

## License

This project is open for personal and educational use. If you plan to use it commercially, confirm the licensing terms for the data sources and APIs you integrate with.

## Acknowledgements

- TMDb API for movie metadata and poster images
- OMDb API for poster fallback support
- Streamlit for the interactive front-end
- The open-source data and recommendation community

## Author

Sonal Vishwakarma

## Contact

If you'd like to contribute, report an issue, or discuss improvements, feel free to open an issue or reach out through the repository.
