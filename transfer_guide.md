# Transfer Guide: Smart Agriculture Platform

This guide will help you transfer the Smart Agriculture Platform project to your local VS Code environment.

## Project Structure

Make sure to maintain this folder structure:

```
smart-agriculture/
├── .streamlit/
│   └── config.toml
├── assets/
│   └── app_data.py
├── components/
│   ├── crop_recommendations.py
│   ├── information_display.py
│   ├── season_selector.py
│   ├── soil_selector.py
│   └── three_js_viewer.py
├── data/
│   ├── crop_data.py
│   ├── season_data.py
│   └── soil_data.py
└── app.py
```

## Required Dependencies

Install these Python packages in your local environment:

```bash
pip install streamlit==1.31.0
pip install streamlit-card==0.0.61
pip install streamlit-lottie==0.0.5
pip install streamlit-option-menu==0.3.6
pip install streamlit-extras==0.3.5
pip install plotly==5.18.0
pip install pandas==2.1.4
pip install requests==2.31.0
pip install numpy==1.26.3
```

Alternatively, you can copy all the package versions from the `pyproject.toml` file in this project.

## Configuration

1. Make sure the `.streamlit/config.toml` file exists with the following content:

```toml
[server]
headless = true
address = "0.0.0.0"
port = 5000

[theme]
base = "dark"
primaryColor = "#1DB954"
backgroundColor = "#121212"
secondaryBackgroundColor = "#212121"
textColor = "#FFFFFF"
```

## Running the Application

To run the application in VS Code:

1. Open the project folder in VS Code
2. Open a terminal in VS Code (Terminal > New Terminal)
3. Run the Streamlit application:

```bash
streamlit run app.py
```

The application should be accessible at `http://localhost:5000` by default.

## Development Notes

- The main application logic is in `app.py`
- UI components are modularized in the `/components` directory
- Data and models are in the `/data` directory
- Text content is stored in `/assets/app_data.py`

## Troubleshooting

If you encounter any issues:

1. Make sure all dependencies are installed correctly
2. Check that your folder structure matches the one provided
3. Ensure the `.streamlit/config.toml` file is in the correct location
4. If visualizations don't render, check for any browser console errors 
5. For Lottie animations, verify your internet connection as they're loaded from URLs