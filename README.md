## depthviz: Transform your dive footage with depth tracking

[![PyPI - Version](https://img.shields.io/pypi/v/depthviz)](https://pypi.org/project/depthviz/) [![License](https://img.shields.io/github/license/noppanut15/depthviz)](LICENSE) [![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/noppanut15/depthviz/deploy.yaml)](https://github.com/noppanut15/depthviz/actions) [![Coveralls](https://img.shields.io/coveralls/github/noppanut15/depthviz?logo=coveralls)](https://coveralls.io/github/noppanut15/depthviz) [![PyPI - Status](https://img.shields.io/pypi/status/depthviz)](https://pypi.org/project/depthviz/)




> [!NOTE]
> This project is in active development. Feel free to [open an issue](https://github.com/noppanut15/depthviz/issues) for any feedback or feature requests.

**depthviz** makes it easy to add dynamic depth tracking, giving your viewers a deeper understanding of your underwater sensation. It is a command-line tool for generating depth overlay videos from the data recorded by your dive computer. It processes your dive log and creates a video that visualizes the depth over time.

![depthviz DEMO](https://raw.githubusercontent.com/noppanut15/depthviz/main/assets/demo-compressed.gif)

This allows you to create more informative and engaging dive videos, enriching the storytelling experience for both yourself and your audience. [Click here to watch a sample video.](https://www.instagram.com/p/DAWI3jvy6Or/)

## Installation

**Prerequisites:**

* [Python](https://www.python.org/downloads/) (3.9 or higher) installed on your system.
* [pipx](https://pipx.pypa.io/stable/installation/) for installing Python CLI tools.

**Installation:**

```bash
pipx install depthviz
```

## Usage

**1. Download Your Data:**

Export your dive log data from [Apnealizer](https://apnealizer.com/) in CSV format. 
> [!NOTE]
> We are currently working on adding support for direct logs from dive computers, so we don't just rely on Apnealizer. Stay tuned for updates!

**2. Generate the Overlay:**

```bash
depthviz -i <input_file.csv> -s <source> -o <output_video.mp4>
```

**Arguments:**

* `-i`, `--input <input_file.csv>`: Path to your file containing your dive log.
* `-s`, `--source <source>`: Source of the dive computer data. Currently, only `apnealizer` is supported.
* `-o`, `--output <output_video.mp4>`: Path or filename for the generated video with the depth overlay.

**Source Options:**

| Source       | Description                                                                                    | File type | Development Status                                                                                                 |
| ------------ | ---------------------------------------------------------------------------------------------- | --------- | ------------------------------------------------------------------------------------------------------------------ |
| `apnealizer` | Data exported from [Apnealizer](https://apnealizer.com/), logging and analyzing application.   | CSV       | :white_check_mark: Supported                                                                                       |
| `shearwater` | Data exported from [Shearwater](https://shearwater.com/pages/shearwater-cloud) dive computers. | XML       | :construction: Under development, not supported yet                                                                |
| `garmin`     | Data exported from [Garmin](https://connect.garmin.com/) dive computers.                       | -         | :x: Not supported yet, [**sample data needed**](https://github.com/noppanut15/depthviz/issues/15) :rotating_light: |
| `manual`     | Manually input the dive data, for those who don't have a dive computer.                        | -         | :x: Not supported yet                                                                                              |

**Example**:

Here's an example of using `depthviz` to generate a depth overlay video named `depth_tracking.mp4`, using the data from `my_dive.csv` exported from Apnealizer:

```bash
depthviz -i my_dive.csv -s apnealizer -o depth_tracking.mp4
```

**3. Integrate with Your Footage:**

Import the generated overlay video into your preferred video editing software and combine it with your original dive footage. Adjust the blending and position of the overlay to suit your video style. 
> [Watch this tutorial](https://www.youtube.com/watch?v=ZggKrWk98Ag) on how to import an overlay video in CapCut Desktop.


## Contribution

We welcome contributions to the `depthviz` project! If you have any ideas for improvement, bug fixes, or feature suggestions, feel free to [open an issue](https://github.com/noppanut15/depthviz/issues) to discuss or [submit a pull request](https://github.com/noppanut15/depthviz/pulls).

## Help Us Expand Dive Computer Support!

**Missing your dive computer?** Help us add support! [Submit a Dive Computer Support Request](https://github.com/noppanut15/depthviz/issues) issue with your dive log file and export source.

By providing this information, you'll be helping us understand the specific format of your dive computer's exported data. This allows us to implement the necessary parsing logic and add support for your device in a future release.


## License

This project is licensed under the Apache-2.0 License. See the [LICENSE](LICENSE) file for details.


## Contact

For any inquiries, please [open an issue](https://github.com/noppanut15/depthviz/issues). We'd love to hear from you!

