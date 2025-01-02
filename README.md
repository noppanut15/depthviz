## depthviz: Transform your dive footage with depth tracking

[![License](https://img.shields.io/github/license/noppanut15/depthviz)](LICENSE) [![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/noppanut15/depthviz/deploy.yaml)](https://github.com/noppanut15/depthviz/actions) [![Coveralls](https://img.shields.io/coverallsCoverage/github/noppanut15/depthviz)
](https://coveralls.io/github/noppanut15/depthviz) 



> [!NOTE]
> This project is in active development. Feel free to [open an issue](https://github.com/noppanut15/depthviz/issues) for any feedback or feature requests.

**depthviz** makes it easy to add dynamic depth tracking, giving your viewers a deeper understanding of your underwater sensation. It is a command-line tool for generating depth overlay videos from the data recorded by your dive computer. It processes your dive log and creates a video that visualizes the depth over time.

This allows you to create more informative and engaging dive videos, enriching the storytelling experience for both yourself and your audience.

### Installation

**Prerequisites:**

* Python 3.10 or later
* [pipx](https://pipx.pypa.io/stable/installation/) for installing Python CLI tools in isolated environments.

**Installation:**

```bash
pipx install depthviz
```

### Usage

**1. Download Your Data:**

* Ensure your dive computer data is exported in a CSV format with two columns:
    * `Time`: Represents the time elapsed since the dive start (e.g., in seconds).
    * `Depth`: Represents the current depth during the dive (e.g., in meters).

**2. Generate the Overlay:**

```bash
depthviz -i <input_file.csv> -s <sample_rate> -o <output_video.mp4>
```

**Arguments:**

* `-i`, `--input <input_file.csv>`: Path to your CSV file containing depth data. 
* `-o`, `--output <output_video.mp4>`: Path or filename for the generated video with the depth overlay.
* `-s`, `--sample-rate <sample_rate>`: Sample rate (in seconds) at which your dive computer recorded the data. (e.g., 0.25, 0.5, 1, etc.) 
> [!IMPORTANT]
> **Sample rate** is crucial for the accuracy of the depth visualization over time. Consult your dive computer manual for this information.

> [!TIP]
> If your dive computer recorded data every 1 second, **set the sample rate to 1**. (i.e., 1 sample per second) If your dive computer recorded data 4 samples per second, **set the sample rate to 0.25**. (i.e., 1 sample every 0.25 seconds)

**Example**:

Here's an example of using `depthviz` to generate a depth overlay video named `depth_tracking.mp4` with a sample rate of 0.5 seconds, using the data from `my_dive.csv`:

```bash
depthviz -i my_dive.csv -s 0.5 -o depth_tracking.mp4
```

**3. Integrate with Your Footage:**

Import the generated overlay video into your preferred video editing software and combine it with your original dive footage. Adjust the blending and position of the overlay to suit your video style. 
> [Watch this tutorial](https://www.youtube.com/watch?v=ZggKrWk98Ag) on how to import an overlay video in CapCut Desktop.


### Contribution

We welcome contributions to the `depthviz` project! If you have any ideas for improvement, bug fixes, or feature suggestions, feel free to [open an issue](https://github.com/noppanut15/depthviz/issues) to discuss or [submit a pull request](https://github.com/noppanut15/depthviz/pulls).


## License

This project is licensed under the Apache-2.0 License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements

- [MoviePy](https://github.com/Zulko/moviepy) for video processing
- [Open Sans](https://github.com/googlefonts/opensans) font

## Contact

For any inquiries, please [open an issue](https://github.com/noppanut15/depthviz/issues).

