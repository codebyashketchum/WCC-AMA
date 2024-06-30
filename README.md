# Wireless Cellular Communications RAG Application

This project implements an advanced Retrieval-Augmented Generation (RAG) application focused on wireless cellular communications. It serves as an interactive learning and reference tool, capable of answering questions, explaining topics, and visualizing concepts related to cellular communications.

For a detailed overview of the project architecture and design, please refer to the [Design Document](DESIGN.md).

## Setup

1. Ensure you have Python 3.11.5 and Pipenv installed.
2. Clone the repository:
   ```
   git clone https://github.com/yourusername/wireless_rag_app.git
   cd wireless_rag_app
   ```
3. Install dependencies:
   ```
   pipenv install
   ```
4. Activate the virtual environment:
   ```
   pipenv shell
   ```

## Running the Application

To run the application, use the following command:

```
streamlit run app.py
```

The application will start and can be accessed through your web browser.

## Development

- Use `pipenv install <package>` to add new dependencies.
- Run tests using `pytest`.
- Use `black` for code formatting and `isort` for import sorting.

## Project Structure

- `src/`: Contains the main application code
- `src/tests/`: Contains test files
- `data/`: Stores knowledge base documents
- `notebooks/`: Jupyter notebooks for experimentation and analysis
- `app.py`: Main Streamlit application file
- `DESIGN.md`: Detailed design document

## Contributing

Please read CONTRIBUTING.md for details on our code of conduct and the process for submitting pull requests.

## License

This project is licensed under the MIT License - see the LICENSE.md file for details.
