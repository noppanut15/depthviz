# depthviz: Transform your freediving footage with depth tracking

[![PyPI - Version](https://img.shields.io/pypi/v/depthviz?label=version&logo=pypi&logoColor=white)](https://pypi.org/project/depthviz/) [![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/noppanut15/depthviz/deploy.yaml?logo=github)](https://github.com/noppanut15/depthviz/actions) [![Coveralls](https://img.shields.io/coveralls/github/noppanut15/depthviz?logo=coveralls)](https://coveralls.io/github/noppanut15/depthviz) [![PyPI - Status](https://img.shields.io/pypi/status/depthviz?logo=pypi&logoColor=white)](https://pypi.org/project/depthviz/) [![PyPI Downloads](https://static.pepy.tech/badge/depthviz)](https://pepy.tech/projects/depthviz)

**depthviz** makes it easy to add dynamic depth tracking into your freediving footage. It is a command-line tool for generating depth overlay videos from the data recorded by your dive computer. It processes your dive log and creates a video that visualizes the depth over time.

![depthviz DEMO](https://raw.githubusercontent.com/noppanut15/depthviz/main/assets/demo-compressed-v2.gif)

This allows you to create more informative and engaging dive videos, enriching the storytelling experience for both yourself and your audience. [Click here to watch a sample video.](https://www.instagram.com/p/DAWI3jvy6Or/)

> [!TIP]
> For performance freedivers, you can incorporate `depthviz` into your dive analysis. By visualizing your dive profile, you can identify areas for improvement and track your progress over time.

# 🌟 Like depthviz?

Please give us a shiny [![star](https://img.shields.io/github/stars/noppanut15/depthviz
)](https://github.com/noppanut15/depthviz) and share `depthviz` with your freediving community! ⭐️

# 🛠️ Installation

**Prerequisites:**

* [Python](https://www.python.org/downloads/) (3.9 or higher) installed on your system.
* [pipx](https://pipx.pypa.io/stable/installation/) for installing Python CLI tools.

**Installation:**

```bash
pipx install depthviz
```

# 🚀 Usage

## 1. Download Your Data

- **✅ If you have a dive computer:**<br>Export your dive log from your dive computer or diving application. See the [source options table](#source-options) for supported formats.
- **🚫 If you don't have a dive computer:**<br>Record your dive profile manually using depth markers in your footage. See the [No Dive Computer?](#-no-dive-computer) section for more details.

## 2. Generate the Overlay

Use `depthviz` to generate a depth overlay video from your dive log.

```bash
depthviz -i <input_file> -s <source> -o <output_video.mp4>
```

**Required Arguments:**

* `-i`, `--input <input_file>`: Path to your dive log file.
* `-s`, `--source <source>`: Source of the data. See the table below for supported sources.
* `-o`, `--output <output_video.mp4>`: Path or filename for the generated video with the depth overlay. The output file format must be `.mp4`.

**Optional Arguments:**
* `-d`, `--decimal-places <0-2>`: Number of decimal places to display in the depth overlay. Valid values are `0`, `1`, or `2`. (Default: `0`)
* `--no-minus`: Hide the minus sign for depth values (e.g., display `10m` instead of `-10m`).
* `--font <font_file>`: Path to a custom font file for the text.
* `--bg-color <color>`: Background color (e.g., `green`, `'#000000'`). (Default: `black`)
  > 💡 You can use this option to set the background color to match your video editor's [chroma key](https://en.wikipedia.org/wiki/Chroma_key) color, if needed. (e.g., `--bg-color green`)
* `--stroke-width <0,1,2,...>`: Width of the stroke around the text in pixels. (Default: `2`)

<p align="center"><img src="https://raw.githubusercontent.com/noppanut15/depthviz/main/assets/depth-decimal-places-5s-trimmed.gif" alt="decimal places comparison"/></p>

> [!TIP]
> Use the `--decimal-places` option to control the precision of the depth display (e.g., `--decimal-places 1` displays depths like `-12.5m`)


### Source Options

|    Source    | Description                                                                                                                                     | File type | Status |
| :----------: | ----------------------------------------------------------------------------------------------------------------------------------------------- | :-------: | :----: |
| `apnealizer` | Data from [Apnealizer](https://apnealizer.com/) application.                                                                                    |    CSV    |   ✅    |
| `shearwater` | Data from [Shearwater](https://shearwater.com/pages/shearwater-cloud) dive computers.                                                           |    XML    |   ✅    |
|   `garmin`   | Data from [Garmin](https://github.com/noppanut15/depthviz/blob/main/docs/GARMIN.md) dive computers.                                             |    FIT    |   ✅    |
|   `suunto`   | Data from [Suunto](https://www.suunto.com/Support/faq-articles/suunto-app/what-type-of-files-can-i-export-from-the-suunto-app/) dive computers. |    FIT    |   ✅    |
|   `manual`   | Manual depth input. See the [No Dive Computer?](#-no-dive-computer) section for more details.                                                   |    CSV    |   ✅    |

**Example**:

Example of generating a depth overlay video named `depth_overlay.mp4` using data from `123456_ACTIVITY.fit` exported from [Garmin Connect](https://github.com/noppanut15/depthviz/blob/main/docs/GARMIN.md) (source: `garmin`).

```bash
depthviz -i 123456_ACTIVITY.fit -s garmin -o depth_overlay.mp4
```

## 3. Integrate with Your Footage

Import the generated overlay video into your preferred video editing software and combine it with your original dive footage. Adjust the blending and position of the overlay to suit your video style. 

> [Watch this short tutorial](https://www.youtube.com/watch?v=ZggKrWk98Ag) on how to import an overlay video in CapCut Desktop.

<br>

# 🚫 No Dive Computer?

**No Dive Computer, No Problem!** You can still create a depth overlay video by **manually inputting your dive log** using the `manual` source option.

**Example**:
```bash
depthviz -i <manual_input.csv> -s manual -o <output_video.mp4>
```

Freediving ropes with **depth markers** can help you record your dive profile manually. Use the depth markers in your footage as reference points to manually record your dive profile. Simply note the time and depth at each marker point to create your dive log.


|  ![Example of a Freediving Rope with Depth Markers](https://raw.githubusercontent.com/noppanut15/depthviz/main/assets/marked-rope-example.png)   |
| :----------------------------------------------------------------------------------------------------------------------------------------------: |
| *Example of a [Freediving Rope](https://2bfreeequipment.com/shop/2-b-free-freediving-rope-superstatic-marked-with-stopper/) with depth markers.* |

**Manual Mode Input File Format:**

The input file for manual mode should be a CSV file with the following columns:

* `Time`: The time in seconds (e.g., `0`, `1`, `2`, ...).
* `Depth`: The depth in meters (e.g., `10`, `9`, `8`, ...).

**You don't need to record the depth at every second.** Record the depth at each time point where a depth marker is visible in your footage. `depthviz` will interpolate the depth values between the recorded points to create a smooth depth profile. 

> [!TIP]
> To quickly generate a basic depth overlay, you can record just three points: **the start** (0m), **the maximum depth**, and **the end** (0m). `depthviz` will handle the rest! For more complex dives (e.g., dives with significant variations in descent/ascent rate or bottom time), more data points are recommended.

Here is an example of a manual mode input file:

| Time  | Depth |
| :---: | :---: |
|   0   |   0   |
|   6   |   5   |
|  12   |  10   |
|  19   |  15   |
|  26   |  10   |
|  33   |   5   |
|  39   |   0   |

Download the example input file [here](https://github.com/noppanut15/depthviz/blob/main/assets/manual-input-example.csv).

# 🧠 How It Works
`depthviz` works by parsing dive log data exported from various dive computers (or manually inputting dive data) and generating an overlay video that displays depth information.

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

<p align="center"><img src="https://raw.githubusercontent.com/noppanut15/depthviz/main/assets/linear-interpolation.png" width="750" alt="Linear Interpolation"/></p>

> [!NOTE]
> Learn more about the [Linear Interpolation](https://en.wikipedia.org/wiki/Linear_interpolation) method and how it is used to estimate values between two known depths.

4. **Generate Overlay Video**: The depth information from the linearly interpolated data is rendered into an overlay video, displaying the depth over time. This overlay can then be combined with your original dive footage in your video editor.


# 🌱 Contribution

We welcome contributions to the `depthviz` project! If you have any ideas for improvement, bug fixes, or feature suggestions, feel free to [open an issue](https://github.com/noppanut15/depthviz/issues) to discuss or [submit a pull request](https://github.com/noppanut15/depthviz/pulls).

## ⌚ Help Us Expand Dive Computer Support!

**Missing your dive computer?** Help us add support! If you have a dive computer that is not currently supported by `depthviz`, you can help us by donating a sample dive log file exported from your device. This will allow us to analyze the data format and implement the necessary parsing logic to add support for your device.

To share your dive data, please follow the detailed instructions in our "[**Donate My Dive**](https://github.com/noppanut15/depthviz/issues/15)" guide.

## ⚖️ License

This project is licensed under the Apache License 2.0. See the [LICENSE](https://github.com/noppanut15/depthviz/blob/main/LICENSE) file for details.

## 📦 CycloneDX SBOM

This project provides a CycloneDX Software Bill of Materials (SBOM) in JSON format. The SBOM is generated by the [GitHub Actions workflow](https://github.com/noppanut15/depthviz/blob/main/.github/workflows/deploy.yaml) and is available as an artifact for each release. The SBOM is generated using the [cyclonedx-python](https://github.com/CycloneDX/cyclonedx-python) library.

## 📬 Contact

For any inquiries, please [open an issue](https://github.com/noppanut15/depthviz/issues) or contact the maintainer at [noppanut.connect@gmail.com](mailto:noppanut.connect@gmail.com).
