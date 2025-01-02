# depthviz

depthviz is a command-line tool for generating depth overlay videos from dive log CSV files. It processes depth data and creates a video that visualizes the depth over time.

## Features

- Parse CSV files containing depth data
- Generate depth overlay videos
- Customizable sample rate for dive data

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/depthviz.git
    cd depthviz
    ```

2. Install dependencies using Poetry:
    ```sh
    poetry install
    ```

## Usage

To generate a depth overlay video, run the following command:

```sh
poetry run python -m depthviz -i <input_csv> -s <sample_rate> -o <output_video>
```

- `<input_csv>`: Path to the CSV file containing depth data.
- `<sample_rate>`: Sample rate of your dive computer in seconds (e.g., 1, 0.50, 0.25).
- `<output_video>`: Path or filename of the output video file.

### Example

```sh
poetry run python -m depthviz -i data/dive_log.csv -s 1 -o output/depth_video.mp4
```

## Development

### Running Tests

To run the tests, use the following command:

```sh
poetry run pytest
```

### Code Style

This project uses `black` and `flake8` for code formatting and linting. To check the code style, run:

```sh
poetry run black .
poetry run flake8
```

## License

This project is licensed under the Apache-2.0 License. See the LICENSE file for details.

## Acknowledgements

- [MoviePy](https://zulko.github.io/moviepy/) for video processing
- [Open Sans](https://fonts.google.com/specimen/Open+Sans) font

## Contact

For any inquiries, please open an issue on GitHub.

