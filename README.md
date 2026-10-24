# 🎬 MovieMatch

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.9%2B-3776AB?style=for-the-badge&logo=python" alt="Python 3.9+" />
  <img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit" alt="Streamlit" />
  <img src="https://img.shields.io/badge/Scikit--Learn-F7931E?style=for-the-badge&logo=scikitlearn" alt="Scikit-Learn" />
  <img src="https://img.shields.io/badge/TMDb-01B4E4?style=for-the-badge&logo=themoviedatabase" alt="TMDb" />
  <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" alt="MIT License" />
</p>

<p align="center">
  <strong>Smart, personalized movie recommendations powered by content-based filtering and similarity matching.</strong>
</p>

A polished movie recommendation app that suggests titles similar to the one you select, using metadata like genres, overview, cast, and director. Built with Python, Streamlit, and scikit-learn for a smooth interactive experience.

## ✨ Highlights

- Personalized movie suggestions based on the selected movie
- Content-based recommendation engine using movie metadata and similarity scores
- Genre and rating filters for better discovery
- Poster fetching with TMDb and OMDb fallback
- Modern Streamlit UI with a cinematic dashboard design
- Ready for local use and deployment on cloud hosting platforms

## 🎥 Demo

<p align="center">
  <img src="https://raw.githubusercontent.com/sonalvishwakarma294-creator/MovieMatch/main/assets/demo-preview.png" alt="MovieMatch preview" width="900" />
</p>

> Screenshot preview can be replaced with a local asset in `assets/demo-preview.png` for a more branded experience.

## 🧠 How It Works

The recommendation engine follows a content-based approach:

1. It loads movie metadata such as title, overview, genres, cast, and director.
2. Textual features are transformed into a vector representation.
3. Cosine similarity is computed across the movie catalog.
4. When a user chooses a movie, the system ranks the most similar titles and returns recommendations.

## 🛠️ Tech Stack

- Python
- Streamlit
- Pandas
- NumPy
- scikit-learn
- Requests
- python-dotenv
- TMDb API
- OMDb API

## 📁 Project Structure

```text
MovieMatch/
├── app.py                          # Streamlit web application
├── movie-recommender-system.ipynb  # Notebook for model and recommendation pipeline
├── movies.pkl                     # Movie metadata dataset
├── similarity.pkl                 # Cosine similarity matrix
├── movie_dict.pkl                 # Additional movie metadata dictionary
├── movies_dict.pkl                # Alternative movie dictionary structure
├── requirements.txt               # Python dependencies
├── .env.example                   # Sample environment variables
├── Procfile                       # Deployment config
├── setup.sh                      # Deployment setup script
├── README.md                     # Project documentation
├── .gitignore                    # Git ignore rules
├── assets/                       # Optional screenshots and project assets
└── .streamlit/                   # Streamlit configuration
```

## 🚀 Getting Started

### Prerequisites

- Python 3.9+
- pip
- TMDb API key (recommended for poster fetching)
- OMDb API key (optional fallback)

### Clone the repository

```bash
git clone https://github.com/sonalvishwakarma294-creator/MovieMatch.git
cd MovieMatch
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Configure environment variables

Create a `.env` file in the project root using the sample file:

```bash
cp .env.example .env
```

Example:

```env
TMDB_API_KEY=your_tmdb_api_key_here
OMDB_API_KEY=your_omdb_api_key_here
```

### Run the app

```bash
streamlit run app.py
```

Open the app in your browser at:

```text
http://localhost:8501
```

## 🎯 Features

- Smart recommendation engine based on movie similarity
- Similarity scoring and match percentage visualization
- Genre filtering to narrow recommendations
- Minimum rating filters
- Movie detail cards with cast, director, and genres
- Trailer search links for discovered movies
- Clean, user-friendly layout for browsing recommendations

## 🌐 Deployment

This project is prepared for deployment on hosting services like Render or Heroku.

Included deployment files:

- `Procfile`
- `setup.sh`

Example startup command:

```bash
streamlit run app.py --server.port $PORT
```

## 📊 Project Status

- Recommendation engine: Active
- UI: Interactive and polished
- Deployment support: Included
- Data integration: TMDb/OMDb metadata support

## 🤝 Contributing

Contributions are welcome. If you want to improve the app, add new recommendation logic, or improve the UI:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Open a pull request

## 📜 License

This project is open for personal and educational use. Please review the licensing requirements for external data sources and APIs before commercial use.

## 🙌 Acknowledgements

- TMDb API for movie metadata and artwork
- OMDb API for poster fallback
- Streamlit for interactive app development
- scikit-learn for similarity computation

## 👤 Author

Sonal Vishwakarma

---

<p align="center">
  <a href="https://github.com/sonalvishwakarma294-creator/MovieMatch">
    <img src="https://img.shields.io/badge/View%20on%20GitHub-181717?style=for-the-badge&logo=github" alt="View on GitHub" />
  </a>
</p>
