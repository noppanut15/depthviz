<div align="center">
  <a href="#">
  <img src="https://raw.githubusercontent.com/noppanut15/depthviz/main/assets/logo/depthviz-temp-logo.png" width="300" alt="depthviz logo"/>
  </a>
  <a name="readme-top"></a>

*A CLI tool that creates heads-up displays <br>for your **freediving videos**, <br>automatically tracking **depth** and **time** <br>from your **dive computer logs** or **manual input**.*

[![PyPI - Version][version_badge_img]][version_badge_url] [![GitHub Actions Workflow Status][build_badge_img]][build_badge_url] [![Coveralls][coverage_badge_img]][coverage_badge_url] [![PyPI - Status][pypi_status_img]][pypi_status_url] [![PyPI Downloads][download_badge_img]][download_badge_url]

**&searr;&nbsp;&nbsp;Quick Links&nbsp;&nbsp;&swarr;**

[Features](#-features) • [Installation](#️-installation) • [Usage](#-usage) • [No Dive Computer?](#-no-dive-computer) • [How It Works](#-how-it-works) • [Contribution](#-contribution) • [License](#️-license) • [Contact](#-contact)

**&searr;&nbsp;&nbsp;Share the project's link to your friends&nbsp;&nbsp;&swarr;**

[![Share on X][x_share_img]][x_share_url] [![Share on Facebook][facebook_share_img]][facebook_share_url] [![Share on Telegram][telegram_share_img]][telegram_share_url] [![Share on WhatsApp][whatsapp_share_img]][whatsapp_share_url] [![Share on Reddit][reddit_share_img]][reddit_share_url]
</div>

![depthviz DEMO](https://raw.githubusercontent.com/noppanut15/depthviz/main/assets/demo-compressed-v2.gif)

---
## ✨ Features

<img src="https://raw.githubusercontent.com/noppanut15/depthviz/main/assets/final-video-showcase-400x400.gif" alt="showcase video" align="right" width="385px" />
 
Why use *depthviz*?

- **Free & Open-Source** – Made for all freedivers, whether or not you have a dive computer.
- **Cross-Platform** – Works on **Windows**, **macOS**, and **Linux**.
- **Multi-Source Dive Log Support:** Works with dive logs from **Apnealizer, Shearwater, Garmin, Suunto**, or even your own **manual input**.
- **Customizable Display** – Control decimal places, fonts, colors, stroke width, etc.
- **Easy Video Integration** – Use your favorite editor (CapCut, etc.) with generated overlays.
- **Smooth Depth Display** – Automatically fills in missing data for a seamless and natural depth display. Includes *zero-based* depth mode to smoothly estimates a 0m start if your dive log starts underwater.

> [!TIP]
> Perfect for performance freedivers tracking PBs or analyzing technique. Overlay your data and see every moment of your dive!

<div align="right">

[&nwarr; Back to top](#readme-top)

</div>

---

## 🌟 Like depthviz?

If you like `depthviz` and find it useful, please give it a shiny [![star](https://img.shields.io/github/stars/noppanut15/depthviz
)](https://github.com/noppanut15/depthviz) ✨

Want **early access** to new open-source projects, exclusive insights, and sneak peeks into upcoming `depthviz` features? 🚀

[![Follow me](https://img.shields.io/badge/follow%20me%20on%20github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white)](https://github.com/noppanut15/) 


I’d also love to see your diving stories or videos made with `depthviz`! Share your creations by tagging me [@noppanut15](https://www.instagram.com/noppanut15/) or using the hashtag **#depthviz**. 

See you in the deep! 🌊

<div align="right">

[&nwarr; Back to top](#readme-top)

</div>

## 🛠️ Installation
### Prerequisites
- **Python 3.9 or higher**  
  [Download Python](https://www.python.org/downloads/) • [How to install Python](https://realpython.com/installing-python/)
- **pipx** – the recommended tool for installing Python CLI tools  
  [How to install pipx](https://pipx.pypa.io/stable/installation/)

### Install depthviz

Open your terminal and run:
```bash
pipx install depthviz
```

### Upgrade

When a new version is available, update with:

```bash
pipx upgrade depthviz
```

Check your installed version with:
```bash
depthviz --version
```

<div align="right">

[&nwarr; Back to top](#readme-top)

</div>

## 🚀 Usage

`depthviz` turns your dive logs into overlay videos that show your depth and elapsed time. Follow these 3 simple steps: 🏊‍♂️🎥

### Step 1: Prepare Your Dive Data

- **✅ With a Dive Computer:**<br>Export your dive log from your dive computer or diving application. (see [Supported Dive Log Formats](#-supported-dive-log-formats) below).
- **🚫 No Dive Computer?**<br>You can record your dive manually (details in [No Dive Computer?](#-no-dive-computer)).


### Step 2: Generate the Overlay 🎬

Run this command to create your depth overlay video from your dive log:

```bash
depthviz -i YOUR_DIVE_LOG -s DATA_SOURCE -o OUTPUT_VIDEO.mp4
```
**Example (Garmin dive log):**
```bash
depthviz -i 123456_ACTIVITY.fit -s garmin -o my_dive_overlay.mp4
```
| &nbsp;&nbsp;&nbsp;&nbsp;Option&nbsp;&nbsp;&nbsp;&nbsp; | Short | Values                                                               | Description                                                                                           |
| ------------------------------------------------------ | :---: | -------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------- |
| `--input`                                              | `-i`  | File path                                                            | Path or filename to your dive log file.                                                               |
| `--source`                                             | `-s`  | `apnealizer`,<br>`shearwater`,<br>`garmin`,<br>`suunto`,<br>`manual` | The data source.<br>(See the [Supported Dive Log Formats](#-supported-dive-log-formats) for details.) |
| `--output`                                             | `-o`  | File path                                                            | Path or filename for the output video. (must end with `.mp4`)                                         |

#### 📂 Supported Dive Log Formats

|    Source    | Description                                                                                                                                                                                                                                                   | File type |
| :----------: | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :-------: |
| `apnealizer` | Exported logs from the **Apnealizer** app. <br> [![Get log][get_log_img]](https://apnealizer.com/)                                                                                                                                                            |    CSV    |
| `shearwater` | Logs from **Shearwater** dive computers. <br> [![Get log][get_log_img]](https://shearwater.com/pages/shearwater-cloud)                                                                                                                                        |    XML    |
|   `garmin`   | Logs from **Garmin** dive computers. <br> [![Get log][get_log_img]](https://connect.garmin.com/signin/) [![How to][how_to_img]](https://github.com/noppanut15/depthviz/blob/main/docs/GARMIN.md)                                                              |    FIT    |
|   `suunto`   | Logs from **Suunto** dive computers. <br> [![Get log][get_log_img]](https://www.suunto.com/suunto-app/suunto-app-2022/)  [![How to][how_to_img]](https://www.suunto.com/Support/faq-articles/suunto-app/what-type-of-files-can-i-export-from-the-suunto-app/) |    FIT    |
|   `manual`   | Manually entered depth logs. <br> [![How to][how_to_img]](#-no-dive-computer)                                                                                                                                                                                 |    CSV    |


#### 🎛 Advanced Customization Options
Want more control? Use these optional parameters:
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Option&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Values&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; |                           Default                           | Description                                                                                                                              |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------ | :----------------------------------------------------------------------------: | :---------------------------------------------------------: | ---------------------------------------------------------------------------------------------------------------------------------------- |
| `-d` or <br/>`--decimal-places`                                                                                                                                    |                                `0`, `1`, or `2`                                |                             `0`                             | Number of decimal places in the depth overlay.                                                                                           |
| `--depth-mode`                                                                                                                                                     |                         `raw` <br/>or<br/>`zero-based`                         |                            `raw`                            | `raw` shows the actual depth; `zero-based` forces the overlay to start/end at 0m. [See Raw vs Zero-Based](#depth-mode-raw-vs-zero-based) |
| `--no-minus`                                                                                                                                                       |                                       -                                        |                              -                              | Removes the minus sign from depth values (e.g., `10m` instead of `-10m`).                                                                |
| `--font`                                                                                                                                                           |                                   File path                                    | [Default font](https://fonts.google.com/specimen/Open+Sans) | Path to a custom font file for the text.                                                                                                 |
| `--bg-color`                                                                                                                                                       |                             Color name or hex code                             |                           `black`                           | Background color (e.g., `green`, `'#000000'`).                                                                                           |
| `--stroke-width`                                                                                                                                                   |                                Positive integer                                |                             `5`                             | Thickness of the text outline for better visibility.                                                                                     |


<details><summary><strong>Example Command with Advanced Options</strong></summary><br>

Example of generating a depth overlay video named `mydive.mp4` using data from `123456_ACTIVITY.fit` exported from [Garmin Connect](https://github.com/noppanut15/depthviz/blob/main/docs/GARMIN.md):

```bash
depthviz -i 123456_ACTIVITY.fit -s garmin -o mydive.mp4 --depth-mode zero-based --decimal-places 1 --no-minus --bg-color green --font ~/Downloads/font.ttf
```

- Set the depth display mode to **zero-based** to start the depth from 0m instead of the actual depth values from the dive log.
- The depth values will be displayed with **one** decimal place.
- The minus sign will be **hidden**.
- The background color will be set to **green**.
- A **custom font** file at `~/Downloads/font.ttf` will be used for the text.


---
</details>
<br>

<p align="center"><img src="https://raw.githubusercontent.com/noppanut15/depthviz/main/assets/depth-decimal-places-5s-trimmed.gif" alt="decimal places comparison"/></p>

> [!TIP]
> Use the `--decimal-places` option to control the precision of the depth display (e.g., `--decimal-places 1` displays depths like `-12.5m`)

#### Depth Mode: Raw vs Zero-based

<p align="center"><img src="https://raw.githubusercontent.com/noppanut15/depthviz/main/assets/depth-mode-comparison.jpg" alt="Depth Mode: raw vs zero-based" width="600px"/></p>


> [!TIP]
> Use `--depth-mode zero-based` to set the **starting depth and ending depth to 0m**. *(right figure)* This can be useful for displaying the depth from the surface.<br><br> Note that it assumes a descent and ascent rate of 1m/s between 0m and the actual starting/ending depth from the dive log.<br><br> If accuracy is important, use `raw` (default mode) to display the actual depth values from the dive log. The depth values **may start from some depth other than 0m, depending on when the dive computer started recording**. *(left figure)*

#### Time Overlay Video

<p align="center"><img src="https://raw.githubusercontent.com/noppanut15/depthviz/main/assets/time-overlays.gif" alt="time overlay demo" width="600px"/></p>

You can also generate a time overlay video as a separate video that displays the time elapsed during the dive. It will be exported in the same directory as the depth overlay video.

| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Option&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; | Values | Description                  |
| ------------------------------------------------------------------------------------------------------------------------------------------------------ | ------ | ---------------------------- |
| `--time`                                                                                                                                               | -      | Create a time overlay video. |

<details><summary><strong>Example Command with Time Overlay</strong></summary><br>

Example of generating a depth overlay video named `mydive.mp4` and a time overlay video by adding the `--time` option:

```bash
depthviz -i 123456_ACTIVITY.fit -s garmin -o mydive.mp4 --time
```
The time overlay video will be automatically generated and saved in the same directory as the depth overlay video with the filename `mydive_time.mp4`.

---

</details>


### Step 3: Integrate with Your Footage

<p align="center"><picture><source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/noppanut15/depthviz/main/assets/step3-dark-v2.jpeg" width="500px"><img src="https://raw.githubusercontent.com/noppanut15/depthviz/main/assets/step3-light-v2.jpeg" width="500px" title="integrate overlays with your footage" /></picture></p> 

Import the generated **depth overlay** and **time overlay** (if used) into your video editing software. Remove the background color. Adjust position of the overlays to suit your video style.

> [🎓 Watch a quick tutorial](https://www.youtube.com/watch?v=ZggKrWk98Ag): How to import overlays in CapCut.

> [!TIP]
> **🎨 Chroma Keying**: If you want to remove the background color from the overlay, use the [chroma key](https://en.wikipedia.org/wiki/Chroma_key) effect in your video editor. You can use the `--bg-color` option to set the background color to match your video editor's chroma key color. Using `--bg-color green` is a common choice.

<div align="right">

[&nwarr; Back to top](#readme-top)

</div>

## 🚫 No Dive Computer?

Even without a dive computer, **you can** create a depth overlay! Simply record **key moments** of your dive (using depth markers on your rope, for example) and prepare a CSV file with two columns:
- **Time**: in seconds
- **Depth**: in meters

**Example Manual Input File:**

| Time  | Depth |
| :---: | :---: |
|   0   |   0   |
|   6   |   5   |
|  12   |  10   |
|  19   |  15   |
|  26   |  10   |
|  33   |   5   |
|  39   |   0   |

[![Download Input File](https://img.shields.io/badge/Download%20Input%20File-1974D2?style=for-the-badge&logo=readdotcv)](https://github.com/noppanut15/depthviz/blob/main/assets/manual-input-example.csv)

**Example Command**:
```bash
depthviz -i manual_input.csv -s manual -o output_video.mp4
```

> [!TIP]
> For a simple dive, recording just three points (start, maximum depth, end) is enough. `depthviz` will interpolate the values for a smooth depth profile!

> [!IMPORTANT]
> For more complex dives (e.g., dives with significant variations in descent/ascent rate or bottom time), more data points are recommended.

| [![Example of a Freediving Rope with Depth Markers](https://raw.githubusercontent.com/noppanut15/depthviz/main/assets/marked-rope-example.png)](https://2bfreeequipment.com/shop/2-b-free-freediving-rope-superstatic-marked-with-stopper/) |
| :-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------: |
|                                                                                 *Freediving rope with depth markers helps record key moments of your dive.*                                                                                 |


<div align="right">

[&nwarr; Back to top](#readme-top)

</div>

## 🧠 How It Works
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

<div align="right">

[&nwarr; Back to top](#readme-top)

</div>

## 🌱 Contribution

We welcome contributions to the `depthviz` project! If you have any ideas for improvement, bug fixes, or feature suggestions, feel free to [open an issue](https://github.com/noppanut15/depthviz/issues) to discuss or [submit a pull request](https://github.com/noppanut15/depthviz/pulls).

<div align="right">

[&nwarr; Back to top](#readme-top)

</div>

## ⌚ Help Us Expand Dive Computer Support!

**Missing your dive computer?** Help us add support! If you have a dive computer that is not currently supported by `depthviz`, you can help us by donating a sample dive log file exported from your device. This will allow us to analyze the data format and implement the necessary parsing logic to add support for your device.

To share your dive data, please follow the detailed instructions in our [**Donate My Dive**](https://github.com/noppanut15/depthviz/issues/15) guide.

<div align="right">

[&nwarr; Back to top](#readme-top)

</div>

## ⚖️ License

**depthviz** is free and open-source software licensed under the [Apache License 2.0](https://github.com/noppanut15/depthviz/blob/main/LICENSE), created and supported by [Noppanut Ploywong](https://github.com/noppanut15) with ❤️ for fellow freedivers.

<!-- This project is licensed under the Apache License 2.0. See the [LICENSE](https://github.com/noppanut15/depthviz/blob/main/LICENSE) file for details. -->

<div align="right">

[&nwarr; Back to top](#readme-top)

</div>

## 📦 CycloneDX SBOM

This project provides a CycloneDX Software Bill of Materials (SBOM) in JSON format. The SBOM is generated by the [GitHub Actions workflow](https://github.com/noppanut15/depthviz/blob/main/.github/workflows/deploy.yaml) and is available as an artifact for each release. The SBOM is generated using the [cyclonedx-python](https://github.com/CycloneDX/cyclonedx-python) library.

<div align="right">

[&nwarr; Back to top](#readme-top)

</div>

## 📬 Contact

For any inquiries, please [open an issue](https://github.com/noppanut15/depthviz/issues) or contact the maintainer at [noppanut.connect@gmail.com](mailto:noppanut.connect@gmail.com).

<div align="right">

[&nwarr; Back to top](#readme-top)

</div>

<!-- Badge links -->
[version_badge_img]: https://img.shields.io/pypi/v/depthviz?label=version&logo=pypi&logoColor=white
[build_badge_img]: https://img.shields.io/github/actions/workflow/status/noppanut15/depthviz/deploy.yaml?logo=github
[coverage_badge_img]: https://img.shields.io/coveralls/github/noppanut15/depthviz?logo=coveralls
[pypi_status_img]: https://img.shields.io/pypi/status/depthviz?logo=pypi&logoColor=white
[download_badge_img]: https://static.pepy.tech/badge/depthviz
[version_badge_url]: https://pypi.org/project/depthviz/
[build_badge_url]: https://github.com/noppanut15/depthviz/actions
[coverage_badge_url]: https://coveralls.io/github/noppanut15/depthviz
[pypi_status_url]: https://pypi.org/project/depthviz/
[download_badge_url]: https://pepy.tech/projects/depthviz

<!-- Social links -->
[x_share_url]: https://x.com/intent/tweet?hashtags=depth%2Cfreediving%2Chud&text=A%20CLI%20tool%20that%20creates%20heads-up%20displays%20for%20your%20freediving%20videos%2C%20automatically%20tracking%20depth%20and%20time%20from%20dive%20computer%20logs%20or%20manual%20records.&url=https%3A%2F%2Fgithub.com%2Fnoppanut15%2Fdepthviz
[telegram_share_url]: https://t.me/share/url?url=https%3A//github.com/noppanut15/depthviz&text=A%20CLI%20tool%20that%20creates%20heads-up%20displays%20for%20your%20freediving%20videos,%20automatically%20tracking%20depth%20and%20time%20from%20dive%20computer%20logs%20or%20manual%20records.
[whatsapp_share_url]: https://api.whatsapp.com/send?text=A%20CLI%20tool%20that%20creates%20heads-up%20displays%20for%20your%20freediving%20videos%2C%20automatically%20tracking%20depth%20and%20time%20from%20dive%20computer%20logs%20or%20manual%20records.%20https%3A%2F%2Fgithub.com%2Fnoppanut15%2Fdepthviz
[reddit_share_url]: https://www.reddit.com/submit?url=https%3A%2F%2Fgithub.com%2Fnoppanut15%2Fdepthviz&title=A%20CLI%20tool%20that%20creates%20heads-up%20displays%20for%20your%20freediving%20videos%2C%20automatically%20tracking%20depth%20and%20time%20from%20dive%20computer%20logs%20or%20manual%20records.%20%23depth%20%23freediving
[facebook_share_url]: https://www.facebook.com/sharer/sharer.php?u=https%3A//github.com/noppanut15/depthviz
[x_share_img]: https://img.shields.io/badge/x_(twitter)-black?style=for-the-badge&logo=x
[telegram_share_img]: https://img.shields.io/badge/telegram-black?style=for-the-badge&logo=telegram
[whatsapp_share_img]: https://img.shields.io/badge/whatsapp-black?style=for-the-badge&logo=whatsapp
[reddit_share_img]: https://img.shields.io/badge/reddit-black?style=for-the-badge&logo=reddit
[facebook_share_img]: https://img.shields.io/badge/facebook-black?style=for-the-badge&logo=facebook

<!-- Help -->
[how_to_img]: https://img.shields.io/badge/How%20to-1974D2?style=flat-square&logo=gitbook&logoColor=white
[get_log_img]: https://img.shields.io/badge/Get%20log-1974D2?style=flat-square&logo=transmission&logoColor=white