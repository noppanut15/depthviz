## depthviz: Transform your freediving footage with depth tracking

[![PyPI - Version](https://img.shields.io/pypi/v/depthviz)](https://pypi.org/project/depthviz/) [![License](https://img.shields.io/github/license/noppanut15/depthviz)](LICENSE) [![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/noppanut15/depthviz/deploy.yaml)](https://github.com/noppanut15/depthviz/actions) [![Coveralls](https://img.shields.io/coveralls/github/noppanut15/depthviz?logo=coveralls)](https://coveralls.io/github/noppanut15/depthviz) [![PyPI - Status](https://img.shields.io/pypi/status/depthviz)](https://pypi.org/project/depthviz/)




> [!NOTE]
> This project is in active development. Feel free to [open an issue](https://github.com/noppanut15/depthviz/issues) for any feedback or feature requests.

**depthviz** makes it easy to add dynamic depth tracking, giving your viewers a deeper understanding of your underwater sensation. It is a command-line tool for generating depth overlay videos from the data recorded by your dive computer. It processes your dive log and creates a video that visualizes the depth over time.

![depthviz DEMO](https://raw.githubusercontent.com/noppanut15/depthviz/main/assets/demo-compressed-v2.gif)

This allows you to create more informative and engaging dive videos, enriching the storytelling experience for both yourself and your audience. [Click here to watch a sample video.](https://www.instagram.com/p/DAWI3jvy6Or/)

> [!TIP]
> For performance freedivers, you can incorporate `depthviz` into your dive analysis. By visualizing your dive profile, you can identify areas for improvement and track your progress over time.


<!-- ## Support depthviz!

Please give us a shiny ![star](https://img.shields.io/github/stars/noppanut15/depthviz
) and share `depthviz` with your freediving community! -->

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

Export your dive log data from your dive computer or diving application. See the source options below for supported formats.

**2. Generate the Overlay:**

In this step, you will use the `depthviz` to generate a video overlay that displays the depth information from your dive log.

```bash
depthviz -i <input_file> -s <source> -o <output_video.mp4>
```

**Required Arguments:**

* `-i`, `--input <input_file>`: Path to your file containing your dive log.
* `-s`, `--source <source>`: Source of the dive computer data. See the table below for supported sources.
* `-o`, `--output <output_video.mp4>`: Path or filename for the generated video with the depth overlay. The output file format must be `.mp4`.

**Optional Arguments:**
* `-d`, `--decimal-places <0-2>`: Number of decimal places to display in the depth overlay. Valid values are `0`, `1`, or `2`. (Default is `0`)

<p align="center"><img src="https://raw.githubusercontent.com/noppanut15/depthviz/docs/fix-gif/assets/depth-decimal-places-5s-trimmed.gif" alt="decimal places comparison"/></p>

> [!TIP]
> The decimal places option allows you to customize the level of detail in the depth overlay. For example, setting `--decimal-places 1` will display the depth with one decimal place (e.g., `-12.5m`).


**Source Options:**

| Source       | Description                                                                                                                            | File type | Development Status                                                                                                 |
| ------------ | -------------------------------------------------------------------------------------------------------------------------------------- | --------- | ------------------------------------------------------------------------------------------------------------------ |
| `apnealizer` | Data exported from [Apnealizer](https://apnealizer.com/), logging and analyzing application.                                           | CSV       | :white_check_mark: Supported                                                                                       |
| `shearwater` | Data exported from [Shearwater](https://shearwater.com/pages/shearwater-cloud) dive computers.                                         | XML       | :white_check_mark: Supported                                                                                       |
| `garmin`     | Data exported from [Garmin](https://connect.garmin.com/) dive computers.                                                               | -         | :x: [**Sample data needed**](https://github.com/noppanut15/depthviz/issues/15) :rotating_light: |
| `suunto`     | Data exported from [Suunto](https://www.suunto.com/Support/faq-articles/dm5/how-do-i-import--export-dive-logs-to-dm5/) dive computers. | -         | :x: [**Sample data needed**](https://github.com/noppanut15/depthviz/issues/15) :rotating_light: |
| `manual`     | Manually input the dive data, for those who don't have a dive computer.                                                                | -         | :construction: Under development                                                                |

**Example**:

Example of generating a depth overlay video named `depth_overlay.mp4` using data from `my_dive.xml` exported from Shearwater dive computers (source: `shearwater`).

```bash
depthviz -i my_dive.xml -s shearwater -o depth_overlay.mp4
```

**3. Integrate with Your Footage:**

Import the generated overlay video into your preferred video editing software and combine it with your original dive footage. Adjust the blending and position of the overlay to suit your video style. 
> [Watch this tutorial](https://www.youtube.com/watch?v=ZggKrWk98Ag) on how to import an overlay video in CapCut Desktop.

## How It Works
`depthviz` works by parsing dive log data exported from various dive computers and generating an overlay video that displays depth information.

Dive computers typically record either depth directly or pressure data. If the data is recorded as pressure, it is in the form of **absolute pressure**, which includes both atmospheric pressure and the pressure exerted by the water itself (hydrostatic pressure).


To determine the depth, `depthviz` uses the following approach:
1.  **If the dive log contains depth data directly:** `depthviz` uses this data directly.
2.  **If the dive log contains pressure data:**
    * First, the **hydrostatic pressure** is calculated by subtracting atmospheric pressure (collected during the surface interval or dive start) from the absolute pressure:<br><br><p align="center"><picture><source media="(prefers-color-scheme: dark)" srcset="https://latex.codecogs.com/svg.image?\large&space;{\color{White}\text{Hydrostatic&space;Pressure}=\text{Absolute&space;Pressure}-\text{Atmospheric&space;Pressure}}"><img src="https://latex.codecogs.com/svg.image?\large&space;\text{Hydrostatic&space;Pressure}=\text{Absolute&space;Pressure}-\text{Atmospheric&space;Pressure}" title="\text{Hydrostatic Pressure}=\text{Absolute Pressure}-\text{Atmospheric Pressure}" /></picture></p><br>
    * Then, the **fluid pressure formula** is used to calculate the depth:<br><br><p align="center"><picture><source media="(prefers-color-scheme: dark)" srcset="https://latex.codecogs.com/svg.image?\LARGE&space;{\color{White}P=\rho&space;g&space;h}"><img src="https://latex.codecogs.com/svg.image?\LARGE&space;&space;P=\rho&space;g&space;h" title=" P=\rho g h" /></picture></p> 
       Where:
         - $` P `$ is the fluid pressure,
         - $` \rho `$ is the density of the fluid (water),
         - $` g `$ is the acceleration due to gravity (9.80665 m/s²),
         - $` h `$ is the height (or depth) of the fluid column (what we want to calculate).
    * Rearranging the formula to solve for depth ($` h `$):<br><br><p align="center"><picture><source media="(prefers-color-scheme: dark)" srcset="https://latex.codecogs.com/svg.image?\LARGE&space;{\color{White}h=\frac{P}{\rho&space;g}}"><img src="https://latex.codecogs.com/svg.image?\LARGE&space;$$h=\frac{P}{\rho&space;g}$$" title="$$h=\frac{P}{\rho g}$$" /></picture></p><br>

Currently, `depthviz` uses a water density ($` \rho `$) according to the **EN13319 standard**, a European CE standard for dive computers, which assumes a water density of 1019.7 kg/m³.

The water density can vary depending on the type of water (e.g., freshwater, saltwater). Even different locations in the ocean can have varying densities. This variability can affect the accuracy of depth calculations. For more precise measurements, users may need to adjust the density value based on their specific diving environment. Especially for freshwater diving, the water density is lower than the standard value, which can lead to depth overestimation. We will add support for custom water density in future releases.
    
> [!NOTE]
> The EN13319 standard ensures the accuracy and reliability of depth measurements in dive computers. For more information, you can refer to the [EN13319 standard](https://standards.iteh.ai/catalog/standards/cen/5d35e933-ca50-4d80-8c9d-631f5597b784/en-13319-2000).

3. **Fill in the Gaps**: Different dive computers have different sampling rates, and the data may not be recorded at regular intervals. If the dive log data contains gaps or missing values, `depthviz` uses **Linear Interpolation** to estimate the depth at those points. This method calculates the depth at each time point by interpolating between the two nearest known depth values recorded by the dive computer. This will help ensure a smooth and continuous depth profile in the overlay video.

<p align="center"><img src="https://raw.githubusercontent.com/noppanut15/depthviz/main/assets/linear-interpolation.png" alt="Linear Interpolation"/></p>

> [!NOTE]
> Learn more about the [Linear Interpolation](https://en.wikipedia.org/wiki/Linear_interpolation) method and how it is used to estimate values between two known depths.

4. **Generate Overlay Video**: The depth information from the linearly interpolated data is rendered into an overlay video, displaying the depth over time. This overlay video can then be integrated with your original dive footage.


## Contribution

We welcome contributions to the `depthviz` project! If you have any ideas for improvement, bug fixes, or feature suggestions, feel free to [open an issue](https://github.com/noppanut15/depthviz/issues) to discuss or [submit a pull request](https://github.com/noppanut15/depthviz/pulls).

## Help Us Expand Dive Computer Support!

**Missing your dive computer?** Help us add support! [Submit a Dive Computer Support Request](https://github.com/noppanut15/depthviz/issues) issue with your dive log file and export source.

By providing this information, you'll be helping us understand the specific format of your dive computer's exported data. This allows us to implement the necessary parsing logic and add support for your device in a future release.


## License

This project is licensed under the Apache License 2.0. See the [LICENSE](LICENSE) file for details.

## CycloneDX SBOM

This project provides a CycloneDX Software Bill of Materials (SBOM) in JSON format. The SBOM is generated by the [GitHub Actions workflow](.github/workflows/deploy.yaml) and is available as an artifact for each release. The SBOM is generated using the [cyclonedx-python](https://github.com/CycloneDX/cyclonedx-python) library.


## Contact

For any inquiries, please [open an issue](https://github.com/noppanut15/depthviz/issues). We'd love to hear from you!

